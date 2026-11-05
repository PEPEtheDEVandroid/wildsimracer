#!/usr/bin/env python3
"""Genera sitemap.xml a partir de los index.html del sitio.

Sin dependencias: python3 generar-sitemap.py
Hay que ejecutarlo cada vez que se añade o se quita una página.
"""
import os
import re

BASE = "https://wildsimracer.es"
RAIZ = os.path.dirname(os.path.abspath(__file__))

def paginas():
    for dirpath, dirnames, nombres in os.walk(RAIZ):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if "index.html" not in nombres:
            continue
        rel = os.path.relpath(dirpath, RAIZ)
        url = BASE + "/" if rel == "." else f"{BASE}/{rel.replace(os.sep, '/')}/"
        html = open(os.path.join(dirpath, "index.html"), encoding="utf-8").read()
        m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', html)
        yield url, (m.group(1) if m else None)

def main():
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, fecha in sorted(paginas(), key=lambda p: (p[0] != BASE + "/", p[0])):
        lineas.append("  <url>")
        lineas.append(f"    <loc>{url}</loc>")
        if fecha:
            lineas.append(f"    <lastmod>{fecha}</lastmod>")
        lineas.append("  </url>")
    lineas.append("</urlset>")
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"sitemap.xml generado con {len(lineas) // 4} páginas")

if __name__ == "__main__":
    main()
