# Blog API
## Instalación

### Requisitos

- Python
- Django
- Lista completa disponible en el archivo `requirements.txt`

### Inicio rápido

1. Clonar el repositorio.

    ```sh
    git clone https://github.com/Eduardonjratb/Django-REST-Framework---Blog-CRUD-.git
    ```

2. Dentro de la carpeta del proyecto, crea un entorno virtual y actívalo.

    ```sh
    cd blog2
    pip install virtualenv
    virtualenv env
    source env/bin/activate
    ```

3. Instalar los requisitos desde `requirements.txt`.

    ```sh
    pip install -r requirements.txt
    ```

4. Realizar migraciones y migrar el proyecto.

    ```sh
    python manage.py makemigrations && python manage.py migrate
    ```

5. Crear un superusuario.

    ```sh
    python manage.py createsuperuser
    ```

6. Ejecutar el servidor.

    ```sh
    python manage.py runserver
    ```

## Models

### User Model
**User:**
- `username`: string (unico)
- `email`: email
- `password`: string (min 8 chars)

### Post Model
**Post:**
- `id`: Post id (solo lectura)
- `slug`: string
- `title`: string
- `author`: user id (solo lectura)
- `body`: string
- `description`: string
- `image`: image (opcional)
- `created_at`: datetime (solo lectura)
- `updated_at`: datetime (solo lectura)

### Comment Model
**Comment:**
- `parent`: post id (solo lectura)
- `author`: user id (solo lectura)
- `body`: string
- `created_at`: datetime (solo lectura)
- `updated_at`: datetime (solo lectura)

## Puntos importantes

### Post 

| Function                          | REQUEST   | Endpoint                                      | form-data                                     |
|-----------------------------------|-----------|-----------------------------------------------|-----------------------------------------------|
| Devuelve una lista de todas las publicaciones existentes. | GET     | `http://127.0.0.1:8000/blog/`                |                                               |
| Crea una nueva publicación       | POST      | `http://127.0.0.1:8000/blog/create/`         | `title`, `body`, `description`, `image`: optional |
| Devuelve los detalles de una publicación en especifico. | GET  | `http://127.0.0.1:8000/blog/{str:slug}/`     |                                               |
| Actualiza una publicación existente          | PUT | `http://127.0.0.1:8000/blog/{str:slug}/edit`     | `title`, `body`, `description`, `image`: optional |
| Elimina una publicación existente         | DELETE    | `http://127.0.0.1:8000/blog/{str:slug}/delete`     |                                               |

### Comment 

| Function                          | REQUEST   | Endpoint                                             | form-data            |
|-----------------------------------|-----------|------------------------------------------------------|----------------------|
| Devuelve la lista de comentarios de una publicación en particular. | GET | `http://127.0.0.1:8000/blog/{str:slug}/comment/` |                      |
| Crear una nuevo comentario        | POST      | `http://127.0.0.1:8000/blog/{str:slug}/comment/create/` | `body`: comment body |
| devuelve los detalles de un comentario en especifico | GET  | `http://127.0.0.1:8000/blog/{str:slug}/comment/{int:id}/` |                      |
| Actualiza un comentario existente       | PUT | `http://127.0.0.1:8000/blog/{str:slug}/comment/{int:id}/` | `body`: comment body |
| Elimina un comentario existente       | DELETE    | `http://127.0.0.1:8000/blog/{str:slug}/comment/{int:id}/` |                      |
