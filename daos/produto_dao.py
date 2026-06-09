class ProdutoDAO:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor(dictionary=True)

    def inserir(self, produto):
        sql = "INSERT INTO Produto (nome_produto, preco, restaurante_id, descricao) VALUES (%s, %s, %s, %s)"
        valores = (produto.nome_produto, produto.preco, produto.restaurante_id, produto.descricao)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def listar_todos(self):
        self.cursor.execute("SELECT * FROM Produto")
        return self.cursor.fetchall()

    def atualizar_preco(self, cod_produto, novo_preco):
        sql = "UPDATE Produto SET preco = %s WHERE cod_produto = %s"
        self.cursor.execute(sql, (novo_preco, cod_produto))
        self.conexao.commit()

    def deletar(self, cod_produto):
        sql = "DELETE FROM Produto WHERE cod_produto = %s"
        self.cursor.execute(sql, (cod_produto,))
        self.conexao.commit()

    def buscar_por_nome(self, nome):
        sql = "SELECT * FROM Produto WHERE nome_produto LIKE %s"
        self.cursor.execute(sql, (f"%{nome}%",))
        return self.cursor.fetchall()