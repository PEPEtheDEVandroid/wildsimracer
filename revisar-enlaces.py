#!/usr/bin/env python3
"""Revisa la salud de los enlaces internos de la web.

Se ejecuta igual que generar-sitemap.py, sin argumentos, y avisa de tres cosas:

  1. Enlaces rotos: apuntan a una pagina que no existe.
  2. Callejones sin salida: articulos que no enlazan a ningun otro articulo.
  3. Huerfanos: articulos a los que no apunta ningun otro articulo.

Los dos ultimos no son errores, son avisos. Un articulo recien publicado
siempre sale como huerfano hasta que se enlaza desde algun sitio, que es
justamente lo que este script sirve para no olvidar.

Las paginas de listado (portada y archivos de seccion) no cuentan: enlazan a
todo por definicion y falsearian el resultado.
"""
import os
import re
import sys

LISTADOS = {"index.html", "novedades/index.html", "opinion/index.html",
            "tutoriales/index.html", "historias/index.html", "404.html"}

RE_HREF = re.compile(r'href="(/[^"#]*)"')


def paginas():
    for raiz, _, ficheros in os.walk("."):
        if ".git" in raiz:
            continue
        for f in ficheros:
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(raiz, f), ".")


def destino(url):
    """De una url de la web al fichero que deberia servirla."""
    if os.path.splitext(url)[1]:      # .css, .jpg, .xml...
        return "." + url
    return "." + url + "index.html"


def main():
    todas = sorted(paginas())
    # Las paginas con noindex (p. ej. la confirmacion del formulario) no se
    # enlazan a proposito, asi que no cuentan como huerfanas.
    def noindex(ruta):
        with open(ruta, encoding="utf-8") as fh:
            return re.search(r'<meta name="robots"[^>]*noindex', fh.read())
    articulos = [p for p in todas if p not in LISTADOS and not noindex(p)]
    enlaces = {}
    rotos = []

    for p in todas:
        with open(p, encoding="utf-8") as fh:
            urls = set(RE_HREF.findall(fh.read()))
        salen = set()
        for u in urls:
            if u == "/":
                continue
            if not os.path.exists(destino(u)):
                rotos.append((p, u))
                continue
            d = destino(u).lstrip("./")
            if d in articulos:
                salen.add(d)
        enlaces[p] = salen

    print(f"{len(todas)} paginas, {len(articulos)} articulos\n")

    if rotos:
        print("ENLACES ROTOS")
        for p, u in rotos:
            print(f"  {p} -> {u}")
    else:
        print("Enlaces rotos: ninguno")

    entrantes = {a: 0 for a in articulos}
    for p, salen in enlaces.items():
        if p in LISTADOS:
            continue          # los listados enlazan a todo, no cuentan
        for d in salen:
            entrantes[d] += 1

    # Las notas de novedades caducan y no se enlazan entre ellas: es normal
    # que queden sueltas y no hace falta avisar. Lo que importa es el
    # contenido que aguanta, que es el de opinion, tutoriales e historias.
    fondo = [a for a in articulos if not a.startswith("novedades/")]

    sin_salida = [a for a in fondo if not enlaces[a]]
    print(f"\nNo enlazan a ningun otro articulo ({len(sin_salida)} de {len(fondo)})")
    for a in sin_salida:
        print(f"  {os.path.dirname(a) or a}")

    huerfanos = [a for a in fondo if entrantes[a] == 0]
    print(f"\nNadie les enlaza ({len(huerfanos)} de {len(fondo)})")
    for a in huerfanos:
        print(f"  {os.path.dirname(a) or a}")

    sueltas = sum(1 for a in articulos
                  if a.startswith("novedades/") and not enlaces[a] and entrantes[a] == 0)
    print(f"\n({sueltas} notas de novedades sueltas, que es lo normal)")

    return 1 if rotos else 0


if __name__ == "__main__":
    sys.exit(main())
