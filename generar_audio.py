#!/usr/bin/env python3
"""
Genera los audios (MP3) de la pestaña «Nuevo» con una voz neuronal en español.

Con audios reales (en vez de la voz del navegador) la lectura sigue sonando con la
pantalla bloqueada o con Brave en segundo plano, y se retoma al segundo exacto.

Uso (una sola vez, en el PC, con internet):
    pip install edge-tts
    python generar_audio.py                 # busca index.html en esta carpeta
    python generar_audio.py --voz es-ES-AlvaroNeural     # voz masculina
    python generar_audio.py --comprobar     # solo cuenta textos, no genera nada

Crea la carpeta  audio/  (intro.mp3, s01.mp3 … s28.mp3, x1.mp3 …, n1.mp3 … y lista.json).
Sube esa carpeta a GitHub/Vercel junto al index.html. Si lo repites, salta los
audios que ya existen (usa --forzar para rehacerlos).
Otras voces en español: es-ES-ElviraNeural (por defecto), es-ES-AlvaroNeural,
es-MX-DaliaNeural, es-MX-JorgeNeural, es-AR-ElenaNeural …
"""
import argparse, asyncio, json, sys
from pathlib import Path


def leer_textos(html):
    dec = json.JSONDecoder()
    i = html.index('var SECTIONS = ') + len('var SECTIONS = ')
    secciones, _ = dec.raw_decode(html[i:])
    j = html.index('var INTRO = ') + len('var INTRO = ')
    intro, _ = dec.raw_decode(html[j:])
    return intro, secciones


def texto_seccion(s):
    # Igual que lo que lee la voz del navegador: época, título y párrafos.
    return s['era'] + '. ' + s['title'] + '.\n' + '\n'.join(s['paras'])


async def generar(texto, destino, voz, velocidad, intentos=4):
    import edge_tts
    for n in range(1, intentos + 1):
        try:
            await edge_tts.Communicate(texto, voz, rate=velocidad).save(str(destino))
            if destino.stat().st_size > 1000:
                return True
        except Exception as e:  # red caída, límite temporal…
            print('   reintento %d/%d (%s)' % (n, intentos, e))
        await asyncio.sleep(2 * n)
    if destino.exists():
        destino.unlink()
    return False


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', default='index.html')
    ap.add_argument('--salida', default='audio')
    ap.add_argument('--voz', default='es-ES-ElviraNeural')
    ap.add_argument('--velocidad', default='+0%', help='p. ej. -10%% o +10%%')
    ap.add_argument('--forzar', action='store_true', help='rehacer aunque ya existan')
    ap.add_argument('--comprobar', action='store_true', help='solo contar, sin generar')
    a = ap.parse_args()

    html = Path(a.html).read_text(encoding='utf-8')
    intro, secciones = leer_textos(html)
    trabajos = [('intro', 'intro.mp3', intro)]
    for s in secciones:
        # La clave es estable aunque cambie el orden: 'aid' (audios ya hechos: s01…s28)
        # o 'key' (apartados añadidos después: x1.mp3, n1.mp3…). Así no se pisa ningún audio.
        clave = str(s.get('aid') or s.get('key'))
        nombre = ('s%02d.mp3' % int(clave)) if clave.isdigit() else ('%s.mp3' % clave)
        trabajos.append((clave, nombre, texto_seccion(s)))
    total = sum(len(t) for _, _, t in trabajos)
    print('%d audios, %d caracteres (≈ %d min de audio)' % (len(trabajos), total, total // 900))
    if a.comprobar:
        return

    out = Path(a.salida)
    out.mkdir(exist_ok=True)
    lista = {'voz': a.voz, 'intro': None, 'sections': {}}
    for clave, nombre, texto in trabajos:
        destino = out / nombre
        if destino.exists() and destino.stat().st_size > 1000 and not a.forzar:
            print('· %s ya existe' % nombre)
            ok = True
        else:
            print('→ generando %s …' % nombre)
            ok = await generar(texto, destino, a.voz, a.velocidad)
        if not ok:
            print('   ✗ no se pudo generar %s (vuelve a ejecutar el script para reintentar)' % nombre)
            continue
        if clave == 'intro':
            lista['intro'] = nombre
        else:
            lista['sections'][clave] = nombre
    (out / 'lista.json').write_text(json.dumps(lista, ensure_ascii=False, indent=1), encoding='utf-8')
    print('\nListo: %d de %d audios en %s/. Sube la carpeta junto al index.html.' % (
        len(lista['sections']) + (1 if lista['intro'] else 0), len(trabajos), out))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except ImportError:
        sys.exit('Falta edge-tts: ejecuta  pip install edge-tts')
