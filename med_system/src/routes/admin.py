from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from src.models.user import db, User, Medico, Paciente
from src.models.medical import Doenca, Remedio, Consulta

admin_bp = Blueprint('admin', __name__)

# Rota para inicialização de dados (apenas para desenvolvimento)
@admin_bp.route('/init_data')
def init_data():
    # Verifica se já existem dados
    if User.query.count() > 0:
        flash('Banco de dados já inicializado!', 'warning')
        return redirect(url_for('index'))
    
    # Cria doenças
    doencas = [
        Doenca(nome='Hipertensão', descricao='Pressão arterial elevada'),
        Doenca(nome='Diabetes Tipo 1', descricao='Diabetes insulino-dependente'),
        Doenca(nome='Diabetes Tipo 2', descricao='Diabetes não insulino-dependente'),
        Doenca(nome='Asma', descricao='Doença respiratória crônica'),
        Doenca(nome='Artrite', descricao='Inflamação das articulações'),
        Doenca(nome='Enxaqueca', descricao='Dor de cabeça intensa e recorrente'),
        Doenca(nome='Depressão', descricao='Transtorno de humor'),
        Doenca(nome='Ansiedade', descricao='Transtorno de ansiedade'),
        Doenca(nome='Hipotireoidismo', descricao='Baixa produção de hormônios da tireoide'),
        Doenca(nome='Hipertireoidismo', descricao='Produção excessiva de hormônios da tireoide')
    ]
    
    # Cria remédios
    remedios = [
        Remedio(nome='Losartana', descricao='Anti-hipertensivo'),
        Remedio(nome='Metformina', descricao='Antidiabético'),
        Remedio(nome='Insulina', descricao='Hormônio para controle de glicemia'),
        Remedio(nome='Salbutamol', descricao='Broncodilatador'),
        Remedio(nome='Ibuprofeno', descricao='Anti-inflamatório'),
        Remedio(nome='Paracetamol', descricao='Analgésico'),
        Remedio(nome='Fluoxetina', descricao='Antidepressivo'),
        Remedio(nome='Alprazolam', descricao='Ansiolítico'),
        Remedio(nome='Levotiroxina', descricao='Hormônio tireoidiano'),
        Remedio(nome='Omeprazol', descricao='Inibidor da bomba de prótons')
    ]
    
    # Adiciona ao banco de dados
    db.session.add_all(doencas)
    db.session.add_all(remedios)
    db.session.commit()
    
    flash('Dados iniciais criados com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota para gerenciamento de usuários (apenas para administradores)
@admin_bp.route('/usuarios')
def listar_usuarios():
    # Aqui poderia ter uma verificação de administrador
    usuarios = User.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)
