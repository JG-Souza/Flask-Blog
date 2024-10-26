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

    # Exibe a página com a tabela de usuários
    return render_template('admin-page.html', users=users)


@main_blueprint.route('/menu/criar_user', methods=['POST'])
@login_required
def criar_user():
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
        return redirect(url_for('main.menu'))


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


@main_blueprint.route('/menu/delete_user<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = carrega_user_por_id(user_id)
    if user:
        with sq.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        return redirect(url_for('main.menu', user=user))
    else:
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
    



# Rotas para a criação de Alunos
alunos = Blueprint('alunos', __name__)

@alunos.route('/home')
def home():
    alunos = carrega_alunos()
    
    return render_template('lista_alunos.html', alunos=alunos)

@alunos.route('/criar_aluno', methods=['POST'])
def criar_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        idade = request.form['idade']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form.get('complemento', '')
        cep = request.form['cep']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        tel_celular = request.form['tel_celular']
        tel_responsavel = request.form['tel_responsavel']
        email = request.form['email']
        profissao = request.form['profissao']
        cpf = request.form['cpf']
        inicio = request.form['inicio']
        instagram = request.form.get('instagram', '')

        tabagista = 'tabagista' in request.form
        hipertenso = 'hipertenso' in request.form
        diabetico = 'diabetico' in request.form
        medicacao = 'medicacao' in request.form
        medicacao_detalhes = request.form.get('medicacao_detalhes', '')
        cirurgia = 'cirurgia' in request.form
        cirurgia_detalhes = request.form.get('cirurgia_detalhes', '')
        atividade_fisica = 'atividade_fisica' in request.form
        atividade_fisica_detalhes = request.form.get('atividade_fisica_detalhes', '')
        dor = 'dor' in request.form
        dor_detalhes = request.form.get('dor_detalhes', '')
        info_studio = request.form.get('info_studio', '')
        pilates = 'pilates' in request.form
        patricia = request.form.get('patricia', '')
        objetivo = request.form.get('objetivo', '')
        obs_fisio = request.form.get('obs_fisio', '')

        values = (nome, data_nascimento, idade, endereco, numero, complemento, cep,
                  bairro, cidade, tel_celular, tel_responsavel, email, profissao, cpf,
                  inicio, instagram, tabagista, hipertenso, diabetico, medicacao,
                  medicacao_detalhes, cirurgia, cirurgia_detalhes, atividade_fisica,
                  atividade_fisica_detalhes, dor, dor_detalhes, info_studio, pilates,
                  patricia, objetivo, obs_fisio)

        print(f"Valores a serem inseridos: {values}")  # Log para depuração

        with sq.connect('alunos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alunos (nome, data_nascimento, idade, endereco, numero, complemento, cep,
                                    bairro, cidade, tel_celular, tel_responsavel, email, profissao, cpf,
                                    inicio, instagram, tabagista, hipertenso, diabetico, medicacao,
                                    medicacao_detalhes, cirurgia, cirurgia_detalhes, atividade_fisica,
                                    atividade_fisica_detalhes, dor, dor_detalhes, info_studio, pilates,
                                    patricia, objetivo, obs_fisio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)

            conn.commit()

        return redirect(url_for('alunos.home'))
    

def carrega_alunos():
    alunos = []
    with sq.connect('alunos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alunos')
        aluno_data = cursor.fetchall()
        for aluno in aluno_data:
            aluno_info = {
                'id': aluno[0],
                'nome': aluno[1],
                'data_nascimento': aluno[2],
                'idade': aluno[3],
                'endereco': aluno[4],
                'numero': aluno[5],
                'complemento': aluno[6],
                'cep': aluno[7],
                'bairro': aluno[8],
                'cidade': aluno[9],
                'tel_celular': aluno[10],
                'tel_responsavel': aluno[11],
                'email': aluno[12],
                'profissao': aluno[13],
                'cpf': aluno[14],
                'inicio': aluno[15],
                'instagram': aluno[16],
                'tabagista': aluno[17],
                'hipertenso': aluno[18],
                'diabetico': aluno[19],
                'medicacao': aluno[20],
                'medicacao_detalhes': aluno[21],
                'cirurgia': aluno[22],
                'cirurgia_detalhes': aluno[23],
                'atividade_fisica': aluno[24],
                'atividade_fisica_detalhes': aluno[25],
                'dor': aluno[26],
                'dor_detalhes': aluno[27],
                'info_studio': aluno[28],
                'pilates': aluno[29],
                'patricia': aluno[30],
                'objetivo': aluno[31],
                'obs_fisio': aluno[32]
            }
            alunos.append(aluno_info)

    return alunos


