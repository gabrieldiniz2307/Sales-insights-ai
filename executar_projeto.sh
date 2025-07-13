#!/bin/bash

echo "========================================"
echo "Sales Insights AI - Execução Automática"
echo "Desenvolvido por: João Gabriel de Araujo Diniz"
echo "========================================"
echo

echo "[1/6] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python não encontrado!"
    echo "Instale Python 3.11+ em: https://www.python.org/downloads/"
    exit 1
fi
python3 --version

echo "[2/6] Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "[3/6] Ativando ambiente virtual..."
source venv/bin/activate

echo "[4/6] Instalando dependências..."
pip install -r requirements.txt

echo "[5/6] Configurando ambiente..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Arquivo .env criado! Configure sua chave OpenAI se necessário."
fi

echo "[6/6] Configurando banco de dados..."
if [ ! -f "sales.db" ]; then
    echo "Criando banco de dados..."
    if command -v sqlite3 &> /dev/null; then
        sqlite3 sales.db < database_script_updated.sql
    else
        python3 -c "
import sqlite3
import os
if os.path.exists('database_script_updated.sql'):
    with open('database_script_updated.sql', 'r') as f:
        script = f.read()
    conn = sqlite3.connect('sales.db')
    conn.executescript(script)
    conn.close()
    print('Banco criado com sucesso!')
"
    fi
fi

echo
echo "========================================"
echo "INICIANDO APLICAÇÃO..."
echo "========================================"
echo "Interface: http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo
echo "Pressione Ctrl+C para parar"
echo "========================================"

uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload

