# 🍔 Sistema de Gerenciamento de Delivery (BD)

Projeto prático de Banco de Dados Relacional desenvolvido por estudantes de Engenharia do Instituto Nacional de Telecomunicações (Inatel). O objetivo deste projeto é modelar e implementar a infraestrutura de dados para um aplicativo de delivery, conectando Clientes, Restaurantes e Entregadores.

## 📌 Visão Geral do Projeto

O sistema `app_servico` gerencia o fluxo completo de um pedido de delivery, desde o cadastro dos usuários e restaurantes até a alocação de entregadores e cálculo financeiro dos itens solicitados. O projeto foi construído utilizando **MySQL** e aplica conceitos avançados de DDL, DML, DQL e DCL.

## 👥 Equipe de Desenvolvimento
* **Gabriel Faria** - [fariagabriel1509@gmial.com]
* **[Nome do Colega 1]** - [Matrícula/Contato]
* **[Nome do Colega 2]** - [Matrícula/Contato]

## 🏗️ Estrutura do Banco de Dados (Tabelas)

O banco de dados está normalizado e estruturado nas seguintes entidades principais:

* **`Cliente`**: Armazena dados dos usuários (nome, e-mail único, telefone, endereço).
* **`Restaurante`**: Cadastro dos estabelecimentos parceiros (nome, CNPJ único, endereço).
* **`Produto`**: Catálogo de itens vendidos, vinculados a um restaurante específico via Chave Estrangeira (FK).
* **`Entregador`**: Informações da frota de entregadores e seus veículos.
* **`Pedido`**: Tabela central que registra a transação. Possui controle de data, `status` (via ENUM) e liga o Cliente ao Entregador alocado.
* **`Pedido_Itens`**: Tabela associativa (N:M) que detalha a composição do pedido, registrando a quantidade e travando o preço unitário no momento da compra.

## 🚀 Recursos Avançados Implementados

Para garantir a integridade, automação e segurança dos dados, o script implementa os seguintes objetos programáveis:

### 1. Triggers (Gatilhos)
* **`statusped_inicial`**: Garante regra de negócio automatizada. Toda vez que um novo registro é inserido na tabela `Pedido` sem um status definido, a trigger atua em nível `BEFORE INSERT` e altera o status automaticamente para `'Pendente'`.

### 2. Stored Procedures (Procedimentos Armazenados)
* **`criar_pedido_automatico`**: Facilita testes e integrações. Recebe apenas o ID de um cliente, sorteia um entregador aleatório do banco de dados (usando `ORDER BY RAND()`) e gera um pedido inicial de forma automatizada.

### 3. Views (Visões)
* **`pedido_detalhado`**: Consolida dados espalhados em múltiplas tabelas através de `INNER JOINs`, gerando um relatório completo com o nome do cliente, restaurante, produto e total por linha de item.
* **`v_entregador_cliente`**: View focada em segurança e regra de negócio, expondo apenas as informações vitais para o entregador (ID do pedido, nome do cliente, telefone e endereço de entrega), ocultando dados sensíveis e financeiros.

### 4. Functions (Funções)
* **`calcular_total_geral_pedido`**: Encapsula a lógica financeira. Recebe o ID de um pedido e consulta a view `pedido_detalhado` para retornar o valor total exato a ser cobrado do cliente, lidando automaticamente com verificações nulas (`IFNULL`).

### 5. Segurança e Controle de Acesso (DCL)
* Implementação de criação de usuários específicos (`PedrinhoSushi`, `RicardoCliente`, `LuizinhoMotoboy`) e gerenciamento de permissões (ex: `GRANT SELECT`) para restringir o acesso apenas aos dados necessários (como a leitura da `v_entregador_cliente`).

## 🛠️ Como Executar o Projeto

1. Certifique-se de ter o **MySQL Server** e o **MySQL Workbench** instalados na sua máquina.
2. Clone este repositório ou baixe o arquivo `script_delivery.sql`.
3. Abra o arquivo `.sql` no MySQL Workbench.
4. Execute o script completo (clicando no ícone do raio sem selecionar nenhuma linha específica).
   * *Nota: O script possui a instrução `DROP DATABASE IF EXISTS app_servico;` no topo, o que significa que ele apagará versões anteriores e criará um banco limpo e populado com dados de teste automaticamente.*
5. Para testar a visualização dos dados, execute as consultas no final do arquivo, como:
   ```sql
   SELECT * FROM pedido_detalhado;
   SELECT calcular_total_geral_pedido(1) AS Total;
