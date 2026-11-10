# ClassroomHub

ClassroomHub es una aplicación web educativa desarrollada con Django para el Laboratorio 7 del SENA. Su objetivo es organizar y mostrar recursos de aprendizaje mediante categorías, utilizando una base de datos MySQL.

El proyecto permite consultar recursos, conocer su disponibilidad y administrar la información desde el panel de Django.

## Requisitos

- Python 3.12 o superior compatible con Django 6.1.3.
- MySQL Server 8.4 o superior.
- Git (opcional, para descargar y versionar el proyecto).

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Ca-Milo22/Laboratorio-7.git
cd Laboratorio-7
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows CMD:

```cmd
.venv\Scripts\activate
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración de MySQL

1. Iniciar MySQL Server.
2. Crear la base de datos `classroom_hub`.
3. Crear un usuario de MySQL con permisos sobre esa base de datos.
4. Copiar el archivo `.env.example` y crear un archivo llamado `.env` en la raíz del proyecto.
5. Configurar los datos de conexión en `.env`:

```env
DB_NAME=classroom_hub
DB_USER=classroomhub_user
DB_PASSWORD=tu_contrasena_privada
DB_HOST=127.0.0.1
DB_PORT=3306
```

Reemplazar `tu_contrasena_privada` por la contraseña correspondiente.

**Importante:** el archivo `.env` contiene información privada y no debe subirse a GitHub.

## Migraciones

Para crear las tablas y aplicar los cambios de los modelos en MySQL, ejecutar:

```bash
python manage.py migrate
```

## Crear administrador

Para ingresar al panel administrativo:

```bash
python manage.py createsuperuser
```

Django solicitará un nombre de usuario y una contraseña.

## Ejecutar el servidor

Comprobar la configuración:

```bash
python manage.py check
```

Iniciar el servidor:

```bash
python manage.py runserver
```

Abrir en el navegador:

http://127.0.0.1:8000/

## Rutas disponibles

- `/` — Página principal.
- `/resources/` — Listado de recursos de aprendizaje.
- `/resources/available/` — Listado de recursos disponibles.
- `/about/` — Información del proyecto.
- `/admin/` — Panel administrativo de Django.

## Ejecutar pruebas

Para ejecutar las pruebas automatizadas:

```bash
python manage.py test pages
```

Las pruebas verifican el funcionamiento de las páginas, las plantillas, los recursos, las categorías, las relaciones entre modelos, la disponibilidad y las respuestas de error.

Las pruebas utilizan una base de datos temporal independiente.

## Estructura principal

```text
classroom-hub/
├── config/
│   ├── settings.py
│   └── urls.py
├── pages/
│   ├── migrations/
│   ├── templates/pages/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Tecnologías utilizadas

- Python.
- Django.
- MySQL.
- HTML y CSS.
- Git y GitHub.

## Nota

ClassroomHub es un proyecto académico desarrollado para el aprendizaje y la práctica de desarrollo web. La configuración actual está orientada al entorno de desarrollo y no debe utilizarse directamente en producción.