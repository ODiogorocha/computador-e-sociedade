# Documentação Completa do Sistema MedSystem

## Índice
1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Estrutura de Pastas e Arquivos](#2-estrutura-de-pastas-e-arquivos)
3. [Modelos de Dados](#3-modelos-de-dados)
4. [Sistema de Autenticação](#4-sistema-de-autenticação)
5. [Rotas e Funcionalidades](#5-rotas-e-funcionalidades)
6. [Fila de Prioridade](#6-fila-de-prioridade)
7. [Interface do Usuário](#7-interface-do-usuário)
8. [Fluxos de Usuário](#8-fluxos-de-usuário)
9. [Scripts e Funções Auxiliares](#9-scripts-e-funções-auxiliares)
10. [Configuração e Implantação](#10-configuração-e-implantação)

## 1. Visão Geral do Sistema

O MedSystem é um sistema completo de cadastro médico com gerenciamento de pacientes, médicos, consultas e fila de prioridade. O sistema foi desenvolvido utilizando Flask (Python) para o backend e HTML/CSS para o frontend, com banco de dados MySQL para armazenamento de dados.

### Principais Funcionalidades

- **Sistema de autenticação** com diferenciação entre perfis de médico e paciente
- **Cadastro completo** de médicos, pacientes, doenças e medicamentos
- **Gerenciamento de consultas** com status e observações
- **Fila de prioridade inteligente** baseada em gravidade, faixa etária e horário
- **Interfaces específicas** para médicos e pacientes
- **Visualização em tempo real** da posição na fila de atendimento

### Tecnologias Utilizadas

- **Backend**: Python 3.x com Flask
- **ORM**: SQLAlchemy
- **Banco de Dados**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Autenticação**: Sistema próprio com hash seguro de senhas

## 2. Estrutura de Pastas e Arquivos

A estrutura do projeto MedSystem é organizada da seguinte forma:

```
med_system/
├── src/                      # Diretório principal do código-fonte
│   ├── __init__.py           # Inicialização do pacote Python
│   ├── main.py               # Arquivo principal da aplicação Flask
│   ├── models/               # Modelos de dados (ORM)
│   │   ├── user.py           # Modelos de usuário (User, Medico, Paciente)
│   │   └── medical.py        # Modelos médicos (Doenca, Remedio, Consulta)
│   ├── routes/               # Rotas da aplicação (Blueprints)
│   │   ├── admin.py          # Rotas administrativas
│   │   ├── auth.py           # Rotas de autenticação
│   │   ├── medico.py         # Rotas específicas para médicos
│   │   ├── paciente.py       # Rotas específicas para pacientes
│   │   └── user.py           # Rotas gerais de usuário
│   └── static/               # Arquivos estáticos e templates
│       ├── index.html        # Página inicial
│       └── templates/        # Templates HTML
│           ├── auth/         # Templates de autenticação
│           │   ├── login.html
│           │   └── registro.html
│           ├── base.html     # Template base (layout)
│           ├── index.html    # Template da página inicial
│           ├── medico/       # Templates específicos para médicos
│           │   ├── adicionar_doenca.html
│           │   ├── adicionar_remedio.html
│           │   ├── dashboard.html
│           │   ├── paciente_detalhes.html
│           │   └── pacientes.html
│           └── paciente/     # Templates específicos para pacientes
│               ├── dashboard.html
│               ├── fila.html
│               ├── meus_remedios.html
│               ├── minhas_doencas.html
│               └── perfil.html
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação básica
└── test_system.sh            # Script de teste do sistema
```

### Descrição dos Arquivos Principais

#### Arquivos de Configuração

- **main.py**: Arquivo principal que inicializa a aplicação Flask, configura o banco de dados, registra os blueprints e define as rotas principais.
- **__init__.py**: Arquivo vazio que marca o diretório como um pacote Python.
- **requirements.txt**: Lista todas as dependências do projeto para fácil instalação.

#### Modelos de Dados

- **models/user.py**: Define os modelos de usuário, incluindo a classe base `User` e as classes derivadas `Medico` e `Paciente`.
- **models/medical.py**: Define os modelos médicos, incluindo `Doenca`, `DoencaPaciente`, `Remedio`, `RemedioPaciente` e `Consulta`.

#### Rotas (Blueprints)

- **routes/auth.py**: Gerencia autenticação, login, logout e registro de usuários.
- **routes/medico.py**: Contém todas as rotas específicas para o perfil de médico.
- **routes/paciente.py**: Contém todas as rotas específicas para o perfil de paciente.
- **routes/admin.py**: Rotas administrativas para inicialização de dados e gerenciamento do sistema.
- **routes/user.py**: Rotas gerais relacionadas a usuários.

#### Templates

- **templates/base.html**: Template base que define o layout comum para todas as páginas.
- **templates/auth/**: Templates relacionados à autenticação (login e registro).
- **templates/medico/**: Templates específicos para a interface do médico.
- **templates/paciente/**: Templates específicos para a interface do paciente.

## 3. Modelos de Dados

O MedSystem utiliza SQLAlchemy como ORM (Object-Relational Mapping) para interagir com o banco de dados. Os modelos são divididos em dois arquivos principais: `user.py` e `medical.py`.

### Modelo de Usuário (user.py)

#### Classe User

```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'medico' ou 'paciente'
    
    # Relacionamento polimórfico
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }
```

A classe `User` é a classe base para todos os usuários do sistema. Ela implementa:

- **Atributos básicos**: ID, nome de usuário, senha (hash), email e tipo de usuário
- **Métodos de senha**: `set_password()` e `check_password()` para gerenciar senhas com segurança
- **Polimorfismo**: Usa o campo `user_type` para determinar o tipo concreto de usuário

#### Classe Medico

```python
class Medico(User):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relacionamento com consultas
    consultas = db.relationship('Consulta', backref='medico', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'medico',
    }
```

A classe `Medico` estende `User` e adiciona:

- **Atributos específicos**: Nome completo, especialidade e CRM
- **Relacionamento**: Com consultas (um médico pode ter várias consultas)

#### Classe Paciente

```python
class Paciente(User):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    fx_etaria = db.Column(db.String(50), nullable=False)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)
    doencas = db.relationship('DoencaPaciente', backref='paciente', lazy=True)
    remedios = db.relationship('RemedioPaciente', backref='paciente', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'paciente',
    }
```

A classe `Paciente` estende `User` e adiciona:

- **Atributos específicos**: Nome completo, data de nascimento e faixa etária
- **Relacionamentos**: Com consultas, doenças e remédios

### Modelos Médicos (medical.py)

#### Classe Doenca

```python
class Doenca(db.Model):
    __tablename__ = 'doencas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Relacionamento com pacientes
    pacientes = db.relationship('DoencaPaciente', backref='doenca', lazy=True)
```

Representa uma doença no sistema, com:

- **Atributos**: ID, nome e descrição
- **Relacionamento**: Com pacientes através da tabela de associação `DoencaPaciente`

#### Classe DoencaPaciente

```python
class DoencaPaciente(db.Model):
    __tablename__ = 'doenca_paciente'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doenca_id = db.Column(db.Integer, db.ForeignKey('doencas.id'), nullable=False)
    data_diagnostico = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    nivel_gravidade = db.Column(db.Integer, nullable=False, default=1)  # 1-5, onde 5 é mais grave
    observacoes = db.Column(db.Text, nullable=True)
```

Tabela de associação entre pacientes e doenças, com:

- **Chaves estrangeiras**: Para paciente e doença
- **Atributos adicionais**: Data de diagnóstico, nível de gravidade (1-5) e observações

#### Classe Remedio

```python
class Remedio(db.Model):
    __tablename__ = 'remedios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Relacionamento com pacientes
    pacientes = db.relationship('RemedioPaciente', backref='remedio', lazy=True)
```

Representa um medicamento no sistema, com:

- **Atributos**: ID, nome e descrição
- **Relacionamento**: Com pacientes através da tabela de associação `RemedioPaciente`

#### Classe RemedioPaciente

```python
class RemedioPaciente(db.Model):
    __tablename__ = 'remedio_paciente'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    remedio_id = db.Column(db.Integer, db.ForeignKey('remedios.id'), nullable=False)
    dosagem = db.Column(db.String(50), nullable=False)
    frequencia = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    data_fim = db.Column(db.Date, nullable=True)
```

Tabela de associação entre pacientes e remédios, com:

- **Chaves estrangeiras**: Para paciente e remédio
- **Atributos adicionais**: Dosagem, frequência, data de início e data de fim (opcional)

#### Classe Consulta

```python
class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='agendada')  # agendada, realizada, cancelada
    prioridade = db.Column(db.Integer, nullable=False, default=3)  # 1-5, onde 1 é mais prioritário
    observacoes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def obter_fila_ordenada():
        """
        Retorna a fila de consultas ordenada por prioridade e outros fatores
        """
        return Consulta.query.join(Paciente).filter(
            Consulta.status == 'agendada',
            Consulta.data == func.current_date()
        ).order_by(
            Consulta.prioridade,
            Paciente.fx_etaria,
            Consulta.hora
        ).all()
```

Representa uma consulta médica no sistema, com:

- **Chaves estrangeiras**: Para paciente e médico
- **Atributos**: Data, hora, status, prioridade e observações
- **Timestamps**: Para controle de criação e atualização
- **Método estático**: `obter_fila_ordenada()` para implementar a lógica da fila de prioridade

## 4. Sistema de Autenticação

O sistema de autenticação do MedSystem é implementado no arquivo `routes/auth.py` e utiliza sessões Flask para gerenciar o estado de login dos usuários.

### Registro de Usuários

O processo de registro é diferenciado por tipo de usuário:

1. **Formulário comum**: Coleta username, email e senha
2. **Validações**: Verifica campos obrigatórios, senhas coincidentes e unicidade de username/email
3. **Campos específicos**:
   - **Médico**: Nome, especialidade e CRM (com validação de unicidade)
   - **Paciente**: Nome e data de nascimento (com cálculo automático da faixa etária)
4. **Segurança**: Senhas são armazenadas com hash seguro usando `werkzeug.security`

```python
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        # ... validações ...
        
        if user_type == 'medico':
            # ... validações específicas para médico ...
            new_user = Medico(
                username=username,
                email=email,
                nome=nome,
                especialidade=especialidade,
                crm=crm
            )
        else:  # paciente
            # ... cálculo de faixa etária ...
            new_user = Paciente(
                username=username,
                email=email,
                nome=nome,
                data_nascimento=data_nascimento,
                fx_etaria=fx_etaria
            )
        
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
```

### Login e Autenticação

O processo de login:

1. **Validação de credenciais**: Verifica username e senha
2. **Sessão**: Armazena `user_id`, `user_type` e `username` na sessão
3. **Redirecionamento**: Direciona para o dashboard específico do tipo de usuário

```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            session['username'] = user.username
            
            if user.user_type == 'medico':
                return redirect(url_for('medico.dashboard'))
            else:
                return redirect(url_for('paciente.dashboard'))
```

### Controle de Acesso

O sistema implementa decorators personalizados para controle de acesso:

1. **medico_required**: Garante que apenas médicos acessem determinadas rotas
2. **paciente_required**: Garante que apenas pacientes acessem determinadas rotas

```python
# Exemplo do decorator medico_required
def medico_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'medico':
            flash('Acesso restrito a médicos.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

## 5. Rotas e Funcionalidades

O sistema é organizado em blueprints Flask, cada um responsável por um conjunto específico de funcionalidades.

### Rotas de Autenticação (auth.py)

| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/login` | GET, POST | `login()` | Exibe formulário de login e processa autenticação |
| `/logout` | GET | `logout()` | Encerra a sessão do usuário |
| `/registro` | GET, POST | `registro()` | Exibe formulário de registro e processa cadastro |

### Rotas de Médico (medico.py)

| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/medico/dashboard` | GET | `dashboard()` | Exibe dashboard do médico com consultas do dia |
| `/medico/pacientes` | GET | `listar_pacientes()` | Lista todos os pacientes atendidos pelo médico |
| `/medico/paciente/<id>` | GET | `ver_paciente()` | Exibe detalhes de um paciente específico |
| `/medico/consultas` | GET | `listar_consultas()` | Lista todas as consultas do médico |
| `/medico/consulta/<id>` | GET, POST | `gerenciar_consulta()` | Gerencia status de uma consulta |
| `/medico/adicionar_doenca/<id>` | GET, POST | `adicionar_doenca()` | Adiciona doença a um paciente |
| `/medico/adicionar_remedio/<id>` | GET, POST | `adicionar_remedio()` | Adiciona remédio a um paciente |

### Rotas de Paciente (paciente.py)

| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/paciente/dashboard` | GET | `dashboard()` | Exibe dashboard do paciente com consultas e posição na fila |
| `/paciente/perfil` | GET, POST | `perfil()` | Exibe e atualiza perfil do paciente |
| `/paciente/minhas_doencas` | GET | `minhas_doencas()` | Lista doenças do paciente |
| `/paciente/adicionar_doenca` | GET, POST | `adicionar_doenca()` | Permite paciente adicionar doença |
| `/paciente/meus_remedios` | GET | `meus_remedios()` | Lista remédios do paciente |
| `/paciente/adicionar_remedio` | GET, POST | `adicionar_remedio()` | Permite paciente adicionar remédio |
| `/paciente/fila` | GET | `ver_fila()` | Exibe fila de atendimento e posição do paciente |

### Rotas Administrativas (admin.py)

| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/admin/init_data` | GET | `init_data()` | Inicializa dados básicos (doenças e remédios) |
| `/admin/usuarios` | GET | `listar_usuarios()` | Lista todos os usuários do sistema |

### Rota Principal (main.py)

| Rota | Método | Função | Descrição |
|------|--------|--------|-----------|
| `/` | GET | `index()` | Página inicial do sistema |
| `/api/fila` | GET | `get_fila()` | API para obter a fila de atendimento em formato JSON |

## 6. Fila de Prioridade

Uma das funcionalidades mais importantes do MedSystem é a fila de prioridade inteligente, implementada no modelo `Consulta` através do método estático `obter_fila_ordenada()`.

### Lógica da Fila de Prioridade

A fila é ordenada considerando três fatores principais:

1. **Prioridade da consulta**: Valor de 1 a 5, onde 1 é mais prioritário
2. **Faixa etária do paciente**: Crianças e idosos têm prioridade
3. **Horário agendado**: Em caso de empate nos critérios anteriores

```python
@staticmethod
def obter_fila_ordenada():
    """
    Retorna a fila de consultas ordenada por prioridade e outros fatores
    """
    return Consulta.query.join(Paciente).filter(
        Consulta.status == 'agendada',
        Consulta.data == func.current_date()
    ).order_by(
        Consulta.prioridade,
        Paciente.fx_etaria,
        Consulta.hora
    ).all()
```

### Visualização da Fila

A fila pode ser visualizada de duas formas:

1. **Interface Web**: Através da rota `/paciente/fila` para pacientes
2. **API JSON**: Através da rota `/api/fila` para integração com outros sistemas

```python
@app.route('/api/fila')
def get_fila():
    consultas = Consulta.obter_fila_ordenada()
    fila = []
    
    for consulta in consultas:
        fila.append({
            'id': consulta.id,
            'nome_paciente': consulta.paciente.nome,
            'nome_medico': consulta.medico.nome,
            'hora': consulta.hora.strftime('%H:%M'),
            'prioridade': consulta.prioridade,
            'doencas': [dp.doenca.nome for dp in consulta.paciente.doencas]
        })
    
    return jsonify(fila)
```

### Atualização em Tempo Real

A interface de visualização da fila para pacientes (`fila.html`) inclui um script JavaScript que atualiza a página automaticamente a cada 10 segundos, garantindo que o paciente sempre veja sua posição atual:

```javascript
// Atualiza a página a cada 10 segundos para manter a fila atualizada
setTimeout(function() {
    location.reload();
}, 10000);
```

## 7. Interface do Usuário

O MedSystem possui interfaces específicas para cada tipo de usuário, implementadas através de templates HTML.

### Templates Base

- **base.html**: Define o layout comum para todas as páginas, incluindo:
  - Cabeçalho com logo e menu de navegação
  - Sistema de mensagens flash
  - Rodapé
  - Inclusão de CSS e JavaScript

### Interface de Autenticação

- **login.html**: Formulário de login com campos para username e senha
- **registro.html**: Formulário de registro com campos comuns e específicos por tipo de usuário

### Interface do Médico

- **dashboard.html**: Visão geral das consultas do dia
- **pacientes.html**: Lista de pacientes atendidos pelo médico
- **paciente_detalhes.html**: Detalhes de um paciente específico, incluindo doenças e remédios
- **adicionar_doenca.html**: Formulário para adicionar doença a um paciente
- **adicionar_remedio.html**: Formulário para adicionar remédio a um paciente

### Interface do Paciente

- **dashboard.html**: Visão geral das consultas agendadas e posição na fila
- **perfil.html**: Visualização e edição dos dados pessoais
- **minhas_doencas.html**: Lista de doenças do paciente
- **meus_remedios.html**: Lista de remédios do paciente
- **fila.html**: Visualização da fila de atendimento e posição do paciente

## 8. Fluxos de Usuário

### Fluxo de Médico

1. **Login**: Médico acessa o sistema com suas credenciais
2. **Dashboard**: Visualiza consultas agendadas para o dia
3. **Gerenciamento de Pacientes**:
   - Lista todos os pacientes atendidos
   - Seleciona um paciente para ver detalhes
   - Visualiza histórico de doenças e remédios
   - Adiciona novas doenças ou remédios ao paciente
4. **Gerenciamento de Consultas**:
   - Marca consultas como realizadas
   - Adiciona observações
   - Cancela consultas quando necessário

### Fluxo de Paciente

1. **Login**: Paciente acessa o sistema com suas credenciais
2. **Dashboard**: Visualiza próximas consultas e posição na fila
3. **Gerenciamento de Perfil**:
   - Atualiza dados pessoais
   - Altera senha
4. **Gerenciamento de Saúde**:
   - Visualiza e adiciona doenças
   - Visualiza e adiciona remédios
5. **Acompanhamento da Fila**:
   - Verifica posição na fila de atendimento
   - Recebe atualizações em tempo real

### Fluxo de Registro

1. **Seleção de Tipo**: Usuário escolhe entre médico ou paciente
2. **Preenchimento de Dados Comuns**: Username, email e senha
3. **Preenchimento de Dados Específicos**:
   - **Médico**: Nome, especialidade e CRM
   - **Paciente**: Nome e data de nascimento
4. **Confirmação**: Sistema valida dados e cria o usuário
5. **Redirecionamento**: Usuário é direcionado para a página de login

## 9. Scripts e Funções Auxiliares

### Inicialização de Dados

O sistema inclui um script para inicialização de dados básicos, implementado na rota `/admin/init_data`:

```python
@admin_bp.route('/init_data')
def init_data():
    # Verifica se já existem dados
    if User.query.count() > 0:
        flash('Banco de dados já inicializado!', 'warning')
        return redirect(url_for('index'))
    
    # Cria doenças
    doencas = [
        Doenca(nome='Hipertensão', descricao='Pressão arterial elevada'),
        # ... outras doenças ...
    ]
    
    # Cria remédios
    remedios = [
        Remedio(nome='Losartana', descricao='Anti-hipertensivo'),
        # ... outros remédios ...
    ]
    
    # Adiciona ao banco de dados
    db.session.add_all(doencas)
    db.session.add_all(remedios)
    db.session.commit()
```

### Cálculo de Faixa Etária

Durante o registro de pacientes, o sistema calcula automaticamente a faixa etária com base na data de nascimento:

```python
# Determina a faixa etária
hoje = datetime.now().date()
idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

if idade < 12:
    fx_etaria = 'criança'
elif idade < 18:
    fx_etaria = 'jovem'
elif idade < 60:
    fx_etaria = 'adulto'
else:
    fx_etaria = 'idoso'
```

### Decorators de Controle de Acesso

O sistema implementa decorators personalizados para controle de acesso às rotas:

```python
def medico_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'medico':
            flash('Acesso restrito a médicos.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def paciente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'paciente':
            flash('Acesso restrito a pacientes.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

### Script de Teste

O sistema inclui um script de teste (`test_system.sh`) que verifica a integridade da estrutura de arquivos e configurações:

```bash
#!/bin/bash

# Script para testar o sistema MedSystem
echo "Iniciando testes do MedSystem..."

# Verifica se o banco de dados está configurado
echo "Verificando configuração do banco de dados..."
if grep -q "SQLALCHEMY_DATABASE_URI" /home/ubuntu/med_system/src/main.py; then
    echo "✅ Configuração do banco de dados encontrada"
else
    echo "❌ Configuração do banco de dados não encontrada"
    exit 1
fi

# ... outras verificações ...

echo "Todos os testes de verificação de arquivos concluídos com sucesso!"
echo "O sistema está pronto para ser iniciado e testado manualmente."
```

## 10. Configuração e Implantação

### Requisitos do Sistema

- Python 3.8+
- MySQL 5.7+
- Pip (gerenciador de pacotes Python)

### Configuração do Banco de Dados

O sistema utiliza MySQL como banco de dados, configurado no arquivo `main.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
```

A configuração pode ser personalizada através de variáveis de ambiente:
- `DB_USERNAME`: Nome de usuário do MySQL (padrão: 'root')
- `DB_PASSWORD`: Senha do MySQL (padrão: 'password')
- `DB_HOST`: Host do MySQL (padrão: 'localhost')
- `DB_PORT`: Porta do MySQL (padrão: '3306')
- `DB_NAME`: Nome do banco de dados (padrão: 'mydb')

### Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/med-system.git
   cd med-system
   ```

2. **Configure o ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**:
   - Crie um banco de dados MySQL
   - Ajuste as variáveis de ambiente ou edite diretamente o arquivo `main.py`

5. **Inicialize o banco de dados**:
   ```bash
   python src/main.py
   ```

6. **Acesse o sistema**:
   - Abra o navegador e acesse `http://localhost:5000`
   - Acesse a rota `/admin/init_data` para inicializar dados básicos
   - Registre-se como médico ou paciente para começar a usar

### Considerações de Segurança

- **Senhas**: Armazenadas com hash seguro usando `werkzeug.security`
- **Controle de Acesso**: Implementado através de decorators personalizados
- **Validação de Dados**: Implementada em todas as rotas de formulário
- **Proteção contra CSRF**: Implementada nativamente pelo Flask

### Ambiente de Produção

Para implantação em ambiente de produção, recomenda-se:

1. **Servidor Web**: Utilizar Gunicorn ou uWSGI como servidor WSGI
2. **Proxy Reverso**: Configurar Nginx ou Apache como proxy reverso
3. **Variáveis de Ambiente**: Configurar todas as variáveis sensíveis como variáveis de ambiente
4. **Debug**: Desativar o modo debug (`app.run(debug=False)`)
5. **Secret Key**: Configurar uma chave secreta forte e persistente

```python
# Exemplo de configuração para produção
import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['DEBUG'] = False
```

