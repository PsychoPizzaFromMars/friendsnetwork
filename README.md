# Профильное задание на стажировку VK Python-разработчик
## [OpenAPI спецификация](./openapi.yaml)
## Запуск
Запуск в виртуальном окружении
```shell
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000     // http://0.0.0.0:8000 or http://localhost:8000
```
или используя **Poetry**
```shell
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000      // http://0.0.0.0:8000 or http://localhost:8000
```
либо с помощью **Docker**:
```shell
docker build . -t friendsnetworkapi
docker run -p 8000:8000 friendsnetworkapi    // http://0.0.0.0:8000 or http://localhost:8000
```
## Примеры использования
### Регистрация пользователя
```json
POST /api/register
body: {
    username: "user",
    password: "12345"
}
```
### Логин
```json
POST /api/login
body: {
    username: "user",
    password: "12345"
}
```
### Просмотреть статуса отношений с пользователем под идентификатором id
```json
GET /api/profile/friendships/:id
```
### Просмотреть списка входящих и исходящих заявок в друзья
```json
GET /api/profile/friendships
```
### Просмотреть списка друзей
```json
GET /api/profile/friends
```
### Отправить или принять заявку в друзья с пользователем под идентификатором id
```json
POST /api/profile/friendships/:id
```
### Удалить из списка друзей, удалить исходящую заявку в друзья или отклонить входящую заявку в друзья с пользователем под идентификатором id
```json
DELETE /api/profile/friendships/:id
```