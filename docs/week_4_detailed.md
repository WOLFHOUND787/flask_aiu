
# Неделя 4: Продвинутая работа с базой данных и создание RESTful API

## Урок 1: Миграции базы данных и управление изменениями

### Цель:
Научиться работать с миграциями базы данных и вносить изменения в существующую структуру базы данных с помощью Flask-Migrate.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── migrations/           # Папка для хранения файлов миграций
├── templates/            # Папка с HTML-шаблонами
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Установка Flask-Migrate

Для управления миграциями используйте расширение Flask-Migrate.

1. Установите Flask-Migrate:
   ```bash
   pip install Flask-Migrate
   ```

2. Настройте Flask-Migrate в `app.py`:
   ```python
   from flask_migrate import Migrate
   migrate = Migrate(app, db)
   ```

### Шаг 2: Инициализация миграций

1. Инициализируйте миграции:
   ```bash
   flask db init
   ```

2. Создайте первую миграцию для базы данных:
   ```bash
   flask db migrate -m "Инициализация базы данных"
   ```

3. Примените миграцию:
   ```bash
   flask db upgrade
   ```

### Шаг 3: Внесение изменений в структуру базы данных

1. Добавьте новое поле `age` в модель `User` в `app.py`:

   ```python
   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       age = db.Column(db.Integer, nullable=True)  # Новое поле
   ```

2. Создайте новую миграцию:
   ```bash
   flask db migrate -m "Добавлено поле возраст"
   ```

3. Примените миграцию:
   ```bash
   flask db upgrade
   ```

### Шаг 4: Тестирование изменений

1. Запустите приложение и убедитесь, что новое поле добавлено в базу данных.
2. Обновите существующих пользователей или добавьте новых с указанием возраста.

### Домашнее задание:
1. Добавьте новые поля в модель пользователя (например, адрес или телефон).
2. Реализуйте возможность обновления этих данных через веб-формы.

---

## Урок 2: Создание RESTful API

### Цель:
Научиться создавать простые RESTful API с использованием Flask для взаимодействия с клиентскими приложениями.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами (необязательно для API)
├── static/               # Папка для стилей (необязательно для API)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Определение маршрутов для API

RESTful API основывается на стандартных методах HTTP (GET, POST, PUT, DELETE). Мы реализуем API для управления пользователями.

1. В `app.py` создайте маршрут для получения всех пользователей (GET):
   ```python
   @app.route('/api/users', methods=['GET'])
   def get_users():
       users = User.query.all()
       return {
           'users': [
               {'id': user.id, 'username': user.username, 'email': user.email}
               for user in users
           ]
       }
   ```

2. Маршрут для создания нового пользователя (POST):
   ```python
   @app.route('/api/users', methods=['POST'])
   def create_user():
       data = request.get_json()
       new_user = User(username=data['username'], email=data['email'])
       db.session.add(new_user)
       db.session.commit()
       return {'message': 'User created successfully'}, 201
   ```

3. Маршрут для обновления данных пользователя (PUT):
   ```python
   @app.route('/api/users/<int:id>', methods=['PUT'])
   def update_user(id):
       user = User.query.get_or_404(id)
       data = request.get_json()
       user.username = data['username']
       user.email = data['email']
       db.session.commit()
       return {'message': 'User updated successfully'}
   ```

4. Маршрут для удаления пользователя (DELETE):
   ```python
   @app.route('/api/users/<int:id>', methods=['DELETE'])
   def delete_user(id):
       user = User.query.get_or_404(id)
       db.session.delete(user)
       db.session.commit()
       return {'message': 'User deleted successfully'}
   ```

### Шаг 2: Тестирование API

1. Используйте инструменты, такие как Postman или cURL, для тестирования API.

   Пример запроса GET:
   ```bash
   curl -X GET http://127.0.0.1:5000/api/users
   ```

2. Пример запроса POST для создания нового пользователя:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" -d '{"username": "newuser", "email": "newuser@example.com"}'
   ```

### Домашнее задание:
1. Расширьте API, добавив маршруты для получения одного пользователя по ID.
2. Реализуйте валидацию данных для запросов POST и PUT.
