
# Неделя 5: Аутентификация пользователей и работа с Flask-Login

## Урок 1: Аутентификация пользователей с использованием Flask-Login

### Цель:
Научиться реализовывать аутентификацию пользователей в веб-приложении с помощью расширения Flask-Login.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── login.html        # Шаблон формы для входа пользователя
│   ├── dashboard.html    # Шаблон для панели пользователя после входа
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Установка Flask-Login

Для реализации аутентификации необходимо установить расширение Flask-Login.

1. Установите Flask-Login:
   ```bash
   pip install Flask-Login
   ```

2. Настройте Flask-Login в `app.py`:
   ```python
   from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

   login_manager = LoginManager()
   login_manager.init_app(app)
   login_manager.login_view = 'login'
   ```

### Шаг 2: Создание модели пользователя

1. Добавьте класс пользователя, который наследуется от `UserMixin`, в `app.py`:

   ```python
   class User(UserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password = db.Column(db.String(120), nullable=False)
   ```

2. Настройте загрузку пользователя для Flask-Login:

   ```python
   @login_manager.user_loader
   def load_user(user_id):
       return User.query.get(int(user_id))
   ```

### Шаг 3: Создание формы для входа

1. В папке `templates` создайте файл `login.html` для формы входа:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Вход в систему</h2>
   <form action="/login" method="POST">
       <label for="username">Имя пользователя:</label><br>
       <input type="text" id="username" name="username"><br><br>
       
       <label for="password">Пароль:</label><br>
       <input type="password" id="password" name="password"><br><br>
       
       <button type="submit">Войти</button>
   </form>
   {% endblock %}
   ```

### Шаг 4: Реализация маршрута для входа

1. В `app.py` создайте маршрут для обработки формы входа:

   ```python
   @app.route('/login', methods=['GET', 'POST'])
   def login():
       if request.method == 'POST':
           username = request.form['username']
           password = request.form['password']
           user = User.query.filter_by(username=username).first()
           if user and user.password == password:
               login_user(user)
               return redirect(url_for('dashboard'))
           return "Неправильное имя пользователя или пароль"
       return render_template('login.html')
   ```

### Шаг 5: Создание панели пользователя

1. В папке `templates` создайте файл `dashboard.html`:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Добро пожаловать, {{ current_user.username }}!</h2>
   <p>Это ваша панель управления после успешного входа в систему.</p>
   <a href="/logout">Выйти</a>
   {% endblock %}
   ```

2. В `app.py` создайте маршрут для панели управления и выхода:

   ```python
   @app.route('/dashboard')
   @login_required
   def dashboard():
       return render_template('dashboard.html')

   @app.route('/logout')
   def logout():
       logout_user()
       return redirect(url_for('login'))
   ```

### Шаг 6: Тестирование входа и выхода

1. Запустите приложение и перейдите на `/login`, чтобы войти в систему.
2. После успешного входа вы будете перенаправлены на `/dashboard`.

### Домашнее задание:
1. Добавьте возможность регистрации новых пользователей.
2. Реализуйте проверку пароля при входе с использованием хэширования (например, с использованием библиотеки `bcrypt`).

---

## Урок 2: Хэширование паролей и регистрация пользователей

### Цель:
Научиться реализовывать безопасное хранение паролей с использованием хэширования и добавить возможность регистрации новых пользователей.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── login.html        # Шаблон формы для входа пользователя
│   ├── register.html     # Шаблон формы для регистрации
│   ├── dashboard.html    # Шаблон для панели пользователя после входа
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Установка библиотеки для хэширования

Для безопасного хранения паролей установим библиотеку `bcrypt`.

1. Установите `bcrypt`:
   ```bash
   pip install bcrypt
   ```

2. Обновите модель пользователя, чтобы хранить хэшированные пароли:

   ```python
   import bcrypt

   class User(UserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(80), unique=True, nullable=False)
       email = db.Column(db.String(120), unique=True, nullable=False)
       password = db.Column(db.String(120), nullable=False)

       def set_password(self, password):
           self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

       def check_password(self, password):
           return bcrypt.checkpw(password.encode('utf-8'), self.password)
   ```

### Шаг 2: Реализация регистрации пользователей

1. В папке `templates` создайте файл `register.html`:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Регистрация</h2>
   <form action="/register" method="POST">
       <label for="username">Имя пользователя:</label><br>
       <input type="text" id="username" name="username"><br><br>
       
       <label for="email">Email:</label><br>
       <input type="email" id="email" name="email"><br><br>

       <label for="password">Пароль:</label><br>
       <input type="password" id="password" name="password"><br><br>
       
       <button type="submit">Зарегистрироваться</button>
   </form>
   {% endblock %}
   ```

2. В `app.py` создайте маршрут для регистрации:

   ```python
   @app.route('/register', methods=['GET', 'POST'])
   def register():
       if request.method == 'POST':
           username = request.form['username']
           email = request.form['email']
           password = request.form['password']
           hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
           new_user = User(username=username, email=email, password=hashed_password)
           db.session.add(new_user)
           db.session.commit()
           return redirect(url_for('login'))
       return render_template('register.html')
   ```

### Шаг 3: Обновление формы входа с проверкой пароля

1. Обновите маршрут для входа, чтобы использовать метод проверки пароля:

   ```python
   @app.route('/login', methods=['GET', 'POST'])
   def login():
       if request.method == 'POST':
           username = request.form['username']
           password = request.form['password']
           user = User.query.filter_by(username=username).first()
           if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
               login_user(user)
               return redirect(url_for('dashboard'))
           return "Неправильное имя пользователя или пароль"
       return render_template('login.html')
   ```

### Шаг 4: Тестирование регистрации и входа

1. Зарегистрируйте нового пользователя через `/register`.
2. Проверьте, что пароль хранится в зашифрованном виде, а вход происходит корректно.

### Домашнее задание:
1. Добавьте проверку уникальности для имени пользователя и email при регистрации.
2. Реализуйте функцию сброса пароля.
