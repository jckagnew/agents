#!/usr/bin/env node

/**
 * DevOps Scaffold Generator
 * Generates Docker configuration and infrastructure setup for Software Factory applications
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  outputDir: '.claude/idea-to-design/devops-scaffold',
  templatesDir: 'config/devops',
  sessionId: process.env.SESSION_ID || 'devops-scaffold-' + Date.now()
};

// Ensure output directory exists
function ensureOutputDir() {
  const outputPath = path.join(process.cwd(), CONFIG.outputDir);
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
    console.log(`✅ Created output directory: ${outputPath}`);
  }
}

// Copy template files
function copyTemplates() {
  const templates = [
    'docker/Dockerfile.base',
    'docker/docker-compose.base.yml',
    'nginx/nginx.conf',
    'monitoring/prometheus.yml',
    'database/init.sql',
    'env/env.base'
  ];

  templates.forEach(template => {
    const sourcePath = path.join(CONFIG.templatesDir, template);
    const targetPath = path.join(CONFIG.outputDir, path.basename(template));
    
    if (fs.existsSync(sourcePath)) {
      fs.copyFileSync(sourcePath, targetPath);
      console.log(`✅ Copied ${template} → ${path.basename(template)}`);
    } else {
      console.warn(`⚠️  Template not found: ${sourcePath}`);
    }
  });
}

// Generate Dockerfile
function generateDockerfile() {
  const dockerfileContent = `# Software Factory Generated Dockerfile
# Generated on: ${new Date().toISOString()}

FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY src/ ./src/
COPY public/ ./public/

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Create app user
RUN addgroup -g 1001 -S nodejs && \\
    adduser -S nextjs -u 1001

WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./

# Copy additional files
COPY --chown=nextjs:nodejs public/ ./public/

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]

# Labels
LABEL maintainer="Software Factory <dev@softwarefactory.com>"
LABEL version="1.0.0"
LABEL description="Software Factory generated application"
LABEL generated="${new Date().toISOString()}"
`;

  const dockerfilePath = path.join(CONFIG.outputDir, 'Dockerfile');
  fs.writeFileSync(dockerfilePath, dockerfileContent);
  console.log('✅ Generated Dockerfile');
}

// Generate docker-compose.yml
function generateDockerCompose() {
  const composeContent = `# Software Factory Generated Docker Compose
# Generated on: ${new Date().toISOString()}

version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: software-factory-app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    env_file:
      - .env
    depends_on:
      - database
      - redis
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  database:
    image: postgres:15-alpine
    container_name: software-factory-db
    environment:
      - POSTGRES_DB=\${DATABASE_NAME:-software_factory}
      - POSTGRES_USER=\${DATABASE_USER:-postgres}
      - POSTGRES_PASSWORD=\${DATABASE_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: software-factory-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: software-factory-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  app-network:
    driver: bridge
`;

  const composePath = path.join(CONFIG.outputDir, 'docker-compose.yml');
  fs.writeFileSync(composePath, composeContent);
  console.log('✅ Generated docker-compose.yml');
}

// Generate .env template
function generateEnvTemplate() {
  const envContent = `# Software Factory Environment Template
# Generated on: ${new Date().toISOString()}
# Copy this file to .env and fill in your values

# Application Configuration
NODE_ENV=development
PORT=3000
HOST=0.0.0.0

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/software_factory
DATABASE_NAME=software_factory
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d
SESSION_SECRET=your-super-secret-session-key-change-this-in-production

# API Configuration
API_BASE_URL=http://localhost:3000
API_VERSION=v1
CORS_ORIGIN=http://localhost:3000

# External Services
OPENAI_API_KEY=your-openai-api-key-here
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url-here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key-here
HF_TOKEN=your-huggingface-token-here

# Security Configuration
BCRYPT_ROUNDS=12
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Monitoring Configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
GRAFANA_PASSWORD=admin

# Logging Configuration
LOG_LEVEL=info
LOG_FORMAT=combined
LOG_FILE=logs/app.log

# Development Configuration
DEBUG=true
HOT_RELOAD=true
MOCK_EXTERNAL_SERVICES=false
`;

  const envPath = path.join(CONFIG.outputDir, '.env.template');
  fs.writeFileSync(envPath, envContent);
  console.log('✅ Generated .env.template');
}

// Generate deployment guide
function generateDeploymentGuide() {
  const guideContent = `# DevOps Scaffold Deployment Guide

## Overview
This guide explains how to deploy the Software Factory generated application using Docker and Docker Compose.

## Prerequisites
- Docker Desktop or Docker Engine installed
- Docker Compose v2.0+
- 8GB+ RAM available for containers
- 20GB+ free disk space

## Quick Start

### 1. Environment Setup
\`\`\`bash
# Copy environment template
cp .env.template .env

# Edit environment variables
nano .env
\`\`\`

### 2. Build and Start Services
\`\`\`bash
# Build application container
docker build -t software-factory-app .

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
\`\`\`

### 3. View Logs
\`\`\`bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f database
\`\`\`

### 4. Access Application
- **Application**: http://localhost:3000
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Nginx**: http://localhost:80

## Service Management

### Start Services
\`\`\`bash
docker-compose up -d
\`\`\`

### Stop Services
\`\`\`bash
docker-compose down
\`\`\`

### Restart Services
\`\`\`bash
docker-compose restart
\`\`\`

### Scale Services
\`\`\`bash
# Scale application to 3 instances
docker-compose up --scale app=3 -d
\`\`\`

## Database Operations

### Connect to Database
\`\`\`bash
docker-compose exec database psql -U postgres -d software_factory
\`\`\`

### Backup Database
\`\`\`bash
docker-compose exec database pg_dump -U postgres software_factory > backup.sql
\`\`\`

### Restore Database
\`\`\`bash
docker-compose exec -T database psql -U postgres software_factory < backup.sql
\`\`\`

## Monitoring

### Health Checks
\`\`\`bash
# Check application health
curl http://localhost:3000/api/health

# Check all service health
docker-compose ps
\`\`\`

### Resource Usage
\`\`\`bash
# View container resource usage
docker stats
\`\`\`

## Troubleshooting

### Common Issues

#### Port Conflicts
\`\`\`bash
# Check port usage
lsof -i :3000
lsof -i :5432

# Kill process using port
kill -9 $(lsof -t -i:3000)
\`\`\`

#### Container Build Failures
\`\`\`bash
# Rebuild without cache
docker-compose build --no-cache

# Check build logs
docker-compose build app
\`\`\`

#### Database Connection Issues
\`\`\`bash
# Check database status
docker-compose ps database

# Check database logs
docker-compose logs database
\`\`\`

### Clean Up
\`\`\`bash
# Stop and remove all containers
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove all containers and images
docker-compose down --rmi all
\`\`\`

## Production Deployment

### 1. Environment Configuration
\`\`\`bash
# Set production environment variables
export NODE_ENV=production
export DATABASE_URL=postgresql://user:pass@prod-db:5432/app
export REDIS_URL=redis://prod-redis:6379
\`\`\`

### 2. Build Production Images
\`\`\`bash
# Build production images
docker-compose -f docker-compose.prod.yml build
\`\`\`

### 3. Deploy to Production
\`\`\`bash
# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d
\`\`\`

## Security Considerations

- Change default passwords in production
- Use secrets management for sensitive data
- Enable SSL/TLS termination
- Configure firewall rules
- Regular security updates

## Support

For issues and questions:
- Check Docker logs: \`docker-compose logs\`
- Review application logs: \`docker-compose logs app\`
- Verify environment variables: \`docker-compose config\`
- Check service health: \`docker-compose ps\`

Generated on: ${new Date().toISOString()}
`;

  const guidePath = path.join(CONFIG.outputDir, 'deployment-guide.md');
  fs.writeFileSync(guidePath, guideContent);
  console.log('✅ Generated deployment-guide.md');
}

// Main execution
function main() {
  console.log('🐳 DevOps Scaffold Generator');
  console.log('============================');
  
  try {
    ensureOutputDir();
    copyTemplates();
    generateDockerfile();
    generateDockerCompose();
    generateEnvTemplate();
    generateDeploymentGuide();
    
    // TODO: Integrate with Future-Feature Parking system
    // This will help identify infrastructure requirements for parked features
    console.log('\n📝 TODO: Integrate with Future-Feature Parking system');
    console.log('   - Analyze parked features for infrastructure needs');
    console.log('   - Generate service configurations based on feature requirements');
    console.log('   - Update docker-compose.yml with feature-specific services');
    
    console.log('\n✅ DevOps scaffold generation complete!');
    console.log(`📁 Output directory: ${CONFIG.outputDir}`);
    console.log('\nNext steps:');
    console.log('1. Copy .env.template to .env and configure your values');
    console.log('2. Run: docker-compose up -d');
    console.log('3. Access your application at http://localhost:3000');
    
  } catch (error) {
    console.error('❌ Error generating DevOps scaffold:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { main };