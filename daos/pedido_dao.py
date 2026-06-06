class PedidoDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, id_cliente, id_entregador):
        # Usando NOW() do MySQL para a data e deixando a Trigger definir o status 'Pendente'
        sql = "INSERT INTO Pedido (data, cliente_id, entregador_id) VALUES (NOW(), %s, %s)"
        self.cursor.execute(sql, (id_cliente, id_entregador))
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Pedido")
        return self.cursor.fetchall()

    def atualizar_status(self, id_pedido, novo_status):
        sql = "UPDATE Pedido SET status = %s WHERE id = %s"
        self.cursor.execute(sql, (novo_status, id_pedido))
        self.conexao.commit()

    def deletar(self, id_pedido):
      
        sql_itens = "DELETE FROM Pedido_Itens WHERE pedido_id = %s"
        self.cursor.execute(sql_itens, (id_pedido,))
        
        sql_pedido = "DELETE FROM Pedido WHERE id = %s"
        self.cursor.execute(sql_pedido, (id_pedido,))
        self.conexao.commit()

    # --- REQUISITO: Busca por atributo (1 por entidade) ---
    def buscar_por_status(self, status):
        sql = "SELECT * FROM Pedido WHERE status = %s"
        self.cursor.execute(sql, (status,))
        return self.cursor.fetchall()

    # --- REQUISITO: JOIN 2/3 ---
    def listar_pedidos_com_entregador(self):
        sql = """
            SELECT p.id AS pedido_id, p.status, e.nome AS nome_entregador, e.veiculo
            FROM Pedido p
            INNER JOIN Entregador e ON p.entregador_id = e.id_entregador
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # --- REQUISITO: JOIN 3/3 ---
    def relatorio_pedido_completo(self):
        # Aqui podemos até reaproveitar a sua View 'pedido_detalhado', 
        # mas como a regra pede "SELECT com JOIN", faremos na raça para garantir a nota:
        sql = """
            SELECT p.id, c.nome_cliente, pr.nome_produto, r.nome AS restaurante
            FROM Pedido p
            INNER JOIN Cliente c ON p.cliente_id = c.id
            INNER JOIN Pedido_Itens pi ON p.id = pi.pedido_id
            INNER JOIN Produto pr ON pi.cod_produto = pr.cod_produto
            INNER JOIN Restaurante r ON pr.restaurante_id = r.id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()