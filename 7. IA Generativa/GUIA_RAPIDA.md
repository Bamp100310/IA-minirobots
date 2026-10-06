# Guía Rápida: Chatbot con documentos de clase

## 🚀 Iniciar en 30 segundos

### 1. Abrir en Colab
```
https://colab.research.google.com
→ Archivo → Abrir notebook → GitHub
→ Repositorio: Bamp100310/IA-minirobots
→ Seleccionar: 7. IA Generativa/notebooks/Ejercicio_3_Chatbot_con_documentos_de_clase.ipynb
```

### 2. Ejecutar las celdas (en orden)
- ✅ Celda 1: **Instalar dependencias** (pymupdf, requests) — ~30 seg
- ✅ Celda 2: **Cargar PDF** — ~5 seg
- ✅ Celda 3: **Extraer texto** — ~2 seg
- ✅ Celda 4: **Dividir en fragmentos** — ~1 seg
- ✅ Celda 5: **Iniciar Ollama + descargar modelos** — **10-30 min** ⏱️
- ✅ Celda 6: **Crear índice semántico** — ~2 min
- ✅ Celda 7-8: **Probar con una pregunta** — ~15 seg
- ✅ Celda 9: **Conversación interactiva** — ∞ (hasta que cierres)

---

## 📋 ¿Qué pasa en cada paso?

| Paso | Código | Salida esperada |
|------|--------|-----------------|
| **Instalar** | `%pip -q install pymupdf requests` | ✅ (sin errores) |
| **Cargar PDF** | Busca en `documentos_clase/` | Encuentra 7 PDF |
| **Extraer** | Lee cada página preservando número | 500+ páginas extraídas |
| **Fragmentar** | Divide en trozos de 1200 caracteres | 1500+ fragmentos |
| **Ollama** | Descarga `bge-m3` y `llama3.2:3b` | Modelos listos en `~3.5 GB` |
| **Indexar** | Crea embeddings para cada fragmento | 1500+ embeddings en memoria |
| **Consultar** | `ask_documents("¿Qué es la IA?")` | Respuesta con citas |

---

## 🎯 Ejemplo de uso

```python
# Una vez que el índice está creado (celda 6), ejecuta:

answer = ask_documents("¿Qué es la inteligencia artificial?")
```

### Salida esperada:
```
📚 RESPUESTA DEL ASISTENTE:

La inteligencia artificial es una rama de la informática que se ocupa del 
desarrollo de máquinas y sistemas que pueden realizar tareas que normalmente 
requerirían inteligencia humana. Esto incluye el aprendizaje automático, 
el reconocimiento del lenguaje natural, la visión por computadora, etc. [1][2]

---
FUENTES RECUPERADAS:
[1] 1._INTRODUCCION_IA_26_2.pdf (página 2) — similitud: 0.87
[2] 1._INTRODUCCION_IA_26_2.pdf (página 5) — similitud: 0.83
[3] 7._Gen_Ai_2026_2.pdf (página 1) — similitud: 0.78
```

---

## 🔧 Personalización

### Cambiar el número de resultados recuperados
```python
TOP_K = 3  # Mostrar solo los 3 más relevantes (por defecto: 5)
```

### Cambiar el tamaño de los fragmentos
```python
CHUNK_SIZE = 800      # Fragmentos más pequeños = búsqueda más precisa
CHUNK_OVERLAP = 100   # Solapamiento más pequeño = menos contexto compartido
```

### Usar otro modelo de IA generativa
```python
CHAT_MODEL = 'mistral'  # En lugar de 'llama3.2:3b'
# (Disponible en https://ollama.com/library)
```

### Aumentar creatividad de la respuesta
```python
TEMPERATURE = 0.5  # De 0.1 (determinista) a 0.9 (creativo)
```

---

## ⚠️ Problemas comunes

### "ModuleNotFoundError: No module named 'pymupdf'"
```
→ Ejecutar la celda de instalación (celda 1)
```

### "Connection refused" en Ollama
```
→ En Windows: Iniciar la aplicación Ollama primero
→ En Colab: La celda 5 inicia automáticamente
```

### "CUDA out of memory"
```
→ En Colab: Cambiar a runtime con GPU T4
→ En local: Cambiar a modelo más pequeño (ej. llama2 en lugar de llama3.2)
```

### Las respuestas no son relevantes
```
→ Aumentar TOP_K (buscar más contexto)
→ Reducir CHUNK_SIZE (fragmentos más granulares)
→ Verificar que los PDF tengan texto extraíble (no escaneados)
```

### "No se encuentran los PDF"
```
→ Verificar ruta: documentos_clase/ debe estar en la misma carpeta que el notebook
→ En Colab: Subir manualmente o montar Google Drive con:
   from google.colab import drive
   drive.mount('/content/drive')
   PDF_FOLDER = '/content/drive/My Drive/documentos_clase/'
```

---

## 📊 Performance esperado

| Componente | Tiempo | Notas |
|-----------|--------|-------|
| Instalación de dependencias | 30 seg | Una sola vez |
| Descarga de modelos | 10-30 min | Depende de conexión; una sola vez |
| Extracción de texto | 2 seg | Una sola vez por sesión |
| Indexación (embeddings) | 2-5 min | Una sola vez; depende de `CHUNK_SIZE` |
| Consulta individual | 10-30 seg | Recuperación + generación |

**En Colab con GPU T4:** ~5 min de setup total, después consultas en 15 seg  
**En Colab con CPU:** ~30 min de setup, después consultas en 30 seg  
**En local (GPU RTX):** ~2 min de setup, después consultas en 5 seg

---

## 🎓 Conceptos clave aprendidos

### RAG (Retrieval-Augmented Generation)
- **Retrieval:** Busca documentos relevantes
- **Augment:** Incluye los documentos en el prompt
- **Generation:** El modelo genera respuesta basada en documentos reales

### Embeddings
- Representación numérica de texto (vector de 1024 números)
- Permite medir similitud entre textos
- `bge-m3`: multilingüe, optimizado para español

### Similitud coseno
- Mide qué tan parecidos son dos vectores de 0 a 1
- 1.0 = idénticos, 0.0 = completamente diferentes
- Se usa para ranking de documentos relevantes

### Fragmentación con solapamiento
- Divide textos grandes en piezas manejables
- Solapamiento = contexto compartido entre fragmentos
- Evita perder información en límites de fragmentos

---

## 📚 Lecturas adicionales

- **Embedding models:** https://huggingface.co/BAAI/bge-m3
- **Ollama library:** https://ollama.com/library
- **RAG paper:** Lewis et al. "Retrieval-Augmented Generation" (2021)
- **PyMuPDF docs:** https://pymupdf.readthedocs.io/

---

## ✅ Validación final

Una vez que termines, verifica que:
- [ ] Puedes hacer preguntas sobre los 7 PDF de clase
- [ ] Las respuestas incluyen citas con número de página
- [ ] Las respuestas están en español y son relevantes
- [ ] El sistema responde "No tengo información..." cuando no hay contexto
- [ ] Puedes ajustar parámetros y ver cómo cambian los resultados

---

**🎉 ¡Felicidades! Ya tienes tu primer chatbot con RAG.**  
Prueba ahora a hacer preguntas más complejas o ajustar los parámetros.

