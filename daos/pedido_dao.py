class PedidoDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, pedido):
        # Permite deixar o status nulo para que a Trigger 'statusped_inicial' defina como 'Pendente'
        sql = "INSERT INTO Pedido (data, status, cliente_id, entregador_id) VALUES (NOW(), %s, %s, %s)"
        self.cursor.execute(sql, (pedido.status, pedido.cliente_id, pedido.entregador_id))
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Pedido")
        return self.cursor.fetchall()

    def atualizar_status(self, id_pedido, novo_status):
        sql = "UPDATE Pedido SET status = %s WHERE id = %s"
        self.cursor.execute(sql, (novo_status, id_pedido))
        self.conexao.commit()

    def deletar(self, id_pedido):
        sql = "DELETE FROM Pedido WHERE id = %s"
        self.cursor.execute(sql, (id_pedido,))
        self.conexao.commit()

    def buscar_por_status(self, status):
        sql = "SELECT * FROM Pedido WHERE status = %s"
        self.cursor.execute(sql, (status,))
        return self.cursor.fetchall()

    # JOIN 2: Relação de Pedidos e seus respectivos Entregadores alocados
    def listar_pedidos_com_entregador(self):
        sql = """
            SELECT p.id AS pedido_id, p.status, e.nome AS nome_entregador, e.veiculo
            FROM Pedido p
            INNER JOIN Entregador e ON p.entregador_id = e.id_entregador
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()