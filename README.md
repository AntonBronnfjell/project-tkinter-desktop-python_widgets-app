# Lista de Tareas con Tkinter

Aplicación de escritorio (GUI) en Python usando Tkinter y ttk. Permite crear, editar, completar y eliminar tareas. Incluye filtrado, contador y persistencia en JSON con escritura atómica.

## Requisitos
- Python 3.9+

## Ejecutar
```bash
python3 main.py
```

## Estructura
```
app/
  __init__.py
  models.py        # Modelo Task
  storage.py       # Repositorio JSON
  widgets.py       # Widgets reutilizables (ScrollableFrame, TaskItem)
  ui.py            # Ventana principal TodoApp
main.py
```

## Características
- Añadir nuevas tareas con Enter o botón "Añadir".
- Editar título de tarea in-place.
- Marcar como completada con checkbox.
- Eliminar tarea individual.
- Eliminar todas las completadas desde menú Edición.
- Filtros: Todas / Activas / Completadas.
- Contador de total, activas y completadas.
- Diseño responsive con `grid` y contenedor scrollable.
- Persistencia local en `data/tasks.json` (se crea automáticamente).

## Atajos
- Ctrl/Cmd + N: enfocar caja para nueva tarea.
- Enter: añadir tarea cuando estás en la caja de texto.
- Esc: limpiar caja de texto.

## Buenas prácticas aplicadas
- Separación de responsabilidades (modelo, almacenamiento, UI, widgets).
- Nombres descriptivos y tipos explícitos.
- Escritura atómica en JSON para evitar corrupción.

## Licencia
MIT

