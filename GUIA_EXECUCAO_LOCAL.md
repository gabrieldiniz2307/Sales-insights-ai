# GUIA DE EXECUÇÃO LOCAL - Sales Insights AI

**Desenvolvido por:** João Gabriel de Araujo Diniz

## PASSO A PASSO COMPLETO

### 1. PRÉ-REQUISITOS
Antes de começar, certifique-se de ter instalado:

- **Python 3.11 ou superior**
  - Download: https://www.python.org/downloads/
  - Durante a instalação, marque "Add Python to PATH"

- **Git** (opcional, para clonar repositório)
  - Download: https://git-scm.com/downloads

### 2. BAIXAR O PROJETO

#### Opção A: Download do ZIP
1. Baixe o arquivo `sales_insights_ai_professional.zip`
2. Extraia em uma pasta (ex: `C:\projetos\sales_insights_ai`)

#### Opção B: Git Clone
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd sales_insights_ai
```

### 3. CONFIGURAR AMBIENTE

#### 3.1 Abrir Terminal/Prompt
- **Windows:** Pressione `Win + R`, digite `cmd`, Enter
- **Mac/Linux:** Abra o Terminal

#### 3.2 Navegar até a pasta do projeto
```bash
cd C:\caminho\para\sales_insights_ai
# ou no Mac/Linux:
cd /caminho/para/sales_insights_ai
```

#### 3.3 Criar ambiente virtual
```bash
python -m venv venv
```

#### 3.4 Ativar ambiente virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Você verá `(venv)` no início da linha do terminal.

### 4. INSTALAR DEPENDÊNCIAS

```bash
pip install -r requirements.txt
```

Aguarde a instalação (pode demorar alguns minutos).

### 5. CONFIGURAR VARIÁVEIS DE AMBIENTE

#### 5.1 Copiar arquivo de configuração
```bash
copy .env.example .env
# ou no Mac/Linux:
cp .env.example .env
```

#### 5.2 Editar configurações
Abra o arquivo `.env` em um editor de texto e configure:

```env
# Configuração básica (funciona sem OpenAI)
DATABASE_URL=sqlite:///./sales.db
USE_OPENAI=False

# Para usar OpenAI (opcional)
USE_OPENAI=True
OPENAI_API_KEY=sua_chave_openai_aqui

DEBUG=True
```

### 6. CONFIGURAR BANCO DE DADOS

#### 6.1 Criar banco de dados
```bash
sqlite3 sales.db < database_script_updated.sql
```

**Se não tiver sqlite3 instalado:**
- Windows: Baixe em https://www.sqlite.org/download.html
- Mac: `brew install sqlite3`
- Linux: `sudo apt install sqlite3`

#### 6.2 Alternativa (Python)
```bash
python -c "
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
```

### 7. EXECUTAR A APLICAÇÃO

```bash
uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload
```

### 8. ACESSAR A APLICAÇÃO

Abra seu navegador e acesse:

- **Interface Principal:** http://localhost:8000
- **Documentação da API:** http://localhost:8000/docs
- **Status do Sistema:** http://localhost:8000/system-status

### 9. TESTAR FUNCIONALIDADES

#### 9.1 Via Interface Web
1. Acesse http://localhost:8000
2. Digite uma pergunta como: "Mostre um resumo das vendas"
3. Clique em "Enviar"

#### 9.2 Via API Direta
Acesse no navegador:
```
http://localhost:8000/sales-insights?question=Qual foi o produto mais vendido?
```

#### 9.3 Via Documentação Swagger
1. Acesse http://localhost:8000/docs
2. Clique em qualquer endpoint
3. Clique "Try it out"
4. Preencha os parâmetros
5. Clique "Execute"

### 10. PARAR A APLICAÇÃO

No terminal onde está rodando, pressione:
```
Ctrl + C
```

### 11. SOLUÇÃO DE PROBLEMAS

#### Erro: "Python não encontrado"
- Reinstale Python marcando "Add to PATH"
- Reinicie o terminal

#### Erro: "pip não encontrado"
```bash
python -m ensurepip --upgrade
```

#### Erro: "uvicorn não encontrado"
```bash
pip install uvicorn
```

#### Erro: "Porta 8000 em uso"
Use outra porta:
```bash
uvicorn app.main_professional:app --host 0.0.0.0 --port 8001 --reload
```
Acesse: http://localhost:8001

#### Erro: "Banco de dados não encontrado"
Certifique-se de executar o passo 6 (configurar banco).

#### Erro: "OpenAI API"
Se não tiver chave OpenAI, configure no `.env`:
```env
USE_OPENAI=False
```

### 12. DESENVOLVIMENTO

#### Para modificar o código:
1. Edite os arquivos em `app/`
2. A aplicação recarrega automaticamente (--reload)
3. Refresh no navegador para ver mudanças

#### Para adicionar dependências:
```bash
pip install nova_biblioteca
pip freeze > requirements.txt
```

### 13. COMANDOS ÚTEIS

#### Verificar se está funcionando:
```bash
curl http://localhost:8000/health
```

#### Ver logs detalhados:
```bash
uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

#### Executar testes:
```bash
pytest tests/ -v
```

### 14. ESTRUTURA DE PASTAS

```
sales_insights_ai/
├── app/                    # Código principal
│   ├── main_professional.py    # Aplicação FastAPI
│   ├── database.py             # Configuração BD
│   ├── models.py               # Modelos de dados
│   └── ...
├── frontend/               # Interface web
├── venv/                   # Ambiente virtual
├── sales.db               # Banco de dados
├── .env                   # Configurações
└── requirements.txt       # Dependências
```

---

## RESUMO RÁPIDO

```bash
# 1. Extrair projeto
# 2. Abrir terminal na pasta
cd sales_insights_ai

# 3. Criar ambiente
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 4. Instalar
pip install -r requirements.txt

# 5. Configurar
copy .env.example .env

# 6. Banco
sqlite3 sales.db < database_script_updated.sql

# 7. Executar
uvicorn app.main_professional:app --host 0.0.0.0 --port 8000 --reload

# 8. Acessar
# http://localhost:8000
```

**Desenvolvido por:** João Gabriel de Araujo Diniz  
**Sistema:** Sales Insights AI Professional Edition

