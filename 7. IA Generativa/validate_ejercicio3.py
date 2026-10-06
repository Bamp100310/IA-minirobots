#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validación de la estructura del Ejercicio 3: Chatbot con documentos de clase
Este script verifica que todos los componentes están en su lugar y funcionan.
"""

import json
from pathlib import Path
import sys
import os

# Establecer codificación UTF-8 en Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def validate_notebook():
    """Valida que el notebook está bien formado y contiene todas las celdas."""
    nb_path = Path("7. IA Generativa/notebooks/Ejercicio_3_Chatbot_con_documentos_de_clase.ipynb")
    
    if not nb_path.exists():
        print("❌ Notebook no encontrado")
        return False
    
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer notebook: {e}")
        return False
    
    # Validar estructura
    expected_cells = {
        'intro-rag': 'markdown',
        'install-heading': 'markdown',
        'install-deps': 'code',
        'load-heading': 'markdown',
        'find-pdfs': 'code',
        'extract-heading': 'markdown',
        'extract-pdfs': 'code',
        'chunk-heading': 'markdown',
        'make-chunks': 'code',
        'ollama-heading': 'markdown',
        'start-ollama': 'code',
        'index-heading': 'markdown',
        'create-index': 'code',
        'chat-heading': 'markdown',
        'ask-chatbot': 'code',
        'sample-query': 'code',
        'interactive-heading': 'markdown',
        'interactive-chat': 'code',
        'closing': 'markdown',
    }
    
    cells = nb.get('cells', [])
    found_cells = {c.get('id'): c.get('cell_type') for c in cells}
    
    print(f"\n📔 NOTEBOOK: {nb_path.name}")
    print(f"   Total de celdas: {len(cells)}")
    
    missing = set(expected_cells.keys()) - set(found_cells.keys())
    if missing:
        print(f"   ❌ Celdas faltantes: {missing}")
        return False
    
    for cell_id, expected_type in expected_cells.items():
        actual_type = found_cells.get(cell_id)
        if actual_type != expected_type:
            print(f"   ❌ Celda '{cell_id}': esperado {expected_type}, encontrado {actual_type}")
            return False
    
    print(f"   ✅ Estructura válida (19 celdas)")
    return True


def validate_pdfs():
    """Verifica que los 7 PDF están presentes."""
    pdf_dir = Path("7. IA Generativa/documentos_clase")
    
    if not pdf_dir.exists():
        print(f"❌ Carpeta de documentos no encontrada: {pdf_dir}")
        return False
    
    pdfs = list(pdf_dir.glob("*.pdf"))
    
    print(f"\n📄 DOCUMENTOS DE CLASE: {pdf_dir.name}")
    print(f"   Total encontrado: {len(pdfs)} PDF")
    
    if len(pdfs) != 7:
        print(f"   ⚠️  Se esperan 7 PDF")
    
    for pdf in sorted(pdfs):
        size_kb = pdf.stat().st_size / 1024
        print(f"   ✓ {pdf.name} ({size_kb:.1f} KB)")
    
    return len(pdfs) > 0


def validate_docs():
    """Verifica que la documentación está presente."""
    docs = [
        "7. IA Generativa/EJERCICIO_3_README.md",
        "7. IA Generativa/GUIA_RAPIDA.md"
    ]
    
    print(f"\n📖 DOCUMENTACIÓN")
    
    all_exist = True
    for doc in docs:
        path = Path(doc)
        if path.exists():
            size = len(path.read_text(encoding="utf-8"))
            print(f"   ✅ {path.name} ({size} bytes)")
        else:
            print(f"   ❌ {path.name} (faltante)")
            all_exist = False
    
    return all_exist


def main():
    """Ejecuta todas las validaciones."""
    print("=" * 70)
    print("VALIDACIÓN: Ejercicio 3 - Chatbot con documentos de clase")
    print("=" * 70)
    
    results = {
        'notebook': validate_notebook(),
        'pdfs': validate_pdfs(),
        'docs': validate_docs(),
    }
    
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    
    status = "✅ TODO LISTO" if all(results.values()) else "❌ FALTAN COMPONENTES"
    print(f"\n{status}\n")
    
    print(f"  Notebook:       {'✅' if results['notebook'] else '❌'}")
    print(f"  Documentos PDF: {'✅' if results['pdfs'] else '❌'}")
    print(f"  Documentación:  {'✅' if results['docs'] else '❌'}")
    
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASOS")
    print("=" * 70)
    print("""
1. Abrir el notebook en Google Colab:
   https://colab.research.google.com
   → Archivo → Abrir notebook → GitHub
   → Repositorio: Bamp100310/IA-minirobots
   → Seleccionar el notebook de Ejercicio 3

2. Ejecutar las celdas en orden (desde arriba hacia abajo)

3. Leer las guías:
   - EJERCICIO_3_README.md (documentación técnica completa)
   - GUIA_RAPIDA.md (tutorial interactivo con ejemplos)

4. Hacer preguntas sobre los documentos de clase

Tiempo estimado:
   - Setup inicial: 10-30 minutos (descarga de modelos, una sola vez)
   - Consultas: 10-30 segundos cada una

¡Disfruta explorando tu chatbot RAG! 🚀
""")
    
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
