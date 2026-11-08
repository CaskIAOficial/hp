#!/usr/bin/env python3
"""Descarga las imágenes de las páginas de la guía de fuentes de Rowling y guarda en imagenes/ y actualiza la galería.
Uso PERSONAL. Muchas imágenes tienen copyright: no las publiques en un repositorio público.
Requisitos:  pip install requests beautifulsoup4
Ejecutar:    python3 descargar_imagenes.py
"""
import os, re, sys, json, time, zipfile, hashlib
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup

# nombre_corto -> URL  (todas las páginas de la guía)
PAGINAS = {
 # Google Arts & Culture (British Library)
 "gac-galeria": "https://artsandculture.google.com/story/lwXRRWBwxUB9Ig",
 "gac-exposicion": "https://artsandculture.google.com/exhibit/the-journey/ZgLSRWBwxUB9Ig",
 "gac-cap17": "https://artsandculture.google.com/asset/HgGGA7aa8HgO3w",
 "gac-hogwarts": "https://artsandculture.google.com/asset/sketch-of-hogwarts-by-j-k-rowling/6QEJy8kFibqARg",
 "gac-sinopsis": "https://artsandculture.google.com/asset/synopsis-of-harry-potter-and-the-philosopher%E2%80%99s-stone-by-j-k-rowling/VgG8oeMrAwPwfg",
 "gac-lista-hipogrifos": "https://artsandculture.google.com/asset/handwritten-list-of-subject-teachers-and-hippogriff-names-by-j-k-rowling/eAEbJC9YvFjySw",
 # Pottermore / Leaky Cauldron / bocetos
 "leaky-pottermore": "https://www.the-leaky-cauldron.org/2016/08/25/original-j-k-rowling-sketches-on-pottermore/",
 "leaky-azkaban-wright": "https://www.the-leaky-cauldron.org/?p=7851",
 "movieweb-snape": "https://movieweb.com/harry-potter-snape-sketches-original-jk-rowling/",
 "creativebloq-bocetos": "https://creativebloq.com/news/jk-rowlings-early-harry-potter-sketches-are-a-must-see",
 "marysue-bocetos": "https://themarysue.com/?p=379120",
 # Plan Orden del Fénix
 "laughingsquid-plan": "https://laughingsquid.com/plot-outline-harry-potter-order-of-phoenix/",
 "flashbak": "https://flashbak.com/jkrowling-sketches-harry-potter-plot-spreadsheet-400969/",
 "openculture-plan": "https://www.openculture.com/2014/07/j-k-rowling-plotted-harry-potter-with-a-hand-drawn-spreadsheet.html",
 "electricliterature-plan": "https://electricliterature.com/j-k-rowlings-spreadsheet-shows-how-she-wrote-harry-potter/",
 "slashfilm-plan": "https://www.slashfilm.com/511514/potd-jk-rowlings-plot-spreadsheet-for-harry-potter-and-the-order-of-the-phoenix/",
 # Ejemplar anotado
 "mugglenet-anotado": "https://mugglenet.com/2013/05/j-k-rowling-shares-handwritten-annotations-in-harry-potter-and-the-philosopher-s-stone/",
 # Árboles genealógicos y canon
 "lexicon-weasley": "https://www.hp-lexicon.org/?p=13181",
 "lexicon-black": "https://www.hp-lexicon.org/?p=1879",
 "lexicon-scrapbook": "https://www.hp-lexicon.org/source/other-canon/jkr/jkr-com-scrapbook/",
 "fanlore-weasley": "https://fanlore.org/wiki/Weasley",
 # Fandom
 "fandom-imagenes-jkr": "https://harrypotter.fandom.com/wiki/Category:Images_by_J._K._Rowling",
 "fandom-subastas": "https://harrypotter.fandom.com/wiki/J._K._Rowling's_contributions_to_charity_auctions",
 # Antigua web oficial
 "rowlinglibrary-guia": "https://www.therowlinglibrary.com/j-k-rowling/official-website/guide/",
 "accio-quote": "https://www.accio-quote.org/jkrwebsite.html",
 "rowlingindex": "https://www.rowlingindex.org/work/ext1dw/",
 # Edición 25 aniversario
 "artnet-25": "https://news.artnet.com/art-world/jk-rowling-drawings-philosophers-stone-2115585",
 "rowlinglibrary-25": "https://www.therowlinglibrary.com/?p=7628",
 # Subastas / Beedle / prólogo
 "sothebys-beedle": "https://www.sothebys.com/en/buy/auction/2024/fine-books-and-manuscripts-including-americana/rowling-j-k-beedle-the-bard-an-original-manuscript",
 "sothebys-articulo": "https://www.sothebys.com/en/articles/the-five-most-valuable-harry-potter",
 "artnet-beedle": "https://news.artnet.com/market/harry-potter-book-sells-for-467000-783746",
 "electricliterature-beedle": "https://electricliterature.com/beedle-the-bard-earns-368750-at-auction/",
 "bookriot-prologo": "https://bookriot.com/someone-stole-a-32100-handwritten-harry-potter-prequel",
 "dawn-prologo": "https://images.dawn.com/news/1177588",
 "malaymail-silla": "https://www.malaymail.com/news/read/2016/04/05/chair-jk-rowling-used-to-write-harry-potter-books-to-sell-at-auction/1093885",
 "businessinsider-black": "https://www.businessinsider.in/heres-the-one-thing-that-stumped-harry-potter-filmmakers/articleshow/53328951.cms",
 # Prensa ejemplar anotado
 "cbc-anotado": "https://www.cbc.ca/news/entertainment/j-k-rowling-annotated-harry-potter-sells-for-234k-1.1366354",
 "gulfnews-anotado": "https://gulfnews.com/entertainment/harry-potter-book-with-author-notes-sold-for-228000-1.1186770",
 "eluniverso-anotado": "https://www.eluniverso.com/vida-estilo/2013/05/21/nota/942826/edicion-anotaciones-autora-harry-potter-vendida-228083",
 "eldinamo-anotado": "https://www.eldinamo.cl/entretencion/2013/05/21/copia-de-primera-edicion-de-libro-de-harry-potter-fue-vendida-en-mas-de-110-millones-de-pesos/",
 # Exposiciones
 "sundaypost-bl": "https://www.sundaypost.com/fp/harry-potter-exhibition-go-show-british-library",
 "irishnews-bl": "https://irishnews.com/magazine/entertainment/2017/03/31/news/jk-rowling-s-hand-written-sorting-hat-song-joins-a-new-harry-potter-exhibition-984917",
 "phillyvoice-ny": "https://phillyvoice.com/harry-potter-exhibit-new-york-jk-rowling-manuscripts",
 "scholastic-ny": "https://www.scholastic.com/newsroom/all-news/press-release/harry-potter-a-history-of-magic-explores-folklore-and-magic-at-t.html",
 "gulfnews-20aniv": "https://gulfnews.com/entertainment/harry-potter-exhibit-marks-20th-anniversary-of-first-book-1.2109307",
 "wiki-history-of-magic": "https://en.wikipedia.org/wiki/Harry_Potter:_A_History_of_Magic",
 "wiki-beedle": "https://en.wikipedia.org/wiki/The_Tales_of_Beedle_the_Bard",
 # Web oficial
 "rowling-my-story": "https://stories.jkrowling.com/my-story/",
 "wizardingworld-cursed": "https://www.harrypotter.com/news/jk-rowling-notes-on-cursed-child-cast",
 "extra-01": "https://www.gamesradar.com/harry-potter-jk-rowling-sketches",
 "extra-02": "https://slashfilm.com/j-k-rowling-harry-potter-sketches",
 "extra-03": "https://www.bustle.com/articles/180177-jk-rowlings-harry-potter-sketches-she-drew-in-the-90s-are-stunning",
 "extra-04": "https://www.refinery29.com/2016/08/120944/harry-potter-jk-rowling-sketches",
 "extra-05": "https://themarysue.com/harry-potter-sketches",
 "extra-06": "https://www.mentalfloss.com/article/85216/pottermore-releases-original-jk-rowling-sketches",
 "extra-07": "https://www.mentalfloss.com/entertainment/harry-potter/tiny-handwritten-harry-potter-book-hits-auction-block",
 "extra-08": "https://www.smithsonianmag.com/smart-news/handwritten-harry-potter-prequel-stolen-180963279/",
 "extra-09": "https://artistsnetwork.com/art-mediums/drawing/jk-rowling-drawings",
 "extra-12": "https://www.the-leaky-cauldron.org/2006/08/23/display-of-jkr-handwritten-chapter-to-end-soon",
}

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "imagenes")
JSON_PATH = os.path.join(RAIZ, "datos", "imagenes.json")
HTML_PATH = os.path.join(RAIZ, "index.html")

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
      "Accept-Language": "es,en;q=0.8"}
MIN_BYTES = 20_000          # descarta iconos / miniaturas diminutas
EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
BASURA = re.compile(r"(logo|avatar|icon|sprite|gravatar|badge|banner|ads?/|pixel|tracking|emoji|button|social|\bshare\b)", re.I)


def actualizar_catalogo(nuevos):
    """Añade las imágenes descargadas al JSON y al catálogo embebido en index.html."""
    try: items = json.load(open(JSON_PATH, encoding="utf-8"))
    except Exception: items = []
    items = [i for i in items if i.get("origen") != "auto"]   # regenerar entradas automáticas
    for n in nuevos:
        items.append({
            "id": os.path.splitext(n["archivo"])[0], "origen": "auto",
            "titulo": n["titulo"], "categoria": "Imagen descargada",
            "descripcion": "Imagen obtenida de: " + urlparse(n["pagina"]).netloc,
            "archivo": n["archivo"], "estado": "incluida", "alt": n["titulo"],
            "credito": urlparse(n["pagina"]).netloc,
            "licencia": "Uso personal; derechos de sus titulares (repositorio privado)",
            "fuente": n["pagina"], "url_imagen": n["url_imagen"]})
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    json.dump(items, open(JSON_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    html = open(HTML_PATH, encoding="utf-8").read()
    blob = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    html2 = re.sub(r'(<script type="application/json" id="imageCatalog">).*?(</script>)',
                   lambda m: m.group(1) + blob + m.group(2), html, flags=re.S)
    open(HTML_PATH, "w", encoding="utf-8").write(html2)

def main():
    os.makedirs(OUT, exist_ok=True)
    vistos, informe, nuevos = set(), [], []
    s = requests.Session(); s.headers.update(UA)
    for nombre, url in PAGINAS.items():
        try:
            r = s.get(url, timeout=30); r.raise_for_status()
        except Exception as e:
            informe.append(f"FALLO página [{nombre}] {url}: {e}"); print(informe[-1]); continue
        titulo_pag = (BeautifulSoup(r.text, "html.parser").title or type("t", (), {"string": nombre})).string or nombre
        n_ok = 0
        for u in candidatas(url, r.text):
            try:
                im = s.get(u, timeout=60, headers={"Referer": url})
                ct = im.headers.get("content-type", "").split(";")[0]
                if im.status_code != 200 or ct not in EXT or len(im.content) < MIN_BYTES: continue
                h = hashlib.sha1(im.content).hexdigest()
                if h in vistos: continue
                vistos.add(h); n_ok += 1
                fn = f"{nombre}-{n_ok:02d}{EXT[ct]}"
                open(os.path.join(OUT, fn), "wb").write(im.content)
                nuevos.append({"archivo": fn, "pagina": url, "url_imagen": u, "titulo": f"{titulo_pag.strip()[:90]} ({n_ok})"})
                informe.append(f"OK    {fn} ({len(im.content)//1024} KB) <- {u}")
            except Exception as e:
                informe.append(f"FALLO imagen {u}: {e}")
        if n_ok == 0: informe.append(f"SIN IMÁGENES [{nombre}] {url}")
        print(f"[{nombre}] {n_ok} imágenes"); time.sleep(1)
    open(os.path.join(RAIZ, "datos", "informe_descarga.txt"), "w", encoding="utf-8").write("\n".join(informe))
    actualizar_catalogo(nuevos)
    print(f"\nListo: {len(nuevos)} imágenes únicas en imagenes/")

if __name__ == "__main__":
    main()
