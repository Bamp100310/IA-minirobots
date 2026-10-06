# Esquema de `contenido.json`

```json
{
  "titulo": "Texto del título",
  "subtitulo": "Proyecto, ticket o fecha",
  "metricas": [{"valor": "11/11", "etiqueta": "pruebas que pasan"}],
  "secciones": [
    {"id": "resumen", "titulo": "Resumen", "bloques": [ ... ]}
  ]
}
```

## Tipos de bloque

| `tipo` | Campos | Uso |
|---|---|---|
| `parrafo` | `texto` | Texto corrido. Admite `**negrita**` y `` `código` `` en línea |
| `lista` | `items` (lista de textos), `ordenada` (opcional) | Viñetas o pasos |
| `codigo` | `texto`, `lenguaje`, `titulo` (opcional) | Fragmentos de código o comandos |
| `tabla` | `encabezados`, `filas` | Comparaciones y resultados |
| `nota` | `texto`, `clase` (`info`, `ok`, `aviso`) | Llamadas de atención |
| `pasos` | `items` (lista de `{"titulo", "texto"}`) | Flujos o recorridos numerados |

Una celda de tabla que empieza por `OK` o `FALLA` se colorea como resultado.
