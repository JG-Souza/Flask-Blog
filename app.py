from flask import Flask
from flask_login import LoginManager
import sqlite3 as sq
from routes import main_blueprint, alunos
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

with sq.connect('alunos.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento DATE NOT NULL,
                idade INTEGER NOT NULL,
                endereco TEXT NOT NULL,
                numero TEXT NOT NULL,
                complemento TEXT,
                cep TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                tel_celular TEXT NOT NULL,
                tel_responsavel TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                profissao TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                inicio DATE NOT NULL,
                instagram TEXT,
                tabagista BOOLEAN DEFAULT 0,
                hipertenso BOOLEAN DEFAULT 0,
                diabetico BOOLEAN DEFAULT 0,
                medicacao BOOLEAN DEFAULT 0,
                medicacao_detalhes TEXT,
                cirurgia BOOLEAN DEFAULT 0,
                cirurgia_detalhes TEXT,
                atividade_fisica BOOLEAN DEFAULT 0,
                atividade_fisica_detalhes TEXT,
                dor BOOLEAN DEFAULT 0,
                dor_detalhes TEXT,
                info_studio TEXT,
                pilates BOOLEAN DEFAULT 0,
                patricia TEXT,
                objetivo TEXT,
                obs_fisio TEXT
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
app.register_blueprint(alunos, url_prefix='/alunos')

if __name__ == '__main__':
    app.run(debug=True)
