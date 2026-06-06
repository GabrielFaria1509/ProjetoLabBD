from conexao.db_connection import conectar
from models.cliente import Cliente
from daos.cliente_dao import ClienteDAO
from daos.pedido_dao import PedidoDAO

def mostrar_resultados(resultados):
    if not resultados:
        print("Nenhum registro encontrado.")
        return
    for linha in resultados:
        print(linha)
    print("-" * 30)

def main():
    conexao = conectar()
    if not conexao:
        return

    cliente_dao = ClienteDAO(conexao)
    pedido_dao = PedidoDAO(conexao)

    while True:
        print("\n=== SISTEMA APP SERVIÇO ===")
        print("1. [CLIENTE] Cadastrar")
        print("2. [CLIENTE] Listar Todos")
        print("3. [CLIENTE] Buscar por Email (Atributo)")
        print("4. [PEDIDO] Atualizar Status")
        print("5. [PEDIDO] Deletar Pedido")
        print("6. [JOIN 1] Clientes e seus Pedidos")
        print("7. [JOIN 2] Pedidos e Entregadores")
        print("8. [JOIN 3] Relatório Completo de Pedidos")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                nome = input("Nome: ")
                email = input("Email: ")
                telefone = input("Telefone: ")
                endereco = input("Endereço: ")
                novo_cliente = Cliente(None, nome, email, telefone, endereco)
                cliente_dao.inserir(novo_cliente)
                print("Cliente cadastrado com sucesso!")

            elif opcao == '2':
                mostrar_resultados(cliente_dao.listar_todos())

            elif opcao == '3':
                email = input("Digite o email para busca: ")
                mostrar_resultados(cliente_dao.buscar_por_email(email))

            elif opcao == '4':
                id_ped = input("ID do Pedido: ")
                # Status ENUM('Pendente', 'Em preparo', 'A caminho', 'Saiu para entrega', 'Entregue', 'Atrasado', 'Cancelado')
                novo_status = input("Novo Status: ") 
                pedido_dao.atualizar_status(id_ped, novo_status)
                print("Status atualizado!")

            elif opcao == '5':
                id_ped = input("ID do Pedido a deletar: ")
                pedido_dao.deletar(id_ped)
                print("Pedido deletado!")

            elif opcao == '6':
                mostrar_resultados(cliente_dao.listar_clientes_com_seus_pedidos())

            elif opcao == '7':
                mostrar_resultados(pedido_dao.listar_pedidos_com_entregador())

            elif opcao == '8':
                mostrar_resultados(pedido_dao.relatorio_pedido_completo())

            elif opcao == '0':
                print("Encerrando conexão...")
                break
            else:
                print("Opção inválida.")
        
        except Exception as e:
            print(f"Ocorreu um erro na operação: {e}")

    conexao.close()

if __name__ == "__main__":
    main()