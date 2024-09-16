
# Неделя 3: Взаимодействие с пользователем и работа с формами и данными

## Урок 1: Создание и обработка форм для управления пользователями

### Цель:
Научиться создавать формы для управления пользователями (создание, просмотр) и сохранять данные в базе данных.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── add_user.html     # Шаблон формы для добавления пользователя
│   ├── list_users.html   # Шаблон для отображения списка пользователей
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Создание формы для добавления пользователя

1. В папке `templates` создайте файл `add_user.html`:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Добавить нового пользователя</h2>
   <form action="/add_user" method="POST">
       <label for="username">Имя пользователя:</label><br>
       <input type="text" id="username" name="username"><br><br>
       
       <label for="email">Email:</label><br>
       <input type="text" id="email" name="email"><br><br>
       
       <button type="submit">Добавить</button>
   </form>
   {% endblock %}
   ```

2. В `app.py` создайте маршрут для добавления пользователя:

   ```python
   @app.route('/add_user', methods=['GET', 'POST'])
   def add_user():
       if request.method == 'POST':
           username = request.form['username']
           email = request.form['email']
           new_user = User(username=username, email=email)
           try:
               db.session.add(new_user)
               db.session.commit()
               return redirect(url_for('list_users'))
           except Exception as e:
               return f"Произошла ошибка: {str(e)}"
       return render_template('add_user.html')
   ```

### Шаг 2: Отображение списка пользователей

1. В папке `templates` создайте файл `list_users.html` для отображения списка пользователей:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Список пользователей</h2>
   <ul>
       {% for user in users %}
           <li>{{ user.username }} ({{ user.email }})</li>
       {% endfor %}
   </ul>
   <a href="/add_user">Добавить нового пользователя</a>
   {% endblock %}
   ```

2. В `app.py` создайте маршрут для отображения пользователей:

   ```python
   @app.route('/list_users')
   def list_users():
       users = User.query.all()
       return render_template('list_users.html', users=users)
   ```

### Шаг 3: Тестирование приложения

1. Запустите приложение и перейдите по адресу `/add_user` для добавления новых пользователей.
2. После добавления пользователя, вы будете перенаправлены на `/list_users` для просмотра всех пользователей.

### Домашнее задание:
1. Создайте возможность редактирования пользователя.
2. Создайте интерфейс для удаления пользователя из списка.

---

## Урок 2: Редактирование и удаление пользователей

### Цель:
Добавить функциональность для редактирования и удаления пользователей через веб-интерфейс.

### Структура проекта

```bash
flask_project/
├── app.py                # Основной файл Flask приложения
├── templates/            # Папка с HTML-шаблонами
│   ├── base.html         # Базовый шаблон для всех страниц
│   ├── add_user.html     # Шаблон формы для добавления пользователя
│   ├── edit_user.html    # Шаблон для редактирования пользователя
│   ├── list_users.html   # Шаблон для отображения списка пользователей
├── static/               # Папка для стилей (необязательно)
├── users.db              # Файл базы данных SQLite
```

### Шаг 1: Создание формы для редактирования пользователя

1. В папке `templates` создайте файл `edit_user.html`:

   ```html
   {% extends "base.html" %}

   {% block content %}
   <h2>Редактировать пользователя</h2>
   <form action="/edit_user/{{ user.id }}" method="POST">
       <label for="username">Имя пользователя:</label><br>
       <input type="text" id="username" name="username" value="{{ user.username }}"><br><br>
       
       <label for="email">Email:</label><br>
       <input type="text" id="email" name="email" value="{{ user.email }}"><br><br>
       
       <button type="submit">Сохранить</button>
   </form>
   {% endblock %}
   ```

2. В `app.py` создайте маршрут для редактирования пользователя:

   ```python
   @app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
   def edit_user(id):
       user = User.query.get_or_404(id)
       if request.method == 'POST':
           user.username = request.form['username']
           user.email = request.form['email']
           try:
               db.session.commit()
               return redirect(url_for('list_users'))
           except Exception as e:
               return f"Произошла ошибка: {str(e)}"
       return render_template('edit_user.html', user=user)
   ```

### Шаг 2: Добавление возможности удаления пользователя

1. Добавьте кнопку удаления в `list_users.html`:

   ```html
   <ul>
       {% for user in users %}
           <li>
               {{ user.username }} ({{ user.email }})
               <a href="/edit_user/{{ user.id }}">Редактировать</a>
               <a href="/delete_user/{{ user.id }}" onclick="return confirm('Вы уверены, что хотите удалить этого пользователя?');">Удалить</a>
           </li>
       {% endfor %}
   </ul>
   ```

2. В `app.py` создайте маршрут для удаления пользователя:

   ```python
   @app.route('/delete_user/<int:id>')
   def delete_user(id):
       user = User.query.get_or_404(id)
       try:
           db.session.delete(user)
           db.session.commit()
           return redirect(url_for('list_users'))
       except Exception as e:
           return f"Произошла ошибка: {str(e)}"
   ```

### Шаг 3: Тестирование приложения

1. Запустите приложение и перейдите на `/list_users`.
2. Попробуйте редактировать и удалять пользователей.

### Домашнее задание:
1. Добавьте подтверждение перед удалением пользователя.
2. Реализуйте возможность поиска пользователей по имени.

