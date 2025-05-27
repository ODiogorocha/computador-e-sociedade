from datetime import datetime
from sqlalchemy import func
from .user import db, Paciente, Medico

class Doenca(db.Model):
    __tablename__ = 'doencas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Relacionamento com pacientes
    pacientes = db.relationship('DoencaPaciente', backref='doenca', lazy=True)
    
    def __repr__(self):
        return f'<Doenca {self.nome}>'


class DoencaPaciente(db.Model):
    __tablename__ = 'doenca_paciente'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doenca_id = db.Column(db.Integer, db.ForeignKey('doencas.id'), nullable=False)
    data_diagnostico = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    nivel_gravidade = db.Column(db.Integer, nullable=False, default=1)  # 1-5, onde 5 é mais grave
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<DoencaPaciente {self.paciente_id}:{self.doenca_id}>'


class Remedio(db.Model):
    __tablename__ = 'remedios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Relacionamento com pacientes
    pacientes = db.relationship('RemedioPaciente', backref='remedio', lazy=True)
    
    def __repr__(self):
        return f'<Remedio {self.nome}>'


class RemedioPaciente(db.Model):
    __tablename__ = 'remedio_paciente'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    remedio_id = db.Column(db.Integer, db.ForeignKey('remedios.id'), nullable=False)
    dosagem = db.Column(db.String(50), nullable=False)
    frequencia = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    data_fim = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return f'<RemedioPaciente {self.paciente_id}:{self.remedio_id}>'


class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='agendada')  # agendada, realizada, cancelada
    prioridade = db.Column(db.Integer, nullable=False, default=3)  # 1-5, onde 1 é mais prioritário
    observacoes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consulta {self.id}>'
    
    @staticmethod
    def obter_fila_ordenada():
        """
        Retorna a fila de consultas ordenada por prioridade e outros fatores
        """
        return Consulta.query.join(Paciente).filter(
            Consulta.status == 'agendada',
            Consulta.data == func.current_date()
        ).order_by(
            Consulta.prioridade,
            Paciente.fx_etaria,
            Consulta.hora
        ).all()
