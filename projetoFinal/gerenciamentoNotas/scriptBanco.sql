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

    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        ON DELETE CASCADE,

    FOREIGN KEY (id_turma) REFERENCES Turmas(id_turma)
        ON DELETE CASCADE
);

CREATE TABLE Professores (
    id_professor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    matricula_professor VARCHAR(20) UNIQUE NOT NULL,
    formacao VARCHAR(100),

    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        ON DELETE CASCADE
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

    FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno)
        ON DELETE CASCADE,

    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
        ON DELETE CASCADE,

    FOREIGN KEY (id_professor) REFERENCES Professores(id_professor)
        ON DELETE CASCADE
);

CREATE TABLE Professores_Materias (
    id_professor INT,
    id_materia INT,
    PRIMARY KEY (id_professor, id_materia),

    FOREIGN KEY (id_professor) REFERENCES Professores(id_professor)
        ON DELETE CASCADE,

    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
        ON DELETE CASCADE
);

CREATE TABLE Turmas_Materias (
    id_turma INT,
    id_materia INT,
    PRIMARY KEY (id_turma, id_materia),

    FOREIGN KEY (id_turma) REFERENCES Turmas(id_turma)
        ON DELETE CASCADE,

    FOREIGN KEY (id_materia) REFERENCES Materias(id_materia)
        ON DELETE CASCADE
);

-- TRIGGERS
DELIMITER $$

CREATE TRIGGER trg_criar_aluno
AFTER INSERT ON Usuarios
FOR EACH ROW
BEGIN
    IF NEW.tipo_usuario = 'aluno' THEN
        INSERT INTO Alunos (id_usuario, matricula_aluno)
        VALUES (
            NEW.id_usuario,
            CONCAT('ALU', LPAD(NEW.id_usuario, 5, '0'))
        );
    END IF;
END$$

CREATE TRIGGER trg_criar_professor
AFTER INSERT ON Usuarios
FOR EACH ROW
BEGIN
    IF NEW.tipo_usuario = 'professor' THEN
        INSERT INTO Professores (id_usuario, matricula_professor)
        VALUES (
            NEW.id_usuario,
            CONCAT('PRO', LPAD(NEW.id_usuario, 5, '0'))
        );
    END IF;
END$$

CREATE TRIGGER trg_assoc_materia_todas_turmas
AFTER INSERT ON Materias
FOR EACH ROW
BEGIN
    INSERT INTO Turmas_Materias (id_turma, id_materia)
    SELECT t.id_turma, NEW.id_materia
    FROM Turmas t;
END$$

CREATE TRIGGER trg_assoc_turma_todas_materias
AFTER INSERT ON Turmas
FOR EACH ROW
BEGIN
    INSERT INTO Turmas_Materias (id_turma, id_materia)
    SELECT NEW.id_turma, m.id_materia
    FROM Materias m;
END$$

DELIMITER ;

-- POVOANDO TABELAS
INSERT INTO Turmas (nome_turma, ano_letivo, turno)
VALUES 
('1º Ano A', 2025, 'manhã'),
('1º Ano B', 2025, 'tarde'),
('2º Ano A', 2025, 'noite');

INSERT INTO Materias (nome_materia, carga_horaria, descricao)
VALUES
('Matemática', 80, 'Matemática básica e avançada'),
('Português', 80, 'Gramática e literatura'),
('História', 60, 'História geral e do Brasil');

INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario)
VALUES
('João Silva', 'joao@gmail.com', '11111111111', SHA2('123456', 256), 'aluno'),
('Maria Souza', 'maria@gmail.com', '22222222222', SHA2('123456', 256), 'aluno'),
('Carlos Pereira', 'carlos@gmail.com', '33333333333', SHA2('123456', 256), 'aluno');

INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario)
VALUES
('Prof. Ricardo', 'ricardo@gmail.com', '44444444444', SHA2('123456', 256), 'professor'),
('Prof. Ana', 'ana@gmail.com', '55555555555', SHA2('123456', 256), 'professor');

INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario)
VALUES
('Coordenador Paulo', 'paulo@gmail.com', '66666666666', SHA2('123456', 256), 'coordenador'),
('Administrador Pedro', 'pedro@gmail.com', '77777777777', SHA2('123456', 256), 'administrador');

UPDATE Alunos SET id_turma = 1 WHERE id_aluno = 1;
UPDATE Alunos SET id_turma = 1 WHERE id_aluno = 2;
UPDATE Alunos SET id_turma = 2 WHERE id_aluno = 3;

INSERT INTO Professores_Materias (id_professor, id_materia) VALUES
(9, 5),   
(9, 6),   
(10, 7);  

INSERT INTO Notas 
(id_aluno, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo)
VALUES
(8, 5, 9, 7.0, 8.0, 6.5, NULL, 7.2, 2024),
(8, 6, 9, 9.0, 8.5, 9.5, NULL, 9.0, 2024),
(9, 5, 9, 5.0, 6.0, 7.0, 8.0, 7.1, 2024),
(10, 7, 10, 8.0, 7.5, 9.0, NULL, 8.2, 2024);

UPDATE Usuarios
SET senha = 
    CASE 
        WHEN tipo_usuario = 'aluno' THEN '$2b$12$qVNVViivJtB1kJSdk8a/jOQeQeQ1uUwwZxRsNQWtq0qPIglxGX21X8O' -- 123456
        WHEN tipo_usuario = 'professor' THEN '$2b$12$H0p3y2OB7CBdaJNu9r09uOu/sgny9KfULpuTxq7VXBL5xIfN66QHS' -- prof123
        WHEN tipo_usuario = 'coordenador' THEN '$2b$12$8NLyVgP3hWrtqzXp8vsnHOlFtZjV3NUVxesJoHgLFNu6C1OwWk.xm' -- coord123
        WHEN tipo_usuario = 'administrador' THEN '$2b$12$5nKiMk9FuEVv42dOJXqR2uUpMKlPIh8mdClDy357pCceErn4SFFQS' -- admin123
    END
WHERE tipo_usuario IN ('aluno','professor','coordenador','administrador');