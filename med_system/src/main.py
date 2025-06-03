from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Adiciona o diretório pai ao path para importaçõesfrom flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# Adiciona o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Importa os modelos após inicializar o db
from src.models.user import User, Medico, Paciente
from src.models.medical import Doenca, DoencaPaciente, Remedio, RemedioPaciente, Consulta

# Importa as rotas
from src.routes.auth import auth_bp
from src.routes.medico import medico_bp
from src.routes.paciente import paciente_bp
from src.routes.admin import admin_bp

# Registra os blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(medico_bp, url_prefix='/medico')
app.register_blueprint(paciente_bp, url_prefix='/paciente')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para obter a fila de prioridade (API)
@app.route('/api/fila')
def get_fila():
    consultas = Consulta.obter_fila_ordenada()
    fila = []
    
    for consulta in consultas:
        fila.append({
            'id': consulta.id,
            'nome_paciente': consulta.paciente.nome,
            'nome_medico': consulta.medico.nome,
            'hora': consulta.hora.strftime('%H:%M'),
            'prioridade': consulta.prioridade,
            'doencas': [dp.doenca.nome for dp in consulta.paciente.doencas]
        })
    
    return jsonify(fila)

# Inicializa o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
