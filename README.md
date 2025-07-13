**Desenvolvido por:** João Gabriel de Araujo Diniz

Sistema inteligente de análise de vendas utilizando IA generativa com FastAPI, LangChain e OpenAI GPT.

## 🚀 Tecnologias

- **Backend:** FastAPI + SQLAlchemy
- **IA:** LangChain + OpenAI GPT
- **Banco:** SQLite
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Arquitetura:** RAG (Retrieval-Augmented Generation)

## 📋 Funcionalidades

- ✅ Análise inteligente de dados de vendas
- ✅ Chat com IA para insights de negócio
- ✅ Dashboard interativo
- ✅ API REST documentada
- ✅ Interface responsiva

## 🛠️ Instalação

```bash
# Clonar repositório
git clone https://github.com/gabrieldiniz2307/sales-insights-ai.git
cd sales-insights-ai

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco
python -c "import sqlite3; script=open('database_script_updated.sql' ).read(); conn=sqlite3.connect('sales.db'); conn.executescript(script); conn.close()"

# Executar
uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload
