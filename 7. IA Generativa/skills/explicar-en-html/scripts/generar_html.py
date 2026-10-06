"""Genera la explicación HTML autocontenida a partir de contenido.json.

Uso:  python generar_html.py contenido.json salida.html

El formato de contenido.json está en ESQUEMA.md. El script escapa todo el texto,
arma el índice y reporta advertencias (secciones obligatorias que faltan, bloques
vacíos, fragmentos de código demasiado largos). Código de salida 1 si hay advertencias.
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

OBLIGATORIAS = ["resumen", "problema", "decisiones", "funcionamiento",
                "codigo", "pruebas", "limitaciones", "reproducir"]
MAX_LINEAS_CODIGO = 25
PLANTILLA = Path(__file__).resolve().parent.parent / "assets" / "plantilla.html"


def en_linea(texto):
    """Escapa y aplica **negrita** y `código` en línea."""
    t = html.escape(str(texto))
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)


def celda(valor):
    v = str(valor)
    clase = ' class="ok"' if v.startswith("OK") else ' class="mal"' if v.startswith("FALLA") else ""
    return f"<td{clase}>{en_linea(v)}</td>"


def bloque(b, avisos, donde):
    tipo = b.get("tipo")
    if tipo == "parrafo":
        return f"<p>{en_linea(b['texto'])}</p>"
    if tipo == "lista":
        etiqueta = "ol" if b.get("ordenada") else "ul"
        items = "".join(f"<li>{en_linea(i)}</li>" for i in b["items"])
        return f"<{etiqueta}>{items}</{etiqueta}>"
    if tipo == "codigo":
        lineas = b["texto"].rstrip("\n").count("\n") + 1
        if lineas > MAX_LINEAS_CODIGO:
            avisos.append(f"{donde}: fragmento de {lineas} líneas (máximo {MAX_LINEAS_CODIGO}).")
        titulo = f"<figcaption>{en_linea(b['titulo'])}</figcaption>" if b.get("titulo") else ""
        lenguaje = html.escape(b.get("lenguaje", ""))
        return (f'<figure class="codigo">{titulo}<pre><code class="lenguaje-{lenguaje}">'
                f"{html.escape(b['texto'].rstrip())}</code></pre></figure>")
    if tipo == "tabla":
        cabeza = "".join(f"<th>{en_linea(h)}</th>" for h in b["encabezados"])
        filas = "".join("<tr>" + "".join(celda(c) for c in f) + "</tr>" for f in b["filas"])
        if not b["filas"]:
            avisos.append(f"{donde}: tabla sin filas.")
        return f'<div class="tabla"><table><thead><tr>{cabeza}</tr></thead><tbody>{filas}</tbody></table></div>'
    if tipo == "nota":
        return f'<div class="nota {html.escape(b.get("clase", "info"))}">{en_linea(b["texto"])}</div>'
    if tipo == "pasos":
        items = "".join(f"<li><b>{en_linea(p['titulo'])}.</b> {en_linea(p['texto'])}</li>" for p in b["items"])
        return f'<ol class="pasos">{items}</ol>'
    avisos.append(f"{donde}: tipo de bloque desconocido '{tipo}'.")
    return ""


def generar(contenido):
    avisos = []
    ids = [s.get("id") for s in contenido.get("secciones", [])]
    for falta in [o for o in OBLIGATORIAS if o not in ids]:
        avisos.append(f"Falta la sección obligatoria '{falta}'.")
    indice, secciones = [], []
    for n, s in enumerate(contenido.get("secciones", []), 1):
        if not s.get("bloques"):
            avisos.append(f"La sección '{s.get('id')}' no tiene contenido.")
        cuerpo = "\n".join(bloque(b, avisos, f"sección '{s.get('id')}'") for b in s.get("bloques", []))
        ident = html.escape(s["id"])
        indice.append(f'<li><a href="#{ident}">{en_linea(s["titulo"])}</a></li>')
        secciones.append(f'<section id="{ident}"><h2><span class="num">{n}.</span>{en_linea(s["titulo"])}</h2>\n{cuerpo}</section>')
    metricas = "".join(f'<div class="metrica"><b>{en_linea(m["valor"])}</b><span>{en_linea(m["etiqueta"])}</span></div>'
                       for m in contenido.get("metricas", []))
    reemplazos = {"{{TITULO}}": html.escape(contenido["titulo"]),
                  "{{SUBTITULO}}": en_linea(contenido.get("subtitulo", "")),
                  "{{METRICAS}}": f'<div class="metricas">{metricas}</div>' if metricas else "",
                  "{{INDICE}}": "".join(indice), "{{SECCIONES}}": "\n".join(secciones),
                  "{{FECHA}}": date.today().isoformat()}
    pagina = PLANTILLA.read_text(encoding="utf-8")
    for marca, valor in reemplazos.items():
        pagina = pagina.replace(marca, valor)
    return pagina, avisos


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    contenido = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pagina, avisos = generar(contenido)
    Path(sys.argv[2]).write_text(pagina, encoding="utf-8")
    print(f"HTML generado: {sys.argv[2]} ({len(pagina) / 1024:.1f} KB, "
          f"{len(contenido.get('secciones', []))} secciones, {len(avisos)} advertencias)")
    for a in avisos:
        print(f"  AVISO  {a}")
    sys.exit(1 if avisos else 0)
