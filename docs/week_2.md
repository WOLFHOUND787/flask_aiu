
# Неделя 2: Формы и передача данных, Работа с базами данных (SQLAlchemy)

## Урок 3: Формы и передача данных

### Цель:
Научиться работать с HTML-формами, обрабатывать POST-запросы и передавать данные между страницами.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── form_page.html    # Шаблон страницы с формой
│   ├── response.html     # Шаблон для отображения результата формы
├── static/               # Папка для стилей (необязательно)
```

### Шаг 1: Создание базового шаблона `base.html`

1. В папке `templates` создайте файл `base.html`. Этот файл будет содержать общую структуру для всех страниц:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Flask Project</title>
   </head>
   <body>
       <header>
           <h1>Добро пожаловать на сайт</h1>
       </header>
       <div class="content">
           {% block content %}{% endblock %}
       </div>
       <footer>
           <p>© 2024 Flask Project</p>
       </footer>
   </body>
   </html>
   ```

2. Все страницы будут "наследовать" этот шаблон, добавляя свой контент в блок `content`.

### Шаг 2: Создание страницы с формой

1. В папке `templates` создайте новый файл `form_page.html` для страницы с формой:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Оставьте ваше сообщение</h2>

   <form method="POST" action="/submit">
       <label for="name">Имя:</label><br>
       <input type="text" id="name" name="name"><br>

       <label for="message">Сообщение:</label><br>
       <textarea id="message" name="message" rows="4" cols="50"></textarea><br>

       <button type="submit">Отправить</button>
   </form>

   {% endblock %}
   ```

2. Добавьте маршрут в `app.py`, чтобы отобразить эту страницу. В файле `app.py` добавьте:

   ```python
   @app.route('/form')
   def form_page():
       return render_template('form_page.html')
   ```

### Шаг 3: Обработка данных формы

1. В папке `templates` создайте файл `response.html`, который будет отображать результат отправки формы:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Спасибо за ваше сообщение, {{ name }}!</h2>
   <p>Вы отправили следующее сообщение:</p>
   <p>{{ message }}</p>
   {% endblock %}
   ```

2. В файле `app.py` добавьте обработку данных формы:

   ```python
   @app.route('/submit', methods=['POST'])
   def submit():
       name = request.form['name']
       message = request.form['message']
       return render_template('response.html', name=name, message=message)
   ```

### Шаг 4: Тестирование приложения

1. Запустите приложение, выполнив команду в терминале:
   ```bash
   python app.py
   ```

2. Откройте браузер и перейдите по адресу `http://127.0.0.1:5000/form`, чтобы заполнить форму.

3. Отправьте форму и убедитесь, что данные правильно отображаются на странице подтверждения.

### Домашнее задание:
Создайте форму обратной связи, которая отправляет имя пользователя и сообщение на сервер, а затем отображает их на новой странице.

---

## Урок 4: Работа с базами данных (SQLAlchemy)

### Цель:
Изучить подключение к базе данных и использование ORM (SQLAlchemy) для работы с данными.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── form_page.html    # Шаблон страницы с формой
│   ├── response.html     # Шаблон для отображения результата формы
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Установка и настройка SQLAlchemy

1. Установите библиотеку `Flask-SQLAlchemy`:
   ```bash
   pip install Flask-SQLAlchemy
   ```

2. Настройте подключение к базе данных в файле `app.py`. Добавьте следующий код в начало файла:

   ```python
   from flask_sqlalchemy import SQLAlchemy

   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   db = SQLAlchemy(app)
   ```

### Шаг 2: Создание модели данных

1. Определите модель данных для пользователей в `app.py`:

   ```python
   class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)

       def __repr__(self):
           return f'<User {self.username}>'
   ```

2. Ваш app.py на данный момент `app.py`:

   ```python
   from flask import Flask, request, render_template
   from flask_sqlalchemy import SQLAlchemy
   
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   db = SQLAlchemy(app)
   
   class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   
       def __repr__(self):
           return f'<User {self.username}>'
   
   @app.route('/')
   def home():
   return render_template('base.html')
   
   @app.route('/user/<username>')
   def show_user_profile(username):
   return render_template('user_profile.html', username=username)
   
   @app.route('/form')
   def form_page():
   return render_template('form_page.html')
   
   @app.route('/submit', methods=['POST'])
   def submit():
   name = request.form['name']
   message = request.form['message']
   return render_template('response.html', name=name, message=message)
   
   if __name__ == '__main__':
   with app.app_context():
   db.create_all()
   app.run(debug=True)

   ```
3. Создайте базу данных, выполнив в терминале:

   ```bash
   python app.py
   ```

   Это создаст файл базы данных `users.db` в корне проекта.

### Шаг 3: Добавление и получение данных

1. Добавьте нового пользователя в базу данных в файле `app.py`:

   ```python
   with app.app_context():
       new_user = User(username="test_user", email="test@example.com")
       db.session.add(new_user)
       db.session.commit()
   ```

2. Получите данные всех пользователей и выведите их на экран:

   ```python
   users = User.query.all()
   for user in users:
       print(user.username, user.email)
   ```

### Шаг 4: CRUD операции

1. **Чтение:** Получение всех пользователей:
   ```python
   users = User.query.all()
   ```

2. **Обновление:** Обновление данных пользователя:
   ```python
   user = User.query.filter_by(username="test_user").first()
   user.email = "newemail@example.com"
   db.session.commit()
   ```

3. **Удаление:** Удаление пользователя:
   ```python
   user = User.query.filter_by(username="test_user").first()
   db.session.delete(user)
   db.session.commit()
   ```

### Домашнее задание:
1. Реализуйте CRUD операции для пользователей: создание, чтение, обновление, удаление.
2. Создайте интерфейс с HTML-формами для добавления и удаления пользователей.
