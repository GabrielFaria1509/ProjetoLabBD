import mysql.connector
from mysql.connector import Error;

def conectar():
    try:
        conexao = mysql.connector.connect(
            host = "localhost",
            database = "app_servico",
            user = "root",
            password = "root"
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None