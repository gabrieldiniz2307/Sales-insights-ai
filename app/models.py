"""
Modelos de dados SQLAlchemy para o sistema de vendas
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    """
    Modelo para produtos
    """
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Numeric(10, 2))
    
    # Relacionamento com vendas
    sales = relationship("Sale", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"

class Customer(Base):
    """
    Modelo para clientes
    """
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # Relacionamento com vendas
    sales = relationship("Sale", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"

class Sale(Base):
    """
    Modelo para vendas
    """
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(DateTime, nullable=False)
    
    # Relacionamentos
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    
    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, customer_id={self.customer_id}, total_amount={self.total_amount})>"

