from sistema import SistemaCadastroMedico

def main():
    sistema = SistemaCadastroMedico()
    
    ascii_art = r"""
                    _ _.-'`-._ _                 
                    ;.'________'.;                
        _________n.[____________].n_________     
        |""_""_""_""||==||==||==||""_""_""_""]    
        |"""""""""""||..||..||..||"""""""""""|    
        |LI LI LI LI||LI||LI||LI||LI LI LI LI|    
        |.. .. .. ..||..||..||..||.. .. .. ..|    
        |LI LI LI LI||LI||LI||LI||LI LI LI LI|    
    ,,;;,;;;,;;;,;;;,;;;,;;;,;;;,;;,;;;,;;;,;;,, 
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    """
    print(ascii_art)
    print("Bem-vindo ao sistema de cadastro médico!")

    try:
        while True:
            print("\nO QUE VOCÊ GOSTARIA DE FAZER:")
            print("1 - PESQUISA DE PRIORIDADE")
            print("2 - CADASTRO")
            print("3 - VER A FILA")
            print("0 - SAIR")

            opcao = input("Opção: ")

            match opcao:
                case "1":
                    print("Função de prioridade ainda será implementada.")
                case "2":
                    print("\nO QUE GOSTARIA DE CADASTRAR:")
                    print("1 - PACIENTE")
                    print("2 - MÉDICO")
                    print("3 - CONSULTA")
                    print("0 - VOLTAR")

                    opcao_cadastro = input("Opção: ")

                    match opcao_cadastro:
                        case "1":
                            sistema.inserir_paciente()
                        case "2":
                            sistema.inserir_medico()
                        case "3":
                            sistema.inserir_consulta()
                        case "0":
                            continue
                        case _:
                            print("Opção inválida.")
                case "3":
                    print("Função para ver a fila ainda será implementada.")
                case "0":
                    print("Encerrando o sistema...")
                    break
                case _:
                    print("Opção inválida.")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        sistema.encerrar_conexao()

if __name__ == "__main__":
    main()
