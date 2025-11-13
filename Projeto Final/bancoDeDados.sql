CREATE DATABASE IF NOT EXISTS gerenciamento_notas_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
  
USE gerenciamento_notas_db;  

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf CHAR(11) UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('aluno', 'professor', 'coordenador', 'administrador') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Turmas (
    id_turma INT AUTO_INCREMENT PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    ano_letivo YEAR NOT NULL,
    turno ENUM('manhã', 'tarde', 'noite') NOT NULL
);

CREATE TABLE Materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    nome_materia VARCHAR(100) NOT NULL,
    carga_horaria INT,
     descricao TEXT
);

CREATE TABLE Alunos (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    matricula_aluno VARCHAR(20) UNIQUE NOT NULL,
    data_nascimento DATE,
    id_turma INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_turma) REFERENCES Turmas(id_turma)
);

CREATE TABLE Professores (
    id_professor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    matricula_professor VARCHAR(20) UNIQUE NOT NULL,
    formacao VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

CREATE TABLE Notas (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_materia INT NOT NULL,
    id_professor INT NOT NULL,
    nota1 DECIMAL(5,2),
    nota2 DECIMAL(5,2),
    nota3 DECIMAL(5,2),
    recuperacao DECIMAL(5,2),
    nota_final DECIMAL(5,2),
    ano_letivo YEAR,
    FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia),
    FOREIGN KEY (id_professor) REFERENCES Professores(id_professor)
);

CREATE TABLE Professores_Materias (
    id_professor INT,
    id_materia INT,
    PRIMARY KEY (id_professor, id_materia),
    FOREIGN KEY (id_professor) REFERENCES Professores(id_professor),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);

CREATE TABLE Turmas_Materias (
    id_turma INT,
    id_materia INT,
    PRIMARY KEY (id_turma, id_materia),
    FOREIGN KEY (id_turma) REFERENCES Turmas(id_turma),
    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
);



-- TABELA: Usuarios
INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario, ativo) VALUES
('João da Silva', 'joao.silva@email.com', '12345678901', 'senha123', 'aluno', TRUE),
('Maria Oliveira', 'maria.oliveira@email.com', '23456789012', 'senha123', 'aluno', TRUE),
('Pedro Santos', 'pedro.santos@email.com', '34567890123', 'senha123', 'professor', TRUE),
('Ana Costa', 'ana.costa@email.com', '45678901234', 'senha123', 'professor', TRUE),
('Carla Souza', 'carla.souza@email.com', '56789012345', 'senha123', 'coordenador', TRUE),
('Admin Sistema', 'admin@email.com', '67890123456', 'admin123', 'administrador', TRUE);

-- TABELA: Turmas
INSERT INTO Turmas (nome_turma, ano_letivo, turno) VALUES
('1º Ano A', 2025, 'manhã'),
('2º Ano B', 2025, 'tarde');

-- TABELA: Materias
INSERT INTO Materias (nome_materia, carga_horaria, descricao) VALUES
('Matemática', 80, 'Conceitos fundamentais de aritmética, álgebra e geometria.'),
('Português', 80, 'Leitura, interpretação e produção textual.'),
('História', 60, 'Estudo das civilizações antigas e modernas.'),
('Física', 60, 'Princípios básicos da mecânica e eletricidade.');

-- TABELA: Alunos
INSERT INTO Alunos (id_usuario, matricula_aluno, data_nascimento, id_turma) VALUES
(1, 'A2025001', '2008-03-15', 1),
(2, 'A2025002', '2008-07-21', 2);

-- TABELA: Professores
INSERT INTO Professores (id_usuario, matricula_professor, formacao) VALUES
(3, 'P2025001', 'Licenciatura em Matemática'),
(4, 'P2025002', 'Licenciatura em Letras');

-- TABELA: Professores_Materias (relação professor → matéria)
INSERT INTO Professores_Materias (id_professor, id_materia) VALUES
(1, 1), -- Pedro ensina Matemática
(1, 4), -- Pedro ensina Física
(2, 2); -- Ana ensina Português

-- TABELA: Turmas_Materias (relação turma → matéria)
INSERT INTO Turmas_Materias (id_turma, id_materia) VALUES
(1, 1), -- 1º Ano A → Matemática
(1, 2), -- 1º Ano A → Português
(1, 3), -- 1º Ano A → História
(2, 1), -- 2º Ano B → Matemática
(2, 4); -- 2º Ano B → Física

-- TABELA: Notas
INSERT INTO Notas (id_aluno, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo) VALUES
(1, 1, 1, 7.5, 8.0, 9.0, NULL, 8.2, 2025), -- João em Matemática com Pedro
(1, 2, 2, 6.0, 7.0, 8.0, NULL, 7.0, 2025), -- João em Português com Ana
(2, 1, 1, 8.0, 8.5, 9.0, NULL, 8.5, 2025), -- Maria em Matemática
(2, 4, 1, 5.0, 6.0, 6.5, 7.0, 6.5, 2025);  -- Maria em Física, passou na recuperação
