from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from functools import wraps
from src.models.user import db, Paciente
from src.models.medical import Consulta, DoencaPaciente, RemedioPaciente, Doenca, Remedio
from datetime import datetime

paciente_bp = Blueprint('paciente', __name__)

# Decorator para verificar se o usuário é paciente
def paciente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'paciente':
            flash('Acesso restrito a pacientes.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@paciente_bp.route('/dashboard')
@paciente_required
def dashboard():
    paciente_id = session.get('user_id')
    paciente = Paciente.query.get(paciente_id)
    
    # Consultas agendadas do paciente
    consultas = Consulta.query.filter_by(
        paciente_id=paciente_id,
        status='agendada'
    ).order_by(
        Consulta.data,
        Consulta.hora
    ).all()
    
    # Posição na fila (se tiver consulta hoje)
    posicao_fila = None
    consulta_hoje = None
    
    hoje = datetime.now().date()
    for consulta in consultas:
        if consulta.data == hoje:
            consulta_hoje = consulta
            # Busca a posição na fila
            fila_ordenada = Consulta.obter_fila_ordenada()
            for i, c in enumerate(fila_ordenada):
                if c.id == consulta.id:
                    posicao_fila = i + 1
                    break
            break
    
    # Doenças e remédios do paciente
    doencas = DoencaPaciente.query.filter_by(paciente_id=paciente_id).all()
    remedios = RemedioPaciente.query.filter_by(paciente_id=paciente_id).all()
    
    return render_template(
        'paciente/dashboard.html',
        paciente=paciente,
        consultas=consultas,
        doencas=doencas,
        remedios=remedios,
        posicao_fila=posicao_fila,
        consulta_hoje=consulta_hoje
    )

@paciente_bp.route('/perfil', methods=['GET', 'POST'])
@paciente_required
def perfil():
    paciente_id = session.get('user_id')
    paciente = Paciente.query.get(paciente_id)
    
    if request.method == 'POST':
        # Atualiza apenas os campos permitidos
        paciente.nome = request.form.get('nome')
        paciente.email = request.form.get('email')
        
        # Verifica se a senha foi fornecida para alteração
        nova_senha = request.form.get('nova_senha')
        if nova_senha:
            confirmar_senha = request.form.get('confirmar_senha')
            if nova_senha == confirmar_senha:
                paciente.set_password(nova_senha)
                flash('Senha atualizada com sucesso!', 'success')
            else:
                flash('As senhas não coincidem.', 'danger')
                return render_template('paciente/perfil.html', paciente=paciente)
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('paciente.dashboard'))
    
    return render_template('paciente/perfil.html', paciente=paciente)

@paciente_bp.route('/minhas_doencas')
@paciente_required
def minhas_doencas():
    paciente_id = session.get('user_id')
    
    doencas = DoencaPaciente.query.filter_by(paciente_id=paciente_id).all()
    
    return render_template(
        'paciente/minhas_doencas.html',
        doencas=doencas
    )

@paciente_bp.route('/adicionar_doenca', methods=['GET', 'POST'])
@paciente_required
def adicionar_doenca():
    paciente_id = session.get('user_id')
    
    if request.method == 'POST':
        doenca_id = request.form.get('doenca_id')
        nivel_gravidade = request.form.get('nivel_gravidade')
        observacoes = request.form.get('observacoes')
        
        # Verifica se a doença já está registrada para este paciente
        doenca_existente = DoencaPaciente.query.filter_by(
            paciente_id=paciente_id,
            doenca_id=doenca_id
        ).first()
        
        if doenca_existente:
            flash('Esta doença já está registrada no seu perfil.', 'warning')
        else:
            nova_doenca = DoencaPaciente(
                paciente_id=paciente_id,
                doenca_id=doenca_id,
                nivel_gravidade=nivel_gravidade,
                observacoes=observacoes
            )
            db.session.add(nova_doenca)
            db.session.commit()
            flash('Doença adicionada com sucesso!', 'success')
        
        return redirect(url_for('paciente.minhas_doencas'))
    
    # Lista de doenças disponíveis
    doencas = Doenca.query.all()
    
    return render_template(
        'paciente/adicionar_doenca.html',
        doencas=doencas
    )

@paciente_bp.route('/meus_remedios')
@paciente_required
def meus_remedios():
    paciente_id = session.get('user_id')
    
    remedios = RemedioPaciente.query.filter_by(paciente_id=paciente_id).all()
    
    return render_template(
        'paciente/meus_remedios.html',
        remedios=remedios
    )

@paciente_bp.route('/adicionar_remedio', methods=['GET', 'POST'])
@paciente_required
def adicionar_remedio():
    paciente_id = session.get('user_id')
    
    if request.method == 'POST':
        remedio_id = request.form.get('remedio_id')
        dosagem = request.form.get('dosagem')
        frequencia = request.form.get('frequencia')
        data_fim = request.form.get('data_fim')
        
        novo_remedio = RemedioPaciente(
            paciente_id=paciente_id,
            remedio_id=remedio_id,
            dosagem=dosagem,
            frequencia=frequencia
        )
        
        if data_fim:
            novo_remedio.data_fim = data_fim
        
        db.session.add(novo_remedio)
        db.session.commit()
        flash('Remédio adicionado com sucesso!', 'success')
        return redirect(url_for('paciente.meus_remedios'))
    
    # Lista de remédios disponíveis
    remedios = Remedio.query.all()
    
    return render_template(
        'paciente/adicionar_remedio.html',
        remedios=remedios
    )

@paciente_bp.route('/fila')
@paciente_required
def ver_fila():
    paciente_id = session.get('user_id')
    
    # Verifica se o paciente tem consulta hoje
    hoje = datetime.now().date()
    consulta_hoje = Consulta.query.filter_by(
        paciente_id=paciente_id,
        data=hoje,
        status='agendada'
    ).first()
    
    # Obtém a fila completa
    fila_ordenada = Consulta.obter_fila_ordenada()
    
    # Encontra a posição do paciente na fila
    posicao = None
    if consulta_hoje:
        for i, consulta in enumerate(fila_ordenada):
            if consulta.id == consulta_hoje.id:
                posicao = i + 1
                break
    
    return render_template(
        'paciente/fila.html',
        fila=fila_ordenada,
        posicao=posicao,
        consulta_hoje=consulta_hoje
    )
