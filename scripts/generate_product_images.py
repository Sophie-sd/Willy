#!/usr/bin/env python3
"""Generate product-style placeholder images (packaging, not animals)."""
from PIL import Image, ImageDraw
import os

SIZE = 800
BG = (242, 239, 232)
OUT = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'products')


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, quality=92, optimize=True, subsampling=0)
    print('saved', name)


def canvas():
    img = Image.new('RGB', (SIZE, SIZE), BG)
    return img, ImageDraw.Draw(img)


def dog_food_bag():
    img, d = canvas()
    x, y, w, h = 220, 120, 360, 520
    d.rounded_rectangle([x, y + 40, x + w, y + h], radius=28, fill=(139, 105, 20), outline=(110, 82, 16), width=3)
    d.polygon([(x + 30, y + 40), (x + w - 30, y + 40), (x + w - 50, y), (x + 50, y)], fill=(168, 128, 32))
    d.rounded_rectangle([x + 70, y + 100, x + w - 70, y + 220], radius=12, fill=(245, 236, 210))
    for i, cx in enumerate(range(x + 100, x + w - 60, 42)):
        for j, cy in enumerate(range(y + 380, y + h - 40, 36)):
            color = (180, 130, 50) if (i + j) % 2 else (150, 105, 35)
            d.ellipse([cx, cy, cx + 24, cy + 18], fill=color)
    save(img, 'dog-food.jpg')


def cat_food_pouch():
    img, d = canvas()
    pts = [(180, 180), (620, 160), (600, 580), (200, 600)]
    d.polygon(pts, fill=(107, 45, 91), outline=(80, 32, 68), width=3)
    d.rounded_rectangle([260, 240, 540, 380], radius=16, fill=(255, 245, 250))
    d.ellipse([340, 420, 460, 500], fill=(255, 180, 120))
    d.arc([320, 400, 480, 520], 200, 340, fill=(255, 140, 80), width=8)
    save(img, 'cat-food.jpg')


def dog_rope_toy():
    img, d = canvas()
    cx, cy, r = 400, 400, 170
    for i in range(12):
        angle = i * 30
        import math
        rad = math.radians(angle)
        ox = int(cx + math.cos(rad) * r * 0.85)
        oy = int(cy + math.sin(rad) * r * 0.85)
        color = (160, 110, 60) if i % 2 else (120, 80, 45)
        d.ellipse([ox - 28, oy - 28, ox + 28, oy + 28], fill=color, outline=(90, 58, 30), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(130, 88, 48), width=14)
    d.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(200, 160, 100))
    save(img, 'dog-toy.jpg')


def bird_food_bag():
    img, d = canvas()
    d.rounded_rectangle([210, 140, 590, 620], radius=20, fill=(240, 248, 255), outline=(180, 200, 220), width=3)
    colors = [(220, 180, 40), (90, 160, 60), (200, 120, 40), (180, 180, 180)]
    import random
    random.seed(7)
    for _ in range(120):
        cx = random.randint(240, 560)
        cy = random.randint(280, 580)
        c = random.choice(colors)
        d.ellipse([cx, cy, cx + random.randint(8, 16), cy + random.randint(8, 16)], fill=c)
    d.rounded_rectangle([280, 180, 520, 260], radius=10, fill=(90, 189, 40))
    save(img, 'bird-food.jpg')


def rodent_food_bag():
    img, d = canvas()
    d.rounded_rectangle([220, 130, 580, 610], radius=24, fill=(76, 140, 60), outline=(56, 110, 44), width=3)
    d.rounded_rectangle([280, 200, 520, 300], radius=10, fill=(220, 240, 210))
    for i in range(8):
        for j in range(10):
            d.ellipse([300 + i * 28, 360 + j * 22, 318 + i * 28, 374 + j * 22], fill=(180, 150, 100))
    save(img, 'rodent-food.jpg')


def dog_bed():
    """М'який овальний лежак з бортиками та плюшевою текстурою."""
    img, d = canvas()
    cx, cy = 400, 420

    shadow = (200, 192, 180)
    rim_outer = (168, 148, 128)
    rim_inner = (188, 168, 148)
    plush = (228, 212, 196)
    plush_light = (245, 235, 224)
    plush_dark = (205, 185, 168)

    d.ellipse([cx - 235, cy - 95, cx + 235, cy + 115], fill=shadow)
    d.ellipse([cx - 230, cy - 130, cx + 230, cy + 100], fill=rim_outer, outline=(140, 120, 100), width=3)
    d.ellipse([cx - 195, cy - 105, cx + 195, cy + 75], fill=rim_inner)

    d.ellipse([cx - 175, cy - 55, cx + 175, cy + 55], fill=plush)

    import random
    random.seed(42)
    for _ in range(90):
        px = random.randint(cx - 160, cx + 140)
        py = random.randint(cy - 45, cy + 40)
        r = random.randint(6, 14)
        tone = random.choice([plush_light, plush, plush_dark])
        d.ellipse([px, py, px + r, py + r * 0.7], fill=tone)

    d.ellipse([cx - 175, cy - 55, cx + 175, cy + 55], outline=(195, 175, 155), width=2)

    bolster_y = cy - 118
    d.rounded_rectangle(
        [cx - 200, bolster_y - 28, cx + 200, bolster_y + 38],
        radius=22, fill=rim_outer, outline=(130, 110, 90), width=2,
    )
    d.rounded_rectangle(
        [cx - 175, bolster_y - 12, cx + 175, bolster_y + 22],
        radius=14, fill=plush_light,
    )

    for bx in range(cx - 160, cx + 140, 28):
        d.ellipse([bx, bolster_y - 4, bx + 18, bolster_y + 10], fill=plush)

    d.ellipse([cx - 230, cy + 55, cx - 175, cy + 100], fill=rim_outer)
    d.ellipse([cx + 175, cy + 55, cx + 230, cy + 100], fill=rim_outer)
    d.ellipse([cx - 210, cy + 62, cx - 182, cy + 90], fill=rim_inner)
    d.ellipse([cx + 182, cy + 62, cx + 210, cy + 90], fill=rim_inner)

    save(img, 'dog-bed.jpg')


def cat_litter():
    img, d = canvas()
    d.rounded_rectangle([200, 200, 600, 580], radius=16, fill=(255, 255, 255), outline=(200, 200, 200), width=3)
    for i in range(15):
        for j in range(12):
            g = 200 + (i + j) % 3 * 15
            d.ellipse([230 + i * 24, 280 + j * 22, 246 + i * 24, 294 + j * 22], fill=(g, g, g + 10))
    save(img, 'cat-litter.jpg')


def cat_toy():
    img, d = canvas()
    d.ellipse([280, 280, 520, 520], fill=(255, 100, 80), outline=(200, 60, 50), width=4)
    d.ellipse([360, 360, 440, 440], fill=(255, 220, 60))
    d.line([(400, 200), (400, 280)], fill=(180, 180, 180), width=6)
    save(img, 'cat-toy.jpg')


def dog_leash():
    img, d = canvas()
    import math
    cx, cy = 400, 400
    for t in range(0, 360, 8):
        rad = math.radians(t)
        rad2 = math.radians(t + 8)
        r1, r2 = 180, 200
        pts = [
            (cx + math.cos(rad) * r1, cy + math.sin(rad) * r1),
            (cx + math.cos(rad2) * r1, cy + math.sin(rad2) * r1),
            (cx + math.cos(rad2) * r2, cy + math.sin(rad2) * r2),
            (cx + math.cos(rad) * r2, cy + math.sin(rad) * r2),
        ]
        d.polygon(pts, fill=(90, 189, 40))
    d.rounded_rectangle([340, 120, 460, 200], radius=12, fill=(60, 60, 60))
    save(img, 'dog-leash.jpg')


def dog_collar():
    img, d = canvas()
    d.arc([150, 280, 650, 520], 15, 165, fill=(120, 80, 50), width=40)
    d.rounded_rectangle([370, 500, 430, 560], radius=8, fill=(180, 180, 180))
    save(img, 'dog-collar.jpg')


def bird_cage():
    img, d = canvas()
    d.rounded_rectangle([200, 160, 600, 620], radius=12, outline=(100, 100, 100), width=4)
    for x in range(230, 570, 28):
        d.line([(x, 180), (x, 600)], fill=(160, 160, 160), width=3)
    for y in range(200, 580, 40):
        d.line([(220, y), (580, y)], fill=(160, 160, 160), width=2)
    save(img, 'bird-cage.jpg')


def rodent_cage():
    img, d = canvas()
    d.rounded_rectangle([180, 200, 620, 580], radius=16, fill=(245, 245, 240), outline=(150, 150, 140), width=4)
    d.rounded_rectangle([220, 240, 580, 540], radius=8, outline=(180, 180, 170), width=2)
    d.ellipse([340, 420, 460, 500], fill=(200, 180, 140))
    save(img, 'rodent-cage.jpg')


def bird_mirror():
    img, d = canvas()
    d.ellipse([280, 220, 520, 460], fill=(200, 230, 255), outline=(120, 160, 200), width=6)
    d.ellipse([330, 270, 470, 410], fill=(230, 245, 255))
    d.rectangle([385, 460, 415, 560], fill=(100, 100, 100))
    save(img, 'bird-mirror.jpg')


def rodent_wheel():
    img, d = canvas()
    d.ellipse([200, 200, 600, 600], outline=(80, 80, 80), width=8)
    d.ellipse([280, 280, 520, 520], outline=(120, 120, 120), width=4)
    d.line([(400, 400), (400, 250)], fill=(100, 100, 100), width=6)
    save(img, 'rodent-wheel.jpg')


def general_product():
    img, d = canvas()
    d.rounded_rectangle([240, 180, 560, 580], radius=20, fill=(255, 255, 255), outline=(210, 210, 210), width=3)
    d.rounded_rectangle([300, 240, 500, 340], radius=10, fill=(90, 189, 40))
    save(img, 'general-pet.jpg')


def main():
    os.makedirs(OUT, exist_ok=True)
    dog_food_bag()
    cat_food_pouch()
    dog_rope_toy()
    bird_food_bag()
    rodent_food_bag()
    dog_bed()
    cat_litter()
    cat_toy()
    dog_leash()
    dog_collar()
    bird_cage()
    rodent_cage()
    bird_mirror()
    rodent_wheel()
    general_product()


if __name__ == '__main__':
    main()
