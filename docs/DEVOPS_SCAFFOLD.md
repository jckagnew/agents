# 🐳 DevOps Scaffold Guide

## Overview

The DevOps Scaffold automatically generates deployment-ready infrastructure configuration for Software Factory applications. It creates Docker containers, orchestration files, environment templates, and deployment documentation.

**Status**: ✅ Production Ready
**Last Updated**: October 2024

---

## Purpose

Automates the creation of DevOps artifacts so each generated application is immediately deployable with:
- Production-ready Dockerfile
- Docker Compose orchestration
- Environment variable templates
- Deployment guides
- Health checks and monitoring

---

## Installation

### Prerequisites

**Required**:
- Docker (v20.10+)
- Docker Compose (v2.0+)
- Node.js (v18+)

**Optional**:
- Docker Buildx (for multi-platform builds)
- Kubernetes CLI (for K8s deployments)

### Setup

```bash
# Clone repository
git clone <repository-url>
cd agents

# Install dependencies
npm install

# Verify installation
npm run devops:scaffold -- --help
```

---

## Usage

### Quick Start

```bash
# Generate basic DevOps scaffold
npm run devops:scaffold

# Generate with PostgreSQL
npm run devops:scaffold:postgres

# Generate with full stack (PostgreSQL + Redis)
npm run devops:scaffold:full

# Strict mode (fail on missing env vars)
npm run devops:scaffold:strict
```

### Command Line Interface

```bash
node scripts/devops-scaffold.js [options]

Options:
  --session-dir DIR      Output directory (default: .claude/idea-to-design/devops-scaffold)
  --services LIST        Comma-separated services (postgres,redis,nginx)
  --fail-on-missing-env  Exit with error if required env vars are missing
  --help                 Show help message
```

### Examples

**Basic Application**:
```bash
node scripts/devops-scaffold.js --session-dir .claude/idea-to-design/my-app
```

**Application with Database**:
```bash
node scripts/devops-scaffold.js \
  --session-dir .claude/idea-to-design/my-app \
  --services postgres
```

**Full Stack Application**:
```bash
node scripts/devops-scaffold.js \
  --session-dir .claude/idea-to-design/my-app \
  --services postgres,redis,nginx
```

**CI/CD Mode (Strict)**:
```bash
node scripts/devops-scaffold.js \
  --session-dir .claude/idea-to-design/my-app \
  --fail-on-missing-env
```

---

## Generated Artifacts

### File Structure

```
.claude/idea-to-design/session-X/
└── devops/
    ├── Dockerfile               # Multi-stage production build
    ├── docker-compose.yml       # Service orchestration
    ├── env.example             # Environment variable template
    ├── env.default             # Default environment values
    ├── runbook.md              # Operations guide
    ├── monitoring.json         # Monitoring configuration
    └── scaffold-metadata.json  # Generation metadata
```

### Dockerfile

**Purpose**: Multi-stage production-ready container image

**Features**:
- Multi-stage build (builder → production)
- Non-root user execution
- Health checks
- Optimized layer caching
- Security best practices

**Example Output**:
```dockerfile
# Multi-stage build for Next.js application
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

### docker-compose.yml

**Purpose**: Multi-service orchestration for local development and testing

**Features**:
- Application service
- Database service (PostgreSQL)
- Cache service (Redis)
- Reverse proxy (Nginx)
- Health checks
- Volume management
- Network isolation

**Example Output**:
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    env_file:
      - .env
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=${POSTGRES_DB:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

### env.example & env.default

**Purpose**: Document and provide default environment variables

**Categories**:
- Application configuration (NODE_ENV, PORT)
- Database credentials
- Redis configuration
- API keys and secrets
- Monitoring settings
- Feature flags

**Example Output**:
```bash
# Application Configuration
NODE_ENV=production
PORT=3000

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/appdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=appdb

# Redis Configuration
REDIS_URL=redis://redis:6379

# API Keys
API_SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Monitoring
LOG_LEVEL=info
ENABLE_METRICS=true
```

### runbook.md

**Purpose**: Comprehensive operational guide for deployment and maintenance

**Sections**:
1. **Overview**: Architecture and dependencies
2. **Prerequisites**: Required tools and access
3. **Deployment**: Initial deployment and updates
4. **Startup & Shutdown**: Service management commands
5. **Backup & Restore**: Data backup procedures
6. **Monitoring**: Health checks and log viewing
7. **Incident Response**: Common issues and solutions
8. **Troubleshooting**: Debug procedures
9. **Maintenance**: Regular maintenance tasks

**Example Section**:
```markdown
## Deployment

### Initial Deployment

bash
# 1. Clone repository
git clone <repository-url>
cd <repository-name>

# 2. Copy environment file
cp devops/env.example .env

# 3. Edit environment variables
nano .env

# 4. Build and start services
docker-compose -f devops/docker-compose.yml up -d

# 5. Verify deployment
curl http://localhost:3000/health
```

### monitoring.json

**Purpose**: Define monitoring configuration for observability tools

**Features**:
- Health check endpoints
- Service dependencies
- Metrics collection
- Alert definitions
- Logging configuration

**Example Output**:
```json
{
  "application": {
    "name": "next",
    "version": "1.0.0",
    "environment": "production"
  },
  "healthChecks": [
    {
      "name": "application-health",
      "type": "http",
      "endpoint": "http://localhost:3000/health",
      "interval": "30s",
      "timeout": "10s",
      "retries": 3,
      "expectedStatus": 200
    }
  ],
  "metrics": {
    "enabled": true,
    "port": 9090,
    "endpoint": "/metrics",
    "collectors": [
      "cpu",
      "memory",
      "disk",
      "network",
      "http_requests",
      "http_response_time"
    ]
  },
  "alerts": [
    {
      "name": "high-error-rate",
      "condition": "error_rate > 5%",
      "severity": "critical",
      "notification": ["email", "slack"]
    }
  ]
}
```

---

## Application Type Detection

The scaffold automatically detects your application type and generates appropriate configurations.

### Supported Frameworks

**Next.js**:
- Multi-stage build with standalone output
- Static file optimization
- Built-in telemetry disabled
- Port 3000

**Express.js**:
- Node.js runtime
- Custom server entry point
- Middleware support
- Port 3000

**React (CRA)**:
- Build with `npm run build`
- Serve with static server
- Port 3000

**Python**:
- Python 3.11 runtime
- requirements.txt installation
- WSGI/ASGI support
- Port 8000

### Detection Logic

```javascript
// Package.json scan
if (packageJson.dependencies?.next) {
  framework = 'next';
  buildCommand = 'npm run build';
  startCommand = 'npm start';
}

// Database detection
if (packageJson.dependencies?.pg) {
  hasDatabase = true;
  envVars.push('DATABASE_URL');
}

// Redis detection
if (packageJson.dependencies?.redis) {
  hasRedis = true;
  envVars.push('REDIS_URL');
}
```

---

## Service Options

### PostgreSQL

**Image**: postgres:15-alpine
**Port**: 5432
**Use Case**: Relational database for structured data

**Environment Variables**:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=appdb
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/appdb
```

**Volume**: `postgres-data:/var/lib/postgresql/data`

**Health Check**:
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Redis

**Image**: redis:7-alpine
**Port**: 6379
**Use Case**: Caching, session storage, pub/sub

**Environment Variables**:
```bash
REDIS_URL=redis://redis:6379
```

**Volume**: `redis-data:/data`

**Health Check**:
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Nginx

**Image**: nginx:alpine
**Ports**: 80, 443
**Use Case**: Reverse proxy, SSL termination, load balancing

**Configuration**:
- Custom nginx.conf required
- SSL certificate mounting
- Upstream load balancing

---

## Environment Variable Validation

### Required Variables

The scaffold validates that critical environment variables are set before deployment.

**Core Variables**:
- `NODE_ENV`: Application environment (development, production)
- `PORT`: Application port
- `API_SECRET_KEY`: API authentication secret
- `JWT_SECRET`: JWT signing secret

**Database Variables** (if database detected):
- `DATABASE_URL`: Full database connection string
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password

**Redis Variables** (if Redis detected):
- `REDIS_URL`: Redis connection string

### Validation Modes

**Permissive Mode** (default):
```bash
npm run devops:scaffold
# Warns about missing variables but continues
```

**Strict Mode** (CI/CD):
```bash
npm run devops:scaffold:strict
# Exits with error code 1 if any required variable is missing
```

### Example Output

```
🔍 Validating environment variables...

   ✅ Found: 4 variables
      - NODE_ENV
      - PORT
      - API_SECRET_KEY
      - JWT_SECRET

   ⚠️  Missing: 2 variables
      - DATABASE_URL
      - REDIS_URL

   ℹ️  Copy env.example to .env and configure missing variables
```

---

## CI/CD Integration

### GitHub Actions

The DevOps scaffold integrates automatically into the CI/CD pipeline.

**Workflow**: `.github/workflows/ci.yml`

```yaml
devops-verification:
  runs-on: ubuntu-latest
  needs: test

  steps:
  - uses: actions/checkout@v4

  - name: Set up Node.js
    uses: actions/setup-node@v4
    with:
      node-version: 20

  - name: Install dependencies
    run: npm ci

  - name: Generate DevOps scaffold
    run: npm run devops:scaffold

  - name: Verify DevOps artifacts
    run: |
      test -f .claude/idea-to-design/devops-scaffold/Dockerfile
      test -f .claude/idea-to-design/devops-scaffold/docker-compose.yml
      test -f .claude/idea-to-design/devops-scaffold/env.example
      test -f .claude/idea-to-design/devops-scaffold/runbook.md
      test -f .claude/idea-to-design/devops-scaffold/monitoring.json

  - name: Validate Dockerfile syntax
    run: |
      docker build -f .claude/idea-to-design/devops-scaffold/Dockerfile -t validation .

  - name: Validate docker-compose syntax
    run: |
      cd .claude/idea-to-design/devops-scaffold
      docker-compose config > /dev/null

  - name: Upload DevOps artifacts
    if: always()
    uses: actions/upload-artifact@v3
    with:
      name: devops-artifacts
      path: .claude/idea-to-design/devops-scaffold/
```

**Pipeline Flow**:
1. Lint → Tests → Security → **DevOps Verification** → Build → Deploy

**Benefits**:
- Ensures deployment artifacts are always up-to-date
- Validates Docker configuration syntax
- Detects missing environment variables early
- Archives artifacts for review

---

## Deployment

### Local Development

```bash
# 1. Generate scaffold
npm run devops:scaffold

# 2. Configure environment
cp .claude/idea-to-design/devops-scaffold/env.example .env
nano .env

# 3. Start services
cd .claude/idea-to-design/devops-scaffold
docker-compose up -d

# 4. View logs
docker-compose logs -f app

# 5. Access application
open http://localhost:3000
```

### Production Deployment

```bash
# 1. Generate production scaffold
NODE_ENV=production npm run devops:scaffold

# 2. Configure production environment
cp .claude/idea-to-design/devops-scaffold/env.example .env.production
# Edit with production values

# 3. Build production image
docker build -f .claude/idea-to-design/devops-scaffold/Dockerfile -t myapp:latest .

# 4. Deploy to registry
docker tag myapp:latest registry.example.com/myapp:latest
docker push registry.example.com/myapp:latest

# 5. Deploy to production
kubectl apply -f k8s/deployment.yml
# OR
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

**AWS ECS**:
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -f .claude/idea-to-design/devops-scaffold/Dockerfile -t myapp .
docker tag myapp:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# Deploy to ECS
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

**Google Cloud Run**:
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/my-project/myapp -f .claude/idea-to-design/devops-scaffold/Dockerfile
gcloud run deploy myapp --image gcr.io/my-project/myapp --platform managed --region us-central1
```

**Azure Container Instances**:
```bash
# Build and push to ACR
az acr build --registry myregistry --image myapp:latest -f .claude/idea-to-design/devops-scaffold/Dockerfile .

# Deploy to ACI
az container create --resource-group mygroup --name myapp --image myregistry.azurecr.io/myapp:latest
```

---

## Monitoring & Observability

### Health Checks

**Application Health**:
```bash
# HTTP health check
curl http://localhost:3000/health

# Expected response
{
  "status": "ok",
  "timestamp": "2025-10-24T12:00:00.000Z",
  "uptime": 3600,
  "services": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

**Container Health**:
```bash
# Check container status
docker-compose ps

# Expected output
NAME                    STATUS
app                     Up 10 minutes (healthy)
postgres                Up 10 minutes (healthy)
redis                   Up 10 minutes (healthy)
```

### Metrics

**Prometheus Integration**:
```yaml
# monitoring.json → Prometheus config
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:9090']
```

**Grafana Dashboards**:
- CPU/Memory usage
- Request rate
- Error rate
- Response time percentiles (p50, p95, p99)
- Database connection pool

### Logging

**View Logs**:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app

# Last 100 lines
docker-compose logs --tail=100 app

# Search for errors
docker-compose logs app | grep ERROR
```

**Log Aggregation**:
```yaml
# docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## Troubleshooting

### Common Issues

**Issue**: Port already in use
```bash
# Check what's using the port
lsof -i :3000

# Kill the process
kill -9 $(lsof -t -i:3000)

# Or change port in .env
PORT=3001
```

**Issue**: Container exits immediately
```bash
# Check logs
docker-compose logs app

# Run interactively
docker-compose run --rm app sh

# Check environment
docker-compose run --rm app env
```

**Issue**: Cannot connect to database
```bash
# Check database status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U postgres -d appdb -c "SELECT 1"
```

**Issue**: Build fails
```bash
# Build without cache
docker-compose build --no-cache

# Check disk space
df -h

# Clean up Docker
docker system prune -a
```

### Debug Mode

```bash
# Enable debug logging
DEBUG=* npm run devops:scaffold

# Run container with shell access
docker-compose run --rm app sh

# Inspect container
docker inspect <container-id>

# Check resource limits
docker stats
```

---

## Best Practices

### Security

✅ **DO**:
- Use multi-stage builds to minimize image size
- Run as non-root user
- Scan images for vulnerabilities
- Use secrets management (not .env in production)
- Enable HTTPS/TLS
- Keep base images updated

❌ **DON'T**:
- Commit .env files to version control
- Use `latest` tags in production
- Run as root user
- Store secrets in Dockerfile
- Expose unnecessary ports

### Performance

✅ **DO**:
- Use layer caching effectively
- Minimize image layers
- Use .dockerignore
- Enable health checks
- Set resource limits

❌ **DON'T**:
- Install dev dependencies in production
- Copy unnecessary files
- Use large base images
- Skip health checks

### Maintenance

**Weekly**:
- Review application logs
- Check disk space
- Monitor resource usage

**Monthly**:
- Update base images
- Review security advisories
- Backup database

**Quarterly**:
- Review and update runbooks
- Test disaster recovery
- Performance optimization review

---

## FAQ

**Q: Can I customize the generated Dockerfile?**
A: Yes, the generated files are templates. Edit them as needed for your application.

**Q: How do I add custom services?**
A: Edit `docker-compose.yml` and add your service definition. Update `monitoring.json` with health checks.

**Q: What if my app needs a build tool like Webpack?**
A: The Dockerfile includes a builder stage. Add your build commands there.

**Q: How do I handle database migrations?**
A: Add a migration step to your Dockerfile or create a separate migration container.

**Q: Can I use this with Kubernetes?**
A: Yes, the Dockerfile works with any container orchestrator. For Kubernetes, create separate manifest files.

**Q: How do I handle secrets in production?**
A: Use a secrets manager like AWS Secrets Manager, HashiCorp Vault, or Kubernetes Secrets instead of .env files.

---

## Resources

### Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### Tools
- [Hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter
- [Dive](https://github.com/wagoodman/dive) - Docker image analysis
- [docker-slim](https://github.com/docker-slim/docker-slim) - Image optimization

### Tutorials
- [Docker for Beginners](https://docker-curriculum.com/)
- [Production-Ready Docker](https://productionreadydocker.com/)

---

**Last Updated**: October 2024
**Next Review**: January 2025
