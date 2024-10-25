from flask import Flask
from flask_login import LoginManager
import sqlite3 as sq
from routes import main_blueprint
from models import User

app = Flask(__name__)
app.secret_key = 'nescal'

with sq.connect('usuarios.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                senha TEXT NOT NULL
                
    )
    ''')

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    with sq.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])

# Registrar Blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
