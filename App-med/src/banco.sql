CREATE DATABASE IF NOT EXISTS cadastro_med;
USE cadastro_med;


CREATE TABLE IF NOT EXISTS paciente (
    idPaciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,           
    prioridade INT NOT NULL,
    fx_etaria VARCHAR(50) NOT NULL,
    doenca VARCHAR(500) NOT NULL
);


CREATE TABLE IF NOT EXISTS medico (
    idMedico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS consulta (
    idConsulta INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    paciente_idpaciente INT NOT NULL,
    medico_idmedico INT NOT NULL,
    FOREIGN KEY (paciente_idpaciente) REFERENCES paciente(idPaciente),
    FOREIGN KEY (medico_idmedico) REFERENCES medico(idMedico)
);
