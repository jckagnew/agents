# =============================================================================
# MULTI-STAGE DOCKERFILE
# =============================================================================
# This Dockerfile follows best practices for production-ready containers
# =============================================================================

# =============================================================================
# STAGE 1: BASE IMAGE
# =============================================================================
FROM node:18-alpine AS base

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel \
    build-base \
    python3-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Create app directory
WORKDIR /app

# =============================================================================
# STAGE 2: DEPENDENCIES
# =============================================================================
FROM base AS dependencies

# Copy package files
COPY package*.json ./
COPY requirements.txt ./
COPY pyproject.toml ./

# Install Node.js dependencies
RUN npm ci --only=production && npm cache clean --force

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 3: DEVELOPMENT
# =============================================================================
FROM base AS development

# Copy package files
COPY package*.json ./
COPY requirements.txt ./
COPY pyproject.toml ./

# Install all dependencies (including dev)
RUN npm ci && npm cache clean --force
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start development server
CMD ["npm", "run", "dev"]

# =============================================================================
# STAGE 4: BUILD
# =============================================================================
FROM base AS build

# Copy package files
COPY package*.json ./
COPY requirements.txt ./
COPY pyproject.toml ./

# Install dependencies
RUN npm ci && npm cache clean --force
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Build application
RUN npm run build

# =============================================================================
# STAGE 5: PRODUCTION
# =============================================================================
FROM base AS production

# Install only production dependencies
COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy built application
COPY --from=build /app/dist ./dist
COPY --from=build /app/src ./src

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start production server
CMD ["npm", "start"]

# =============================================================================
# METADATA
# =============================================================================
LABEL maintainer="Jack Agnew <jack@example.com>"
LABEL version="1.0.0"
LABEL description="Project Starter Template"
LABEL org.opencontainers.image.source="https://github.com/jckagnew/project-starter"
LABEL org.opencontainers.image.licenses="MIT"
