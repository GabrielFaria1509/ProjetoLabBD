from conexao.db_connection import conectar
from models.Cliente import Cliente
from models.Entregador import Entregador
from models.Restaurante import Restaurante
from models.Produto import Produto
from models.Pedido import Pedido
from models.Pedidoitem import PedidoItem

from daos.cliente_dao import ClienteDAO
from daos.entregador_dao import EntregadorDAO
from daos.restaurante_dao import RestauranteDAO
from daos.produto_dao import ProdutoDAO
import daos.pedido_dao
import daos.pedido_itens_dao

def exibir_tabela(dados):
    if not dados:
        print("\n[!] Nenhum registro encontrado para esta consulta.")
        return
    print("\n" + "="*60)
    for registro in dados:
        print(registro)
    print("="*60)

def main():
    conexao = conectar()
    if not conexao:
        print("Falha crítica ao iniciar o sistema: Sem conexão com o banco.")
        return

    # Instanciação central de todos os DAOs
    c_dao = ClienteDAO(conexao)
    e_dao = EntregadorDAO(conexao)
    r_dao = RestauranteDAO(conexao)
    pr_dao = ProdutoDAO(conexao)
    p_dao = daos.pedido_dao.PedidoDAO(conexao)
    pi_dao = daos.pedido_itens_dao.PedidoItensDAO(conexao)

    while True:
        print("\n=== PAINEL DE CONTROLE - APP SERVIÇO ===")
        print("1. Gerenciar Clientes ")
        print("2. Gerenciar Entregadores")
        print("3. Gerenciar Restaurantes")
        print("4. Gerenciar Produtos")
        print("5. Gerenciar Pedidos e Itens")
        print("6. Executar Consultas Avançadas")
        print("0. Encerrar Sistema")
        
        opcao = input("Selecione um módulo: ")

        if opcao == '1':
            print("\n-- MÓDULO CLIENTE --")
            print("1. Cadastrar Cliente | 2. Listar Todos | 3. Atualizar Telefone | 4. Deletar | 5. Buscar por Email")
            sub = input("Escolha: ")
            if sub == '1':
                c = Cliente(None, input("Nome: "), input("Email: "), input("Telefone: "), input("Endereço: "))
                c_dao.inserir(c)
                print("[+] Cliente inserido e registrado no banco.")
            elif sub == '2':
                exibir_tabela(c_dao.listar_todos())
            elif sub == '3':
                c_dao.atualizar(int(input("ID do Cliente: ")), input("Novo Telefone: "))
                print("[+] Alteração salva com sucesso.")
            elif sub == '4':
                c_dao.deletar(int(input("ID do Cliente a remover: ")))
                print("[-] Registro deletado com sucesso.")
            elif sub == '5':
                exibir_tabela(c_dao.buscar_por_email(input("Email exato para busca: ")))

        elif opcao == '2':
            print("\n-- MÓDULO ENTREGADOR --")
            print("1. Cadastrar Entregador | 2. Listar Todos | 3. Atualizar Veículo | 4. Deletar | 5. Buscar por Veículo")
            sub = input("Escolha: ")
            if sub == '1':
                e = Entregador(None, input("Nome Único: "), input("Telefone: "), input("Tipo de Veículo: "))
                e_dao.inserir(e)
                print("[+] Entregador cadastrado.")
            elif sub == '2':
                exibir_tabela(e_dao.listar_todos())
            elif sub == '3':
                e_dao.atualizar_veiculo(int(input("ID do Entregador: ")), input("Novo Veículo: "))
                print("[+] Veículo modificado no backend.")
            elif sub == '4':
                e_dao.deletar(int(input("ID do Entregador a remover: ")))
                print("[-] Registro removido.")
            elif sub == '5':
                exibir_tabela(e_dao.buscar_por_veiculo(input("Filtrar por veículo (ex: Moto): ")))

        elif opcao == '3':
            print("\n-- MÓDULO RESTAURANTE --")
            print("1. Cadastrar Restaurante | 2. Listar Todos | 3. Atualizar Telefone | 4. Deletar | 5. Buscar por CNPJ")
            sub = input("Escolha: ")
            if sub == '1':
                r = Restaurante(None, input("Nome: "), input("CNPJ Único: "), input("Telefone: "), input("Endereço: "))
                r_dao.inserir(r)
                print("[+] Restaurante adicionado.")
            elif sub == '2':
                exibir_tabela(r_dao.listar_todos())
            elif sub == '3':
                r_dao.atualizar_telefone(int(input("ID do Restaurante: ")), input("Novo Telefone: "))
                print("[+] Contato atualizado.")
            elif sub == '4':
                r_dao.deletar(int(input("ID do Restaurante a remover: ")))
                print("[-] Registro removido.")
            elif sub == '5':
                exibir_tabela(r_dao.buscar_por_cnpj(input("CNPJ exato: ")))

        elif opcao == '4':
            print("\n-- MÓDULO PRODUTO --")
            print("1. Cadastrar Produto | 2. Listar Todos | 3. Atualizar Preço | 4. Deletar | 5. Buscar por Nome")
            sub = input("Escolha: ")
            if sub == '1':
                pr = Produto(None, input("Nome do Produto: "), float(input("Preço (ex: 25.50): ")), int(input("ID do Restaurante: ")), input("Descrição: "))
                pr_dao.inserir(pr)
                print("[+] Produto vinculado ao restaurante.")
            elif sub == '2':
                exibir_tabela(pr_dao.listar_todos())
            elif sub == '3':
                pr_dao.atualizar_preco(int(input("Código do Produto: ")), float(input("Novo Preço: ")))
                print("[+] Preço atualizado.")
            elif sub == '4':
                pr_dao.deletar(int(input("Código do Produto a remover: ")))
                print("[-] Produto removido do cardápio.")
            elif sub == '5':
                exibir_tabela(pr_dao.buscar_por_nome(input("Parte do nome do produto: ")))

        elif opcao == '5':
            print("\n-- MÓDULO PEDIDOS E ITENS --")
            print("1. Gerar Pedido (Trigger) | 2. Inserir Item ao Pedido | 3. Listar Pedidos | 4. Modificar Status | 5. Buscar por Status")
            sub = input("Escolha: ")
            if sub == '1':
                # Passar status como None força o banco a executar a Trigger 'statusped_inicial'
                p = Pedido(None, None, None, int(input("ID do Cliente: ")), int(input("ID do Entregador (ou 0): ")) or None)
                p_dao.inserir(p)
                print("[+] Pedido inicializado via backend (Verifique o status 'Pendente' gerado pela Trigger).")
            elif sub == '2':
                pi = PedidoItem(int(input("ID do Pedido: ")), int(input("Código do Produto: ")), int(input("Quantidade: ")), float(input("Preço Unitário: ")))
                pi_dao.inserir(pi)
                print("[+] Item adicionado com sucesso ao pedido.")
            elif sub == '3':
                exibir_tabela(p_dao.listar_todos())
            elif sub == '4':
                p_dao.atualizar_status(int(input("ID do Pedido: ")), input("Novo Status (Pendente/Em preparo/A caminho/...): "))
                print("[+] Status do pedido alterado.")
            elif sub == '5':
                exibir_tabela(p_dao.buscar_por_status(input("Filtrar por status exato: ")))

        elif opcao == '6':
            print("\n-- CONSULTAS AVANÇADAS --")
            print("1.Clientes e seus respectivos Pedidos")
            print("2.Pedidos vinculados aos seus Entregadores")
            print("3.Relatório Completo (Pedido + Cliente + Produto + Restaurante)")
            sub = input("Escolha a consulta: ")
            if sub == '1':
                exibir_tabela(c_dao.listar_clientes_com_seus_pedidos())
            elif sub == '2':
                exibir_tabela(p_dao.listar_pedidos_com_entregador())
            elif sub == '3':
                exibir_tabela(pi_dao.relatorio_detalhado_itens())

        elif opcao == '0':
            print("\nEncerrando conexões com o banco de dados...")
            break
        else:
            print("[!] Opção inválida no menu principal.")

    conexao.close()
    print("[+] Sistema encerrado de forma segura.")

if __name__ == "__main__":
    main()