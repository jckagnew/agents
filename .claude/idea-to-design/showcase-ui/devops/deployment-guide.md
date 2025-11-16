# DevOps Scaffold Deployment Guide

## Overview
This guide explains how to deploy the Software Factory generated application using Docker and Docker Compose.

## Prerequisites
- Docker Desktop or Docker Engine installed
- Docker Compose v2.0+
- 8GB+ RAM available for containers
- 20GB+ free disk space

## Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.template .env

# Edit environment variables
nano .env
```

### 2. Build and Start Services
```bash
# Build application container
docker build -t software-factory-app .

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. View Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f database
```

### 4. Access Application
- **Application**: http://localhost:3000
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Nginx**: http://localhost:80

## Service Management

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Scale Services
```bash
# Scale application to 3 instances
docker-compose up --scale app=3 -d
```

## Database Operations

### Connect to Database
```bash
docker-compose exec database psql -U postgres -d software_factory
```

### Backup Database
```bash
docker-compose exec database pg_dump -U postgres software_factory > backup.sql
```

### Restore Database
```bash
docker-compose exec -T database psql -U postgres software_factory < backup.sql
```

## Monitoring

### Health Checks
```bash
# Check application health
curl http://localhost:3000/api/health

# Check all service health
docker-compose ps
```

### Resource Usage
```bash
# View container resource usage
docker stats
```

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
lsof -i :3000
lsof -i :5432

# Kill process using port
kill -9 $(lsof -t -i:3000)
```

#### Container Build Failures
```bash
# Rebuild without cache
docker-compose build --no-cache

# Check build logs
docker-compose build app
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps database

# Check database logs
docker-compose logs database
```

### Clean Up
```bash
# Stop and remove all containers
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove all containers and images
docker-compose down --rmi all
```

## Production Deployment

### 1. Environment Configuration
```bash
# Set production environment variables
export NODE_ENV=production
export DATABASE_URL=postgresql://user:pass@prod-db:5432/app
export REDIS_URL=redis://prod-redis:6379
```

### 2. Build Production Images
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build
```

### 3. Deploy to Production
```bash
# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d
```

## Security Considerations

- Change default passwords in production
- Use secrets management for sensitive data
- Enable SSL/TLS termination
- Configure firewall rules
- Regular security updates

## Support

For issues and questions:
- Check Docker logs: `docker-compose logs`
- Review application logs: `docker-compose logs app`
- Verify environment variables: `docker-compose config`
- Check service health: `docker-compose ps`

Generated on: 2025-10-24T19:25:31.757Z
