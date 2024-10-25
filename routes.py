from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3 as sq
from models import User

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('main.menu'))
    return render_template('form_login.html')

@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_blueprint.route('/menu', methods=['POST', 'GET'])
@login_required
def menu():
    users = carrega_users()  # Carrega os usuários para a tabela

    # Lógica de inserir usuário na tabela do banco de dados
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with sq.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, senha)
                VALUES (?, ?)
            ''', (email, senha))
            conn.commit()  # Assegura que os dados são salvos no banco de dados

        # Redireciona para a rota menu após o POST (PRG)
        return redirect(url_for('main.menu', success=True))

    # Exibe a página com a tabela de usuários e verifica se há sucesso na criação do usuário
    success = request.args.get('success')  # Pega o parâmetro de sucesso da URL
    return render_template('admin-page.html', users=users, success=success)

@main_blueprint.route('/menu/view_user<int:user_id>')
@login_required
def view_user(user_id):
    user = carrega_user_por_id(user_id)

    if user:
        return render_template('view-user.html', user=user)
    else:
        return redirect(url_for('main.menu'))
    
@main_blueprint.route('/menu/edit_user<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    email = request.form['email']
    senha = request.form['senha']

    with sq.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuarios
            SET email = ?, senha = ?
            WHERE id = ?
        ''', (email, senha, user_id))
        conn.commit()  # Assegura que os dados são salvos no banco de dados

    return redirect(url_for('main.menu'))


        
def carrega_users():
    users = []
    with sq.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        user_data = cursor.fetchall()
        for user in user_data:
            users.append(User(user[0], user[1], user[2]))

        return users
    
def carrega_user_por_id(user_id):
    with sq.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])  # Crie a instância do usuário
        return None