# DevOps Setup Guide

## Overview

This guide explains how to set up the DevOps infrastructure for the Software Factory, including Docker containerization, orchestration, monitoring, and deployment automation.

## Prerequisites

- macOS, Linux, or Windows with WSL2
- 8GB+ RAM available for Docker
- 20GB+ free disk space
- Git repository with code to containerize

## Docker Installation

### 1. Install Docker Desktop

#### macOS
```bash
# Install via Homebrew (recommended)
brew install --cask docker

# Or download from Docker website
# https://www.docker.com/products/docker-desktop/
```

#### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install required packages
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

#### Windows
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Run the installer and follow the setup wizard
3. Enable WSL2 integration if using WSL2

### 2. Verify Installation

```bash
# Check Docker version
docker --version
# Expected: Docker version 20.10.x or higher

# Check Docker Compose version
docker-compose --version
# Expected: Docker Compose version 2.x.x or higher

# Test Docker installation
docker run --rm hello-world
# Expected: "Hello from Docker!" message
```

### 3. Configure Docker Resources

#### Docker Desktop (macOS/Windows)
1. Open Docker Desktop
2. Go to Settings → Resources
3. Configure:
   - **Memory**: 8GB+ (recommended)
   - **CPUs**: 4+ cores
   - **Disk**: 60GB+ available
   - **Swap**: 2GB+

#### Docker Engine (Linux)
```bash
# Check system resources
free -h
df -h

# Configure Docker daemon (optional)
sudo nano /etc/docker/daemon.json
```

Example `daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

## Environment Setup

### 1. Create Environment File

```bash
# Copy the template
cp env.template .env

# Edit with your values
nano .env
```

### 2. Required Environment Variables

#### Database Configuration
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/software_factory
DATABASE_NAME=software_factory
DATABASE_USER=postgres
DATABASE_PASSWORD=password
```

#### Authentication
```bash
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
SESSION_SECRET=your-super-secret-session-key-change-this-in-production
```

#### External Services
```bash
OPENAI_API_KEY=your-openai-api-key-here
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url-here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key-here
```

## Docker Configuration

### 1. Project Structure

```
config/devops/
├── docker/
│   ├── Dockerfile.base          # Base application Dockerfile
│   └── docker-compose.base.yml  # Base Docker Compose template
├── nginx/
│   └── nginx.conf               # Nginx reverse proxy config
├── monitoring/
│   ├── prometheus.yml           # Prometheus monitoring config
│   └── grafana/                 # Grafana dashboards and datasources
├── database/
│   └── init.sql                 # Database initialization script
└── env/
    └── env.base                 # Base environment template
```

### 2. Dockerfile Template

The base Dockerfile (`config/devops/docker/Dockerfile.base`) provides:
- **Multi-stage build**: Optimized for production
- **Security**: Non-root user execution
- **Health checks**: Application health monitoring
- **Labels**: Metadata for container management

### 3. Docker Compose Template

The base Docker Compose (`config/devops/docker/docker-compose.base.yml`) includes:
- **Application service**: Main application container
- **Database service**: PostgreSQL with persistent storage
- **Redis service**: Caching and session storage
- **Nginx service**: Reverse proxy and load balancer
- **Monitoring stack**: Prometheus and Grafana
- **Networking**: Isolated network for services

## Container Orchestration

### 1. Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

### 2. Production Environment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up --scale app=3 -d
```

### 3. Service Management

```bash
# Check service status
docker-compose ps

# Restart specific service
docker-compose restart app

# View service logs
docker-compose logs app

# Execute commands in container
docker-compose exec app npm run migrate
```

## Monitoring Setup

### 1. Prometheus Configuration

Prometheus is configured to scrape metrics from:
- Application metrics endpoint (`/api/metrics`)
- Node.js runtime metrics
- Nginx metrics
- PostgreSQL metrics
- Redis metrics

### 2. Grafana Dashboards

Pre-configured dashboards include:
- **Application Overview**: Request rates, response times, error rates
- **Infrastructure**: CPU, memory, disk usage
- **Database**: Query performance, connection pools
- **Custom Metrics**: Business-specific KPIs

### 3. Accessing Monitoring

```bash
# Prometheus (metrics)
http://localhost:9090

# Grafana (dashboards)
http://localhost:3001
# Default credentials: admin/admin
```

## Database Management

### 1. Database Initialization

The `config/devops/database/init.sql` script provides:
- **Schema creation**: Users, sessions, application tables
- **Indexes**: Performance optimization
- **Triggers**: Automatic timestamp updates
- **Sample data**: Development seed data
- **Views**: Pre-built queries for common operations

### 2. Database Operations

```bash
# Connect to database
docker-compose exec database psql -U postgres -d software_factory

# Run migrations
docker-compose exec app npm run migrate

# Backup database
docker-compose exec database pg_dump -U postgres software_factory > backup.sql

# Restore database
docker-compose exec -T database psql -U postgres software_factory < backup.sql
```

## Nginx Configuration

### 1. Reverse Proxy Setup

Nginx provides:
- **SSL termination**: HTTPS encryption
- **Load balancing**: Multiple app instances
- **Rate limiting**: API protection
- **Static file serving**: Optimized delivery
- **Security headers**: XSS, CSRF protection

### 2. SSL Certificate Setup

```bash
# Generate self-signed certificates for development
mkdir -p config/devops/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout config/devops/nginx/ssl/key.pem \
  -out config/devops/nginx/ssl/cert.pem
```

## Security Configuration

### 1. Container Security

- **Non-root user**: Applications run as non-privileged user
- **Read-only filesystem**: Immutable container filesystem
- **Resource limits**: CPU and memory constraints
- **Network isolation**: Services communicate through private network

### 2. Application Security

- **Environment variables**: Sensitive data in environment
- **Secrets management**: Docker secrets for production
- **Security headers**: Nginx security headers
- **Rate limiting**: API abuse prevention

## CI/CD Integration

### 1. GitHub Actions

The DevOps scaffold integrates with GitHub Actions for:
- **Container building**: Automated Docker image creation
- **Security scanning**: Container vulnerability scanning
- **Deployment**: Automated production deployment
- **Monitoring**: Health checks and alerting

### 2. Deployment Pipeline

```yaml
# Example GitHub Actions workflow
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t app:latest .
      - name: Deploy to production
        run: docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

#### 1. Docker Daemon Not Running
```bash
# Start Docker daemon (Linux)
sudo systemctl start docker

# Check Docker status
sudo systemctl status docker
```

#### 2. Port Conflicts
```bash
# Check port usage
lsof -i :3000
lsof -i :5432

# Kill process using port
kill -9 $(lsof -t -i:3000)
```

#### 3. Container Build Failures
```bash
# Check Docker logs
docker-compose logs app

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build --no-cache -t test .
```

#### 4. Database Connection Issues
```bash
# Check database status
docker-compose ps database

# Check database logs
docker-compose logs database

# Test database connection
docker-compose exec app npm run db:test
```

#### 5. Memory Issues
```bash
# Check container resource usage
docker stats

# Increase Docker memory limit
# (Docker Desktop: Settings → Resources → Memory)
```

### Performance Optimization

#### 1. Container Optimization
- Use multi-stage builds to reduce image size
- Leverage Docker layer caching
- Use .dockerignore to exclude unnecessary files
- Optimize base image selection

#### 2. Database Optimization
- Configure connection pooling
- Set appropriate memory limits
- Use read replicas for read-heavy workloads
- Implement proper indexing strategy

#### 3. Monitoring Optimization
- Set up proper alerting thresholds
- Use log aggregation (ELK stack)
- Implement distributed tracing
- Monitor resource utilization

## Best Practices

### 1. Container Best Practices
- Keep containers stateless
- Use specific image tags, not `latest`
- Implement health checks
- Use secrets management for sensitive data

### 2. Environment Management
- Use environment-specific configurations
- Never commit secrets to version control
- Use configuration management tools
- Implement proper secret rotation

### 3. Monitoring Best Practices
- Set up comprehensive logging
- Implement proper alerting
- Monitor both infrastructure and application metrics
- Use distributed tracing for complex applications

### 4. Security Best Practices
- Regularly update base images
- Scan containers for vulnerabilities
- Use least privilege principle
- Implement proper network segmentation

## Next Steps

1. **Customize Configuration**: Modify templates for your specific needs
2. **Set Up Monitoring**: Configure alerts and dashboards
3. **Implement CI/CD**: Set up automated deployment pipeline
4. **Security Hardening**: Implement additional security measures
5. **Performance Tuning**: Optimize based on monitoring data

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Use
