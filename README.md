# Description
Funny pictures REST server written in Python/Django.

# API description
Every response has a `result` property which in case of success should be equal to `ok`, otherwise it contains error message.


- `POST /auth/`
  - login.
    - `username`
    - `password`
- `DELETE /auth/`
  - logout.
- `GET /users/`
  - returns list of usernames in system (not sure if it's needed.
- `POST /users/`
  - registers new user.
    - `username`
    - `password`
    - `email`
- `GET /users/<username>`
  - returns some info about user.
- `DELETE /users/<username>`
  - removes a user. available only for user itself and for superuser.
- `GET /images/`
  - returns the images (all by default).
  - optional parameters:
    - `my` - returns only images owned by user that is currently logged in.
    - `popularity`
        - `main` - returns images that have more than 10% of whole like count.
        - `waiting` - returns images that have less than 10% of whole like count.
- `POST /images/`
  - adds an image to service.
    - `image` - image itself.
    - `title` - image's/post's displayed name.
- `GET /images/<n>`
  - returns only image itself.
- `PATCH /image/<n>`
  - performs action on individual image.
    - `like` adds a 'plus' to an image or removes it if it already exists. for authenticated users.
- `DELETE /image/<n>`
  - removes an image. available only for user itself and for superuser.
