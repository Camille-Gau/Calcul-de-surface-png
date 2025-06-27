# -*- coding: utf-8 -*-
"""
 Original Author:  Camille Gautier
 Contributors:
 Last edited by: Camille GAutier
 Repository:  https://github.com/Camille_Gau/Calcul-de-desurface-png/
 Created:    2025-27-06
 Updated:
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

%matplotlib qt5   #To have an exterior console to interact with

# === SCALE : 1 pixel = ? meters
scale_m_per_pixel = 100/76  # adapt

# === CHARGE IMAGE ===
image_path = r"goteborg.png"  # adapt
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# === INITIALISATION ===
points = []
mask = np.zeros(image.shape[:2], dtype=np.uint8)
mode = 'draw'  # ou 'zoom'

# ===ZOOM ===
def preserve_limits():
    """
    Returns the current x and y axis limits of the plot.
    
    Useful for preserving the zoom level or view window before updating the figure.
    
    Returns:
        tuple: A tuple containing (x_limits, y_limits).
    """
    return ax.get_xlim(), ax.get_ylim()

def restore_limits(lims):
    """
    Restores previously saved axis limits to the current plot.
    
    Parameters:
        lims (tuple): A tuple of axis limits in the form (x_limits, y_limits).
                      The y-axis is reversed to maintain consistent orientation.
    """
    ax.set_xlim(lims[0])
    #ax.set_ylim(lims[1][::-1])  # in case it flips

# === CALLBACKS ===
def onclick(event):
    """
    Callback function for mouse clicks on the plot.
    
    In draw mode, captures clicked points within the axes and stores them.
    Each point is plotted in red. Only active if mode is 'draw'.
    
    Parameters:
        event (MouseEvent): Matplotlib mouse event with coordinates and axes context.
    """
    global points
    if mode != 'draw':
        return
    if event.inaxes:
        x, y = int(event.xdata), int(event.ydata)
        points.append((x, y))
        ax.plot(x, y, 'ro')
        fig.canvas.draw()

def on_key(event):
    """
    Callback function for keyboard input.
    
    - Enter: Validates the drawn polygon, computes surface area, and displays it.
    - 'z': Switches to zoom mode and updates the figure title.
    - 'd': Switches to draw mode and resets the display for new input.
    
    Parameters:
        event (KeyEvent): Matplotlib keyboard event indicating the key pressed.
    """
    global mode, points, mask
    if event.key == 'enter' and len(points) >= 3:
        poly = np.array(points, dtype=np.int32)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [poly], 1)
        surface_pixels = np.sum(mask)
        surface_m2 = surface_pixels * (scale_m_per_pixel ** 2)

        # Print the zone in color
        image_with_poly = image_rgb.copy()
        image_with_poly[mask == 1] = [255, 0, 0]

        # Preserve zoom
        lims = preserve_limits()
        ax.clear()
        ax.imshow(image_with_poly)
        ax.set_title(f"Surface : {surface_m2:.4f} m²", fontsize=12, color='blue')
        restore_limits(lims)
        fig.canvas.draw()

        points = []  # reset

    elif event.key == 'z':
        mode = 'zoom'
        ax.set_title("🔍 Zoom mode — you can zoom and move the image", fontsize=10)
        print("🔍 Zoom mode. your click wont begin a surface calcul.")
    elif event.key == 'd':
        mode = 'draw'
        print("✏️ Mode dessin activé.")
        lims = preserve_limits()
        ax.clear()
        ax.imshow(image_rgb)
        ax.set_title("✏️ Draw mode — clic to trace", fontsize=10)
        restore_limits(lims)
        fig.canvas.draw()

# === AFFICHAGE ===
fig, ax = plt.subplots()
ax.imshow(image_rgb)
ax.set_title("✏️  Draw mode — tap enter to launch calcul", fontsize=10)
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
