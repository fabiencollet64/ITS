#!/usr/bin/env python3
"""Génère les images optimisées du site (AVIF + WebP, plusieurs largeurs).

Usage :
    python3 tools/build-images.py

Pour chaque image déclarée dans IMAGES :
  - si photos-src/<nom>.jpg (ou .png/.webp) existe, la photo réelle est utilisée ;
  - sinon un visuel de substitution est généré, clairement marqué
    « Photo de chantier à remplacer » (voir tools/fetch-photos.sh pour
    récupérer les vraies photos depuis its-entreprise.com).

Sorties : assets/img/<nom>-<largeur>.avif et .webp, poids cible < 100 Ko.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos-src"
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# nom, ratio (l/h), largeurs à produire, graine aléatoire, teinte
IMAGES = [
    ("hero-chantier",        16 / 9, [480, 800, 1200, 1600], 1, (62, 66, 72)),
    ("parc-des-princes",     4 / 3,  [400, 800],             2, (70, 72, 78)),
    ("parking-lorilleux",    4 / 3,  [400, 800],             3, (58, 60, 66)),
    ("centre-commercial",    4 / 3,  [400, 800],             4, (74, 70, 68)),
    ("equipe-chantier",      3 / 2,  [480, 960],             5, (66, 68, 74)),
]

AVIF_Q = 48
WEBP_Q = 72
MAX_BYTES = 100 * 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_source(name):
    for ext in ("jpg", "jpeg", "png", "webp", "avif"):
        p = SRC / f"{name}.{ext}"
        if p.exists():
            return Image.open(p).convert("RGB")
    return None


def placeholder(width, height, seed, tint):
    """Texture type béton + vignettage, marquée « à remplacer »."""
    rng = np.random.default_rng(seed)
    # nuages larges (surface de béton) + grain fin très discret
    small = np.clip(rng.normal(0.55, 0.10, (max(4, height // 40), max(4, width // 40))), 0, 1)
    noise = Image.fromarray((small * 255).astype("uint8"), "L").resize((width, height), Image.BICUBIC)
    noise = noise.filter(ImageFilter.GaussianBlur(width / 90))
    fine = Image.fromarray((np.clip(rng.normal(0.55, 0.04, (height, width)), 0, 1) * 255).astype("uint8"), "L")
    base = Image.blend(noise, fine, 0.3)

    arr = np.asarray(base).astype("float32") / 255.0
    # dégradé vertical + vignettage pour donner de la profondeur
    yy, xx = np.mgrid[0:height, 0:width]
    grad = 0.8 + 0.4 * (1 - yy / height)
    vign = 1 - 0.5 * (((xx / width - 0.5) ** 2 + (yy / height - 0.5) ** 2) ** 0.5)
    lum = arr * grad * vign
    rgb = np.stack([np.clip(lum * tint[i] * 2.1, 0, 255) for i in range(3)], axis=-1).astype("uint8")
    img = Image.fromarray(rgb, "RGB")

    # quelques bandes sombres (ombres de structure) pour casser l'uniformité
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(3):
        x = int(width * (0.12 + 0.3 * i)) + int(rng.integers(-20, 20))
        d.rectangle([x, 0, x + int(width * 0.012), height], fill=(0, 0, 0, 60))
        d.rectangle([x + int(width * 0.012), 0, x + int(width * 0.09), height], fill=(255, 255, 255, 10))

    # étiquette discrète : visuel de substitution
    label = "Photo de chantier à remplacer"
    fs = max(14, width // 44)
    font = ImageFont.truetype(FONT, fs)
    tw = d.textlength(label, font=font)
    pad = fs // 2
    x0, y0 = width - tw - 3 * pad, height - fs - 3 * pad
    d.rounded_rectangle([x0, y0, width - pad, height - pad], radius=fs // 3, fill=(0, 0, 0, 120))
    d.text((x0 + pad, y0 + pad * 0.9), label, font=font, fill=(255, 255, 255, 230))
    return img


def cover(img, width, height):
    """Recadre au ratio voulu puis redimensionne (équivalent object-fit: cover)."""
    sw, sh = img.size
    target = width / height
    if sw / sh > target:
        nw = int(sh * target)
        left = (sw - nw) // 2
        img = img.crop((left, 0, left + nw, sh))
    else:
        nh = int(sw / target)
        top = (sh - nh) // 2
        img = img.crop((0, top, sw, top + nh))
    return img.resize((width, height), Image.LANCZOS)


def save_under_limit(img, path, fmt, quality):
    q = quality
    while True:
        kwargs = {"quality": q}
        if fmt == "AVIF":
            kwargs["speed"] = 4
        else:
            kwargs["method"] = 6
        img.save(path, fmt, **kwargs)
        if path.stat().st_size <= MAX_BYTES or q <= 20:
            return q
        q -= 6


def main():
    for name, ratio, widths, seed, tint in IMAGES:
        src = load_source(name)
        origin = "photo réelle" if src else "visuel de substitution"
        for w in widths:
            h = round(w / ratio)
            img = cover(src, w, h) if src else placeholder(w, h, seed, tint)
            for fmt, ext, q in (("AVIF", "avif", AVIF_Q), ("WEBP", "webp", WEBP_Q)):
                p = OUT / f"{name}-{w}.{ext}"
                used = save_under_limit(img, p, fmt, q)
                print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024:>3} Ko  q={used}  ({origin})")


if __name__ == "__main__":
    main()
