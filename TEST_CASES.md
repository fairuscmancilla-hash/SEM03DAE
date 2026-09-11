# Casos de prueba — Quiz Studio

## Objetivo

Validar los modelos, relaciones y flujos principales de la aplicación `quiz` sin modificar la base de datos local. Django ejecuta estos casos en una base de datos temporal que se elimina al terminar.

## Ejecución

Desde la carpeta `src/`:

```text
python manage.py test quiz --verbosity 2
```

## Casos automatizados

| ID | Caso | Datos o acción | Resultado esperado |
|---|---|---|---|
| TC-01 | Relaciones y puntaje predeterminado | Crear un examen, una pregunta y una alternativa | La pregunta pertenece al examen, la alternativa pertenece a la pregunta y `score` es `1` |
| TC-02 | Representación de modelos | Convertir `Exam`, `Question` y `Choice` a texto | Cada modelo devuelve su título o texto correspondiente |
| TC-03 | Listado de exámenes | Solicitar la ruta principal con un examen registrado | Respuesta HTTP `200`, plantilla correcta y datos del examen visibles |
| TC-04 | Detalle del examen | Solicitar el detalle de un examen con preguntas y alternativas | Respuesta HTTP `200`, contenido completo y respuesta correcta identificada |
| TC-05 | Formulario de nueva pregunta | Abrir el formulario de creación | Respuesta HTTP `200` y cuatro formularios de alternativas disponibles |
| TC-06 | Creación válida | Enviar una pregunta con cuatro alternativas y exactamente una correcta | Redirección al detalle; se crean una pregunta y cuatro alternativas con una sola correcta |
| TC-07 | Ninguna alternativa correcta | Enviar una pregunta sin marcar una alternativa correcta | El formulario muestra un error y no se guarda la pregunta |
| TC-08 | Varias alternativas correctas | Enviar una pregunta con dos alternativas marcadas como correctas | El formulario muestra un error y no se guarda la pregunta |

## Resultado obtenido

```text
Found 8 test(s).
Ran 8 tests
OK
```

Todos los casos terminaron correctamente. La ejecución no alteró `src/db.sqlite3` porque Django utilizó y destruyó una base de datos de prueba independiente.
