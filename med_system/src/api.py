from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.sistema_cadastro import MedicalRegistrationSystem
from backend.fila_prioridade import PriorityQueue

app = Flask(__name__, static_folder="static")
CORS(app)

# Instâncias do sistema e fila
system = MedicalRegistrationSystem()
queue = PriorityQueue()

# Rota para servir o front-end
@app.route("/")
def frontend():
    return send_from_directory("static", "index.html")

# Rota para adicionar paciente
@app.route("/api/pacientes", methods=["POST"])
def criar_paciente():
    data = request.get_json()
    nome = data.get("nome")
    idade = data.get("idade")
    prioridade = data.get("prioridade")

    if nome and idade is not None and prioridade is not None:
        system.add_patient(nome, int(idade), int(prioridade))
        return jsonify({"status": "ok"})
    return jsonify({"status": "erro", "mensagem": "Campos incompletos"}), 400

# Rota para obter a fila atual
@app.route("/api/fila", methods=["GET"])
def obter_fila():
    fila = queue.get_sorted_queue()
    pacientes = [
        {"id": p[0], "nome": p[1], "idade": p[2], "prioridade": p[3]}
        for p in fila
    ]
    return jsonify(pacientes)

# Rodar a API
if __name__ == "__main__":
    app.run(debug=True)
