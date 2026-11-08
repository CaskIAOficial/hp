#!/usr/bin/env python3
"""Descarga AGRESIVA de imágenes con un navegador real (Chromium + Playwright).
Por cada página: carga, cierra avisos de cookies, hace scroll (lazy-load), abre las imágenes que se
amplían en ventana emergente (lightbox, con "X"), captura todo lo que carga la red, sigue enlaces
directos a imágenes y pide la versión grande. Filtra iconos, banners y publicidad.
Uso PERSONAL. Requisitos: pip install requests beautifulsoup4 playwright pillow && playwright install chromium
"""
import time, os, re, io, json, hashlib, asyncio, sys
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from PIL import Image

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
TIEMPO_PAGINA = int(os.environ.get("TIEMPO_PAGINA", "420"))
PRESUPUESTO_CLICS = int(os.environ.get("PRESUPUESTO_CLICS", "45"))
DETENER = False
FIN = time.monotonic() + int(os.environ.get("LIMITE_TOTAL", str(48 * 60)))
CONCURRENCIA = int(os.environ.get("CONCURRENCIA", "4"))
MIN_BYTES = 25_000
BASURA = re.compile(r"(logo|avatar|icon|sprite|gravatar|emoji|/ads?/|adserver|doubleclick|banner|pixel|tracking|badge|button|social|spinner|placeholder|blank\.)", re.I)
EXT = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}
SEL_MAIN = "article, main, [role=main], .entry-content, .post-content, .article-body, .article-content, .post, #content, .content"

JS_DOM = r"""(selMain) => {
  const mains=[...document.querySelectorAll(selMain)];
  const inMain=el=>mains.length===0||mains.some(m=>m.contains(el));
  const out=[];
  const add=(u,el,tag)=>{ if(u&&!u.startsWith('data:')) out.push({u:new URL(u,location.href).href,main:inMain(el),tag}); };
  for(const i of document.images){
    add(i.currentSrc||i.src,i,'img');
    for(const at of i.getAttributeNames()){ if(at.startsWith('data-')||at==='srcset'){
      for(const m of (i.getAttribute(at)||'').matchAll(/(https?:\/\/[^\s,"']+\.(?:jpe?g|png|webp|gif)[^\s,"']*|\/[^\s,"']+\.(?:jpe?g|png|webp|gif)[^\s,"']*)/gi)) add(m[1],i,'attr'); } }
  }
  for(const a of document.querySelectorAll('a[href]')){ if(/\.(jpe?g|png|webp|gif)(\?|$)/i.test(a.href)) add(a.href,a,'link'); }
  for(const el of document.querySelectorAll('[style*=background]')){
    const m=(el.getAttribute('style')||'').match(/url\(["']?([^"')]+)/); if(m) add(m[1],el,'bg'); }
  for(const m of document.querySelectorAll('meta[property="og:image"],meta[name="twitter:image"]')) add(m.content,m,'meta');
  return out;
}"""

def clave(u):
    p = urlparse(u)
    if "googleusercontent.com" in p.netloc:
        return p.path.split("=")[0]
    return re.sub(r"-\d{2,4}x\d{2,4}(?=\.\w+$)", "", p.path)

def ampliar(u):
    if "googleusercontent.com" in u:
        return re.sub(r"=[swh]\d.*$", "", u) + "=s0"
    u = re.sub(r"-\d{2,4}x\d{2,4}(\.(?:jpe?g|png|webp))", r"\1", u)
    u = re.sub(r"/revision/latest/scale-to-width-down/\d+", "/revision/latest", u)
    return u

async def cerrar_avisos(page):
    for pat in [r"^(accept|accept all|agree|i agree|allow all|got it|ok|aceptar|aceptar todo|entendido)$"]:
        try: await page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1200)
        except Exception: pass

async def scroll_total(page):
    ult = -1
    for _ in range(60):
        h = await page.evaluate("document.documentElement.scrollHeight")
        await page.evaluate("window.scrollBy(0, 900)"); await page.wait_for_timeout(350)
        y = await page.evaluate("window.scrollY + innerHeight")
        if y >= h and h == ult: break
        ult = h
    await page.evaluate("window.scrollTo(0,0)")

async def cerrar_overlay(page):
    for sel in ['[aria-label*="lose" i]', '[aria-label*="errar" i]', '.mfp-close', '.fancybox-close', '.fancybox__button--close',
                '.pswp__button--close', '.modal-close', '.lightbox-close', 'button.close', '[class*="close" i]']:
        try:
            await page.locator(sel).first.click(timeout=500); return
        except Exception: pass
    try: await page.keyboard.press("Escape")
    except Exception: pass
    try: await page.mouse.click(4, 4)
    except Exception: pass

async def procesar(ctx, nombre, url, sem, informe):
    async with sem:
        page = await ctx.new_page()
        capt, tareas, lightbox = {}, [], set()
        async def on_resp(r):
            try:
                if r.status == 200 and r.headers.get("content-type", "").startswith("image/"):
                    b = await r.body()
                    if len(b) >= MIN_BYTES: capt[r.url] = b
            except Exception: pass
        page.on("response", lambda r: tareas.append(asyncio.create_task(on_resp(r))))
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        except Exception as e:
            informe.append(f"FALLO página [{nombre}] {url}: {str(e)[:120]}"); await page.close(); return []
        try: await page.wait_for_load_state("networkidle", timeout=8000)
        except Exception: pass
        dom, principales = [], set()
        limite = time.monotonic() + PRESUPUESTO_CLICS
        async def fases():
            nonlocal dom, principales
            await cerrar_avisos(page); await scroll_total(page)
            try: await page.wait_for_load_state("networkidle", timeout=5000)
            except Exception: pass
            dom = await page.evaluate(JS_DOM, SEL_MAIN)
            principales = {clave(d["u"]) for d in dom if d["main"]}
            # --- abrir ventanas emergentes (lightbox) ---
            n_img = await page.locator("img").count()
            for idx in range(min(n_img, 60)):
                if time.monotonic() > limite: break
                try:
                    loc = page.locator("img").nth(idx)
                    box = await loc.bounding_box()
                    if not box or box["width"] < 80 or box["height"] < 80: continue
                    antes = set(capt)
                    await loc.scroll_into_view_if_needed(timeout=1500)
                    await loc.click(timeout=1500, force=True)
                    await page.wait_for_timeout(900)
                    for t in list(tareas): 
                        try: await asyncio.wait_for(t, 3)
                        except Exception: pass
                    nuevas = set(capt) - antes
                    lightbox |= {clave(u) for u in nuevas}
                    if page.url.split("#")[0] != url.split("#")[0]:
                        await page.goto(url, wait_until="domcontentloaded", timeout=30000); await page.wait_for_timeout(800)
                    else:
                        await cerrar_overlay(page); await page.wait_for_timeout(300)
                except Exception: 
                    try: await cerrar_overlay(page)
                    except Exception: pass
            # --- pedir versiones grandes y enlaces directos ---
            for d in dom[:200]:
                for u in {d["u"], ampliar(d["u"])}:
                    if u in capt or BASURA.search(u): continue
                    try:
                        r = await ctx.request.get(u, timeout=30000, headers={"Referer": url})
                        if r.ok and r.headers.get("content-type", "").startswith("image/"):
                            capt[u] = await r.body()
                            if d["tag"] == "link": lightbox.add(clave(u))
                    except Exception: pass
        try:
            await fases()
        except BaseException as e:          # conservar lo ya capturado aunque algo falle o se agote el tiempo de la página
            if DETENER or time.monotonic() > FIN: raise   # pero una cancelación real SÍ se respeta
            informe.append(f"AVISO [{nombre}] incompleta: {type(e).__name__}")
        try: await asyncio.gather(*tareas, return_exceptions=True)
        except BaseException: pass
        await asyncio.gather(*tareas, return_exceptions=True)
        await page.close()
        # --- filtrar ---
        mejor = {}
        for u, data in capt.items():
            if BASURA.search(u) or len(data) < MIN_BYTES: continue
            try:
                im = Image.open(io.BytesIO(data)); w, h = im.size; fmt = im.format
            except Exception: continue
            if fmt not in EXT or max(w, h) < 500 or min(w, h) < 250 or max(w, h) / max(1, min(w, h)) > 4: continue
            k = clave(u)
            relevante = k in principales or k in lightbox or max(w, h) >= 900
            if not relevante: continue
            if k not in mejor or len(data) > len(mejor[k][1]):
                mejor[k] = (u, data, fmt, w, h)
        res = []
        for u, data, fmt, w, h in mejor.values():
            res.append({"pagina": url, "nombre": nombre, "u": u, "data": data, "fmt": fmt, "w": w, "h": h})
        informe.append(f"[{nombre}] {len(res)} imágenes ({len(capt)} capturadas, {len(lightbox)} de ventanas emergentes)")
        print(informe[-1], flush=True)
        return res

def actualizar_catalogo(nuevos):
    try: items = json.load(open(JSON_PATH, encoding="utf-8"))
    except Exception: items = []
    items = [i for i in items if i.get("origen") != "auto"]
    for n in nuevos:
        items.append({
            "id": os.path.splitext(n["archivo"])[0], "origen": "auto",
            "titulo": n["titulo"], "categoria": "Imagen descargada",
            "descripcion": f"{n['w']}×{n['h']} px · de {urlparse(n['pagina']).netloc}",
            "archivo": n["archivo"], "estado": "incluida", "alt": n["titulo"],
            "credito": urlparse(n["pagina"]).netloc,
            "licencia": "Uso personal; derechos de sus titulares (repositorio privado)",
            "fuente": n["pagina"], "url_imagen": n["u"]})
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    json.dump(items, open(JSON_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    html = open(HTML_PATH, encoding="utf-8").read()
    blob = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    html2 = re.sub(r'(<script type="application/json" id="imageCatalog">).*?(</script>)',
                   lambda m: m.group(1) + blob + m.group(2), html, flags=re.S)
    open(HTML_PATH, "w", encoding="utf-8").write(html2)

async def main():
    import signal
    os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    try:                                   # ANTES de descargar: borrar las descargas automáticas anteriores
        for it in json.load(open(JSON_PATH, encoding="utf-8")):
            if it.get("origen") == "auto" and it.get("archivo"):
                try: os.remove(os.path.join(OUT, it["archivo"]))
                except Exception: pass
    except Exception: pass
    informe, nuevos, vistos, cont = [], [], set(), {}

    def guardar(res):
        """Guarda en disco las imágenes de una página y actualiza catálogo e informe al momento."""
        for x in res:
            h = hashlib.sha1(x["data"]).hexdigest()
            if h in vistos: continue
            vistos.add(h)
            cont[x["nombre"]] = cont.get(x["nombre"], 0) + 1
            fn = f"{x['nombre']}-{cont[x['nombre']]:02d}{EXT[x['fmt']]}"
            open(os.path.join(OUT, fn), "wb").write(x["data"])
            nuevos.append({k: v for k, v in x.items() if k != "data"} | {"archivo": fn, "titulo": f"{x['nombre']} ({cont[x['nombre']]})"})
        open(os.path.join(RAIZ, "datos", "informe_descarga.txt"), "w", encoding="utf-8").write(
            "\n".join(informe) + f"\n\nTOTAL (hasta ahora): {len(nuevos)} imágenes únicas")
        actualizar_catalogo(nuevos)

    async def trabajo():
        async with async_playwright() as p:
            br = await p.chromium.launch()
            ctx = await br.new_context(viewport={"width": 1400, "height": 900}, locale="es-ES",
                  user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36")
            sem = asyncio.Semaphore(CONCURRENCIA)
            libre = asyncio.Semaphore(10_000)
            async def limitada(n, u):
                async with sem:                  # el cronómetro empieza al salir de la cola
                    if DETENER or time.monotonic() > FIN:
                        informe.append(f"OMITIDA [{n}] (ejecución interrumpida)"); return
                    try:
                        res = await asyncio.wait_for(procesar(ctx, n, u, libre, informe), TIEMPO_PAGINA)
                    except asyncio.TimeoutError:
                        informe.append(f"TIEMPO AGOTADO [{n}] {u} ({TIEMPO_PAGINA}s)"); print(informe[-1], flush=True); res = []
                    except asyncio.CancelledError:
                        raise
                    except BaseException as e:
                        informe.append(f"FALLO [{n}] {u}: {type(e).__name__}"); print(informe[-1], flush=True); res = []
                    guardar(res)                 # guardado inmediato, página a página
            await asyncio.gather(*[limitada(n, u) for n, u in PAGINAS.items()])
            try: await asyncio.wait_for(br.close(), 15)
            except BaseException: pass

    tarea = asyncio.ensure_future(trabajo())
    def parar():
        global DETENER
        DETENER = True; tarea.cancel()
    loop = asyncio.get_running_loop()
    for sg in (signal.SIGINT, signal.SIGTERM):      # si cancelas el workflow, lo ya descargado se conserva
        try: loop.add_signal_handler(sg, parar)
        except Exception: pass
    try:
        await asyncio.wait_for(tarea, max(1, FIN - time.monotonic()))
    except BaseException as e:
        informe.append(f"INTERRUMPIDO: {type(e).__name__} (se conserva lo descargado hasta ahora)")
    guardar([])
    print(f"\nListo: {len(nuevos)} imágenes únicas en imagenes/", flush=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        sys.stdout.flush(); sys.stderr.flush()
        os._exit(0)          # salir YA: cerrar Chromium a veces se queda colgado y bloquea el workflow
