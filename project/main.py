from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        with app.app_context():
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация успешна!', 'success')
                return redirect(url_for('login'))
            except:
                flash('Ошибка регистрации. Пожалуйста, выберите другое имя пользователя.', 'danger')

        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    with app.app_context():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                flash('Вход выполнен успешно!', 'success')
                return redirect(url_for('index.html'))
            else:
                flash('Ошибка входа. Проверьте имя пользователя и пароль.', 'danger')

        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)