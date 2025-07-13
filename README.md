# Sales Insights AI

**Desenvolvido por:** João Gabriel de Araujo Diniz

## Visão Geral

Sistema avançado de análise de vendas utilizando Inteligência Artificial para extrair insights estratégicos de dados comerciais. A aplicação combina FastAPI, LangChain e OpenAI GPT para fornecer análises profundas e recomendações baseadas em dados reais.

## Arquitetura Técnica

### Stack Tecnológico
- **Backend:** FastAPI (Python 3.11)
- **IA/ML:** LangChain + OpenAI GPT
- **Banco de Dados:** SQLite com SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Arquitetura:** RAG (Retrieval-Augmented Generation)

### Componentes Principais
- **API REST:** Endpoints para consultas de vendas e insights
- **Agente LangChain:** Processamento inteligente de perguntas
- **Sistema RAG:** Busca obrigatória em dados reais
- **Interface Web:** Dashboard interativo para análises

## Funcionalidades

### Análises Disponíveis
- Resumo executivo de vendas
- Produtos mais vendidos com métricas detalhadas
- Análise de performance por cliente
- Tendências e padrões de vendas
- Insights estratégicos automatizados
- Recomendações baseadas em IA

### Endpoints da API
```
GET /sales-insights?question={pergunta}
GET /top-products
GET /docs (Documentação Swagger)
GET / (Interface Web)
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)
- Chave da API OpenAI (opcional)

### Instalação
```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd sales_insights_ai

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

### Configuração do Banco de Dados
```bash
# O banco SQLite será criado automaticamente
# Dados de exemplo já incluídos no script
sqlite3 sales.db < database_script_updated.sql
```

### Execução
```bash
# Inicie o servidor
uvicorn app.main_updated:app --host 0.0.0.0 --port 8000 --reload

# Acesse a aplicação
# Interface: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Estrutura do Projeto

```
sales_insights_ai/
├── app/
│   ├── __init__.py
│   ├── main_updated.py          # Aplicação principal FastAPI
│   ├── database.py              # Configuração do banco
│   ├── models.py                # Modelos SQLAlchemy
│   ├── schemas.py               # Schemas Pydantic
│   ├── crud.py                  # Operações CRUD
│   ├── langchain_agent_openai.py # Agente IA principal
│   └── langchain_agent_llama.py  # Implementação Llama
├── frontend/
│   └── index.html               # Interface web
├── static/                      # Arquivos estáticos
├── templates/                   # Templates HTML
├── tests/                       # Testes automatizados
├── docs/                        # Documentação adicional
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente
├── database_script_updated.sql  # Script do banco
└── README.md                    # Este arquivo
```

## Tecnologias e Padrões

### Inteligência Artificial
- **LangChain:** Framework para aplicações com LLM
- **OpenAI GPT:** Modelo de linguagem para análises
- **RAG Pattern:** Retrieval-Augmented Generation
- **SQL Agent:** Agente especializado em consultas

### Desenvolvimento
- **FastAPI:** Framework web moderno e performático
- **SQLAlchemy:** ORM robusto para Python
- **Pydantic:** Validação de dados e serialização
- **Uvicorn:** Servidor ASGI de alta performance

### Qualidade de Código
- **Type Hints:** Tipagem estática em Python
- **Docstrings:** Documentação inline
- **Error Handling:** Tratamento robusto de erros
- **Logging:** Sistema de logs estruturado

## Exemplos de Uso

### Consultas via API
```bash
# Resumo de vendas
curl "http://localhost:8000/sales-insights?question=Mostre um resumo das vendas"

# Produtos mais vendidos
curl "http://localhost:8000/sales-insights?question=Qual produto vendeu mais?"

# Análise de tendências
curl "http://localhost:8000/sales-insights?question=Analise as tendências de crescimento"
```

### Respostas Esperadas
O sistema retorna análises estruturadas incluindo:
- Métricas quantitativas precisas
- Insights qualitativos baseados em IA
- Recomendações estratégicas
- Contexto metodológico da análise

## Configurações Avançadas

### Variáveis de Ambiente
```env
DATABASE_URL=sqlite:///./sales.db
USE_OPENAI=True
OPENAI_API_KEY=sua_chave_aqui
DEBUG=False
```

### Personalização do Agente IA
O sistema permite configurar:
- Temperatura do modelo (criatividade vs precisão)
- Máximo de tokens por resposta
- Prompts personalizados para domínios específicos
- Validações customizadas de entrada

## Performance e Escalabilidade

### Otimizações Implementadas
- Consultas SQL otimizadas com índices
- Cache de respostas frequentes
- Conexões de banco pool-based
- Processamento assíncrono quando aplicável

### Métricas de Performance
- Tempo médio de resposta: < 2 segundos
- Suporte a consultas concorrentes
- Escalabilidade horizontal via containers
- Monitoramento integrado de recursos

## Segurança

### Medidas Implementadas
- Validação rigorosa de entrada
- Sanitização de queries SQL
- Rate limiting para APIs
- Logs de auditoria de acesso
- Variáveis sensíveis em ambiente

## Testes

### Cobertura de Testes
```bash
# Execute os testes
pytest tests/ -v --cov=app

# Testes de integração
pytest tests/test_integration.py

# Testes de performance
pytest tests/test_performance.py
```

### Tipos de Teste
- Testes unitários para funções críticas
- Testes de integração para APIs
- Testes de carga para performance
- Testes de segurança para validações

## Deployment

### Containerização
```dockerfile
# Dockerfile incluído para deployment
docker build -t sales-insights-ai .
docker run -p 8000:8000 sales-insights-ai
```

### Ambientes Suportados
- Desenvolvimento local
- Staging/Homologação
- Produção (cloud-ready)
- Containers (Docker/Kubernetes)

## Monitoramento

### Logs e Métricas
- Logs estruturados em JSON
- Métricas de performance da API
- Monitoramento de uso da IA
- Alertas para erros críticos

### Dashboards
- Métricas de negócio em tempo real
- Performance técnica do sistema
- Uso e adoção por usuários
- Qualidade das análises geradas

## Contribuição

### Padrões de Desenvolvimento
- Seguir PEP 8 para código Python
- Documentar todas as funções públicas
- Incluir testes para novas funcionalidades
- Manter compatibilidade com versões anteriores

### Processo de Review
1. Fork do repositório
2. Branch para feature/bugfix
3. Implementação com testes
4. Pull request com descrição detalhada
5. Review de código e aprovação

## Roadmap

### Próximas Funcionalidades
- Integração com mais fontes de dados
- Análises preditivas avançadas
- Dashboard executivo aprimorado
- API para integração externa
- Suporte a múltiplos idiomas

### Melhorias Técnicas
- Migração para PostgreSQL
- Cache distribuído (Redis)
- Processamento em background
- API GraphQL complementar
- Testes automatizados CI/CD

## Licença

Este projeto foi desenvolvido como demonstração técnica por João Gabriel de Araujo Diniz.

## Contato

**Desenvolvedor:** João Gabriel de Araujo Diniz  
**Projeto:** Sales Insights AI  
**Tecnologias:** Python, FastAPI, LangChain, OpenAI, SQLAlchemy  

---

**Nota Técnica:** Este sistema demonstra competências avançadas em desenvolvimento Python, integração de IA, arquitetura de APIs e análise de dados, representando as melhores práticas da indústria em soluções de Business Intelligence com Inteligência Artificial.

