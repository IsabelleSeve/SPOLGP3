CREATE DATABASE IF NOT EXISTS gerenciamento_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

  USE gerenciamento_db;

CREATE TABLE IF NOT EXISTS usuario (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS projeto (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS categoria (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tarefa (
	id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    descricao VARCHAR(150),
    prioridade VARCHAR(20),
    status VARCHAR(20),
    criacao DATETIME,
    prazo DATETIME,
    excluida BOOLEAN DEFAULT FALSE,
    id_projeto INT,
    id_usuario INT,
    id_categoria INT,
    FOREIGN KEY (id_projeto) REFERENCES projeto(id) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE SET NULL

)