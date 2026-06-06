class ClienteDAO:
    def __init__(self,conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)
        
    def inserir(self,cliente):
        sql = "INSERT INTO Cliente (nome_cliente, email, telefone, endereco) VALUES (%s, %s, %s, %s)"
        valores = (cliente.nome_cliente, cliente.email, cliente.telefone, cliente.endereco)
        self.cursor.execute(sql, valores)
        self.conexao.commit()
        
    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Cliente")
        return self.cursor.fetchall()
    
    def atualizar(self, id_cliente, novo_telefone):
        sql = "UPDATE Cliente SET telefone = %s WHERE id = %s"
        self.cursor.execute(sql, (novo_telefone, id_cliente))
        self.conexao.commit()
        
    def deletar(self, id_cliente):
        sql = "DELETE FROM Cliente WHERE id = %s"
        self.cursor.execute(sql, (id_cliente,))
        self.conexao.commit()
        
    # --- REQUISITO: Busca por atributo (1 por entidade) ---
    def buscar_por_email(self, email):
        sql = "SELECT * FROM Cliente WHERE email = %s"
        self.cursor.execute(sql, (email,))
        return self.cursor.fetchall()

    # --- REQUISITO: JOIN 1/3 ---
    def listar_clientes_com_seus_pedidos(self):
        sql = """
            SELECT c.nome_cliente, p.id AS id_pedido, p.status 
            FROM Cliente c
            INNER JOIN Pedido p ON c.id = p.cliente_id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    # --- REQUISITO: JOIN 3/3 ---
    def relatorio_pedido_completo(self):
        
    
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