# Ejercicio 3: Chatbot con documentos de clase

## Objetivo

Desarrollar un asistente de consulta que responda preguntas sobre el contenido de los documentos de clase utilizando **RAG** (*Retrieval-Augmented Generation*), una técnica que busca fragmentos relevantes en los documentos y los pasa a un modelo generativo para elaborar respuestas fundamentadas.

## Archivos

- **Notebook:** `notebooks/Ejercicio_3_Chatbot_con_documentos_de_clase.ipynb`
- **Documentos de entrada:** Siete PDF en `documentos_clase/`
  - `1._INTRODUCCION_IA_26_2.pdf`
  - `2._Autómatas_Celulares_26_2.pdf`
  - `3_Algoritmos_Genéticos_26_2.pdf`
  - `4._Programacion_Genetica_26_2.pdf`
  - `5_Redes_Neuronales1_2026_2.pdf`
  - `6._Machine_Learning_26_2.pdf`
  - `7._Gen_Ai_2026_2.pdf`

## Flujo de la solución

```
Cargar PDF
    ↓
Extraer texto y conservar número de página
    ↓
Dividir en fragmentos (con solapamiento)
    ↓
Crear representaciones semánticas (embeddings)
    ↓
Indexar los embeddings en memoria
    ↓
Procesar pregunta del usuario
    ↓
Recuperar fragmentos más cercanos
    ↓
Enviar al modelo generativo con el contexto
    ↓
Retornar respuesta con citas y fuentes
```

## Ejecución

### En Google Colab

1. Abre el notebook directamente desde el repositorio:
   - Ir a [colab.research.google.com](https://colab.research.google.com)
   - Archivo → Abrir notebook → GitHub
   - Pegar: `Bamp100310/IA-minirobots`
   - Seleccionar `7. IA Generativa/notebooks/Ejercicio_3_Chatbot_con_documentos_de_clase.ipynb`

2. Ejecutar las celdas en orden:
   - **Celda 1-2:** Instalar dependencias (`pymupdf`, `requests`)
   - **Celda 3-4:** Encontrar y cargar los PDF
   - **Celda 5-6:** Extraer texto de cada página
   - **Celda 7-8:** Dividir el texto en fragmentos
   - **Celda 9:** Iniciar Ollama e instalar modelos (`bge-m3`, `llama3.2:3b`)
   - **Celda 10:** Crear el índice de embeddings
   - **Celda 11-12:** Consultar el chatbot con una pregunta de prueba
   - **Celda 13:** Conversación interactiva

3. **Tiempo esperado:**
   - Descarga de modelos: 10–30 minutos (depende de la conexión)
   - Indexación: 2–5 minutos
   - Consulta: 10–30 segundos por pregunta

### En Jupyter local

```bash
# Instalar dependencias
pip install -r "7. IA Generativa/requirements.txt" pymupdf requests

# Abrir el notebook
jupyter notebook "7. IA Generativa/notebooks/Ejercicio_3_Chatbot_con_documentos_de_clase.ipynb"
```

**Prerequisitos:**
- Python 3.10+
- Ollama instalado y ejecutándose en `http://127.0.0.1:11434`
  - Descargar desde [ollama.com](https://ollama.com)
  - Ejecutar: `ollama serve`

## Componentes principales

### 1. Lectura de PDF (`pymupdf`)

Extrae el texto de cada página preservando el nombre del archivo y el número de página como metadatos:

```python
with pymupdf.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text('text').strip()
        pages.append({
            'source': pdf_path.name,
            'page': page_number,
            'text': text
        })
```

### 2. División en fragmentos

Los fragmentos mantienen contexto mediante solapamiento:
- **Tamaño:** 1200 caracteres
- **Solapamiento:** 200 caracteres
- Se respeta los límites de palabras para evitar cortes de texto incompletos

### 3. Embeddings multilingües

Se usa el modelo `bge-m3` (optimizado para español e inglés) para crear representaciones semánticas:

```python
response = requests.post(
    f'{OLLAMA_URL}/api/embed',
    json={'model': 'bge-m3', 'input': texts},
    timeout=300
)
embeddings = response.json()['embeddings']
```

### 4. Búsqueda por similitud coseno

Para cada pregunta se recuperan los `TOP_K=5` fragmentos más cercanos:

```python
ranked = sorted(
    ((cosine_similarity(query_embedding, vector), index)
     for index, vector in enumerate(embedding_vectors)),
    reverse=True
)[:TOP_K]
```

### 5. Generación con modelo local

Se construye un prompt que incluye:
- El contexto recuperado con citas `[1]`, `[2]`, etc.
- La pregunta del usuario
- Instrucciones para responder únicamente en español, citar fuentes y declarar cuando no hay evidencia

```python
prompt = f'''Eres un asistente para estudiar Inteligencia Artificial.
Responde en español y utiliza únicamente la información del CONTEXTO.
Si el contexto no responde la pregunta, indícalo claramente y no inventes datos.

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:'''
```

El modelo `llama3.2:3b` genera una respuesta de hasta 400 tokens con baja temperatura (0.1) para mayor consistencia.

## Validación

Tras cada respuesta, se muestran:
- El contenido de la respuesta
- Las fuentes recuperadas con número de página y puntuación de similitud

**Para validar el resultado:**
1. Revisa la página citada en el PDF original
2. Verifica que el fragmento recuperado realmente respalda la respuesta
3. Si la respuesta no es relevante, ajusta `CHUNK_SIZE`, `CHUNK_OVERLAP` o `TOP_K` y reindexal

## Limitaciones y mejoras

| Aspecto | Limitación | Mejora sugerida |
|---------|-----------|-----------------|
| PDF escaneados | No se extrae texto de imágenes | Integrar OCR (`pytesseract`, `PaddleOCR`) |
| Persistencia | El índice se pierde al reiniciar Colab | Guardar embeddings en archivo o base de datos |
| Precisión | Embeddings pueden recuperar contexto irrelevante | Aumentar `TOP_K` o ajustar `CHUNK_SIZE` |
| Alucinaciones | El modelo puede inventar información | Añadir validación de que la respuesta está en el contexto |
| Soporte multiidioma | Optimizado para español e inglés | Cambiar modelo de embeddings (ej. `multilingual-e5-large`) |

## Preguntas sugeridas para probar

- "¿Qué es la inteligencia artificial?"
- "¿Cómo funcionan los autómatas celulares?"
- "¿Cuál es la diferencia entre algoritmos genéticos y programación genética?"
- "¿Qué es una red neuronal artificial?"
- "¿Para qué se usa el aprendizaje automático?"
- "¿Qué es la inteligencia artificial generativa?"

## Referencia: Modelos de Ollama

### `bge-m3` (embeddings)
- Multilingüe (>100 idiomas, incluyendo español)
- ~15 MB
- Dimensión: 1024
- Tiempo de respuesta: <100 ms por texto

### `llama3.2:3b` (generación)
- Pequeño pero potente (3 mil millones de parámetros)
- Soporte para instrucciones en español
- ~2 GB de memoria
- Tiempo por respuesta: 10–30 segundos (depende de la longitud del prompt y el hardware)

## Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| No encuentra los PDF | Ruta relativa no válida | Verificar que `documentos_clase/` existe en la carpeta correcta |
| Ollama no inicia en Colab | Límite de recursos | Reiniciar la sesión o usar Hardware acelerador (GPU T4) |
| Las respuestas son genéricas | Embeddings no recuperan contexto correcto | Aumentar `TOP_K` o reducir `CHUNK_SIZE` |
| Ollama: "CUDA out of memory" | Falta de VRAM | Usar modelo más pequeño o reducir tamaño del lote |
| PDF no tiene texto extraíble | PDF es una imagen escaneada | Aplicar OCR con `pytesseract` o Colab OCR |

## Referencias

- **RAG:** Lewis et al. (2021). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- **Ollama:** https://ollama.com/
- **BGE-M3:** https://huggingface.co/BAAI/bge-m3
- **Llama 3.2:** https://www.llama.com/
- **PyMuPDF:** https://pymupdf.readthedocs.io/

---

**Autor:** Ejercicio 3, sección 7.11 del curso de Inteligencia Artificial y Minirobots  
**Última actualización:** 2026
