import bcrypt
from flask import Flask, request, render_template, redirect, url_for
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

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template('added_user.html', username=username, email=email)
        except Exception as e:
            return f"An error: {str(e)}"
        return render_template('added_user.html', username=username, email=email)


@app.route('/add')
def add():
    return render_template('add_user.html')

@app.route('/list_users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

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

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('list_users'))
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This ensures that the database and tables are created
    app.run(debug=True)
