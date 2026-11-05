# wildsimracer.es

Web del canal de simracing WildSimRacer. HTML y CSS planos, sin build ni dependencias.

## Cómo se publica

Vercel despliega cada commit a `main` automáticamente. No hay que ejecutar nada.

## Estructura

- `index.html` — portada, con las novedades y los tutoriales
- `styles.css` — estilos de todo el sitio
- `novedades/<slug>/index.html` — notas cortas sobre novedades del simracing
- `<slug>/index.html` — tutoriales y guías, en la raíz para conservar las URLs antiguas

## Añadir un artículo

Crear una carpeta con el slug y dentro un `index.html`, copiando la estructura de
cualquier artículo que ya exista. Después, añadir su entrada en `index.html`.

## Notas

- El vídeo del tutorial de RBR está en Internet Archive: https://archive.org/details/tutorial-rbr
- El contenido de la web anterior en WordPress está exportado en un CSV fuera del repo.
