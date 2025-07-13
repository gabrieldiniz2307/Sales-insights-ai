"""
Aplicação principal FastAPI para Sales Insights AI
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
    description="API REST para análise de vendas com IA usando FastAPI e LangChain",
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
        message="Sales Insights AI está funcionando corretamente",
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

# Endpoint para top produtos (implementação básica)
@app.get("/top-products", response_model=schemas.TopProductsResponse)
async def get_top_products(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Retorna os 5 produtos mais vendidos no último mês
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

# Endpoint para insights de vendas (com IA integrada)
@app.get("/sales-insights", response_model=schemas.SalesInsightResponse)
async def get_sales_insights(
    question: str = Query(..., description="Pergunta sobre as vendas"),
    db: Session = Depends(get_db)
):
    """
    Processa perguntas sobre vendas e retorna insights usando IA
    Suporta OpenAI, modelos locais e sistema baseado em regras
    """
    try:
        from app.ai_agent import sales_ai_agent
        
        # Processa a pergunta usando o agente de IA
        result = sales_ai_agent.process_question(question, db)
        
        return schemas.SalesInsightResponse(
            question=result['question'],
            answer=result['answer'],
            data_source=f"{result['data_source']} (via {result['model_used']})",
            timestamp=result['timestamp']
        )
    
    except Exception as e:
        # Fallback para implementação básica em caso de erro
        question_lower = question.lower()
        
        if "produto mais vendido" in question_lower or "mais vendido" in question_lower:
            top_products = crud.get_top_products_last_month(db, limit=1)
            if top_products:
                product = top_products[0]
                answer = f"🏆 O produto mais vendido no último mês foi **{product['name']}** (SKU: {product['sku']}) com {product['total_quantity']} unidades vendidas e receita total de R$ {product['total_revenue']:.2f}."
            else:
                answer = "❌ Não foram encontradas vendas no último mês."
        
        elif "resumo" in question_lower or "total" in question_lower:
            summary = crud.get_sales_summary(db)
            answer = f"📊 **Resumo das vendas:** {summary['total_sales']} vendas realizadas, receita total de R$ {summary['total_revenue']:.2f}, {summary['total_products']} produtos cadastrados e {summary['total_customers']} clientes."
        
        else:
            answer = f"❌ Erro ao processar pergunta com IA: {str(e)}. Tente perguntar sobre 'produto mais vendido' ou 'resumo das vendas'."
        
        return schemas.SalesInsightResponse(
            question=question,
            answer=answer,
            data_source="banco de dados SQLite (fallback)",
            timestamp=datetime.now()
        )

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
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )

