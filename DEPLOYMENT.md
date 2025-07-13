# Deployment Guide - Sales Insights AI

**Developed by:** João Gabriel de Araujo Diniz

## Quick Start

### Local Development
```bash
# Clone repository
git clone [repository-url]
cd sales_insights_ai

# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Initialize database
sqlite3 sales.db < database_script_updated.sql

# Run application
uvicorn app.main_professional:app --reload
```

### Production Deployment

#### Docker Deployment
```bash
# Build image
docker build -t sales-insights-ai .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key sales-insights-ai
```

#### Cloud Deployment (AWS/GCP/Azure)
```bash
# Install cloud CLI tools
# Configure credentials
# Deploy using platform-specific commands
```

## Environment Configuration

### Required Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Set to False for production

### Optional Variables
- `MAX_QUERY_COMPLEXITY`: Query size limit
- `CACHE_TIMEOUT`: Response cache duration
- `LOG_LEVEL`: Logging verbosity

## Performance Optimization

### Database Optimization
- Index frequently queried columns
- Implement connection pooling
- Use read replicas for analytics

### API Optimization
- Enable response caching
- Implement rate limiting
- Use async processing for heavy queries

### AI Model Optimization
- Configure appropriate temperature settings
- Implement response caching
- Use model-specific optimizations

## Monitoring and Logging

### Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- Usage analytics

### Infrastructure Monitoring
- Server resource usage
- Database performance
- API response times
- AI model latency

## Security Considerations

### API Security
- Input validation and sanitization
- Rate limiting implementation
- Authentication for production use
- HTTPS enforcement

### Data Security
- Database encryption
- Secure API key storage
- Access logging
- Data privacy compliance

## Troubleshooting

### Common Issues
1. **OpenAI API Errors**: Check API key and quota
2. **Database Connection**: Verify DATABASE_URL
3. **Performance Issues**: Check query complexity
4. **Memory Usage**: Monitor AI model memory

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run with verbose output
uvicorn app.main_professional:app --reload --log-level debug
```

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Database connection pooling
- Stateless application design
- Container orchestration

### Vertical Scaling
- Memory optimization for AI models
- CPU optimization for queries
- Storage optimization for data
- Network optimization for APIs

---

**Technical Contact:** João Gabriel de Araujo Diniz  
**System:** Sales Insights AI Professional Edition  
**Architecture:** FastAPI + LangChain + OpenAI GPT + RAG

