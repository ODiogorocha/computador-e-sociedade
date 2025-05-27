# MedSystem - Sistema de Cadastro Médico

## Visão Geral

O MedSystem é um sistema completo de cadastro médico com gerenciamento de pacientes, médicos, consultas e fila de prioridade. O sistema permite dois tipos de perfis de usuário:

1. **Médicos**: Podem visualizar e gerenciar pacientes, doenças, prioridades, remédios e cadastros.
2. **Pacientes**: Podem atualizar seus dados pessoais, registrar doenças e remédios, além de visualizar sua posição na fila de atendimento.

## Funcionalidades Principais

### Para Médicos
- Dashboard com visão geral das consultas do dia
- Gerenciamento de pacientes (visualização de detalhes, histórico)
- Registro de doenças e medicamentos para pacientes
- Visualização e gerenciamento da fila de atendimento
- Atualização de status de consultas

### Para Pacientes
- Dashboard personalizado com próximas consultas
- Visualização da posição na fila de atendimento
- Registro e gerenciamento de doenças e medicamentos
- Atualização de dados pessoais

### Sistema de Fila de Prioridade
- Ordenação automática baseada em:
  - Nível de prioridade da consulta
  - Faixa etária do paciente (crianças e idosos têm prioridade)
  - Horário agendado da consulta

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Banco de Dados**: MySQL
- **Autenticação**: Sistema próprio com diferenciação de perfis

## Instalação e Configuração

### Requisitos
- Python 3.8+
- MySQL
- Pip

### Passos para Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/med-system.git
cd med-system
```

2. Configure o ambiente virtual:
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Configure o banco de dados:
   - Crie um banco de dados MySQL
   - Atualize as configurações de conexão em `src/main.py`

5. Inicialize o banco de dados:
```
python src/main.py
```

6. Acesse o sistema:
   - Abra o navegador e acesse `http://localhost:5000`
   - Registre-se como médico ou paciente para começar a usar

## Estrutura do Projeto

```
med_system/
├── src/
│   ├── models/         # Modelos de dados
│   │   ├── user.py     # Modelos de usuário (médico, paciente)
│   │   └── medical.py  # Modelos médicos (doenças, remédios, consultas)
│   ├── routes/         # Rotas da aplicação
│   │   ├── auth.py     # Autenticação
│   │   ├── medico.py   # Funcionalidades do médico
│   │   ├── paciente.py # Funcionalidades do paciente
│   │   └── admin.py    # Funcionalidades administrativas
│   ├── static/         # Arquivos estáticos
│   │   └── templates/  # Templates HTML
│   └── main.py         # Arquivo principal da aplicação
├── requirements.txt    # Dependências do projeto
└── test_system.sh      # Script de teste do sistema
```

## Uso do Sistema

### Registro e Login
1. Acesse a página inicial e clique em "Registrar-se"
2. Escolha o tipo de perfil (médico ou paciente)
3. Preencha os dados solicitados e crie sua conta
4. Faça login com suas credenciais

### Para Médicos
1. Acesse o dashboard para ver as consultas do dia
2. Navegue até "Pacientes" para gerenciar seus pacientes
3. Clique em um paciente para ver detalhes, adicionar doenças ou remédios
4. Gerencie consultas e atualize seus status

### Para Pacientes
1. Acesse o dashboard para ver suas próximas consultas
2. Verifique sua posição na fila de atendimento
3. Adicione ou atualize suas doenças e medicamentos
4. Mantenha seu perfil atualizado

## Melhorias Implementadas

O sistema foi completamente redesenhado a partir do código original, com as seguintes melhorias:

1. **Sistema de autenticação robusto** com diferenciação de perfis
2. **Interface responsiva e moderna** utilizando Tailwind CSS
3. **Lógica de fila de prioridade aprimorada** considerando múltiplos fatores
4. **Gerenciamento completo de doenças e medicamentos**
5. **Visualização em tempo real da fila de atendimento**
6. **Dashboard personalizado** para cada tipo de usuário

## Considerações de Segurança

- Senhas armazenadas com hash seguro
- Verificação de permissões em todas as rotas
- Proteção contra acesso não autorizado a dados de pacientes
- Sessões seguras para autenticação

