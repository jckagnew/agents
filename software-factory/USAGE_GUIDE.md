# 🏭 Software Factory - Complete Usage Guide

## 🎯 Overview

The Software Factory is an AI-powered platform that transforms ideas into monetizable software products through a systematic, automated process. This guide will walk you through every aspect of using the system.

## 🚀 Quick Start

### 1. Setup and Installation

```bash
# Clone or navigate to the software factory directory
cd /Users/jackagnew/projects/agents/software-factory

# Run the setup script
./setup.sh

# Update your environment variables
nano .env  # Add your API keys

# Start the development server
./start.sh
```

### 2. Access the System

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Factory Dashboard**: http://localhost:8000/factory/dashboard

## 📋 Core Workflows

### Workflow 1: Submit and Process an Idea

#### Step 1: Submit Your Idea
```bash
curl -X POST "http://localhost:8000/ideas/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "idea_description": "I want to create an AI-powered personal finance assistant that helps users track expenses, create budgets, and get personalized financial advice. The app should integrate with bank accounts, provide real-time spending insights, and offer investment recommendations based on user goals.",
    "owner_id": "user_123",
    "team_members": ["dev_456", "designer_789"]
  }'
```

#### Step 2: Monitor Progress
```bash
# Get project status
curl "http://localhost:8000/projects/{project_id}"

# Get project dashboard
curl "http://localhost:8000/projects/{project_id}/dashboard"
```

#### Step 3: Review Results
The system will automatically:
- ✅ Validate your idea (market research, customer analysis, technical feasibility)
- ✅ Create a prototype (code generation, database design, API endpoints)
- ✅ Set up collaboration (partner workspace, feedback collection)
- ✅ Plan monetization (pricing strategy, marketing plan, revenue projections)

### Workflow 2: Validate Ideas Only

If you want to validate ideas without creating full projects:

```bash
curl -X POST "http://localhost:8000/factory/validate-idea" \
  -H "Content-Type: application/json" \
  -d '{
    "idea_description": "Your idea here...",
    "owner_id": "user_123"
  }'
```

### Workflow 3: Create Prototypes Only

For rapid prototyping without full project setup:

```bash
curl -X POST "http://localhost:8000/factory/create-prototype" \
  -H "Content-Type: application/json" \
  -d '{
    "idea_description": "Your idea here...",
    "owner_id": "user_123"
  }'
```

## 🤖 AI Agent System

### Agent Overview

The Software Factory uses 6 specialized AI agents:

1. **Orchestrator Agent** - Master coordinator
2. **Idea Validation Agent** - Market research and feasibility
3. **Rapid Prototyping Agent** - Code generation and architecture
4. **Collaboration Agent** - Partner management and feedback
5. **Monetization Agent** - Pricing and revenue optimization
6. **Analytics Agent** - Metrics and business intelligence

### Agent Capabilities

#### Idea Validation Agent
- **Market Research**: Competitive analysis, market sizing, trends
- **Customer Discovery**: User personas, pain points, acquisition channels
- **Technical Feasibility**: Technology stack, complexity, cost estimation
- **Business Model**: Revenue models, pricing strategies, financial projections

#### Rapid Prototyping Agent
- **Template Selection**: Chooses optimal tech stack and architecture
- **Code Generation**: Automated implementation of core features
- **Database Design**: Schema creation and optimization
- **API Design**: RESTful endpoint specification
- **Deployment Planning**: Infrastructure and scaling strategy

#### Collaboration Agent
- **Partner Onboarding**: Automated partner management
- **Feedback Collection**: User feedback processing and analysis
- **Project Management**: Task tracking and milestone management
- **Communication**: Automated notifications and updates

#### Monetization Agent
- **Pricing Strategy**: Dynamic pricing optimization
- **Marketing Planning**: Campaign creation and budget allocation
- **Revenue Tracking**: Financial metrics and projections
- **Growth Optimization**: A/B testing and performance improvement

#### Analytics Agent
- **Revenue Analytics**: MRR, ARR, LTV, CAC tracking
- **User Analytics**: Engagement, retention, behavior analysis
- **Technical Analytics**: Performance, uptime, error monitoring
- **Business Intelligence**: Strategic insights and recommendations

## 📊 Monitoring and Analytics

### Factory Dashboard

Access the comprehensive factory dashboard:

```bash
curl "http://localhost:8000/factory/dashboard"
```

**Key Metrics:**
- Total projects and active projects
- Average completion time
- Revenue metrics across all projects
- Project status distribution
- Recent activity feed

### Project-Specific Analytics

For individual project metrics:

```bash
# Get project metrics
curl "http://localhost:8000/projects/{project_id}/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_123",
    "metric_types": ["revenue", "users", "technical"]
  }'

# Get project dashboard
curl "http://localhost:8000/projects/{project_id}/dashboard"
```

### Revenue Analytics

Track financial performance:

```bash
curl "http://localhost:8000/factory/analytics"
```

**Metrics Include:**
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Customer Lifetime Value (LTV)
- Customer Acquisition Cost (CAC)
- Churn rate and retention
- Revenue by project and tier

## 🔄 Collaboration Features

### Partner Management

#### Add Partners
```bash
curl -X POST "http://localhost:8000/projects/{project_id}/partners" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "role": "advisor"
    }
  }'
```

#### Get Collaboration Dashboard
```bash
curl "http://localhost:8000/projects/{project_id}/dashboard"
```

### Feedback Collection

#### Submit Feedback
```bash
curl -X POST "http://localhost:8000/projects/{project_id}/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "customer_123",
    "category": "feature_request",
    "description": "Please add dark mode support",
    "priority": "medium"
  }'
```

#### Feedback Analysis
The system automatically:
- Analyzes sentiment and themes
- Assigns priority levels
- Routes to appropriate team members
- Tracks resolution progress

## 💰 Monetization Management

### Pricing Optimization

```bash
curl -X POST "http://localhost:8000/projects/{project_id}/monetization/optimize"
```

**Optimization Features:**
- A/B testing of pricing strategies
- Conversion rate analysis
- Revenue per user optimization
- Market positioning recommendations

### Revenue Tracking

Monitor financial performance:

```bash
# Get revenue metrics
curl "http://localhost:8000/projects/{project_id}/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "proj_123",
    "metric_types": ["revenue"]
  }'
```

## 🛠️ Development and Customization

### Adding Custom Agents

1. Create a new agent file in `src/agents/`
2. Implement the required interface
3. Register with the orchestrator
4. Update the main application

Example:
```python
# src/agents/custom_agent.py
class CustomAgent:
    async def process(self, data):
        # Your custom logic here
        return result

# src/main.py
from agents.custom_agent import CustomAgent
custom_agent = CustomAgent()
```

### Extending Templates

Add new project templates:

1. Create template directory in `templates/`
2. Add template configuration
3. Update the rapid prototyping agent
4. Test with sample projects

### Custom Metrics

Add project-specific metrics:

```python
# In your agent
async def track_custom_metric(self, project_id, metric_data):
    # Your custom metric tracking
    pass
```

## 🚀 Deployment

### Local Development

```bash
# Start development server
./dev.sh

# Or with Docker
./start-docker.sh
```

### Production Deployment

1. **Environment Setup**
   ```bash
   # Update production environment
   export ENVIRONMENT=production
   export DEBUG=False
   ```

2. **Database Setup**
   ```bash
   # Run migrations
   alembic upgrade head
   ```

3. **Docker Deployment**
   ```bash
   # Build and deploy
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Monitoring Setup**
   - Configure Prometheus and Grafana
   - Set up log aggregation
   - Configure alerting

## 📈 Scaling and Performance

### Horizontal Scaling

The system supports horizontal scaling:

```yaml
# docker-compose.yml
services:
  software-factory:
    deploy:
      replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379/0
```

### Performance Optimization

1. **Caching**: Redis for session and data caching
2. **Database**: Read replicas for read-heavy workloads
3. **CDN**: Static asset delivery
4. **Load Balancing**: Distribute traffic across instances

### Monitoring

- **Application Metrics**: Response times, error rates, throughput
- **Business Metrics**: Revenue, user growth, conversion rates
- **Infrastructure Metrics**: CPU, memory, disk usage
- **Custom Metrics**: Project-specific KPIs

## 🔒 Security and Compliance

### Authentication

```bash
# Add authentication to requests
curl -H "Authorization: Bearer your_jwt_token" \
  "http://localhost:8000/projects"
```

### Data Protection

- All data encrypted in transit and at rest
- GDPR compliance features
- Audit logging for all actions
- Regular security scans

### API Security

- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration
- API key management

## 🐛 Troubleshooting

### Common Issues

1. **Agent Not Responding**
   ```bash
   # Check agent status
   curl "http://localhost:8000/health"
   ```

2. **Database Connection Issues**
   ```bash
   # Check database connectivity
   docker-compose logs postgres
   ```

3. **High Memory Usage**
   ```bash
   # Monitor resource usage
   docker stats
   ```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
export DEBUG=True
./start.sh
```

### Logs

View system logs:

```bash
# Application logs
tail -f logs/software-factory.log

# Docker logs
docker-compose logs -f software-factory
```

## 📚 API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | System information |
| `/health` | GET | Health check |
| `/ideas/submit` | POST | Submit new idea |
| `/projects` | GET | List all projects |
| `/projects/{id}` | GET | Get project details |
| `/projects/{id}/dashboard` | GET | Project dashboard |
| `/factory/dashboard` | GET | Factory dashboard |
| `/factory/analytics` | GET | Factory analytics |

### Response Formats

All responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎯 Best Practices

### Idea Submission

1. **Be Specific**: Provide detailed descriptions
2. **Include Context**: Market, users, competition
3. **Set Expectations**: Timeline, budget, resources
4. **Provide Examples**: Similar products or features

### Project Management

1. **Regular Updates**: Check progress frequently
2. **Provide Feedback**: Engage with the system
3. **Monitor Metrics**: Track key performance indicators
4. **Iterate Quickly**: Use feedback to improve

### Collaboration

1. **Clear Communication**: Be specific in feedback
2. **Timely Responses**: Respond to requests quickly
3. **Document Decisions**: Keep track of important choices
4. **Share Knowledge**: Help team members understand

## 🚀 Advanced Features

### Custom Workflows

Create custom agent workflows:

```python
# Custom workflow example
async def custom_workflow(idea):
    # Step 1: Custom validation
    validation = await custom_validator.validate(idea)
    
    # Step 2: Custom prototyping
    prototype = await custom_prototyper.create(idea, validation)
    
    # Step 3: Custom deployment
    deployment = await custom_deployer.deploy(prototype)
    
    return deployment
```

### Integration with External Services

Connect to external APIs:

```python
# Example integration
class ExternalServiceAgent:
    async def integrate_with_service(self, data):
        # Connect to external API
        response = await external_api.post(data)
        return response
```

### Machine Learning Models

Add custom ML models:

```python
# Custom ML agent
class MLAgent:
    def __init__(self):
        self.model = load_model("custom_model.pkl")
    
    async def predict(self, data):
        prediction = self.model.predict(data)
        return prediction
```

## 📞 Support and Community

### Getting Help

1. **Documentation**: Check this guide and API docs
2. **Logs**: Review system logs for errors
3. **Community**: Join our Discord/Slack
4. **Support**: Contact support team

### Contributing

1. **Fork Repository**: Create your own fork
2. **Create Branch**: Make changes in feature branch
3. **Submit PR**: Create pull request with description
4. **Code Review**: Address feedback and iterate

### Roadmap

- [ ] Mobile app for project management
- [ ] Advanced AI model integration
- [ ] Multi-language support
- [ ] Enterprise features
- [ ] API marketplace

---

**Ready to build your software empire? Let's get started! 🚀**

For more information, visit our documentation at `/docs` or contact us at support@softwarefactory.ai

