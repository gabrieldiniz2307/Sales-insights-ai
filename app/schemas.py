"""
Schemas Pydantic para validação de dados da API
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Schemas para Product
class ProductBase(BaseModel):
    sku: str
    name: str
    category: Optional[str] = None
    price: Optional[Decimal] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Customer
class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas para Sale
class SaleBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    total_amount: Decimal
    sale_date: datetime

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    product: Optional[Product] = None
    customer: Optional[Customer] = None
    
    class Config:
        from_attributes = True

# Schemas para respostas da API
class SalesInsightResponse(BaseModel):
    question: str
    answer: str
    data_source: str
    timestamp: datetime

class TopProductsResponse(BaseModel):
    products: List[dict]
    period: str
    total_sales: Decimal
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime

