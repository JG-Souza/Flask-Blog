from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3 as sq



app = Flask(__name__)
app.secret_key = 'nescal'

with sq.connect('usuarios.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL
                
    )
    ''')

# Configuração Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Classe do Uuário
class User(UserMixin):
    def __init__(self, id, email, senha):
        self.id = id
        self.email = email
        self.senha = senha

# Carregar o usuário 
@login_manager.user_loader
def load_user(user_id):
    with sq.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with sq.connect('usuarios.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id, email, senha FROM usuarios WHERE email = ?', (email,))
            user_data = cursor.fetchone()
            if user_data and user_data[2] == senha:
                user = User(user_data[0], user_data[1], user_data[2])
                login_user(user)
                print('oi')
                return redirect(url_for('home'))
            else:
                flash('Email ou senha incorretos')
    return render_template('form_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logou successfully')
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/menu')
@login_required
def menu():
    return render_template('admin-page.html')



@app.route('/menu/criar_user')
@login_required
def criar_user():
    return render_template('form_criar_user.html')





if __name__ == '__main__':
    app.run(debug=True)