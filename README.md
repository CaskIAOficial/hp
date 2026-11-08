# Archivo de J.K. Rowling — paquete preparado para GitHub Pages y consulta sin conexión

## Qué incluye este ZIP

- `index.html`: archivo principal en español, con la recopilación documental y una galería/catálogo que funciona también abriendo el HTML directamente con `file://`.
- `datos/imagenes.json`: catálogo editable de las imágenes investigadas.
- `imagenes/`: carpeta reservada para imágenes locales autorizadas.
- `LICENSE-NOTICE.txt`: aviso de derechos.

**Importante:** no he podido incorporar archivos fotográficos originales en este paquete. No voy a presentar miniaturas remotas como si estuvieran guardadas localmente. La galería señala claramente las imágenes que faltan y enlaza a sus fichas originales cuando tengas conexión.

## Instrucciones prioritarias para la siguiente IA: completar la descarga de imágenes

**Objetivo: conseguir el máximo número posible de imágenes originales y dejar el archivo preparado para consultarlo sin conexión. No te limites a las seis fichas iniciales ni a una cantidad fija de imágenes.** Investiga todas las secciones, páginas y fuentes mencionadas en `index.html`, en este README y en `datos/imagenes.json`; busca también galerías, páginas interiores, archivos históricos y colecciones relacionadas con los materiales originales de J.K. Rowling.

La siguiente IA debe:

1. Revisar cada fuente y localizar todas las imágenes pertinentes, no solo la imagen principal o la miniatura.
2. Descargar la versión de mayor resolución que esté legítimamente disponible y cuya descarga/almacenamiento esté permitida. Priorizar archivos originales, no capturas de pantalla ni miniaturas si existe una versión mejor.
3. Guardar los archivos dentro de `imagenes/`, con nombres descriptivos, sin duplicados y conservando la extensión y calidad originales.
4. Ampliar `datos/imagenes.json` con una ficha por imagen: título, descripción, autor/creador si consta, fuente original, URL de origen, crédito, licencia/estado de derechos, nombre local del archivo y estado `incluida`.
5. Actualizar la galería de `index.html` para que todas las imágenes descargadas se muestren desde rutas locales relativas. No debe depender de imágenes remotas, CDNs ni enlaces externos para mostrar las imágenes ya descargadas.
6. Comprobar que cada ruta local existe y que las imágenes se abren sin conexión. Generar una lista de verificación de archivos descargados y faltantes.
7. Para cada imagen que no pueda incluir, añadirla a la tabla de **Imágenes faltantes** de este README e indicar el enlace directo, el motivo concreto (permiso/licencia, bloqueo técnico, archivo no disponible, etc.) y, si se conoce, la fuente donde puede consultarse.
8. No detenerse tras encontrar unas pocas imágenes: continuar con todas las fuentes relevantes y aprovechar todas las descargas permitidas y técnicamente posibles. Si una fuente falla, intentar su página de origen, una copia oficial o un repositorio autorizado alternativo; no inventar imágenes ni presentar enlaces remotos como archivos descargados.
9. Al terminar, volver a empaquetar todo el proyecto en un ZIP y resumir cuántas imágenes se descargaron, cuántas se descartaron como duplicadas y cuántas quedan pendientes.

**Importante sobre derechos y publicación:** que el archivo sea para consulta personal no significa automáticamente que cualquier imagen pueda republicarse en un repositorio público o en GitHub Pages. Descarga y conserva los archivos cuando la licencia, el permiso o la normativa aplicable lo permitan. No eludas controles de acceso, DRM, inicios de sesión ni restricciones técnicas. Si una imagen protegida no puede alojarse legítimamente en el repositorio público, déjala señalada como faltante con su enlace de consulta. Si el destino es un repositorio privado y existe una base legal para la copia personal, documenta esa circunstancia por separado; no la presentes como autorización de redistribución.

## Imágenes faltantes (pendientes)

Las siguientes piezas se han localizado y están catalogadas, pero no se incluyen como archivos porque sus fichas identifican derechos de autor o no ofrecen una licencia de reutilización verificable. Además, el entorno de descarga no ha podido resolver los servidores externos, por lo que no ha sido posible guardar los originales aquí.

| Imagen pendiente | Fuente directa | Motivo |
|---|---|---|
| Boceto anotado de Hogwarts por J.K. Rowling | https://artsandculture.google.com/asset/sketch-of-hogwarts-by-j-k-rowling/6QEJy8kFibqARg | La ficha declara «Copyright J.K. Rowling». |
| Sinopsis original de *La piedra filosofal* (1995) | https://artsandculture.google.com/asset/synopsis-of-harry-potter-and-the-philosopher%E2%80%99s-stone-by-j-k-rowling/VgG8oeMrAwPwfg | La ficha declara «Copyright J.K. Rowling». |
| Lista manuscrita de asignaturas, profesores e hipogrifos | https://artsandculture.google.com/asset/handwritten-list-of-subject-teachers-and-hippogriff-names-by-j-k-rowling/eAEbJC9YvFjySw | La ficha declara «Copyright J.K. Rowling». |
| Primer borrador manuscrito del capítulo 17 | https://artsandculture.google.com/asset/-/HgGGA7aa8HgO3w?childassetid=OgF1UOHvm1wqLg | La ficha declara «Copyright J.K. Rowling». |
| Bocetos de Pottermore (Weasley, Espejo de Oesed, Quidditch, Peeves, Snape, etc.) | https://www.the-leaky-cauldron.org/2016/08/25/original-j-k-rowling-sketches-on-pottermore/ | No se ha verificado permiso para copiar los archivos de imagen. |
| Manuscrito ilustrado de *Los cuentos de Beedle el Bardo* | https://www.sothebys.com/en/buy/auction/2024/fine-books-and-manuscripts-including-americana/rowling-j-k-beedle-the-bard-an-original-manuscript | Fotografías del manuscrito; no se ha verificado licencia de reproducción. |
| Árboles genealógicos de las familias Weasley y Black | Consultar el Scrapbook y las fuentes reunidas en `index.html` | No se ha localizado un archivo descargable con licencia verificable. |
| Planificación y hojas de cálculo de *La Orden del Fénix* | Consultar las fuentes reunidas en `index.html` | No se ha localizado un archivo descargable con licencia verificable. |
| Siete manuscritos únicos de *Beedle el Bardo*, anotaciones de *La piedra filosofal* y postal James/Sirius | https://www.sothebys.com/ | Fotografías de objetos de subasta; permisos no verificados. |

La ficha de Rowling sobre los bocetos de Hogwarts, la sinopsis, la lista manuscrita y el borrador del capítulo 17 indica explícitamente «Copyright J.K. Rowling». La propia web oficial de Rowling también establece que, en general, no se permite reproducir o republicar su contenido sin permiso escrito previo. El uso personal no convierte automáticamente una copia republicada en un archivo con licencia para alojarla en GitHub.

## Abrir sin internet

1. Descomprime el ZIP.
2. Abre `index.html` con Chrome, Firefox o Edge.
3. El texto, la navegación y el catálogo de imágenes faltantes funcionan sin conexión.
4. Las fichas externas solo abrirán cuando haya internet. Las fotografías no incluidas no pueden visualizarse sin conexión.

## Añadir imágenes locales

Si tienes archivos propios, has obtenido permiso o dispones de una licencia que permita guardarlos y alojarlos:

1. Copia cada imagen en `imagenes/`.
2. Abre `datos/imagenes.json` y rellena `archivo` con el nombre exacto del fichero.
3. Cambia `estado` a `incluida`.
4. Conserva el crédito y la licencia.
5. Actualiza el bloque JSON integrado en `index.html` para que la galería sin conexión refleje los cambios (o vuelve a generar el HTML a partir de `datos/imagenes.json`).

## Publicar en GitHub Pages

1. Sube `index.html`, `datos/`, `imagenes/`, `README.md` y `LICENSE-NOTICE.txt` a la raíz del repositorio.
2. En GitHub, entra en **Settings → Pages**.
3. Selecciona **Deploy from a branch**, rama `main` y carpeta `/ (root)`.
4. Guarda los cambios.

## Fuentes principales

- British Library / Google Arts & Culture, exposición «El Viaje»: https://artsandculture.google.com/story/el-viaje-the-british-library/lwXRRWBwxUB9Ig?hl=es
- Proyecto «Harry Potter: A History of Magic»: https://artsandculture.google.com/project/harry-potter-a-history-of-magic?hl=en-GB
- Términos oficiales de J.K. Rowling: https://stories.jkrowling.com/terms-of-use/
- Bocetos de Pottermore documentados por The-Leaky-Cauldron: https://www.the-leaky-cauldron.org/2016/08/25/original-j-k-rowling-sketches-on-pottermore/
- Sotheby's, manuscrito de *Beedle el Bardo*: https://www.sothebys.com/en/buy/auction/2024/fine-books-and-manuscripts-including-americana/rowling-j-k-beedle-the-bard-an-original-manuscript
