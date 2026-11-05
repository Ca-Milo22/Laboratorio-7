# ClassroomHub

ClassroomHub es una aplicación web educativa creada con Django para el Laboratorio 6. Su objetivo es demostrar el flujo **URL → vista → plantilla → respuesta HTTP** mediante tres páginas navegables.

## Requisitos

- Python 3.12 o superior compatible con Django 6.1.3.
- Git (opcional, para versionar el proyecto).

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# En Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
python manage.py check
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>.

## Rutas disponibles

- `/` — página principal.
- `/resources/` — listado de recursos enviado desde la vista.
- `/about/` — información del proyecto.
- `/admin/` — administración de Django, disponible para prácticas posteriores.

## Ejecutar pruebas

```bash
python manage.py test
```

Las pruebas comprueban respuestas `200`, uso de plantillas, contexto, navegación y respuesta `404` para una ruta inexistente.

## Estructura principal

```text
classroom-hub/
├── config/                 # Configuración y URLs globales
├── pages/                  # Aplicación de páginas públicas
│   ├── templates/pages/    # Plantillas HTML
│   ├── urls.py             # Rutas nombradas
│   ├── views.py            # Vistas y datos de ejemplo
│   └── tests.py            # Pruebas automatizadas
├── manage.py
├── requirements.txt
└── .gitignore
```

Este proyecto es para desarrollo y aprendizaje; `DEBUG=True` y la clave incluida no deben utilizarse en producción.
