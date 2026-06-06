import mysql.connector ##Biblioteca para conectar ao MySQL
from mysql.connector import Error; 

def conectar(): ##Função para estabelecer conexão com o banco de dados
    try: ##try catch para lidar com possíveis erros de conexão
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