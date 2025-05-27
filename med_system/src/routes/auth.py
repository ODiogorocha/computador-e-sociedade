from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import db, User, Medico, Paciente
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            session['username'] = user.username
            
            flash('Login realizado com sucesso!', 'success')
            
            if user.user_type == 'medico':
                return redirect(url_for('medico.dashboard'))
            else:
                return redirect(url_for('paciente.dashboard'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Verificações básicas
        if not all([user_type, username, email, password, confirm_password]):
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('auth/registro.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/registro.html')
        
        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já está em uso.', 'danger')
            return render_template('auth/registro.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso.', 'danger')
            return render_template('auth/registro.html')
        
        # Cria o usuário de acordo com o tipo
        if user_type == 'medico':
            nome = request.form.get('nome')
            especialidade = request.form.get('especialidade')
            crm = request.form.get('crm')
            
            if not all([nome, especialidade, crm]):
                flash('Todos os campos são obrigatórios para médicos.', 'danger')
                return render_template('auth/registro.html')
            
            # Verifica se o CRM já existe
            existing_crm = Medico.query.filter_by(crm=crm).first()
            if existing_crm:
                flash('CRM já está registrado.', 'danger')
                return render_template('auth/registro.html')
            
            new_user = Medico(
                username=username,
                email=email,
                nome=nome,
                especialidade=especialidade,
                crm=crm
            )
            new_user.set_password(password)
            
        else:  # paciente
            nome = request.form.get('nome')
            data_nascimento = request.form.get('data_nascimento')
            
            if not all([nome, data_nascimento]):
                flash('Todos os campos são obrigatórios para pacientes.', 'danger')
                return render_template('auth/registro.html')
            
            # Converte a string de data para objeto Date
            try:
                data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido.', 'danger')
                return render_template('auth/registro.html')
            
            # Determina a faixa etária
            hoje = datetime.now().date()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            if idade < 12:
                fx_etaria = 'criança'
            elif idade < 18:
                fx_etaria = 'jovem'
            elif idade < 60:
                fx_etaria = 'adulto'
            else:
                fx_etaria = 'idoso'
            
            new_user = Paciente(
                username=username,
                email=email,
                nome=nome,
                data_nascimento=data_nascimento,
                fx_etaria=fx_etaria
            )
            new_user.set_password(password)
        
        # Salva o usuário no banco de dados
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')
