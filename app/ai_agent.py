"""
Agente de IA para processamento de perguntas sobre vendas
Suporta tanto OpenAI quanto modelos locais gratuitos
"""
import os
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

# Importações condicionais para diferentes modelos
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from app import crud
from app.database import get_db

class SalesInsightsAI:
    """
    Agente de IA para análise de vendas com suporte a múltiplos modelos
    """
    
    def __init__(self):
        self.use_local_model = os.getenv("USE_LOCAL_MODEL", "True").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
        self.temperature = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        
        # Inicializa o modelo apropriado
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Inicializa o modelo de IA apropriado"""
        if not self.use_local_model and OPENAI_AVAILABLE and self.openai_api_key:
            # Configura OpenAI
            openai.api_key = self.openai_api_key
            print("✅ Usando OpenAI GPT")
        elif TRANSFORMERS_AVAILABLE:
            try:
                # Usa modelo local mais leve para demonstração
                print("🤖 Inicializando modelo local...")
                self.model = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-small",  # Modelo mais leve
                    tokenizer="microsoft/DialoGPT-small",
                    device=-1  # CPU
                )
                print("✅ Modelo local inicializado")
            except Exception as e:
                print(f"❌ Erro ao inicializar modelo local: {e}")
                self.model = None
        else:
            print("⚠️ Nenhum modelo de IA disponível, usando respostas baseadas em regras")
    
    def _get_database_context(self, db: Session) -> str:
        """Obtém contexto do banco de dados para o modelo"""
        try:
            # Busca informações básicas do banco
            summary = crud.get_sales_summary(db)
            top_products = crud.get_top_products_last_month(db, limit=3)
            
            context = f"""
            Contexto do banco de dados de vendas:
            - Total de vendas: {summary['total_sales']}
            - Receita total: R$ {summary['total_revenue']:.2f}
            - Total de produtos: {summary['total_products']}
            - Total de clientes: {summary['total_customers']}
            
            Top 3 produtos mais vendidos no último mês:
            """
            
            for i, product in enumerate(top_products, 1):
                context += f"\n{i}. {product['name']} - {product['total_quantity']} unidades - R$ {product['total_revenue']:.2f}"
            
            return context
        except Exception as e:
            return f"Erro ao obter contexto do banco: {str(e)}"
    
    def _execute_sql_query(self, db: Session, query: str) -> List[Dict]:
        """Executa query SQL de forma segura"""
        try:
            # Lista de palavras-chave permitidas para segurança
            allowed_keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT', 'JOIN', 'COUNT', 'SUM', 'AVG']
            query_upper = query.upper()
            
            # Verifica se é uma query SELECT segura
            if not query_upper.strip().startswith('SELECT'):
                return []
            
            # Executa a query
            result = db.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
            
            # Converte para lista de dicionários
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return []
    
    def _analyze_question_intent(self, question: str) -> Dict[str, Any]:
        """Analisa a intenção da pergunta"""
        question_lower = question.lower()
        
        intent = {
            'type': 'general',
            'entities': [],
            'time_period': None,
            'metric': None
        }
        
        # Detecta tipo de pergunta
        if any(word in question_lower for word in ['mais vendido', 'top', 'melhor', 'maior']):
            intent['type'] = 'top_products'
        elif any(word in question_lower for word in ['total', 'soma', 'receita', 'faturamento']):
            intent['type'] = 'summary'
        elif any(word in question_lower for word in ['cliente', 'comprador']):
            intent['type'] = 'customer_analysis'
        elif any(word in question_lower for word in ['período', 'mês', 'semana', 'ano']):
            intent['type'] = 'time_analysis'
        
        # Detecta período de tempo
        if 'última semana' in question_lower or 'semana passada' in question_lower:
            intent['time_period'] = 'last_week'
        elif 'último mês' in question_lower or 'mês passado' in question_lower:
            intent['time_period'] = 'last_month'
        elif 'hoje' in question_lower:
            intent['time_period'] = 'today'
        
        return intent
    
    def _generate_rule_based_response(self, question: str, db: Session) -> str:
        """Gera resposta baseada em regras quando não há modelo de IA"""
        intent = self._analyze_question_intent(question)
        
        try:
            if intent['type'] == 'top_products':
                top_products = crud.get_top_products_last_month(db, limit=5)
                if top_products:
                    response = "🏆 **Produtos mais vendidos no último mês:**\n\n"
                    for i, product in enumerate(top_products, 1):
                        response += f"{i}. **{product['name']}** (SKU: {product['sku']})\n"
                        response += f"   • Quantidade vendida: {product['total_quantity']} unidades\n"
                        response += f"   • Receita: R$ {product['total_revenue']:.2f}\n"
                        response += f"   • Pedidos: {product['total_orders']}\n\n"
                    return response
                else:
                    return "Não foram encontradas vendas no período analisado."
            
            elif intent['type'] == 'summary':
                summary = crud.get_sales_summary(db)
                return f"""📊 **Resumo Geral das Vendas:**

• **Total de vendas realizadas:** {summary['total_sales']}
• **Receita total:** R$ {summary['total_revenue']:.2f}
• **Produtos cadastrados:** {summary['total_products']}
• **Clientes ativos:** {summary['total_customers']}

💡 *Dados atualizados em tempo real do banco de dados.*"""
            
            else:
                return """🤖 **Assistente de Vendas IA**

Posso ajudar você com análises sobre:
• Produtos mais vendidos
• Resumo de vendas e faturamento
• Análise de clientes
• Relatórios por período

**Exemplos de perguntas:**
- "Qual foi o produto mais vendido no último mês?"
- "Mostre um resumo das vendas"
- "Qual é a receita total?"

*Faça sua pergunta e eu analisarei os dados para você!*"""
        
        except Exception as e:
            return f"❌ Erro ao processar sua pergunta: {str(e)}"
    
    def _use_openai_model(self, question: str, context: str) -> str:
        """Usa modelo OpenAI para gerar resposta"""
        try:
            prompt = f"""
            Você é um assistente especializado em análise de vendas. 
            Responda à pergunta do usuário baseado nos dados fornecidos.
            
            Contexto dos dados:
            {context}
            
            Pergunta: {question}
            
            Responda de forma clara, objetiva e profissional em português brasileiro.
            Use emojis e formatação markdown quando apropriado.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erro ao usar OpenAI: {str(e)}"
    
    def _use_local_model(self, question: str, context: str) -> str:
        """Usa modelo local para gerar resposta"""
        try:
            if not self.model:
                return self._generate_rule_based_response(question, None)
            
            prompt = f"Pergunta sobre vendas: {question}\nContexto: {context}\nResposta:"
            
            response = self.model(
                prompt,
                max_length=200,
                num_return_sequences=1,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=50256
            )
            
            generated_text = response[0]['generated_text']
            # Extrai apenas a resposta gerada
            answer = generated_text.split("Resposta:")[-1].strip()
            
            return answer if answer else "Desculpe, não consegui gerar uma resposta adequada."
        except Exception as e:
            return f"Erro no modelo local: {str(e)}"
    
    def process_question(self, question: str, db: Session) -> Dict[str, Any]:
        """
        Processa uma pergunta sobre vendas e retorna insights
        """
        try:
            # Obtém contexto do banco de dados
            context = self._get_database_context(db)
            
            # Escolhe o método de processamento
            if not self.use_local_model and OPENAI_AVAILABLE and self.openai_api_key:
                answer = self._use_openai_model(question, context)
                model_used = "OpenAI GPT-3.5"
            elif self.model:
                answer = self._use_local_model(question, context)
                model_used = "Modelo Local (DialoGPT)"
            else:
                answer = self._generate_rule_based_response(question, db)
                model_used = "Sistema Baseado em Regras"
            
            return {
                'question': question,
                'answer': answer,
                'model_used': model_used,
                'data_source': 'Banco de dados SQLite',
                'timestamp': datetime.now(),
                'context_used': len(context) > 0
            }
        
        except Exception as e:
            return {
                'question': question,
                'answer': f"❌ Erro ao processar pergunta: {str(e)}",
                'model_used': "Sistema de Erro",
                'data_source': 'N/A',
                'timestamp': datetime.now(),
                'context_used': False
            }

# Instância global do agente
sales_ai_agent = SalesInsightsAI()

