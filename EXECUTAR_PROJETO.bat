@echo off
echo ========================================
echo Sales Insights AI - Execucao Automatica
echo Desenvolvido por: Joao Gabriel de Araujo Diniz
echo ========================================
echo.

echo [1/6] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.11+ em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [2/6] Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
)

echo [3/6] Ativando ambiente virtual...
call venv\Scripts\activate

echo [4/6] Instalando dependencias...
pip install -r requirements.txt

echo [5/6] Configurando ambiente...
if not exist ".env" (
    copy .env.example .env
    echo Arquivo .env criado! Configure sua chave OpenAI se necessario.
)

echo [6/6] Configurando banco de dados...
if not exist "sales.db" (
    echo Criando banco de dados...
    python -c "import sqlite3; import os; script=open('database_script_updated.sql').read() if os.path.exists('database_script_updated.sql') else ''; conn=sqlite3.connect('sales.db'); conn.executescript(script) if script else None; conn.close(); print('Banco criado!')"
)

echo.
echo ========================================
echo INICIANDO APLICACAO...
echo ========================================
echo Interface: http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Pressione Ctrl+C para parar
echo ========================================

uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload

pause

