from sistema import SistemaCadastroMedico, FilaPrioridade as sys

class LoginUser:
    def __init__(self):
        pass

    def valid_login(self, user_id, senha, class_name):

        try:
            if user_id and senha:
                confirmation = class_name
                sys.imprimir_fila()
        except e:
            print(f"Falha de login !! erro ocorrido {e} !! ")



"""colocar a med do paciente por causa da interacao medicamentosa, melhorar o front """