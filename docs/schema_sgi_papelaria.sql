-- 1. Tabelas Auxiliares e Dimensões
CREATE TABLE CATEGORIAS (
    ID_Categoria INT PRIMARY KEY AUTO_INCREMENT,
    Nome_Categoria VARCHAR(100) NOT NULL
);

CREATE TABLE FORNECEDORES (
    ID_Fornecedor INT PRIMARY KEY AUTO_INCREMENT,
    Nome_Fornecedor VARCHAR(100) NOT NULL,
    CNPJ VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE USUARIOS (
    ID_Usuario INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Perfil VARCHAR(50) NOT NULL
);

-- 2. Tabela Principal de Produtos
CREATE TABLE PRODUTOS (
    ID_Produto INT PRIMARY KEY AUTO_INCREMENT,
    SKU_EAN VARCHAR(50) UNIQUE NOT NULL,
    Nome VARCHAR(150) NOT NULL,
    Descricao TEXT,
    Preco_Varejo DECIMAL(10,2) NOT NULL,
    Preco_Atacado DECIMAL(10,2) NOT NULL,
    Qtd_Min_Atacado INT DEFAULT 12,
    NCM VARCHAR(8),
    Unidade_Medida VARCHAR(10),
    Custo_Aquisicao DECIMAL(10,2),
    FK_Categoria INT,
    FK_Fornecedor INT,
    FOREIGN KEY (FK_Categoria) REFERENCES CATEGORIAS(ID_Categoria),
    FOREIGN KEY (FK_Fornecedor) REFERENCES FORNECEDORES(ID_Fornecedor)
);

-- 3. Tabela de Controle de Estoque (Relacionamento 1:1)
CREATE TABLE ESTOQUE (
    FK_Produto INT PRIMARY KEY,
    Quantidade_Atual INT NOT NULL DEFAULT 0,
    Ponto_Pedido INT DEFAULT 5,
    Localizacao_Fisica VARCHAR(100),
    Ultima_Atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (FK_Produto) REFERENCES PRODUTOS(ID_Produto)
);

-- 4. Tabelas de Movimentação Transacional (Vendas)
CREATE TABLE VENDAS_MESTRE (
    ID_Venda INT PRIMARY KEY AUTO_INCREMENT,
    Data_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Origem VARCHAR(50),
    FK_Usuario INT,
    Valor_Total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (FK_Usuario) REFERENCES USUARIOS(ID_Usuario)
);

CREATE TABLE VENDAS_ITENS (
    FK_Venda INT,
    FK_Produto INT,
    Quantidade INT NOT NULL,
    Preco_Aplicado DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (FK_Venda, FK_Produto),
    FOREIGN KEY (FK_Venda) REFERENCES VENDAS_MESTRE(ID_Venda),
    FOREIGN KEY (FK_Produto) REFERENCES PRODUTOS(ID_Produto)
);
