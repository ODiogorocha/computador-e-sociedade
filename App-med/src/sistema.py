import mysql.connector

class SistemaCadastroMedico:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="usuario",
            password="senha",
            database="cadastro_med"
        )
        self.cursor = self.conexao.cursor()

    def inserir_paciente(self):
        print("\n----- INSERIR PACIENTE -----")
        prioridade = int(input("Prioridade do paciente (número): "))
        fx_etaria = input("Faixa etária: ")
        doenca = input("Descrição da doença: ")
        try:
            self.cursor.execute(
                "INSERT INTO paciente (prioridade, fx_etaria, doenca) VALUES (%s, %s, %s)",
                (prioridade, fx_etaria, doenca)
            )
            self.conexao.commit()
            print("Paciente inserido com sucesso.\n")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def inserir_medico(self):
        print("\n----- INSERIR MÉDICO -----")
        nome = input("Nome do médico: ")
        especialidade = input("Especialidade do médico: ")
        try:
            self.cursor.execute(
                "INSERT INTO medico (nome, especialidade) VALUES (%s, %s)",
                (nome, especialidade)
            )
            self.conexao.commit()
            print("Médico inserido com sucesso.\n")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def inserir_consulta(self):
        print("\n----- INSERIR CONSULTA -----")
        id_paciente = int(input("ID do paciente: "))
        id_medico = int(input("ID do médico: "))
        data = input("Data da consulta (AAAA-MM-DD): ")
        hora = input("Hora da consulta (HH:MM:SS): ")
        try:
            self.cursor.execute(
                "INSERT INTO consulta (data, hora, paciente_idpaciente, medico_idmedico) VALUES (%s, %s, %s, %s)",
                (data, hora, id_paciente, id_medico)
            )
            self.conexao.commit()
            print("Consulta inserida com sucesso.\n")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def encerrar_conexao(self):
        self.cursor.close()
        self.conexao.close()
        print("Conexão com o banco de dados encerrada.")


class FilaPrioridade:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()
    
    def calcular_peso_faixa_etaria(self, faixa):
        faixa = faixa.strip().lower()
        
        match faixa:
            case "criança":
                return 0
            case "idoso":
                return 1
            case "adulto":
                return 2
            case "jovem":
                return 3
            case _:
                return 4
            
    def gerar_fila(self):
        query = """
            SELECT 
                p.fx_etaria,
                p.prioridade,
                p.doenca,
                c.idconsulta,
                m.nome AS nome_medico,
                p.idpaciente,
                p.nome AS nome_paciente
            FROM consulta c
            JOIN paciente p ON c.paciente_idpaciente = p.idpaciente
            JOIN medico m ON c.medico_idmedico = m.idmedico;
        """
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()

        fila = []
        for linha in resultados:
            faixa, prioridade, doenca, _, nome_medico, _, nome_paciente = linha
            peso_faixa = self.calcular_peso_faixa_etaria(faixa)
            prioridade_total = prioridade * 10 + peso_faixa  # combinação da prioridade
            fila.append((prioridade_total, nome_paciente, doenca, nome_medico, prioridade))
        
        # Ordenar pela menor prioridade_total
            fila.sort(key=lambda x: x[0])

            # Imprimir fila
            print("\nFILA DE ATENDIMENTO PRIORITÁRIA")
            print("Nome Paciente\tDoença\t\t\tNome Médico\t\tPrioridade")
            print("-" * 60)
            for _, nome_paciente, doenca, nome_medico, prioridade in fila:
                print(f"{nome_paciente:<15}\t{doenca:<20}\t{nome_medico:<20}\t{prioridade}")

    def encerrar(self):
        self.cursor.close()