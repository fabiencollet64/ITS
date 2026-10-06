#!/usr/bin/env python3
"""Change l'URL de base absolue du site (canonical, Open Graph, JSON-LD, sitemap,
robots.txt, llms.txt, pages secondaires).

Usage : python3 tools/set-base-url.py https://www.its-entreprise.com/
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["index.html", "robots.txt", "tools/make-pages.py"]

if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit(__doc__)
new = sys.argv[1].rstrip("/") + "/"
current = re.search(r'<link rel="canonical" href="([^"]+)"', (ROOT / "index.html").read_text(encoding="utf-8")).group(1)
if current == new:
    sys.exit(f"L'URL de base est déjà {new}")
for f in FILES:
    p = ROOT / f
    p.write_text(p.read_text(encoding="utf-8").replace(current, new), encoding="utf-8")
    print("mis à jour :", f)
# Régénère les pages secondaires, sitemap.xml et llms.txt avec la nouvelle base
import runpy
runpy.run_path(str(ROOT / "tools" / "make-pages.py"), run_name="__main__")
print(f"URL de base : {current} → {new}")
