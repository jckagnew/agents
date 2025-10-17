#!/bin/bash
# Software Factory Starter Kit Generator
# Creates a complete project template with all tools configured

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Get project name from user
if [ -z "$1" ]; then
    read -p "Enter project name: " PROJECT_NAME
else
    PROJECT_NAME=$1
fi

PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
PROJECT_DIR="software-factory-starter-$PROJECT_SLUG"

print_header "Creating Software Factory Starter: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize project structure
print_info "Setting up project structure..."

mkdir -p {src,public,scripts,tests/{unit,integration,e2e},docs,.github/workflows}
mkdir -p src/{components,app,lib,types,utils}
mkdir -p .mcp

# Create package.json
print_info "Creating package.json..."
cat > package.json << EOF
{
  "name": "$PROJECT_SLUG",
  "version": "1.0.0",
  "description": "$PROJECT_NAME - Built with Software Factory",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx,.js,.jsx",
    "lint:fix": "eslint . --ext .ts,.tsx,.js,.jsx --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@supabase/supabase-js": "^2.39.0",
    "@heroicons/react": "^2.1.0",
    "recharts": "^2.12.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "typescript": "^5",
    "eslint": "^8",
    "eslint-config-next": "^14.2.0",
    "prettier": "^3.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "playwright": "^1.40.0",
    "jest-environment-jsdom": "^29.0.0",
    "lint-staged": "^15.0.0"
  }
}
EOF

# Create Next.js configuration
print_info "Creating Next.js configuration..."
cat > next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  images: {
    domains: ['localhost'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}

module.exports = nextConfig
EOF

# Create TypeScript configuration
print_info "Creating TypeScript configuration..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

# Create Tailwind configuration
print_info "Creating Tailwind configuration..."
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
EOF

# Create Cursor rules
print_info "Creating Cursor rules..."
cat > .cursorrules << 'EOF'
# 🎯 Software Factory - Cursor Rules

## 🚨 CRITICAL: AI SAFETY PROTOCOLS
- [ ] SHOW: Exact command I will run
- [ ] DISPLAY: All files that will change  
- [ ] COUNT: Exact line additions/deletions
- [ ] WAIT: For explicit user approval
- [ ] VERIFY: Result matches my claim

## 🧪 Testing Requirements
- RECOMMENDED: Write unit tests for critical business logic
- RECOMMENDED: Add integration tests for API endpoints
- RECOMMENDED: Use E2E tests for critical user workflows
- STRETCH GOAL: Achieve 80%+ test coverage on core modules

## 🔧 Code Quality Requirements
- RECOMMENDED: Use linters appropriate to your language
- RECOMMENDED: Format code consistently (Prettier, Black, etc.)
- RECOMMENDED: Run security scans on critical code paths

## 🤖 AI Agent Requirements
- RECOMMENDED: Use structured outputs when possible
- RECOMMENDED: Add error handling and retry logic
- RECOMMENDED: Include logging for debugging

## 📊 Database Requirements
- RECOMMENDED: Use transactions for multi-step operations
- RECOMMENDED: Validate database models
- RECOMMENDED: Test database operations

## 🚀 Deployment Requirements
- RECOMMENDED: Use CI/CD pipeline for deployments
- RECOMMENDED: Include health checks
- RECOMMENDED: Set up monitoring
EOF

# Create MCP configuration
print_info "Creating MCP configuration..."
cat > .mcp/config.json << 'EOF'
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["@supabase/mcp-server"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": ""
      }
    },
    "context7": {
      "command": "npx",
      "args": ["@context7/mcp-server"],
      "env": {
        "CONTEXT7_API_KEY": ""
      }
    },
    "perplexity": {
      "command": "npx",
      "args": ["@perplexity/mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": ""
      }
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": ""
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "mcp-memory-libsql"],
      "env": {
        "LIBSQL_URL": "file:./memory/project.db"
      }
    }
  }
}
EOF

# Create environment template
print_info "Creating environment template..."
cat > .env.example << 'EOF'
# =============================================================================
# SOFTWARE FACTORY - ENVIRONMENT VARIABLES
# =============================================================================

# =============================================================================
# APPLICATION
# =============================================================================
NODE_ENV=development
NEXT_PUBLIC_APP_NAME=PROJECT_NAME
NEXT_PUBLIC_APP_VERSION=1.0.0

# =============================================================================
# SUPABASE
# =============================================================================
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# =============================================================================
# MCP SERVERS
# =============================================================================
CONTEXT7_API_KEY=your_context7_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
BRAVE_API_KEY=your_brave_api_key_here

# =============================================================================
# DEVELOPMENT
# =============================================================================
# Add your development-specific variables here
EOF

# Create GitHub Actions workflow
print_info "Creating GitHub Actions workflow..."
cat > .github/workflows/ci.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linting
      run: npm run lint
    
    - name: Run type checking
      run: npm run type-check
    
    - name: Run tests
      run: npm run test:coverage
    
    - name: Run E2E tests
      run: |
        npx playwright install
        npm run test:e2e
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
        flags: unittests
        name: codecov-umbrella

  build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build application
      run: npm run build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-files
        path: |
          .next/
          public/
          package.json
          package-lock.json
EOF

# Create Supabase schema
print_info "Creating Supabase schema..."
cat > supabase-schema.sql << 'EOF'
-- Software Factory Starter - Supabase Schema
-- Run this in your Supabase SQL editor

-- Enable necessary extensions
create extension if not exists "uuid-ossp";

-- Create users table
create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text,
  avatar_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Create projects table
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  name text not null,
  description text,
  status text default 'active',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Create activities table for audit trail
create table if not exists public.activities (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  project_id uuid references public.projects(id) on delete cascade,
  action text not null,
  details jsonb,
  created_at timestamptz default now()
);

-- Enable Row Level Security
alter table public.users enable row level security;
alter table public.projects enable row level security;
alter table public.activities enable row level security;

-- Create RLS policies
create policy "Users can view own data" on public.users
  for select using (auth.uid() = id);

create policy "Users can update own data" on public.users
  for update using (auth.uid() = id);

create policy "Users can view own projects" on public.projects
  for select using (auth.uid() = user_id);

create policy "Users can create projects" on public.projects
  for insert with check (auth.uid() = user_id);

create policy "Users can update own projects" on public.projects
  for update using (auth.uid() = user_id);

create policy "Users can view own activities" on public.activities
  for select using (auth.uid() = user_id);

create policy "Users can create activities" on public.activities
  for insert with check (auth.uid() = user_id);

-- Create indexes for performance
create index if not exists idx_projects_user_id on public.projects(user_id);
create index if not exists idx_activities_user_id on public.activities(user_id);
create index if not exists idx_activities_project_id on public.activities(project_id);
create index if not exists idx_activities_created_at on public.activities(created_at);
EOF

# Create basic React components
print_info "Creating basic React components..."

# Create root layout
cat > src/app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Software Factory Starter',
  description: 'A modern web application built with the Software Factory stack',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
EOF

# Create globals CSS
cat > src/app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Create main page
cat > src/app/page.tsx << 'EOF'
import { Suspense } from 'react'
import { ProjectList } from '@/components/ProjectList'
import { CreateProject } from '@/components/CreateProject'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Software Factory Starter
        </h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Your Projects
            </h2>
            <Suspense fallback={<div>Loading projects...</div>}>
              <ProjectList />
            </Suspense>
          </div>
          
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Create New Project
            </h2>
            <CreateProject />
          </div>
        </div>
      </div>
    </main>
  )
}
EOF

# Create project list component
cat > src/components/ProjectList.tsx << 'EOF'
'use client'

import { useState, useEffect } from 'react'
import { Project } from '@/types/project'

export function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // TODO: Implement project fetching
    setLoading(false)
  }, [])

  if (loading) {
    return <div className="text-gray-500">Loading projects...</div>
  }

  if (projects.length === 0) {
    return (
      <div className="text-gray-500 text-center py-8">
        No projects yet. Create your first project!
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {projects.map((project) => (
        <div key={project.id} className="bg-white p-4 rounded-lg shadow">
          <h3 className="font-semibold text-gray-900">{project.name}</h3>
          <p className="text-gray-600 text-sm">{project.description}</p>
          <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
            {project.status}
          </span>
        </div>
      ))}
    </div>
  )
}
EOF

# Create project creation component
cat > src/components/CreateProject.tsx << 'EOF'
'use client'

import { useState } from 'react'

export function CreateProject() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    // TODO: Implement project creation
    console.log('Creating project:', { name, description })
    
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Project Name
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          required
        />
      </div>
      
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        />
      </div>
      
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
      >
        {loading ? 'Creating...' : 'Create Project'}
      </button>
    </form>
  )
}
EOF

# Create types
print_info "Creating TypeScript types..."
cat > src/types/project.ts << 'EOF'
export interface Project {
  id: string
  name: string
  description?: string
  status: 'active' | 'inactive' | 'archived'
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  name?: string
  avatar_url?: string
  created_at: string
  updated_at: string
}

export interface Activity {
  id: string
  user_id: string
  project_id: string
  action: string
  details?: Record<string, any>
  created_at: string
}
EOF

# Create Supabase client
print_info "Creating Supabase client..."
cat > src/lib/supabase.ts << 'EOF'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          name: string | null
          avatar_url: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          email: string
          name?: string | null
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          email?: string
          name?: string | null
          avatar_url?: string | null
          created_at?: string
          updated_at?: string
        }
      }
      projects: {
        Row: {
          id: string
          user_id: string
          name: string
          description: string | null
          status: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          name: string
          description?: string | null
          status?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          name?: string
          description?: string | null
          status?: string
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}
EOF

# Create test files
print_info "Creating test files..."

# Jest configuration
cat > jest.config.js << 'EOF'
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testEnvironment: 'jsdom',
}

module.exports = createJestConfig(customJestConfig)
EOF

# Jest setup
cat > jest.setup.js << 'EOF'
import '@testing-library/jest-dom'
EOF

# Playwright configuration
cat > playwright.config.ts << 'EOF'
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
EOF

# Create sample tests
cat > tests/unit/components.test.tsx << 'EOF'
import { render, screen } from '@testing-library/react'
import { CreateProject } from '@/components/CreateProject'

describe('CreateProject', () => {
  it('renders project creation form', () => {
    render(<CreateProject />)
    
    expect(screen.getByLabelText('Project Name')).toBeInTheDocument()
    expect(screen.getByLabelText('Description')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create Project' })).toBeInTheDocument()
  })
})
EOF

cat > tests/e2e/basic.spec.ts << 'EOF'
import { test, expect } from '@playwright/test'

test('homepage loads correctly', async ({ page }) => {
  await page.goto('/')
  
  await expect(page.getByRole('heading', { name: 'Software Factory Starter' })).toBeVisible()
  await expect(page.getByText('Your Projects')).toBeVisible()
  await expect(page.getByText('Create New Project')).toBeVisible()
})
EOF

# Create setup scripts
print_info "Creating setup scripts..."

cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# Software Factory Starter Setup Script

set -e

echo "🚀 Setting up Software Factory Starter..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install MCP servers (using npx to avoid global installs)
echo "🔌 Testing MCP servers..."
npx -y @supabase/mcp-server --version || echo "⚠️  Supabase MCP server not available"
npx -y @context7/mcp-server --version || echo "⚠️  Context7 MCP server not available"
npx -y @perplexity/mcp-server --version || echo "⚠️  Perplexity MCP server not available"
npx -y @modelcontextprotocol/server-brave-search --version || echo "⚠️  Brave Search MCP server not available"
npx -y mcp-memory-libsql --version || echo "⚠️  Memory MCP server not available"

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
npx playwright install

# Initialize Git repository
echo "📦 Initializing Git repository..."
git init
git add .
git commit -m "Initial commit"

# Setup Git hooks (optional - can be added later)
echo "ℹ️  Git hooks can be added later with: npx husky install && npx husky add .husky/pre-commit 'npx lint-staged'"

# Create environment file
echo "⚙️ Creating environment file..."
if [ ! -f .env.local ]; then
  cp .env.example .env.local
  echo "📝 Please update .env.local with your actual values"
fi

echo "✅ Setup complete!"
echo "Next steps:"
echo "1. Update .env.local with your API keys"
echo "2. Set up your Supabase project and run supabase-schema.sql"
echo "3. Run 'npm run dev' to start development"
EOF

chmod +x scripts/setup.sh

# Create README
print_info "Creating comprehensive README..."
cat > README.md << EOF
# $PROJECT_NAME

A modern web application built with the Software Factory stack.

## 🚀 Quick Start

\`\`\`bash
# 1. Install dependencies
npm install

# 2. Set up environment
cp .env.example .env.local
# Edit .env.local with your actual values

# 3. Set up Supabase
# - Create a new Supabase project
# - Run supabase-schema.sql in the SQL editor
# - Update .env.local with your Supabase credentials

# 4. Start development
npm run dev
\`\`\`

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS 3
- **Database**: Supabase
- **Testing**: Jest + Playwright
- **AI Tools**: Cursor + MCP Servers
- **Deployment**: GitHub Actions + Railway

## 📁 Project Structure

\`\`\`
src/
├── app/                 # Next.js app directory
├── components/          # React components
├── lib/                # Utility libraries
├── types/              # TypeScript type definitions
└── utils/              # Helper functions

tests/
├── unit/               # Unit tests
├── integration/        # Integration tests
└── e2e/               # End-to-end tests

.mcp/                  # MCP server configurations
.github/workflows/     # CI/CD pipelines
\`\`\`

## 🔧 Available Scripts

- \`npm run dev\` - Start development server
- \`npm run build\` - Build for production
- \`npm run start\` - Start production server
- \`npm run test\` - Run unit tests
- \`npm run test:e2e\` - Run E2E tests
- \`npm run lint\` - Run ESLint
- \`npm run format\` - Format code with Prettier

## 🔌 MCP Servers

This project includes the following MCP servers:

- **Supabase**: Database operations
- **Context7**: Documentation access
- **Perplexity**: AI-powered research
- **Brave Search**: Web search
- **Memory**: Knowledge storage

## 🚀 Deployment

### Railway (Recommended)

See the [Railway Pilot Runbook](../RAILWAY_PILOT_RUNBOOK.md) for detailed deployment instructions.

**Note**: Railway deployment requires manual setup following the runbook. Do not run global CLI commands without reviewing the runbook first.

### Vercel

\`\`\`bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
\`\`\`

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Software Factory Best Practices](./docs/best-practices.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
EOF

# Create documentation
print_info "Creating documentation..."
mkdir -p docs

cat > docs/best-practices.md << 'EOF'
# Best Practices

## Development Workflow

1. **Start with Cursor Agent**: Use `Cmd+K` for complex tasks
2. **Write Tests First**: Follow TDD principles
3. **Use TypeScript**: Leverage type safety
4. **Follow Git Flow**: Use feature branches and pull requests
5. **Code Review**: Always review AI-generated code

## MCP Usage

- **Context7**: For documentation lookups
- **Perplexity**: For complex problem-solving
- **Brave Search**: For finding specific resources
- **Memory**: For storing project knowledge

## Testing Strategy

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Coverage**: Maintain 90%+ test coverage
EOF

# Create .gitignore
print_info "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output

# Next.js
.next/
out/

# Production
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# MCP
.mcp/.env
memory/*.db
EOF

# Create lint-staged configuration
cat > .lintstagedrc.js << 'EOF'
module.exports = {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix',
    'prettier --write'
  ],
  '*.{json,md}': [
    'prettier --write'
  ]
}
EOF

# Create pre-commit configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.40.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        additional_dependencies: [eslint@^8.40.0]
  
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        files: \.(js|jsx|ts|tsx|json|md)$
EOF

print_status "Software Factory Starter created successfully!"
print_info "Project directory: $PROJECT_DIR"
print_info "Next steps:"
print_info "1. cd $PROJECT_DIR"
print_info "2. Run: ./scripts/setup.sh"
print_info "3. Update .env.local with your API keys"
print_info "4. Set up Supabase and run supabase-schema.sql"
print_info "5. Run: npm run dev"
print_info ""
print_info "🎉 Your Software Factory Starter is ready to go!"
