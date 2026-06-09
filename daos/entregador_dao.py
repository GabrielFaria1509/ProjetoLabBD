class EntregadorDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, entregador):
        sql = "INSERT INTO Entregador (nome, telefone, veiculo) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (entregador.nome, entregador.telefone, entregador.veiculo))
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Entregador")
        return self.cursor.fetchall()

    def atualizar_veiculo(self, id_entregador, novo_veiculo):
        sql = "UPDATE Entregador SET veiculo = %s WHERE id_entregador = %s"
        self.cursor.execute(sql, (novo_veiculo, id_entregador))
        self.conexao.commit()

    def deletar(self, id_entregador):
        sql = "DELETE FROM Entregador WHERE id_entregador = %s"
        self.cursor.execute(sql, (id_entregador,))
        self.conexao.commit()

    def buscar_por_veiculo(self, veiculo):
        sql = "SELECT * FROM Entregador WHERE veiculo = %s"
        self.cursor.execute(sql, (veiculo,))
        return self.cursor.fetchall()