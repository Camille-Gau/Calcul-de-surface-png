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

# === ÉCHELLE : 1 pixel = ? mètres
scale_m_per_pixel = 100/76  # à adapter

# === CHARGEMENT IMAGE ===
image_path = r"goteborg.png"  # adapter
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# === INITIALISATION ===
points = []
mask = np.zeros(image.shape[:2], dtype=np.uint8)
mode = 'draw'  # ou 'zoom'

# === GESTION ZOOM ===
def preserve_limits():
    return ax.get_xlim(), ax.get_ylim()

def restore_limits(lims):
    ax.set_xlim(lims[0])
    ax.set_ylim(lims[1][::-1])  # pour éviter l'inversion verticale

# === CALLBACKS ===
def onclick(event):
    global points
    if mode != 'draw':
        return
    if event.inaxes:
        x, y = int(event.xdata), int(event.ydata)
        points.append((x, y))
        ax.plot(x, y, 'ro')
        fig.canvas.draw()

def on_key(event):
    global mode, points, mask
    if event.key == 'enter' and len(points) >= 3:
        poly = np.array(points, dtype=np.int32)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [poly], 1)
        surface_pixels = np.sum(mask)
        surface_m2 = surface_pixels * (scale_m_per_pixel ** 2)

        # Affichage de la zone coloriée
        image_with_poly = image_rgb.copy()
        image_with_poly[mask == 1] = [255, 0, 0]

        # Préserver le zoom
        lims = preserve_limits()
        ax.clear()
        ax.imshow(image_with_poly)
        ax.set_title(f"Surface : {surface_m2:.4f} m²", fontsize=12, color='blue')
        restore_limits(lims)
        fig.canvas.draw()

        points = []  # reset pour dessiner à nouveau

    elif event.key == 'z':
        mode = 'zoom'
        print("🔍 Mode zoom activé. Utilisez la barre d'outils.")
    elif event.key == 'd':
        mode = 'draw'
        print("✏️ Mode dessin activé.")
        lims = preserve_limits()
        ax.clear()
        ax.imshow(image_rgb)
        ax.set_title("✏️ Mode dessin activé — Cliquez pour tracer", fontsize=10)
        restore_limits(lims)
        fig.canvas.draw()

# === AFFICHAGE INTERACTIF ===
fig, ax = plt.subplots()
ax.imshow(image_rgb)
ax.set_title("✏️ Mode dessin activé — Appuyez sur Entrée pour valider", fontsize=10)
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
