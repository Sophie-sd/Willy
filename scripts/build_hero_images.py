#!/usr/bin/env python3
"""Prepare hero banners, CTA photo, product card images, and spare banner library."""
from __future__ import annotations

import os
import shutil
from PIL import Image, ImageFilter, ImageEnhance

ROOT = os.path.join(os.path.dirname(__file__), '..')
HERO = os.path.join(ROOT, 'static', 'images', 'hero')
PROD = os.path.join(ROOT, 'static', 'images', 'products')
LIB = os.path.join(HERO, 'library')
ASSETS = os.path.join(
    os.path.expanduser('~'),
    '.cursor/projects/Users-olegbonislavskyi-Sites-ZooWilly/assets',
)

BANNER_W, BANNER_H = 1920, 1080
CTA_W, CTA_H = 1200, 900
PRODUCT_SIZE = 800
BG_WARM = (242, 239, 232)
SALE_BG = (232, 196, 88)


def save_jpg(img: Image.Image, path: str, quality: int = 92) -> None:
    img.convert('RGB').save(path, quality=quality, optimize=True, subsampling=0)
    print(f'saved {os.path.relpath(path, ROOT)} ({img.size[0]}x{img.size[1]})')


def save_webp(img: Image.Image, path: str, quality: int = 88) -> None:
    img.convert('RGB').save(path, 'WEBP', quality=quality, method=6)
    print(f'saved {os.path.relpath(path, ROOT)} ({img.size[0]}x{img.size[1]})')


def cover_crop(img: Image.Image, tw: int, th: int, focal_x: float = 0.5, focal_y: float = 0.5) -> Image.Image:
    w, h = img.size
    scale = max(tw / w, th / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    scaled = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(int(nw * focal_x - tw / 2), nw - tw))
    top = max(0, min(int(nh * focal_y - th / 2), nh - th))
    return scaled.crop((left, top, left + tw, top + th))


def extend_horizontal(
    src_path: str,
    dest_path: str,
    tw: int = BANNER_W,
    th: int = BANNER_H,
) -> None:
    """Scale by height, blur-stretch side strips to fill full banner width."""
    im = Image.open(src_path).convert('RGB')
    w, h = im.size
    scale = th / h
    nw, nh = max(1, int(w * scale)), th
    scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)

    if nw >= tw:
        left = (nw - tw) // 2
        out = scaled.crop((left, 0, left + tw, th))
        save_jpg(out, dest_path)
        return

    canvas = Image.new('RGB', (tw, th))
    x_off = (tw - nw) // 2
    strip = max(24, min(80, nw // 8))

    left_strip = scaled.crop((0, 0, strip, nh)).resize((x_off, nh), Image.Resampling.LANCZOS)
    left_strip = left_strip.filter(ImageFilter.GaussianBlur(radius=10))
    canvas.paste(left_strip, (0, 0))

    right_w = tw - x_off - nw
    right_strip = scaled.crop((nw - strip, 0, nw, nh)).resize((right_w, nh), Image.Resampling.LANCZOS)
    right_strip = right_strip.filter(ImageFilter.GaussianBlur(radius=10))
    canvas.paste(right_strip, (x_off + nw, 0))
    canvas.paste(scaled, (x_off, 0))
    save_jpg(canvas, dest_path)


def fit_contain(img: Image.Image, tw: int, th: int, bg=BG_WARM) -> Image.Image:
    w, h = img.size
    scale = min(tw / w, th / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (tw, th), bg)
    canvas.paste(resized, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def paste_product(canvas: Image.Image, img_path: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    scale = max(tw / w, th / h) * 0.88
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, (nh - th) // 2)
    im = im.crop((left, top, left + tw, top + th))
    canvas.paste(im, (x0, y0))


def build_sale_banner() -> None:
    candidates = [
        os.path.join(ASSETS, 'slide-sale-rabbit-banner.png'),
        os.path.join(HERO, 'slide-sale-rabbit-banner.png'),
    ]
    src = next((p for p in candidates if os.path.isfile(p)), None)
    if src:
        extend_horizontal(src, os.path.join(HERO, 'slide-sale-wide.jpg'))
        return

    canvas = Image.new('RGB', (BANNER_W, BANNER_H), SALE_BG)
    enhancer = ImageEnhance.Brightness(canvas)
    canvas = enhancer.enhance(1.04)

    products = [
        ('dog-food.jpg', (40, 40, 500, 1040)),
        ('dog-toy.jpg', (480, 40, 980, 1040)),
        ('bird-food.jpg', (960, 40, 1460, 1040)),
        ('rodent-food.jpg', (1440, 40, 1880, 1040)),
    ]
    for name, box in products:
        paste_product(canvas, os.path.join(PROD, name), box)

    save_jpg(canvas, os.path.join(HERO, 'slide-sale-wide.jpg'))


def build_delivery_banner() -> None:
    candidates = [
        os.path.join(ASSETS, 'slide-delivery-collie-banner-v2.png'),
        os.path.join(ASSETS, 'slide-delivery-collie-banner.png'),
        os.path.join(HERO, 'slide-delivery-collie-banner-v2.png'),
        os.path.join(HERO, 'slide-delivery-collie-banner.png'),
    ]
    src = next((p for p in candidates if os.path.isfile(p)), None)
    if src:
        extend_horizontal(src, os.path.join(HERO, 'slide-delivery-wide.jpg'))
        return
    extend_horizontal(
        os.path.join(HERO, 'slide-delivery.jpg'),
        os.path.join(HERO, 'slide-delivery-wide.jpg'),
    )


def build_cta_photo() -> None:
    src = os.path.join(HERO, 'slide-delivery-alt.jpg')
    if not os.path.isfile(src):
        src = next(
            p for p in [
                os.path.join(ASSETS, '______________2026-06-24___16.56.14-5c312ce1-0ea7-4be8-82ae-071cfe53c253.png'),
            ]
            if os.path.isfile(p)
        )
    im = Image.open(src).convert('RGB')
    w, h = im.size
    ratio = 4 / 3
    if w / h > ratio:
        nh = h
        nw = int(h * ratio)
    else:
        nw = w
        nh = int(w / ratio)
    left = (w - nw) // 2
    top = max(0, min(int(h * 0.42) - nh // 2, h - nh))
    cropped = im.crop((left, top, left + nw, top + nh))
    out = cropped.resize((CTA_W, CTA_H), Image.Resampling.LANCZOS)
    save_jpg(out, os.path.join(HERO, 'cta-photo.jpg'))


def build_cat_food() -> None:
    src = os.path.join(PROD, 'dog-food.jpg')
    im = Image.open(src).convert('RGB')
    w, h = im.size
    pouch = im.crop((int(w * 0.08), int(h * 0.12), int(w * 0.38), int(h * 0.92)))
    pouch = ImageEnhance.Contrast(pouch).enhance(1.05)
    pouch = ImageEnhance.Sharpness(pouch).enhance(1.12)

    pw, ph = pouch.size
    scale = min(PRODUCT_SIZE * 0.88 / pw, PRODUCT_SIZE * 0.88 / ph)
    nw, nh = int(pw * scale), int(ph * scale)
    pouch = pouch.resize((nw, nh), Image.Resampling.LANCZOS)

    canvas = Image.new('RGB', (PRODUCT_SIZE, PRODUCT_SIZE), BG_WARM)
    canvas.paste(pouch, ((PRODUCT_SIZE - nw) // 2, (PRODUCT_SIZE - nh) // 2))
    save_jpg(canvas, os.path.join(PROD, 'cat-food.jpg'))


def copy_banner_library() -> None:
    os.makedirs(LIB, exist_ok=True)
    mapping = {
        'banner-dogs-running.jpg': 'photo-1548199973-03cce0bbc87b-6e1e7a7b-de97-4b89-9613-cb89f9f21c5f.png',
        'banner-dogs-trio-blue.jpg': 'National-Dog-Month-1024x576-18337dbe-684b-4aa5-8da0-cc7fa8a89d38.png',
        'banner-puppies-peach.jpg': '2019-09-27-047888008874024-faa74c37-0979-4d31-a310-eda0f71b810d.png',
        'banner-woman-rabbit.jpg': '360_F_371762328_Wd93bduo7Yk8TvPJmbaiGF6osOVCapLx-3a4abf45-dec0-4c48-ba90-b6ad3f2ca5c9.png',
        'banner-yorkies-white.jpg': '______________2026-06-24___16.56.07-23dcd2ca-5f39-4b9e-a349-8dbe0afb52bd.png',
        'banner-retriever-puppies.jpg': '______________2026-06-24___16.56.14-5c312ce1-0ea7-4be8-82ae-071cfe53c253.png',
    }
    for dest, src_name in mapping.items():
        src = os.path.join(ASSETS, src_name)
        if not os.path.isfile(src):
            print(f'skip library {dest}: missing asset')
            continue
        im = Image.open(src).convert('RGB')
        out = fit_contain(im, BANNER_W, BANNER_H)
        save_jpg(out, os.path.join(LIB, dest))


def build_hero_banner() -> None:
    candidates = [
        os.path.join(ASSETS, 'hero-dachshund-banner-final.png'),
        os.path.join(ASSETS, 'hero-dachshund-banner-v3.png'),
        os.path.join(ASSETS, 'hero-dachshund-banner-v2.png'),
        os.path.join(ASSETS, 'hero-dachshund-interior.png'),
        os.path.join(ASSETS, 'hero-dachshund-gray.png'),
        os.path.join(
            ASSETS,
            'small-dog-being-adorable-studio_23-2149016878-3017b7b7-be91-4741-a185-13e3470240d1.png',
        ),
    ]
    src = next((p for p in candidates if os.path.isfile(p)), None)
    if not src:
        extend_horizontal(
            os.path.join(HERO, 'hero.jpg'),
            os.path.join(HERO, 'hero-wide.jpg'),
        )
        return
    im = Image.open(src).convert('RGB')
    if 'hero-dachshund-banner-final' in src:
        w, h = im.size
        new_h = int(w * 9 / 16)
        top = max(0, min((h - new_h) // 2 - 20, h - new_h))
        im = im.crop((0, top, w, top + new_h))
        out = im.resize((BANNER_W, BANNER_H), Image.Resampling.LANCZOS)
    elif 'hero-dachshund-banner-v3' in src or 'hero-dachshund-banner-v2' in src:
        out = fit_contain(im, BANNER_W, BANNER_H, bg=(210, 218, 226))
    else:
        focal_x = 0.58 if 'hero-dachshund-gray' in src else 0.32
        out = cover_crop(im, BANNER_W, BANNER_H, focal_x=focal_x, focal_y=0.48)
    save_webp(out, os.path.join(HERO, 'hero-wide.webp'))


def main() -> None:
    os.makedirs(HERO, exist_ok=True)
    os.makedirs(PROD, exist_ok=True)

    build_hero_banner()
    build_delivery_banner()
    build_sale_banner()
    build_cta_photo()
    build_cat_food()
    copy_banner_library()


if __name__ == '__main__':
    main()
