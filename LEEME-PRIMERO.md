# Cómo dejarlo funcionando en GitHub (repositorio PRIVADO)

1. Crea un repositorio **privado** y sube todo el contenido de esta carpeta (incluida `.github/`), rama `main`.
2. Entra en **Actions** → "Descargar imágenes" → **Run workflow**. (También se ejecuta solo al subir.)
3. En unos minutos GitHub descarga las imágenes a `imagenes/`, actualiza `datos/imagenes.json` y la galería de `index.html`, y lo guarda en el repo. El detalle queda en `datos/informe_descarga.txt` (qué páginas fallaron o no tenían imágenes).
4. Para verlo: descarga/clona el repo y abre `index.html`. Funciona sin conexión.

## Sobre "página privada"
- GitHub Pages **no es privado** en cuentas normales: aunque el repo sea privado, la web publicada es pública. Solo es privado con GitHub Enterprise Cloud. **No actives Pages** con estas imágenes (tienen copyright de Rowling y otros titulares).
- Alternativas privadas: abrir `index.html` en local, o ver los archivos en el propio repo privado.

## Límites
Algunas webs (Google Arts & Culture, Sotheby's…) pueden bloquear descargas automáticas o cargar las imágenes con JavaScript; las que fallen quedan en el informe y siguen como "IMAGEN FALTANTE" con enlace a su ficha.
Uso personal: las imágenes pertenecen a sus titulares.

## Botón "Más imágenes"
En la cabecera y en el menú de `index.html` hay un botón "Más imágenes" con enlaces a páginas que muestran manuscritos y dibujos de Rowling (requieren internet). El workflow también intenta descargar las imágenes de esas páginas a `imagenes/`.

## Botón "Descargar TODAS las imágenes (ZIP)"
Tras ejecutar el workflow, el repo contiene `imagenes_rowling.zip` con todas las imágenes. El botón de `index.html` descarga ese archivo. Si aún no has ejecutado el workflow, el botón no encuentra el ZIP.
