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
