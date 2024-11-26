# Django CRUD Application

This is a simple Django-based CRUD application for managing tasks.

## Features
- Create, Read, Update, and Delete tasks.
- Uses PostgreSQL as the database.

## Installation
1. Clone the repository
2. Set up a virtual environment and install dependencies:
    - python3 -m venv venv source venv/bin/activate pip install -r requirements.txt
3. Run migrations and start the server:
    - python manage.py migrate python manage.py runserver

## API Endpoints
- `GET /api/tasks/` - List all tasks.
- `POST /api/tasks/` - Create a new task.
- `GET /api/tasks/<id>/` - Retrieve a task.
- `PUT /api/tasks/<id>/` - Update a task.
- `DELETE /api/tasks/<id>/` - Delete a task.

## Preguntas clave

Una vez finalizado el ejercicio, responde las siguientes preguntas:

1. Explica los pasos necesarios para configurar un entorno Django en un servidor Linux, incluyendo la base de datos PostgreSQL, y cómo realizarías el despliegue.

Para configurar un entorno Django en un servidor Linux, el primer paso es asegurar que el sistema esté actualizado e instalar las dependencias necesarias, como Python, pip, y el entorno virtual. Luego, se crea un entorno virtual para gestionar las dependencias del proyecto, lo que permitirá aislar los paquetes que serán utilizaados en la aplicación. Una vez que el entorno virtual esté listo, se debe instalar Django y las librerías requeridas, como `psycopg2`, que es el adaptador de PostgreSQL para Django. Luego, se debe instalar y configurar PostgreSQL, creando una base de datos y un usuario que permita a Django interactuar con la base de datos correctamente. Esto incluye la configuración de los archivos de PostgreSQL para permitir conexiones locales y reiniciar el servicio para aplicar los cambios.

El siguiente paso es configurar Django para que se conecte a PostgreSQL modificando el archivo de configuración del proyecto, `settings.py`, para incluir los detalles de la base de datos. Luego, se deben ejecutar las migraciones de Django para crear las tablas necesarias en la base de datos. Para el despliegue, se utiliza un servidor de aplicaciones como Gunicorn, que se ejecuta en segundo plano para manejar las solicitudes HTTP, o se puede demonizar la app, arrancarla desde un crontab o como un proceso de systemd. Para hacer que la aplicación sea accesible públicamente, se utiliza un servidor web como Nginx, que actúa como proxy inverso, redirigiendo las solicitudes HTTP hacia el servidor de Gunicorn, o hacia el puerto local en el que esté corriendo la aplicación. Finalmente, es importante asegurarse de que la aplicación esté protegida mediante medidas de seguridad como la configuración de HTTPS y la protección contra ataques comunes, como CSRF y la inyección de SQL.

2. Si el sistema de tareas crece y hay miles de registros, ¿cómo optimizarías las consultas para que la aplicación siga siendo rápida? Explica al menos dos estrategias.

Podemos utilizar dos estrategias:

### Paginación
Para evitar que todas las tareas se carguen de una vez y sobrecarguen el servidor, es recomendable usar paginación en las vistas que devuelven listas de tareas. Django proporciona una clase Paginator que puedes usar para dividir los resultados en páginas más pequeñas y hacer que la aplicación sea más eficiente.

Ejemplo:

```python
from django.core.paginator import Paginator

class TaskListCreateView(View):
    def get(self, request):
        tasks = Task.objects.all()
        paginator = Paginator(tasks, 10)  # 10 tareas por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return JsonResponse(list(page_obj), safe=False)
```

### Indexación en la base de datos
Crear índices en las columnas que más se consultan, como el status o created_at, para que las búsquedas y filtros sean más rápidos.

Ejemplo:

```python
class Task(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
```

3. ¿Qué medidas de seguridad implementarías para proteger esta aplicación Django de amenazas comunes como inyección SQL, CSRF y acceso no autorizado?

### Prevención de inyección SQL 
Django utiliza un ORM que, por defecto, protege contra inyección SQL. En lugar de construir consultas SQL manualmente, siempre se debe utilizar el ORM de Django para acceder a la base de datos. Esto asegura que las consultas se construyan de forma segura, escapando los datos correctamente.

### Protección contra CSRF (Cross-Site Request Forgery)
Django incluye protección CSRF por defecto. Es necesaio incluir el token CSRF en las llamadas a la API y asegurarse de que esta protección esté activada en las vistas que aceptan datos de formularios.

### Acceso no autorizado
En necesario utilizar el sistema de autenticación y autorización de Django para proteger las vistas que requieren autenticación de usuario. Es posible usar decoradores como @login_required para proteger vistas, o bien las vistas basadas en clases como LoginRequiredMixin.

### Seguridad HTTPS
Configurar el servidor para usar HTTPS en lugar de HTTP. Esto garantizará que la comunicación entre el cliente y el servidor esté cifrada y protegida contra ataques como "Man-in-the-Middle". Si el reverse proxy utilizado es Nginx, se puede redirigir todo el tráfico HTTP a HTTPS y configurar certificados SSL utilizando herramientas como Let's Encrypt.