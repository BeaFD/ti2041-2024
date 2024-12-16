Instrucciones de uso!

Instalar Python y Django:
Python (Windows)
`https://www.python.org/downloads/windows/`
Python (MacOS)
`https://www.python.org/downloads/macos/`
Python (Linux/UNIX)
`https://www.python.org/downloads/source/`

Python:
Ejecutar CMD como administrador y ejecutar `python -m pip install Django==5.1.1`

Clonar el repositorio: `git clone https://github.com/BeaFD/ti2041-2024.git`
Abrir carpeta del projecto en evaluaciones/sumativa1
Ejecutar el servidor desde la terminal: `python manage.py runserver`

Usuario Admin:
username: admin
password: inacap2024

---------------------------------------------------------------------------------------------------------------------

Funcionamiento

Abrir localhost:8000/ o 127.0.0.1:8000/

Es necesario iniciar sesión antes de empezar. Todo es navegable mediante botones. Cualquier usuario que ingrese con sus credenciales de inicio puede visualizar los productos, sin embargo, solo los usuarios con el permiso de ADMIN_PRODUCTS puede eliminar, editar o eliminar.

---------------------------------------------------------------------------------------------------------------------

Medidas de seguridad:

Protección contra CSRF

Todos los formularios de la aplicación están asegurados con un token CSRF para evitar el envío de instrucciones maliciosas mediante sesiones ya iniciadas.


Manejo de sesiones

Las sesiones de los usuarios se vencen cuando el buscador se cierra, solo pueden ser transmitidas mediante conexiones HTTPS para evitar intercepciones en conexiones inseguras, y solo puede ser accesible mediante metodos HTTP(S), no mediante codigo JavaScript, asi mitigando el riesgo de ataques XSS.


Logging

Se mantiene un log de eventos importantes para identificar potenciales intentos de acceso fallidos, ataques o intentos de acceder a modulos sin permiso.


Información sensible

El debug se mantiene en True, debido a que el debug False necesita la configuracion de un webserver para servir archivos static, por lo que los estilos no se cargarian en un entorno de desarrollo.


CORS

Los headers CORS quedan configurados con todos los hosts habilitados para no tener conflictos en el entorno de desarrollo.

---------------------------------------------------------------------------------------------------------------------

APIs

Para ver la documentación de Django Ninja, acceder a localhost:8000/api/docs o 127.0.0.1:8000/api/docs. Desde esta vista se pueden ver todos los endpoints, además de probarlos.

Para hacer los tests desde la vista de docs, se debe generar un token utilizando el usuario y contraseña "admin", "inacap2024" dentro del body de la API /token/. Posterior a eso se registra el token con el boton the "Authorize" en el campo de AuthBearer y se pueden testear las demas APIs. 