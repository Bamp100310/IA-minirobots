# Lista de revisión antes de entregar

## Pruebas
- [ ] Cada criterio `CA-NN.n` del ticket tiene al menos una prueba (`trazabilidad.py` sin faltantes).
- [ ] Cada prueba se vio fallar en rojo por la razón correcta (bitácora sin avisos).
- [ ] Ninguna prueba es tautológica (el esperado no se calcula igual que en el código).
- [ ] Las pruebas no dependen del orden, de la hora real ni de archivos fuera de `tmp_path`.
- [ ] La suite completa pasa.

## Código
- [ ] La interfaz coincide con la *Interfaz acordada* del ticket (nombres, entradas, salidas, errores).
- [ ] Los errores tienen mensajes que dicen qué se esperaba.
- [ ] No hay código muerto, impresiones de depuración ni funcionalidad fuera de alcance.
- [ ] Nombres en el vocabulario del dominio del ticket.

## Entrega
- [ ] *Commit* con referencia al ticket.
- [ ] Bitácora `bitacora_tdd.json` y salida de `pytest` guardadas para la explicación.
