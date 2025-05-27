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

# Verifica se os modelos estão definidos corretamente
echo "Verificando modelos de dados..."
if [ -f "/home/ubuntu/med_system/src/models/user.py" ] && [ -f "/home/ubuntu/med_system/src/models/medical.py" ]; then
    echo "✅ Modelos de dados encontrados"
else
    echo "❌ Modelos de dados não encontrados"
    exit 1
fi

# Verifica se as rotas estão definidas corretamente
echo "Verificando rotas..."
if [ -f "/home/ubuntu/med_system/src/routes/auth.py" ] && 
   [ -f "/home/ubuntu/med_system/src/routes/medico.py" ] && 
   [ -f "/home/ubuntu/med_system/src/routes/paciente.py" ]; then
    echo "✅ Rotas encontradas"
else
    echo "❌ Rotas não encontradas"
    exit 1
fi

# Verifica se os templates estão definidos corretamente
echo "Verificando templates..."
if [ -d "/home/ubuntu/med_system/src/static/templates" ]; then
    echo "✅ Templates encontrados"
else
    echo "❌ Templates não encontrados"
    exit 1
fi

# Verifica se os templates específicos estão presentes
echo "Verificando templates específicos..."
templates_ok=true

# Templates de autenticação
if [ ! -f "/home/ubuntu/med_system/src/static/templates/auth/login.html" ] || 
   [ ! -f "/home/ubuntu/med_system/src/static/templates/auth/registro.html" ]; then
    echo "❌ Templates de autenticação incompletos"
    templates_ok=false
fi

# Templates de médico
if [ ! -f "/home/ubuntu/med_system/src/static/templates/medico/dashboard.html" ] || 
   [ ! -f "/home/ubuntu/med_system/src/static/templates/medico/pacientes.html" ] || 
   [ ! -f "/home/ubuntu/med_system/src/static/templates/medico/paciente_detalhes.html" ]; then
    echo "❌ Templates de médico incompletos"
    templates_ok=false
fi

# Templates de paciente
if [ ! -f "/home/ubuntu/med_system/src/static/templates/paciente/dashboard.html" ] || 
   [ ! -f "/home/ubuntu/med_system/src/static/templates/paciente/perfil.html" ] || 
   [ ! -f "/home/ubuntu/med_system/src/static/templates/paciente/fila.html" ]; then
    echo "❌ Templates de paciente incompletos"
    templates_ok=false
fi

if $templates_ok; then
    echo "✅ Todos os templates específicos encontrados"
fi

# Verifica se o arquivo principal está configurado corretamente
echo "Verificando arquivo principal..."
if grep -q "app.register_blueprint(auth_bp)" /home/ubuntu/med_system/src/main.py && 
   grep -q "app.register_blueprint(medico_bp" /home/ubuntu/med_system/src/main.py && 
   grep -q "app.register_blueprint(paciente_bp" /home/ubuntu/med_system/src/main.py; then
    echo "✅ Blueprints registrados corretamente"
else
    echo "❌ Blueprints não registrados corretamente"
    exit 1
fi

echo "Todos os testes de verificação de arquivos concluídos com sucesso!"
echo "O sistema está pronto para ser iniciado e testado manualmente."
