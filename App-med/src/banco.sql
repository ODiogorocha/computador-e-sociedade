CREATE DATABASE cadastro_med;

USE cadastro_med;

CREATE TABLE paciente (
    idPaciente INT AUTO_INCREMENT PRIMARY KEY,
    prioridade INT,
    fx_etaria VARCHAR(50),
    doenca VARCHAR(500)
);

CREATE TABLE medico (
    idMedico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),         -- Campo adicional para armazenar o nome do médico
    especialidade VARCHAR(100) -- Campo opcional para indicar a especialidade
);

CREATE TABLE consulta (
    idConsulta INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    hora TIME,
    paciente_idpaciente INT,
    medico_idmedico INT,
    FOREIGN KEY (paciente_idpaciente) REFERENCES paciente(idPaciente),
    FOREIGN KEY (medico_idmedico) REFERENCES medico(idMedico)
);
