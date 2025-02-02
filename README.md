# TalaTrivia!
TalaTrivia es una API que se encarga de gestionar y realizar trivias a los usuarios que se registren e inicien sesión en la API 🚀

Los usuarios podrán revisar las trivias que están inscritas y participar en ellas, y los administradores podrán gestionar las trivias, preguntas e inscribir usuarios en las trivias.

## Tecnologías 🖥️
Las tecnologías que se utilizaron fueron las siguientes:
 - Python
 - Django
 - Django Rest Framework
 - Docker

## Instalación 🔧
Para instalar TalaTrivia se debe realizar los siguientes pasos:

con la terminal en la raiz del proyecto, ejecutar el siguiente comando: `docker compose up -d`. Docker se encargará de realizar la instalación de las dependencias y configurar el ambiente para que TalaTrivia pueda funcionar correctamente.

## Rutas 🛣️
Las diferentes rutas y endpoints para poder utilizar TalaTrivia son las siguientes:

### Autenticación 🔐
Para la autenticación de usuarios, utiliza los siguientes endpoints:

- `api/v1/users/`: Obtiene la información del usuario que ha iniciado sesión. Métodos disponibles: GET. Auth: Bearer JWT

- `api/v1/users/login/`: Inicia sesión de usuario. Métodos disponibles: POST. Body: email: string, password: string 

- `api/v1/users/register/`: Registra nuevos usuarios. Métodos disponibles: POST. Body: name: string, username: string, email: string, password: string

- `api/v1/users/token/refresh/` Refresca el token de acceso. Métodos disponibles: POST. Body: refresh: string

- `api/v1/users/logout/` Cierra sesión del usuario. Métodos disponibles: POST. Auth: Bearer JWT 

- `api/v1/users/edit/` Actualiza los datos del usuario. Métodos disponibles: PATCH. Auth: Bearer JWT. Body: name: string, username: string, email: string, password: string

### Trivia 🎢
Para la gestión de la trivia, se utiliza los siguientes endpoints:
- `api/v1/game/admin/trivia/` permite gestionar las trivias disponibles. Métodos disponibles: GET, POST, PUT. Body: POST, PUT: name: string, description: string. Auth: Bearer JWT

- `api/v1/game/admin/trivia/<int:id>/` permite eliminar la trivia deseada. Métodos disponibles: DELETE. Query Params: id: id de la trivia a eliminar. Auth: Bearer JWT.

- `api/v1/game/admin/trivia/<int:id>/question/` Permite gestionar las preguntas de la trivia. Métodos disponibles: GET, POST, PUT. Query Params: id: id de la trivia. Body: POST: question: string, difficulty: number, PUT: id: number, question: string, difficulty: number. Auth: Bearer JWT.

- `api/v1/game/admin/trivia/<int:id>/question/<int:idQuestion>` Permite eliminar la pregunta seleccionada de la trivia. Métodos disponibles: DELETE, Query Params: id: Id de la trivia, idQuestion: id de la pregunta a eliminar. Auth: Bearer JWT.

- `api/v1/game/admin/trivia/question/<int:id>/` Permite gestionar las respuestas de la pregunta. Métodos disponibles: GET, POST, PUT. Query Params: id: Id de la pregunta. Body: POST: answer: string, is_correct: number. PUT: id: number, answer: string, is_correct: number. Auth: Bearer JWT.

- `api/v1/game/admin/trivia/question/<int:id>/<int:idAnswer>` Permite eliminar la respuesta de la pregunta. Métodos disponibles: DELETE. Query Params: id: Id de la pregunta, idAnswer: id de la respuesta. Auth: Bearer JWT.
- `api/v1/game/admin/trivia/user/` Permite gestionar a los usuarios que participarán en las trivias. Métodos disponibles: GET. Auth: Bearer JWT.

- `api/v1/game/admin/trivia/user/<int:id>/` Permite agregar o eliminar los usuarios que participarán en las trivias. Métodos disponibles: POST, DELETE. Query Params: id: id del usuario. Body: POST: trivia: number. Auth: Bearer JWT

Para los usuarios, se utilizan los siguientes endpoints:

- `api/v1/game/trivia/` Lista todas las trivias que el usuario está registrado. Métodos disponibles: GET. Auth: Bearer JWT.

- `api/v1/game/trivia/<int:id>/` Obtiene la pregunta de la trivia y publica la respuesta. Métodos disponibles: GET, POST. Query Params: id: id de la trivia. Body: POST: question: number, answer: number. Auth: Bearer JWT

- `api/v1/game/leaderboard/` Permite ver el listado general de jugadores y sus puntajes. Métodos disponibles: GET.

- `api/v1/game/leaderboard/<int:id>/` Permite ver el listado específico de jugadores que participan/participaron de la trivia. Métodos disponibles: GET. Query Params: id: id de la trivia. 

## Instrucciones

Se debe iniciar sesión con el usuario y contraseña. Si no posee una cuenta, debe registrarse antes de iniciar sesión. Al iniciar sesión, se entregarán 2 tokens: el access representa el token para el acceso de los diferentes endpoints dependiendo del rol. El refresh ayuda a refrescar el token de acceso si es que este expira.

Para todas las rutas de administración se requiere una autenticación mediante Bearer JWT, mientras que en las rutas de trivia, sólo la tabla de puntuación tiene acceso público. Para participar de las trivias debe iniciar sesión y autenticarse mediante Bearer JWT.


## Próximamente
Hasta el momento esta versión será la que estará disponible para la revisión de la prueba técnica. Sin embargo, estaré trabajando en una interfaz gráfica que conecte la api, todo mediante Django. Por lo que si no alcanzo a terminarla, estará esta versión que será sólo backend 😅
