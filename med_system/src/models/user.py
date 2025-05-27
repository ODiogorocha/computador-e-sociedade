from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'medico' ou 'paciente'
    
    # Relacionamento polimórfico
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Medico(User):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamento com consultas
    consultas = db.relationship('Consulta', backref='medico', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'medico',
    }
    
    def __repr__(self):
        return f'<Medico {self.nome}>'


class Paciente(User):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    fx_etaria = db.Column(db.String(50), nullable=False)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)
    doencas = db.relationship('DoencaPaciente', backref='paciente', lazy=True)
    remedios = db.relationship('RemedioPaciente', backref='paciente', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'paciente',
    }
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'
