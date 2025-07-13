"""
Operações CRUD (Create, Read, Update, Delete) para o banco de dados
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from app import models, schemas

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Busca um produto por ID"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str) -> Optional[models.Product]:
    """Busca um produto por SKU"""
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """Lista produtos com paginação"""
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Busca um cliente por ID"""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str) -> Optional[models.Customer]:
    """Busca um cliente por email"""
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    """Lista clientes com paginação"""
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_sales(db: Session, skip: int = 0, limit: int = 100) -> List[models.Sale]:
    """Lista vendas com paginação"""
    return db.query(models.Sale).offset(skip).limit(limit).all()

def get_sales_by_date_range(db: Session, start_date: datetime, end_date: datetime) -> List[models.Sale]:
    """Busca vendas por período"""
    return db.query(models.Sale).filter(
        and_(models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date)
    ).all()

def get_top_products_last_month(db: Session, limit: int = 5) -> List[dict]:
    """
    Retorna os produtos mais vendidos no último mês
    """
    # Calcula data de um mês atrás
    one_month_ago = datetime.now() - timedelta(days=30)
    
    # Query para produtos mais vendidos
    result = db.query(
        models.Product.id,
        models.Product.name,
        models.Product.sku,
        models.Product.category,
        models.Product.price,
        func.sum(models.Sale.quantity).label('total_quantity'),
        func.sum(models.Sale.total_amount).label('total_revenue'),
        func.count(models.Sale.id).label('total_orders')
    ).join(
        models.Sale, models.Product.id == models.Sale.product_id
    ).filter(
        models.Sale.sale_date >= one_month_ago
    ).group_by(
        models.Product.id
    ).order_by(
        desc('total_quantity')
    ).limit(limit).all()
    
    # Converte resultado para lista de dicionários
    top_products = []
    for row in result:
        top_products.append({
            'id': row.id,
            'name': row.name,
            'sku': row.sku,
            'category': row.category,
            'price': float(row.price) if row.price else 0,
            'total_quantity': row.total_quantity,
            'total_revenue': float(row.total_revenue),
            'total_orders': row.total_orders
        })
    
    return top_products

def get_sales_summary(db: Session) -> dict:
    """
    Retorna resumo geral das vendas
    """
    total_sales = db.query(func.count(models.Sale.id)).scalar()
    total_revenue = db.query(func.sum(models.Sale.total_amount)).scalar()
    total_products = db.query(func.count(models.Product.id)).scalar()
    total_customers = db.query(func.count(models.Customer.id)).scalar()
    
    return {
        'total_sales': total_sales or 0,
        'total_revenue': float(total_revenue) if total_revenue else 0,
        'total_products': total_products or 0,
        'total_customers': total_customers or 0
    }

def search_sales_by_product_name(db: Session, product_name: str) -> List[models.Sale]:
    """
    Busca vendas por nome do produto
    """
    return db.query(models.Sale).join(
        models.Product, models.Sale.product_id == models.Product.id
    ).filter(
        models.Product.name.ilike(f"%{product_name}%")
    ).all()

def get_sales_by_customer_name(db: Session, customer_name: str) -> List[models.Sale]:
    """
    Busca vendas por nome do cliente
    """
    return db.query(models.Sale).join(
        models.Customer, models.Sale.customer_id == models.Customer.id
    ).filter(
        models.Customer.name.ilike(f"%{customer_name}%")
    ).all()

