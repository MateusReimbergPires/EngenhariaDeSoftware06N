-- Apagar o banco de dados se ele já existir e criar um novo
DROP DATABASE IF EXISTS empresa;
CREATE DATABASE empresa
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_general_ci;
USE empresa;

-- Criar a tabela de gestores


CREATE TABLE gestor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100),
    entrada DATE NOT NULL,
    senha VARCHAR(255)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    gestor_id INT NOT NULL,
    FOREIGN KEY (gestor_id) REFERENCES gestor(id)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE areaAtuacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeArea VARCHAR(100) NOT NULL
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE perfil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    areaAtuacao_id INT,
    FOREIGN KEY (areaAtuacao_id) REFERENCES areaAtuacao(id)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    entrada DATE NOT NULL,
    departamento_id INT,
    perfil_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
    FOREIGN KEY (perfil_id) REFERENCES perfil(id)
) DEFAULT CHARSET=utf8mb4;



CREATE TABLE vaga (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeVaga VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    areaAtuacao_id INT NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
    FOREIGN KEY (areaAtuacao_id) REFERENCES areaAtuacao(id)
) DEFAULT CHARSET=utf8mb4;





CREATE TABLE habilidadeBase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeHabilidade VARCHAR(100)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE habilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pontuacao DECIMAL(5, 2),
    habilidadeBase_id INT,
    perfil_id INT,
    FOREIGN KEY (habilidadeBase_id) REFERENCES habilidadeBase(id),
    FOREIGN KEY (perfil_id) REFERENCES perfil(id)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE perfilDesejado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vaga_id INT,
    FOREIGN KEY (vaga_id) REFERENCES vaga(id)
) DEFAULT CHARSET=utf8mb4;
CREATE TABLE habilidadeNecessaria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pontuacao DECIMAL(5, 2) NOT NULL,
    habilidadeBase INT NOT NULL,
    perfilDesejado INT NOT NULL,
    FOREIGN KEY (habilidadeBase) REFERENCES habilidadeBase(id),
    FOREIGN KEY (perfilDesejado) REFERENCES perfilDesejado(id)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE recrutador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeRecrutador VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    senha VARCHAR(255)
) DEFAULT CHARSET=utf8mb4;
 










-- Inserir dados na tabela 'gestor'
INSERT INTO gestor (nome, email, entrada, senha) VALUES
('João Silva', 'joao.silva@email.com', '2023-05-01', 'senha123'),
('Maria Oliveira', 'maria.oliveira@email.com', '2023-05-02', 'senha123'),
('Carlos Mendes', 'carlos.mendes@email.com', '2023-05-03', 'senha123'),
('Luisa Martini', 'luisa.martini@email.com', '2023-05-04', 'senha123'),
('Fernando Costa', 'fernando.costa@email.com', '2023-05-05', 'senha123'),
('Sofia Ribeiro', 'sofia.ribeiro@email.com', '2023-05-06', 'senha123'),
('Ricardo Franco', 'ricardo.franco@email.com', '2023-05-07', 'senha123'),
('Beatriz Santos', 'beatriz.santos@email.com', '2023-05-08', 'senha123'),
('Renato Álvares', 'renato.alvares@email.com', '2023-05-09', 'senha123'),
('Cláudia Moraes', 'claudia.moraes@email.com', '2023-05-10', 'senha123');

-- Inserir dados na tabela 'departamento'
INSERT INTO departamento (nome, gestor_id) VALUES
('Desenvolvimento', 1),
('Marketing', 2),
('Recursos Humanos', 3),
('Suporte Técnico', 4),
('Financeiro', 5),
('Operações', 6),
('Logística', 7),
('Vendas', 8),
('Qualidade', 9),
('Pesquisa e Desenvolvimento', 10);

-- Inserir dados na tabela 'areaAtuacao'
INSERT INTO areaAtuacao (nomeArea) VALUES
('Tecnologia da Informação'),
('Marketing Digital'),
('Gestão de Pessoas'),
('Suporte ao Cliente'),
('Finanças'),
('Administração de Empresas'),
('Logística'),
('Vendas Técnicas'),
('Controle de Qualidade'),
('Pesquisa e Desenvolvimento');

-- Inserir dados na tabela 'perfil'
INSERT INTO perfil (areaAtuacao_id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserir dados na tabela 'funcionario'
INSERT INTO funcionario (nome, email, entrada, departamento_id, perfil_id) VALUES
('Carlos Pereira', 'carlos.pereira@email.com', '2023-05-11', 1, 1),
('Ana Beatriz', 'ana.beatriz@email.com', '2023-05-12', 2, 2),
('Roberto Silva', 'roberto.silva@email.com', '2023-05-13', 3, 3),
('Luciana Estevan', 'luciana.estevan@email.com', '2023-05-14', 4, 4),
('Marcio Gomes', 'marcio.gomes@email.com', '2023-05-15', 5, 5),
('Patricia Almeida', 'patricia.almeida@email.com', '2023-05-16', 6, 6),
('Eduardo Lima', 'eduardo.lima@email.com', '2023-05-17', 7, 7),
('Sandra Goulart', 'sandra.goulart@email.com', '2023-05-18', 8, 8),
('Thiago Nogueira', 'thiago.nogueira@email.com', '2023-05-19', 9, 9),
('Fernanda Correia', 'fernanda.correia@email.com', '2023-05-20', 10, 10);

-- Inserir dados na tabela 'vaga'
INSERT INTO vaga (nomeVaga, departamento_id, areaAtuacao_id) VALUES
('Desenvolvedor Front-end', 1, 1),
('Analista de Marketing', 2, 2),
('Especialista em RH', 3, 3),
('Técnico de Suporte', 4, 4),
('Analista Financeiro', 5, 5),
('Gerente de Operações', 6, 6),
('Coordenador de Logística', 7, 7),
('Vendedor Técnico', 8, 8),
('Inspetor de Qualidade', 9, 9),
('Pesquisador Científico', 10, 10);





-- Inserir dados na tabela 'habilidadeBase'
INSERT INTO habilidadeBase (nomeHabilidade) VALUES
('Programação'),
('SEO'),
('Recrutamento'),
('Atendimento ao Cliente'),
('Análise Financeira'),
('Gestão Estratégica'),
('Planejamento de Rota'),
('Negociação'),
('Testes de Qualidade'),
('Inovação Tecnológica');

-- Inserir dados na tabela 'habilidade'
INSERT INTO habilidade (pontuacao, habilidadeBase_id, perfil_id) VALUES
(95.00, 1, 1),
(89.50, 2, 2),
(88.00, 3, 3),
(92.00, 4, 4),
(90.00, 5, 5),
(85.00, 6, 6),
(93.00, 7, 7),
(87.00, 8, 8),
(91.00, 9, 9),
(94.00, 10, 10);

-- Inserir dados na tabela 'perfilDesejado'
INSERT INTO perfilDesejado (vaga_id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserir dados na tabela 'habilidadeNecessaria'
INSERT INTO habilidadeNecessaria (pontuacao, habilidadeBase, perfilDesejado) VALUES
(90.00, 1, 1),
(88.00, 2, 2),
(85.00, 3, 3),
(92.00, 4, 4),
(89.00, 5, 5),
(86.00, 6, 6),
(93.00, 7, 7),
(91.00, 8, 8),
(90.00, 9, 9),
(95.00, 10, 10);

-- Inserir dados na tabela 'recrutador'
INSERT INTO recrutador (nomeRecrutador, email, senha) VALUES
('Lúcia Fernandes', 'lucia.fernandes@email.com', 'senha12345'),
('Marcos Ribeiro', 'marcos.ribeiro@email.com', 'senha123456'),
('Tânia Barros', 'tania.barros@email.com', 'senha1234567'),
('Pedro Guimarães', 'pedro.guimaraes@email.com', 'senha1234568'),
('Juliana Costa', 'juliana.costa@email.com', 'senha1234569'),
('Ricardo Soares', 'ricardo.soares@email.com', 'senha1234570'),
('Helena Machado', 'helena.machado@email.com', 'senha1234571'),
('Antônio Gomes', 'antonio.gomes@email.com', 'senha1234572'),
('Isabela Freitas', 'isabela.freitas@email.com', 'senha1234573'),
('Carlos Nobrega', 'carlos.nobrega@email.com', 'senha1234574');

-- Inserir novos perfis na tabela 'perfil'
INSERT INTO perfil (areaAtuacao_id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserir novos funcionários na tabela 'funcionario'
INSERT INTO funcionario (nome, email, entrada, departamento_id, perfil_id) VALUES
('Gabriel Souza', 'gabriel.souza@email.com', '2023-06-01', 1, 11),
('Larissa Fernandes', 'larissa.fernandes@email.com', '2023-06-02', 2, 12),
('Diego Lima', 'diego.lima@email.com', '2023-06-03', 3, 13),
('Carla Nunes', 'carla.nunes@email.com', '2023-06-04', 4, 14),
('Bruno Silva', 'bruno.silva@email.com', '2023-06-05', 5, 15),
('Paula Teixeira', 'paula.teixeira@email.com', '2023-06-06', 6, 16),
('Mariana Alves', 'mariana.alves@email.com', '2023-06-07', 7, 17),
('Felipe Rocha', 'felipe.rocha@email.com', '2023-06-08', 8, 18),
('Juliana Mendes', 'juliana.mendes@email.com', '2023-06-09', 9, 19),
('Rafael Costa', 'rafael.costa@email.com', '2023-06-10', 10, 20),
('Vanessa Moura', 'vanessa.moura@email.com', '2023-06-11', 1, 21),
('Fernando Santos', 'fernando.santos@email.com', '2023-06-12', 2, 22),
('Patrícia Araújo', 'patricia.araujo@email.com', '2023-06-13', 3, 23),
('André Neves', 'andre.neves@email.com', '2023-06-14', 4, 24),
('Thaís Ribeiro', 'thais.ribeiro@email.com', '2023-06-15', 5, 25),
('Rodrigo Oliveira', 'rodrigo.oliveira@email.com', '2023-06-16', 6, 26),
('Isabela Campos', 'isabela.campos@email.com', '2023-06-17', 7, 27),
('Lucas Cardoso', 'lucas.cardoso@email.com', '2023-06-18', 8, 28),
('Daniela Vieira', 'daniela.vieira@email.com', '2023-06-19', 9, 29),
('Eduardo Pereira', 'eduardo.pereira@email.com', '2023-06-20', 10, 30);

-- Inserir habilidades para os novos funcionários
INSERT INTO habilidade (pontuacao, habilidadeBase_id, perfil_id) VALUES
(80.00, 1, 11), (75.00, 2, 11), (85.00, 3, 11),
(88.00, 4, 12), (80.00, 5, 12), (78.00, 6, 12),
(92.00, 7, 13), (85.00, 8, 13), (87.00, 9, 13),
(83.00, 10, 14), (89.00, 1, 14), (77.00, 2, 14),
(82.00, 3, 15), (76.00, 4, 15), (90.00, 5, 15),
(91.00, 6, 16), (85.00, 7, 16), (80.00, 8, 16),
(88.00, 9, 17), (84.00, 10, 17), (79.00, 1, 17),
(87.00, 2, 18), (86.00, 3, 18), (80.00, 4, 18),
(92.00, 5, 19), (78.00, 6, 19), (84.00, 7, 19),
(85.00, 8, 20), (90.00, 9, 20), (88.00, 10, 20),
(83.00, 1, 21), (89.00, 2, 21), (77.00, 3, 21),
(82.00, 4, 22), (76.00, 5, 22), (90.00, 6, 22),
(91.00, 7, 23), (85.00, 8, 23), (80.00, 9, 23),
(88.00, 10, 24), (84.00, 1, 24), (79.00, 2, 24),
(87.00, 3, 25), (86.00, 4, 25), (80.00, 5, 25),
(92.00, 6, 26), (78.00, 7, 26), (84.00, 8, 26),
(85.00, 9, 27), (90.00, 10, 27), (88.00, 1, 27),
(83.00, 2, 28), (89.00, 3, 28), (77.00, 4, 28),
(82.00, 5, 29), (76.00, 6, 29), (90.00, 7, 29),
(91.00, 8, 30), (85.00, 9, 30), (80.00, 10, 30);
