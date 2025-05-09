from flask import Flask, jsonify
from sistema import SistemaCadastroMedico, FilaPrioridade

app = Flask(__name__)
sistema = SistemaCadastroMedico()
fila = FilaPrioridade(sistema.conexao)

@app.route("/fila")
def get_fila():
    return jsonify(fila.obter_fila_ordenada())

if __name__ == "__main__":
    app.run(debug=True)
