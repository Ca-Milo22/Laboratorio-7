# Entrega — Laboratorio 6

## Producto

Se entrega **ClassroomHub**, una aplicación web Django con tres páginas navegables:

- `/` — página principal.
- `/resources/` — recursos de aprendizaje recibidos desde el contexto de la vista.
- `/about/` — información del proyecto.

## Recorrido de una solicitud

Cuando el navegador solicita `/resources/`, `config/urls.py` incluye las rutas de `pages/urls.py`. Allí la ruta nombrada `pages:resources` dirige la solicitud a `pages/views.py`. La vista prepara la lista `RESOURCES` y renderiza `pages/resources.html`. La plantilla extiende `pages/base.html`, genera el HTML y Django devuelve una respuesta HTTP `200` al navegador.

Una dirección no declarada, como `/unknown/`, produce una respuesta HTTP `404 Not Found`.

## Responsabilidades

- `config/settings.py`: configuración global y registro de `pages` en `INSTALLED_APPS`.
- `config/urls.py`: configuración principal de URLs.
- `pages/urls.py`: rutas públicas con nombres.
- `pages/views.py`: comportamiento de cada página y datos de ejemplo.
- `pages/templates/pages/`: presentación HTML reutilizable.
- `pages/tests.py`: pruebas automatizadas.
- `.venv/`: entorno aislado, excluido del ZIP y del repositorio.
- `requirements.txt`: versiones de dependencias para reproducir el proyecto.

## Verificación realizada

```text
System check identified no issues (0 silenced).
Ran 4 tests in 0.010s
OK
```

## Comando para reproducir

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py test
python manage.py runserver
```
