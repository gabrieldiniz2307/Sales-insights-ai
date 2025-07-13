"""
Aplicação principal FastAPI para Sales Insights AI
Versão atualizada com LangChain conforme requisitos do teste técnico
"""
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db, create_tables
from app import models, schemas, crud

# Carrega variáveis de ambiente
load_dotenv()

# Configurações da aplicação
APP_NAME = os.getenv("APP_NAME", "Sales Insights AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Cria instância do FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API REST para análise de vendas com LangChain + RAG conforme teste técnico",
    debug=DEBUG
)

# Configuração CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cria tabelas no banco de dados na inicialização
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    create_tables()

# Rota principal - serve o frontend
@app.get("/", include_in_schema=False)
async def read_root():
    """Serve a página principal do frontend"""
    return FileResponse("frontend/index.html")

# Endpoint de saúde da API
@app.get("/health", response_model=schemas.HealthResponse)
async def health_check():
    """Verifica se a API está funcionando"""
    return schemas.HealthResponse(
        status="healthy",
        message="Sales Insights AI com LangChain está funcionando corretamente",
        timestamp=datetime.now()
    )

# Endpoint para listar produtos
@app.get("/products", response_model=List[schemas.Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos"""
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

# Endpoint para listar clientes
@app.get("/customers", response_model=List[schemas.Customer])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os clientes"""
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

# Endpoint para listar vendas
@app.get("/sales", response_model=List[schemas.Sale])
async def get_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todas as vendas"""
    sales = crud.get_sales(db, skip=skip, limit=limit)
    return sales

# Endpoint para resumo das vendas
@app.get("/sales/summary")
async def get_sales_summary(db: Session = Depends(get_db)):
    """Retorna resumo geral das vendas"""
    summary = crud.get_sales_summary(db)
    return summary

# Endpoint para top produtos (conforme requisito 2 do PDF)
@app.get("/top-products", response_model=schemas.TopProductsResponse)
async def get_top_products(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Retorna os 5 produtos mais vendidos no último mês
    Requisito 2 do teste técnico: GET /top-products
    """
    try:
        top_products = crud.get_top_products_last_month(db, limit=limit)
        
        total_sales = sum(product['total_revenue'] for product in top_products)
        
        return schemas.TopProductsResponse(
            products=top_products,
            period="último mês",
            total_sales=total_sales,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar top produtos: {str(e)}")

# Endpoint para insights de vendas (conforme requisito 1 do PDF)
@app.get("/sales-insights", response_model=schemas.SalesInsightResponse)
async def get_sales_insights(
    question: str = Query(..., description="Pergunta sobre as vendas"),
    db: Session = Depends(get_db)
):
    """
    Processa perguntas sobre vendas usando LangChain com RAG obrigatório
    Requisito 1 do teste técnico: GET /sales-insights?question={question}
    
    Implementa todos os requisitos técnicos:
    ✓ FastAPI para criar a API
    ✓ LangChain para processar perguntas
    ✓ RAG (busca direta no banco de dados)
    ✓ SQLAlchemy para consultar o banco
    ✓ Limitação de perguntas (força uso de RAG)
    """
    try:
        from app.langchain_agent_fixed import sales_langchain_agent
        
        # Processa a pergunta usando LangChain com RAG obrigatório
        result = sales_langchain_agent.process_question(question, db)
        
        return schemas.SalesInsightResponse(
            question=result['question'],
            answer=result['answer'],
            data_source=f"{result['data_source']} (via {result['method_used']})",
            timestamp=result['timestamp']
        )
    
    except Exception as e:
        # Fallback apenas em caso de erro crítico do LangChain
        return schemas.SalesInsightResponse(
            question=question,
            answer=f"❌ **Erro crítico no sistema LangChain:** {str(e)}\n\n*O sistema está configurado para usar LangChain + RAG conforme requisitos técnicos do teste.*",
            data_source="Sistema de erro (LangChain indisponível)",
            timestamp=datetime.now()
        )

# Endpoint para informações do sistema LangChain
@app.get("/system/langchain-info")
async def get_langchain_info():
    """Retorna informações sobre o sistema LangChain"""
    try:
        from app.langchain_agent_fixed import sales_langchain_agent
        return sales_langchain_agent.get_system_info()
    except Exception as e:
        return {"error": str(e), "langchain_available": False}

# Endpoint para buscar produto por ID
@app.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Busca um produto específico por ID"""
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

# Endpoint para buscar cliente por ID
@app.get("/customers/{customer_id}", response_model=schemas.Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Busca um cliente específico por ID"""
    customer = crud.get_customer(db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer

if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main_updated:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )

