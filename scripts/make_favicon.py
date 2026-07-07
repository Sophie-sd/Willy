#!/usr/bin/env python3
"""Прибирає чорний фон з логотипа-собаки та генерує favicon-набір.

Використання:
    python3 scripts/make_favicon.py <шлях_до_вихідного_png>

Фон видаляється заливкою від країв (flood fill), тому темні деталі
всередині собаки не постраждають.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'static', 'images', 'favicon')

MARKER = (255, 0, 255)
FLOOD_THRESH = 34
APPLE_BG = (248, 245, 239)  # --color-cream


def remove_black_background(src_path):
    img = Image.open(src_path).convert('RGB')
    w, h = img.size

    work = img.copy()
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(work, seed, MARKER, thresh=FLOOD_THRESH)

    work_arr = np.asarray(work)
    bg = np.all(work_arr == np.array(MARKER), axis=2)

    alpha = np.where(bg, 0, 255).astype(np.uint8)

    rgba = np.dstack([np.asarray(img), alpha])
    out = Image.fromarray(rgba, 'RGBA')

    smoothed = out.split()[3].filter(ImageFilter.GaussianBlur(0.6))
    out.putalpha(smoothed)
    return out


def crop_to_content(img, pad_ratio=0.08):
    bbox = img.split()[3].getbbox()
    if not bbox:
        return img
    img = img.crop(bbox)
    w, h = img.size
    side = max(w, h)
    pad = int(side * pad_ratio)
    canvas = side + pad * 2
    square = Image.new('RGBA', (canvas, canvas), (0, 0, 0, 0))
    square.paste(img, ((canvas - w) // 2, (canvas - h) // 2), img)
    return square


def save_png(img, name, size, background=None):
    resized = img.resize((size, size), Image.LANCZOS)
    if background is not None:
        bg = Image.new('RGBA', (size, size), background + (255,))
        bg.paste(resized, (0, 0), resized)
        resized = bg.convert('RGB')
    path = os.path.join(OUT, name)
    resized.save(path, optimize=True)
    print('saved', name)


def main():
    if len(sys.argv) < 2:
        print('usage: python3 scripts/make_favicon.py <source.png>')
        sys.exit(1)

    os.makedirs(OUT, exist_ok=True)

    cleaned = remove_black_background(sys.argv[1])
    icon = crop_to_content(cleaned)

    icon.resize((512, 512), Image.LANCZOS).save(
        os.path.join(OUT, 'icon.png'), optimize=True,
    )
    print('saved icon.png (512, transparent master)')

    save_png(icon, 'favicon-16x16.png', 16)
    save_png(icon, 'favicon-32x32.png', 32)
    save_png(icon, 'android-chrome-192x192.png', 192)
    save_png(icon, 'android-chrome-512x512.png', 512)
    save_png(icon, 'apple-touch-icon.png', 180, background=APPLE_BG)

    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    icon.save(os.path.join(OUT, 'favicon.ico'), sizes=ico_sizes)
    print('saved favicon.ico', ico_sizes)


if __name__ == '__main__':
    main()
