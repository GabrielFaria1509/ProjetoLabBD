DROP DATABASE IF EXISTS app_servico;
CREATE DATABASE app_servico;
USE app_servico;

-- ==========================================
-- TABELAS
-- ==========================================
CREATE TABLE Cliente(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_cliente VARCHAR(45) NOT NULL,          
    email VARCHAR(45) UNIQUE,                   
    telefone VARCHAR(20),                       
    endereco VARCHAR(100)                       
);

CREATE TABLE Entregador(
    id_entregador INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    nome VARCHAR(45) UNIQUE,                    
    telefone VARCHAR(20),                       
    veiculo VARCHAR(45)                         
);

CREATE TABLE Restaurante(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(45) UNIQUE,
    cnpj VARCHAR(20) UNIQUE,                    
    telefone VARCHAR(20),
    endereco VARCHAR(100)
);

CREATE TABLE Pedido(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    data DATETIME,                              
    status ENUM('Pendente', 'Em preparo', 'A caminho', 'Saiu para entrega', 'Entregue', 'Atrasado', 'Cancelado'), 
    cliente_id INT NOT NULL,                    
    entregador_id INT,                          
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (cliente_id) REFERENCES Cliente(id),
    CONSTRAINT fk_pedido_entregador FOREIGN KEY (entregador_id) REFERENCES Entregador(id_entregador)
);

CREATE TABLE Produto (
    cod_produto INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    nome_produto VARCHAR(45),                            
    preco DECIMAL(10,2),                                 
    restaurante_id INT NOT NULL,                         
    descricao VARCHAR(50),
    CONSTRAINT fk_produto_restaurante FOREIGN KEY (restaurante_id) REFERENCES Restaurante(id)
);

CREATE TABLE Pedido_Itens(
    pedido_id INT NOT NULL,               
    cod_produto INT NOT NULL,             
    quantidade INT,                       
    preco_unitario DECIMAL(10,2),         
    PRIMARY KEY (pedido_id, cod_produto), 
    CONSTRAINT fk_item_pedido FOREIGN KEY (pedido_id) REFERENCES Pedido(id),
    CONSTRAINT fk_item_produto FOREIGN KEY (cod_produto) REFERENCES Produto(cod_produto)
);

-- ==========================================
-- INSERÇÃO DE DADOS 
-- ==========================================
INSERT INTO Restaurante (nome, cnpj, endereco, telefone) VALUES 
('Pizzaria Napoli', '43.782.112/0001-55', 'Rua Cerejeira, 1450 - Centro Novo', '4002-8922'),
('Burger House Grill', '18.945.771/0001-03', 'Avenida Horizonte, 780 - Vila Esperança', '3521-7788'),
('Sushi Express', '62.551.903/0001-41', 'Rua das Oliveiras, 320 - Jardim América', '3344-2233'),
('Pastelaria Sabor Mineiro', '91.447.002/0001-80', 'Rua Pedra Branca, 512 - Bairro União', '3011-9988'),
('Doceria Doce Encanto', '27.113.665/0001-19', 'Avenida Aurora, 1200 - Parque Real', '3254-7766');

INSERT INTO Cliente (nome_cliente, email, telefone, endereco) VALUES 
('Ana Carolina Silva', 'ana.silva@gmail.com', '99874-1122', 'Rua das Acácias, 245 - Jardim Primavera'),
('Carlos Eduardo Souza', 'carlos.souza@gmail.com', '99711-4455', 'Avenida Sol Nascente, 1500 - Bairro Central'),
('Marina Oliveira Lima', 'marina.lima@gmail.com', '98855-6633', 'Rua Monte Azul, 87 - Vila Harmonia'),
('Pedro Henrique Alves', 'pedro.alves@gmail.com', '99122-7788', 'Rua Bela Vista, 420 - Jardim Imperial'),
('Julia Fernanda Costa', 'julia.costa@gmail.com', '99654-8877', 'Avenida Lago Dourado, 980 - Parque das Flores');

INSERT INTO Produto (nome_produto, preco, descricao, restaurante_id) VALUES 
('Pizza Calabresa', 45.00, 'Pizza grande', 1),
('Hamburguer', 30.00, 'Hamburguer artesanal', 2),
('Combo Sushi', 60.00, '20 peças', 3),
('Pastel Queijo', 12.00, 'Pastel crocante', 4),
('Bolo Chocolate', 25.00, 'Bolo caseiro', 5);

INSERT INTO Entregador (nome, telefone, veiculo) VALUES 
('Joao', '98888-1111', 'Moto'),
('Lucas', '98888-2222', 'Carro'),
('Marcos', '98888-3333', 'Moto'),
('Felipe', '98888-4444', 'Bike'),
('Rafael', '98888-5555', 'Moto');

INSERT INTO Pedido (data, status, cliente_id) VALUES 
(NOW(), 'Em preparo', 1),
(NOW(), 'Entregue', 2),
(NOW(), 'Saiu para entrega', 3),
(NOW(), 'Cancelado', 4),
(NOW(), 'Em preparo', 5);

INSERT INTO Pedido_Itens (quantidade, preco_unitario, pedido_id, cod_produto) VALUES 
(2, 45.00, 1, 1),
(1, 30.00, 2, 2),
(3, 60.00, 3, 3),
(2, 12.00, 4, 4),
(1, 25.00, 5, 5);

-- =============================================================================
-- TRIGGER: Status Inicial Pendente
-- =============================================================================
DELIMITER $$
CREATE TRIGGER statusped_inicial
BEFORE INSERT ON Pedido
FOR EACH ROW
BEGIN
    IF NEW.status IS NULL THEN
        SET NEW.status = 'Pendente';
    END IF;
END$$
DELIMITER ;

-- =============================================================================
-- PROCEDURE: Criar pedido testando a Trigger
-- =============================================================================
DELIMITER $$
CREATE PROCEDURE criar_pedido_automatico(
    IN p_cliente INT
)
BEGIN
    DECLARE entregador_sorteado INT;

    -- Sorteia um entregador aleatório
    SELECT id_entregador
    INTO entregador_sorteado
    FROM Entregador
    ORDER BY RAND()
    LIMIT 1;

    -- Cria o pedido SEM o status para forçar a Trigger a agir
    INSERT INTO Pedido(data, cliente_id, entregador_id)
    VALUES(NOW(), p_cliente, entregador_sorteado);
END$$
DELIMITER ;

-- =============================================================================
-- VIEW: Relatório detalhado
-- =============================================================================
CREATE VIEW pedido_detalhado AS 
SELECT 
    p.id AS pedido,   
    c.nome_cliente AS cliente,
    r.nome AS restaurante,
    p.status AS status_pedido,
    pr.nome_produto AS produto,
    pi.preco_unitario AS preco_unitario,
    pi.quantidade,
    (pi.quantidade * pi.preco_unitario) AS total_item 
FROM Pedido p  
INNER JOIN Cliente c ON p.cliente_id = c.id  
INNER JOIN Pedido_Itens pi ON p.id = pi.pedido_id
INNER JOIN Produto pr ON pi.cod_produto = pr.cod_produto
INNER JOIN Restaurante r ON pr.restaurante_id = r.id;

-- =============================================================================
-- FUNCTION: Total do Pedido
-- =============================================================================
DELIMITER $$
CREATE FUNCTION calcular_total_geral_pedido(p_pedido_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_total_geral DECIMAL(10,2);
    
    SELECT IFNULL(SUM(total_item), 0.00)
    INTO v_total_geral
    FROM pedido_detalhado
    WHERE pedido = p_pedido_id; 
    
    RETURN v_total_geral;
END $$
DELIMITER ;

-- =============================================================================

-- =============================================================================
-- Essa view mostra apenas o que o entregador precisa saber: para onde levar e quem contatar
CREATE VIEW v_entregador_cliente AS
SELECT 
    p.id AS numero_pedido,
    c.nome_cliente,
    c.telefone AS telefone_cliente,
    c.endereco AS endereco_entrega,
    p.status AS status_pedido
FROM Pedido p
INNER JOIN Cliente c ON p.cliente_id = c.id;

-- USUÁRIOS
-- =============================================================================
-- Primeiro, apagamos os usuários caso eles já existam de execuções anteriores
DROP USER IF EXISTS 'PedrinhoSushi'@'localhost';
DROP USER IF EXISTS 'RicardoCliente'@'localhost';
DROP USER IF EXISTS 'LuizinhoMotoboy'@'localhost';

-- criamos os usuários do zero
CREATE USER 'PedrinhoSushi'@'localhost' IDENTIFIED BY 'Senha123';
CREATE USER 'RicardoCliente'@'localhost' IDENTIFIED BY 'Senha3535';
CREATE USER 'LuizinhoMotoboy'@'localhost' IDENTIFIED BY 'Senha456';


-- =============================================================================
-- ROLES E PERMISSÕES (DCL)
-- =============================================================================
CREATE ROLE cliente;
CREATE ROLE restaurante;
CREATE ROLE entregador;

-- ==================== VISÃO DO CLIENTE ====================
-- View para cliente ver restaurantes
CREATE VIEW v_cliente_restaurante AS
SELECT nome, endereco
FROM Restaurante;

-- View para cliente ver produtos
CREATE VIEW v_cliente_produto AS
SELECT nome_produto AS nome, preco 
FROM Produto;

-- Permissões do Cliente
GRANT SELECT ON v_cliente_restaurante TO cliente;
GRANT SELECT ON v_cliente_produto TO cliente;
GRANT INSERT (cliente_id, data, status) ON Pedido TO cliente; -- Removido restaurante_id que não existe aqui
GRANT INSERT (pedido_id, cod_produto, quantidade) ON Pedido_Itens TO cliente; -- Corrigido nome da tabela e coluna
GRANT SELECT ON Pedido TO cliente; 

-- ==================== VISÃO DO RESTAURANTE ====================
-- View para restaurante ver pedidos recebidos
CREATE VIEW v_restaurante_pedido AS
SELECT id, cliente_id, data, status
FROM Pedido;

-- Permissões do Restaurante
GRANT SELECT ON v_restaurante_pedido TO restaurante;
GRANT SELECT, INSERT, UPDATE, DELETE ON Produto TO restaurante;
GRANT UPDATE (status) ON Pedido TO restaurante;
GRANT UPDATE (nome, endereco, telefone, cnpj) ON Restaurante TO restaurante;

-- ==================== VISÃO DO ENTREGADOR ====================
-- View para entregador ver pedidos atribuídos 
CREATE VIEW v_entregador_pedido AS
SELECT p.id AS pedido_id, p.cliente_id, c.endereco AS endereco_entrega, p.status
FROM Pedido p
INNER JOIN Cliente c ON p.cliente_id = c.id;

-- Permissões do Entregador
GRANT SELECT ON v_entregador_pedido TO entregador;
GRANT UPDATE (status) ON Pedido TO entregador;
GRANT SELECT ON v_entregador_cliente TO entregador; -- Utiliza aquela View completa que já estava criada mais acima

-- =============================================================================
-- ATRIBUIÇÃO DE ROLES AOS USUÁRIOS
-- =============================================================================
GRANT cliente TO 'RicardoCliente'@'localhost';
GRANT restaurante TO 'PedrinhoSushi'@'localhost';
GRANT entregador TO 'LuizinhoMotoboy'@'localhost';

-- Para o MySQL ativar as roles padrão de cada usuário assim que eles logarem:
SET DEFAULT ROLE cliente TO 'RicardoCliente'@'localhost';
SET DEFAULT ROLE restaurante TO 'PedrinhoSushi'@'localhost';
SET DEFAULT ROLE entregador TO 'LuizinhoMotoboy'@'localhost';

-- =============================================================================
-- TESTE DA VIEW FINAL
-- =============================================================================
SELECT * FROM pedido_detalhado;
