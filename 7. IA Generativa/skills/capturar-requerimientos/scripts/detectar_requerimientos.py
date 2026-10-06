"""Propone candidatos a requerimiento a partir del texto de extraer_texto.py.

Uso:  python detectar_requerimientos.py texto.txt --fuente <nombre> [--json candidatos.json]
                                     [--confianza alta|media|baja]

Detección mecánica con cuatro reglas:
  1. Frases con expresiones de obligación (debe, se requiere, se sugiere, podría...).
  2. Ítems numerados o viñetas de una sección de requerimientos (Ejercicios, Problemas,
     Requerimientos, Actividades, Entregables, Tareas), hasta la siguiente Bibliografía o Referencias.
  3. Ítems y frases que empiezan con un verbo en infinitivo o en imperativo (Crear, Tome, Desarrolle).
  4. Reglas de selección (escoja, desarrolle tres de los seis...), que se marcan como restricción.
Cada candidato lleva tipo, prioridad y confianza *propuestos*; la revisión final la hace el agente.
Confianza: alta (dentro de una sección de requerimientos), media (ítem de una lista introducida
por una frase terminada en ':'), baja (prosa con expresiones de obligación u otros ítems).
"""
import argparse
import json
import re
import sys

PRIORIDAD = [  # orden de evaluación: la primera expresión que aparece decide
    ("Podría",  r"\b(podr[ií]an?|opcional(mente)?|could|may)\b"),
    ("Debería", r"\b(deber[ií]an?|se sugiere|se recomienda|should|recommended)\b"),
    ("Debe",    r"\b(debe[n]?|deber[áa]n?|se requiere|requiere[n]?|tiene[n]? que|"
                r"es necesario|es obligatorio|shall|must|required)\b"),
]
TIPO = [  # restricciones primero: imponen tecnología, plazo, forma de entrega o norma
    ("RES", r"\b(python|java|c\+\+|ollama|docker|linux|windows|github|jupyter|colab|notebook|"
            r"entregar(se)?|plazo|fecha l[ií]mite|licencia|norma|est[áa]ndar|lenguaje)\b"),
    ("RNF", r"\b(segundos?|milisegundos?|ms|tiempo de respuesta|menos de|rendimiento|"
            r"desempe[ñn]o|seguridad|contrase[ñn]a|disponibilidad|usabilidad|sin conexi[óo]n|"
            r"offline|concurrent\w*|memoria|escalab\w*)\b"),
]
# Un título de sección es la línea completa: número opcional + palabra clave (+ "y Problemas", etc.)
# (con mayúscula inicial: "conclusiones." al final de una línea partida no es un título)
SECCION = re.compile(r"^#*\s*(\d+(\.\d+)*\.?)?\s*(?i:(?-i:[EPRAT])(jercicios|roblemas|equerimientos|equisitos|"
                     r"ctividades|ntregables|areas))(\s+(y|e)\s+\w+)?\s*\.?\s*$")
FIN_SECCION = re.compile(r"^#*\s*(\d+(\.\d+)*\.?)?\s*(?i:(?-i:[BRAC])(ibliograf\w*|eferencias|nexos?|onclusiones))\s*\.?\s*$")
ITEM = re.compile(r"^\s*([-*•]|\d+(\.\d+)*[.)]?)\s+(?=\S)")
SELECCION = re.compile(r"\b(escoja|seleccione|elija|(desarrolle|realice|haga|resuelva)\s+\w+\s+(ejercicios\s+)?de los|"
                       r"de los .{0,25}ejercicios.{0,15}\b(haga|escoja|realice|desarrolle))\b", re.I)
ORACION = re.compile(r"\S.*?(?:[.;?](?=\s+[A-ZÁÉÍÓÚÑ¿])|$)")
IMPERATIVOS = {
    "analice", "baje", "calcule", "compare", "considere", "construya", "cree", "dé", "de", "defina",
    "describa", "descargue", "desarrolle", "determine", "dibuje", "diseñe", "elabore", "encuentre",
    "entregue", "escoja", "estudie", "evalúe", "explique", "genere", "haga", "imagínese", "implemente",
    "investigue", "localice", "observe", "pídale", "presente", "programe", "pruebe", "realice", "saque",
    "simule", "suponga", "tome", "use", "utilice", "vea", "busque", "consulte", "actualice",
}
INFINITIVO = re.compile(r"^[a-záéíóúñ]{3,}(ar|er|ir)(se|le|lo|la|los|las)?$")


def empieza_con_verbo(texto):
    primera = re.sub(r"[^\wáéíóúñ]", "", texto.split()[0].lower()) if texto.split() else ""
    if primera in IMPERATIVOS:
        return "verbo en imperativo"
    if INFINITIVO.match(primera):
        return "verbo en infinitivo"
    return None


def unidades(texto):
    """Devuelve (pagina, linea, texto, es_item, seccion) para cada oración y cada ítem de lista.

    Un ítem numerado o una viñeta incluye sus líneas de continuación. 'seccion' es el título
    de la sección de requerimientos en curso, o '' fuera de ellas.
    """
    pagina, linea_pag, bloque, es_item, seccion = 1, 0, [], False, ""
    en_lista = False          # True mientras los ítems siguen a una frase terminada en ':'
    previa = ""               # última línea de texto corrido (no ítem) antes de la lista

    def cerrar():
        if not bloque:
            return
        junto, inicio_de = "", []                  # inicio_de[i]: línea donde empieza el carácter i
        for numero, trozo in bloque:      # numero = (página, línea): un bloque puede cruzar de página
            junto += trozo + " "
            inicio_de += [numero] * (len(trozo) + 1)
        junto = junto.strip()
        if es_item:
            yield (*bloque[0][0], ITEM.sub("", junto), True, seccion, en_lista)
            return
        for m in re.finditer(r"\S.*?(?:[.;?](?=\s+[A-ZÁÉÍÓÚÑ¿])|$)", junto):
            yield (*inicio_de[m.start()], m.group(0).strip(), False, seccion, False)

    for cruda in texto.splitlines():
        m = re.match(r"^### pagina (\d+)$", cruda)
        if m:                             # el salto de página no cierra el párrafo ni el ítem
            pagina, linea_pag = int(m.group(1)), 0
            continue
        linea_pag += 1
        linea = " ".join(cruda.split())
        if not linea:
            yield from cerrar(); bloque, es_item = [], False
        elif len(linea) < 70 and SECCION.match(linea):
            yield from cerrar(); bloque, es_item, previa = [], False, ""
            seccion = linea.lstrip("# ")
        elif len(linea) < 70 and (FIN_SECCION.match(linea) or linea.startswith("#")):
            yield from cerrar(); bloque, es_item, previa = [], False, ""
            seccion = ""
        elif ITEM.match(linea):
            if not es_item:   # primer ítem: ¿lo introduce una frase terminada en ':'?
                en_lista = previa.endswith(":")
            yield from cerrar()
            bloque, es_item = [((pagina, linea_pag), linea)], True
        else:
            if not es_item:
                en_lista, previa = False, linea
            bloque.append(((pagina, linea_pag), linea))
    yield from cerrar()


def clasificar(texto, tabla, defecto):
    for etiqueta, patron in tabla:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return etiqueta, m.group(0)
    return defecto, None


def separar_reglas(unidades_):
    """Un ítem que termina con una regla de selección ("De los últimos 4 ejercicios haga 3.")
    se parte en dos: el ítem y la regla, que se reporta aparte."""
    for pagina, linea, frase, es_item, seccion, en_lista in unidades_:
        oraciones = [m.group(0).strip() for m in ORACION.finditer(frase)]
        reglas = [o for o in oraciones[1:] if SELECCION.search(o)] if es_item else []
        if not reglas:
            yield pagina, linea, frase, es_item, seccion, en_lista
            continue
        yield pagina, linea, " ".join(o for o in oraciones if o not in reglas), es_item, seccion, en_lista
        for r in reglas:
            yield pagina, linea, r, False, seccion, False


def detectar(texto, fuente):
    candidatos, introduccion = [], None
    for pagina, linea, frase, es_item, seccion, en_lista in separar_reglas(unidades(texto)):
        prioridad, disparador = clasificar(frase, PRIORIDAD, None)
        verbo = empieza_con_verbo(frase)
        if prioridad is None and es_item and introduccion:
            prioridad, disparador = introduccion, "ítem de una lista de obligaciones"
        if prioridad is None and es_item and seccion:
            prioridad, disparador = "Debe", f"ítem de la sección «{seccion}»"
        if prioridad is None and verbo and (es_item or seccion):
            prioridad, disparador = "Debe", verbo
        if prioridad is None and seccion and len(frase.split()) >= 5 and not frase.endswith(":"):
            prioridad, disparador = "Debe", f"frase de la sección «{seccion}»"
        if not es_item:  # una frase que termina en ':' abre una lista
            introduccion = prioridad if frase.endswith(":") and prioridad else None
        if prioridad is None or (not es_item and frase.endswith(":") and introduccion):
            continue       # sin señal de requerimiento, o solo introduce la lista
        if SELECCION.search(frase):
            tipo, disparador = "RES", "regla de selección"
        elif seccion:
            tipo = "RF"    # en una sección de ejercicios cada ítem es un entregable
        else:
            tipo, _ = clasificar(frase, TIPO, "RF")
        if seccion:
            confianza = "alta" if es_item or verbo or tipo == "RES" else "media"
        else:
            confianza = "media" if es_item and en_lista else "baja"
        candidatos.append({"id": f"C-{len(candidatos) + 1:02d}", "tipo": tipo, "prioridad": prioridad,
                           "confianza": confianza, "texto": frase, "fuente": fuente, "pagina": pagina,
                           "linea": linea, "seccion": seccion, "disparador": disparador})
    return candidatos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texto")
    ap.add_argument("--fuente", required=True)
    ap.add_argument("--json")
    ap.add_argument("--confianza", choices=["alta", "media", "baja"], default="baja",
                    help="confianza mínima de los candidatos que se reportan (por defecto, todos)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    with open(args.texto, encoding="utf-8") as f:
        candidatos = detectar(f.read(), args.fuente)
    nivel = {"alta": 3, "media": 2, "baja": 1}
    candidatos = [c for c in candidatos if nivel[c["confianza"]] >= nivel[args.confianza]]
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(candidatos, f, ensure_ascii=False, indent=2)
    print(f"{len(candidatos)} candidatos en {args.fuente}")
    for c in candidatos:
        print(f"{c['id']}  {c['tipo']:<3} {c['prioridad']:<8} {c['confianza']:<5} p.{c['pagina']:<2} l.{c['linea']:<3} {c['texto'][:100]}")
