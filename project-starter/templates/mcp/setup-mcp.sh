#!/bin/bash
# MCP Setup Script for Project Starter

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

print_header "Setting up MCP (Model Context Protocol) Integration..."

# Check if we're in a project directory
if [ ! -f "package.json" ] && [ ! -f "pyproject.toml" ]; then
    print_error "Please run this script from a project directory"
    exit 1
fi

# Create MCP configuration directory
mkdir -p .mcp
print_status "Created .mcp directory"

# Create MCP configuration file
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
    "shadcn": {
      "command": "npx", 
      "args": ["@shadcn/mcp-server"]
    },
    "stripe": {
      "command": "npx",
      "args": ["@stripe/mcp-server"],
      "env": {
        "STRIPE_SECRET_KEY": ""
      }
    }
  }
}
EOF
print_status "Created MCP configuration file"

# Create environment template
cat > .mcp/.env.template << 'EOF'
# MCP Environment Variables
# Copy this to .env and fill in your actual values

# Supabase MCP
SUPABASE_ACCESS_TOKEN=your_supabase_personal_access_token_here

# Stripe MCP  
STRIPE_SECRET_KEY=your_stripe_secret_key_here

# Optional: Additional MCP configurations
# GITHUB_TOKEN=your_github_token_here
# OPENAI_API_KEY=your_openai_key_here
EOF
print_status "Created environment template"

# Create MCP setup instructions
cat > .mcp/SETUP_INSTRUCTIONS.md << 'EOF'
# MCP Setup Instructions

## 1. Install MCP Servers

```bash
# Install Supabase MCP
npm install -g @supabase/mcp-server

# Install ShadCN MCP  
npm install -g @shadcn/mcp-server

# Install Stripe MCP
npm install -g @stripe/mcp-server
```

## 2. Get API Keys

### Supabase
1. Go to https://supabase.com/dashboard
2. Click on your profile → Access Tokens
3. Create a new personal access token
4. Copy the token

### Stripe
1. Go to https://dashboard.stripe.com/apikeys
2. Create a new restricted key
3. Copy the secret key

## 3. Configure Environment

```bash
# Copy the template
cp .mcp/.env.template .mcp/.env

# Edit with your actual keys
nano .mcp/.env
```

## 4. Connect to AI Agent

### For Claude Desktop
Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["@supabase/mcp-server"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### For Cursor
Use the MCP commands in the prompt templates.

## 5. Test Connection

Use the test commands in the prompt templates to verify MCP connections.

EOF
print_status "Created setup instructions"

# Create prompt templates directory
mkdir -p .mcp/prompts
print_status "Created prompts directory"

# Create Supabase MCP prompt template
cat > .mcp/prompts/supabase-mcp.md << 'EOF'
# Supabase MCP Prompt Template

## Database Setup Prompt

```
Using the Supabase MCP, create a complete database schema for a [PROJECT_TYPE] application with the following requirements:

[REQUIREMENTS]

Please:
1. Create a new Supabase project
2. Set up the database tables
3. Configure authentication
4. Set up Row Level Security (RLS)
5. Create API endpoints
6. Test the connection

Project details:
- Project name: [PROJECT_NAME]
- Database: [DATABASE_NAME]
- Authentication: [AUTH_METHOD]
```

## API Generation Prompt

```
Using the Supabase MCP, generate REST API endpoints for the following tables:

[TABLES_LIST]

Please create:
1. CRUD operations for each table
2. Proper authentication middleware
3. Input validation
4. Error handling
5. API documentation
```

## Authentication Setup Prompt

```
Using the Supabase MCP, set up authentication for a [PROJECT_TYPE] with:

1. User registration and login
2. Email verification
3. Password reset
4. Social login (Google, GitHub)
5. Role-based access control
6. Session management

Authentication requirements:
- [AUTH_REQUIREMENTS]
```
EOF

# Create ShadCN MCP prompt template
cat > .mcp/prompts/shadcn-mcp.md << 'EOF'
# ShadCN MCP Prompt Template

## UI Component Generation Prompt

```
Using the ShadCN MCP, create a complete UI for a [PROJECT_TYPE] application with:

1. Modern, responsive design
2. ShadCN UI components
3. Tailwind CSS styling
4. Dark/light mode support
5. Mobile-first approach

UI Requirements:
- [UI_REQUIREMENTS]

Components needed:
- [COMPONENTS_LIST]

Theme: [THEME_PREFERENCES]
```

## Layout Generation Prompt

```
Using the ShadCN MCP, create the following layout structure:

1. Header with navigation
2. Sidebar (if needed)
3. Main content area
4. Footer
5. Responsive breakpoints

Layout requirements:
- [LAYOUT_REQUIREMENTS]
- Mobile responsive
- Accessibility compliant
```

## Component Integration Prompt

```
Using the ShadCN MCP, integrate the following components into the existing layout:

[COMPONENTS_TO_INTEGRATE]

Please ensure:
1. Proper TypeScript types
2. Responsive design
3. Accessibility features
4. Consistent styling
5. Error boundaries
```
EOF

# Create Stripe MCP prompt template
cat > .mcp/prompts/stripe-mcp.md << 'EOF'
# Stripe MCP Prompt Template

## Payment Setup Prompt

```
Using the Stripe MCP, set up payment processing for a [PROJECT_TYPE] with:

1. Product catalog
2. Pricing plans
3. Checkout flow
4. Webhook handling
5. Invoice generation

Payment requirements:
- [PAYMENT_REQUIREMENTS]
- Currency: [CURRENCY]
- Payment methods: [PAYMENT_METHODS]
```

## Subscription Management Prompt

```
Using the Stripe MCP, create subscription management for:

1. Multiple pricing tiers
2. Billing cycles
3. Proration handling
4. Cancellation flow
5. Usage tracking

Subscription details:
- [SUBSCRIPTION_DETAILS]
```

## Webhook Integration Prompt

```
Using the Stripe MCP, set up webhook handling for:

1. Payment success/failure
2. Subscription events
3. Invoice events
4. Customer events
5. Error handling

Webhook endpoint: [WEBHOOK_URL]
```
EOF

print_status "Created MCP prompt templates"

# Create full-stack example
cat > .mcp/examples/full-stack-app.md << 'EOF'
# Full-Stack App Example Using MCPs

## Complete Workflow

This example shows how to build a complete e-commerce application using all three MCPs.

### 1. Project Planning
```
Using our AI planning layer, create a comprehensive plan for an e-commerce platform with:
- User authentication
- Product catalog
- Shopping cart
- Payment processing
- Order management
- Admin dashboard
```

### 2. Backend Setup (Supabase MCP)
```
Using the Supabase MCP, create the complete backend for an e-commerce platform:

1. Create new Supabase project
2. Set up database schema:
   - users table
   - products table
   - orders table
   - order_items table
   - categories table
3. Configure authentication
4. Set up Row Level Security
5. Create API endpoints
6. Test all endpoints
```

### 3. Frontend Development (ShadCN MCP)
```
Using the ShadCN MCP, create the complete frontend for an e-commerce platform:

1. Create Next.js project structure
2. Set up ShadCN UI components
3. Create pages:
   - Homepage
   - Product catalog
   - Product details
   - Shopping cart
   - Checkout
   - User dashboard
   - Admin panel
4. Implement responsive design
5. Add dark/light mode
6. Integrate with Supabase backend
```

### 4. Payment Integration (Stripe MCP)
```
Using the Stripe MCP, set up payment processing:

1. Create Stripe products
2. Set up pricing plans
3. Implement checkout flow
4. Handle payment success/failure
5. Set up webhooks
6. Generate invoices
7. Test payment flow
```

### 5. Testing and Deployment
```
1. Test all functionality
2. Set up CI/CD pipeline
3. Deploy to production
4. Monitor performance
5. Set up analytics
```

## Expected Result

A complete, production-ready e-commerce application with:
- ✅ User authentication
- ✅ Product management
- ✅ Shopping cart
- ✅ Payment processing
- ✅ Order management
- ✅ Admin dashboard
- ✅ Responsive design
- ✅ Mobile support
EOF

print_status "Created full-stack example"

# Create MCP workflow script
cat > .mcp/workflow.sh << 'EOF'
#!/bin/bash
# MCP Workflow Script

echo "🤖 MCP Workflow Helper"
echo "======================"
echo ""
echo "Available workflows:"
echo "1. Full-stack app (Supabase + ShadCN + Stripe)"
echo "2. Backend only (Supabase)"
echo "3. Frontend only (ShadCN)"
echo "4. Payment only (Stripe)"
echo "5. Test MCP connections"
echo ""

read -p "Select workflow (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting full-stack app workflow..."
        echo "1. Use AI planning layer to define requirements"
        echo "2. Use Supabase MCP for backend"
        echo "3. Use ShadCN MCP for frontend"
        echo "4. Use Stripe MCP for payments"
        echo "5. Deploy and test"
        ;;
    2)
        echo "🗄️ Starting backend workflow..."
        echo "Use Supabase MCP prompts from .mcp/prompts/supabase-mcp.md"
        ;;
    3)
        echo "🎨 Starting frontend workflow..."
        echo "Use ShadCN MCP prompts from .mcp/prompts/shadcn-mcp.md"
        ;;
    4)
        echo "💳 Starting payment workflow..."
        echo "Use Stripe MCP prompts from .mcp/prompts/stripe-mcp.md"
        ;;
    5)
        echo "🔍 Testing MCP connections..."
        echo "Run: /mcp in your AI agent to test connections"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
EOF

chmod +x .mcp/workflow.sh
print_status "Created MCP workflow script"

print_info "MCP integration setup complete!"
echo ""
print_info "Next steps:"
echo "  1. Follow the setup instructions in .mcp/SETUP_INSTRUCTIONS.md"
echo "  2. Configure your API keys in .mcp/.env"
echo "  3. Connect MCPs to your AI agent"
echo "  4. Use the prompt templates to build applications"
echo "  5. Run .mcp/workflow.sh for guided workflows"
echo ""
print_info "Happy building with MCPs! 🚀"
