from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from functools import wraps
from src.models.user import db, Medico
from src.models.medical import Consulta, Paciente, DoencaPaciente, RemedioPaciente, Doenca, Remedio

medico_bp = Blueprint('medico', __name__)

# Decorator para verificar se o usuário é médico
def medico_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'medico':
            flash('Acesso restrito a médicos.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@medico_bp.route('/dashboard')
@medico_required
def dashboard():
    medico_id = session.get('user_id')
    medico = Medico.query.get(medico_id)
    
    # Consultas do dia para o médico
    consultas_hoje = Consulta.query.filter_by(
        medico_id=medico_id, 
        status='agendada'
    ).order_by(
        Consulta.prioridade, 
        Consulta.hora
    ).all()
    
    return render_template(
        'medico/dashboard.html',
        medico=medico,
        consultas=consultas_hoje
    )

@medico_bp.route('/pacientes')
@medico_required
def listar_pacientes():
    # Lista todos os pacientes que já tiveram consulta com este médico
    medico_id = session.get('user_id')
    
    pacientes = Paciente.query.join(Consulta).filter(
        Consulta.medico_id == medico_id
    ).distinct().all()
    
    return render_template(
        'medico/pacientes.html',
        pacientes=pacientes
    )

@medico_bp.route('/paciente/<int:paciente_id>')
@medico_required
def ver_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Verifica se o médico já atendeu este paciente
    medico_id = session.get('user_id')
    consulta = Consulta.query.filter_by(
        medico_id=medico_id,
        paciente_id=paciente_id
    ).first()
    
    if not consulta:
        flash('Você não tem permissão para acessar este paciente.', 'danger')
        return redirect(url_for('medico.listar_pacientes'))
    
    # Obtém doenças e remédios do paciente
    doencas = DoencaPaciente.query.filter_by(paciente_id=paciente_id).all()
    remedios = RemedioPaciente.query.filter_by(paciente_id=paciente_id).all()
    
    return render_template(
        'medico/paciente_detalhes.html',
        paciente=paciente,
        doencas=doencas,
        remedios=remedios
    )

@medico_bp.route('/consultas')
@medico_required
def listar_consultas():
    medico_id = session.get('user_id')
    
    # Consultas agendadas
    consultas_agendadas = Consulta.query.filter_by(
        medico_id=medico_id,
        status='agendada'
    ).order_by(
        Consulta.data,
        Consulta.hora
    ).all()
    
    # Consultas realizadas
    consultas_realizadas = Consulta.query.filter_by(
        medico_id=medico_id,
        status='realizada'
    ).order_by(
        Consulta.data.desc(),
        Consulta.hora.desc()
    ).limit(10).all()
    
    return render_template(
        'medico/consultas.html',
        consultas_agendadas=consultas_agendadas,
        consultas_realizadas=consultas_realizadas
    )

@medico_bp.route('/consulta/<int:consulta_id>', methods=['GET', 'POST'])
@medico_required
def gerenciar_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    medico_id = session.get('user_id')
    
    # Verifica se a consulta pertence ao médico logado
    if consulta.medico_id != medico_id:
        flash('Você não tem permissão para acessar esta consulta.', 'danger')
        return redirect(url_for('medico.listar_consultas'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'realizar':
            consulta.status = 'realizada'
            observacoes = request.form.get('observacoes')
            if observacoes:
                consulta.observacoes = observacoes
            
            db.session.commit()
            flash('Consulta marcada como realizada com sucesso!', 'success')
            return redirect(url_for('medico.listar_consultas'))
        
        elif action == 'cancelar':
            consulta.status = 'cancelada'
            db.session.commit()
            flash('Consulta cancelada com sucesso!', 'success')
            return redirect(url_for('medico.listar_consultas'))
    
    return render_template(
        'medico/gerenciar_consulta.html',
        consulta=consulta
    )

@medico_bp.route('/adicionar_doenca/<int:paciente_id>', methods=['GET', 'POST'])
@medico_required
def adicionar_doenca(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Verifica se o médico já atendeu este paciente
    medico_id = session.get('user_id')
    consulta = Consulta.query.filter_by(
        medico_id=medico_id,
        paciente_id=paciente_id
    ).first()
    
    if not consulta:
        flash('Você não tem permissão para acessar este paciente.', 'danger')
        return redirect(url_for('medico.listar_pacientes'))
    
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
            flash('Esta doença já está registrada para este paciente.', 'warning')
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
        
        return redirect(url_for('medico.ver_paciente', paciente_id=paciente_id))
    
    # Lista de doenças disponíveis
    doencas = Doenca.query.all()
    
    return render_template(
        'medico/adicionar_doenca.html',
        paciente=paciente,
        doencas=doencas
    )

@medico_bp.route('/adicionar_remedio/<int:paciente_id>', methods=['GET', 'POST'])
@medico_required
def adicionar_remedio(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    
    # Verifica se o médico já atendeu este paciente
    medico_id = session.get('user_id')
    consulta = Consulta.query.filter_by(
        medico_id=medico_id,
        paciente_id=paciente_id
    ).first()
    
    if not consulta:
        flash('Você não tem permissão para acessar este paciente.', 'danger')
        return redirect(url_for('medico.listar_pacientes'))
    
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
        return redirect(url_for('medico.ver_paciente', paciente_id=paciente_id))
    
    # Lista de remédios disponíveis
    remedios = Remedio.query.all()
    
    return render_template(
        'medico/adicionar_remedio.html',
        paciente=paciente,
        remedios=remedios
    )
