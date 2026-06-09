class RestauranteDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, restaurante):
        sql = "INSERT INTO Restaurante (nome, cnpj, telefone, endereco) VALUES (%s, %s, %s, %s)"
        valores = (restaurante.nome, restaurante.cnpj, restaurante.telefone, restaurante.endereco)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Restaurante")
        return self.cursor.fetchall()

    def atualizar_telefone(self, id_restaurante, novo_telefone):
        sql = "UPDATE Restaurante SET telefone = %s WHERE id = %s"
        self.cursor.execute(sql, (novo_telefone, id_restaurante))
        self.conexao.commit()

    def deletar(self, id_restaurante):
        sql = "DELETE FROM Restaurante WHERE id = %s"
        self.cursor.execute(sql, (id_restaurante,))
        self.conexao.commit()

    def buscar_por_cnpj(self, cnpj):
        sql = "SELECT * FROM Restaurante WHERE cnpj = %s"
        self.cursor.execute(sql, (cnpj,))
        return self.cursor.fetchall()