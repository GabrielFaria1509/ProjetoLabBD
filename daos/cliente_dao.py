##Classes DAO são responsáveis por realizar as operações de CRUD (Create, Read, Update, Delete) no banco de dados para cada entidade do sistema.

class ClienteDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, cliente):
        sql = "INSERT INTO Cliente (nome_cliente, email, telefone, endereco) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (cliente.nome_cliente, cliente.email, cliente.telefone, cliente.endereco))
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

    def buscar_por_email(self, email):
        sql = "SELECT * FROM Cliente WHERE email = %s"
        self.cursor.execute(sql, (email,))
        return self.cursor.fetchall()

    # JOIN 1: Relação entre clientes e pedidos realizados
    def listar_clientes_com_seus_pedidos(self):
        sql = """
            SELECT c.nome_cliente, p.id AS id_pedido, p.status 
            FROM Cliente c
            INNER JOIN Pedido p ON c.id = p.cliente_id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()