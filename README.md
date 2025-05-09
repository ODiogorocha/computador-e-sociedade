# Workshop: Computador e Sociedade - Robótica

## 📜 HISTÓRIA

### 📌 Evolução da Computação e da Robótica
Esta seção explora os principais avanços tecnológicos e sua influência na sociedade, desde os primeiros autômatos até os robôs modernos.

### 🛠 Criação: Primeiros Autômatos e Robôs Antigos
- Análise dos primeiros autômatos mecânicos.
- Comparativo entre robôs antigos e modernos (2025).

### ⚠️ Ideias Descartadas: Medos e Tabus
- Discussão sobre distopias tecnológicas.
- Análise dos tabus associados à robótica e IA.

### 🕰 Linha do Tempo Tecnológica
| Período  | Avanço Tecnológico |
|-----------|------------------|
| Século XV | Primeiros autômatos mecânicos |
| 1950-1960 | Surgimento da Inteligência Artificial |
| 1980-1990 | Robôs industriais ganham espaço |
| 2000-2025 | IA avançada e robôs autônomos |

---

## 🔧 PARTE TÉCNICA

### 🏗 Construção: Mecânica e Física
- Tipos de motores e materiais utilizados.
- Sistemas de locomoção e manipulação.

### ⚡ Sistema Elétrico
- Sensores e atuadores.
- Microcontroladores e circuitos.

### 💻 Programação
- Linguagens de programação utilizadas.
- Sistemas operacionais aplicados.
- Introdução ao **ROS (Robot Operating System)**:
  - Nodes
  - Topics
  - Works
  - Lists

#### 🏗 Subponto: Docker Básico
- Aplicação do Docker na robótica.

#### 🖥 Simulação 3D
- Uso do **FIRA Sim** para testar robôs virtualmente.

---

## 🩺 SISTEMA DE CADASTRO MÉDICO (App)

### 📋 Visão Geral
O sistema de cadastro médico é uma aplicação Python integrada com **MySQL**, desenvolvida para gerenciar pacientes, médicos e consultas de forma estruturada.

### 📂 Funcionalidades
- Cadastro de pacientes com base em **prioridade** e **faixa etária**.
- Cadastro de médicos e consultas.
- Geração de **fila de prioridade** automática:
  - Quanto menor o número de prioridade e mais sensível a faixa etária (como crianças e idosos), maior o posicionamento do paciente na fila.
  - Impressão formatada de dados com nome do paciente, doença, médico responsável e prioridade.

### 🛠 Estrutura do App
O código está dividido em:
- `sistemas.py`: contém a lógica de conexão com o banco e inserções.
- `fila_prioridade.py`: gera e organiza a fila de pacientes com base em critérios definidos.
- `main.py`: interface de menu para interação textual com o sistema.

### 🗄 Banco de Dados
O sistema utiliza uma base de dados MySQL com as seguintes tabelas:
- `paciente(id, prioridade, fx_etaria, doenca)`
- `medico(id, nome, especialidade)`
- `consulta(id, data, hora, paciente_id, medico_id)`

---

## 🤖 INTELIGÊNCIA ARTIFICIAL

### 🔍 Diferentes Práticas
| Método | Descrição |
|---------|-------------|
| Decision Tree | Algoritmo baseado em regras para tomada de decisões. |
| A* | Algoritmo de busca heurística eficiente. |
| RRT | Planejamento de trajetória para robôs. |

#### 📊 Subponto: Deep Learning e Machine Learning
- Explicação sobre redes neurais e aprendizado de máquina.
- Relação entre IA e estatística.

---

## 🔹 Criadores
Este workshop foi desenvolvido por:
- [ODiogorocha](https://github.com/ODiogorocha)
- [WeslleyHBM](https://github.com/WeslleyHBM)
