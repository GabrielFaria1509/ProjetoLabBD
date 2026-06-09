class PedidoItensDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, item):
        sql = "INSERT INTO Pedido_Itens (pedido_id, cod_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (item.pedido_id, item.cod_produto, item.quantidade, item.preco_unitario))
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Pedido_Itens")
        return self.cursor.fetchall()

    def atualizar_quantidade(self, pedido_id, cod_produto, nova_qtd):
        sql = "UPDATE Pedido_Itens SET quantidade = %s WHERE pedido_id = %s AND cod_produto = %s"
        self.cursor.execute(sql, (nova_qtd, pedido_id, cod_produto))
        self.conexao.commit()

    def deletar_item(self, pedido_id, cod_produto):
        sql = "DELETE FROM Pedido_Itens WHERE pedido_id = %s AND cod_produto = %s"
        self.cursor.execute(sql, (pedido_id, cod_produto))
        self.conexao.commit()

    def buscar_por_pedido(self, pedido_id):
        sql = "SELECT * FROM Pedido_Itens WHERE pedido_id = %s"
        self.cursor.execute(sql, (pedido_id,))
        return self.cursor.fetchall()

    # JOIN 3: Relatório completo cruzando multiplas tabelas associadas
    def relatorio_detalhado_itens(self):
        sql = """
            SELECT p.id AS num_pedido, c.nome_cliente, pr.nome_produto, r.nome AS restaurante, pi.quantidade
            FROM Pedido_Itens pi
            INNER JOIN Pedido p ON pi.pedido_id = p.id
            INNER JOIN Cliente c ON p.cliente_id = c.id
            INNER JOIN Produto pr ON pi.cod_produto = pr.cod_produto
            INNER JOIN Restaurante r ON pr.restaurante_id = r.id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()