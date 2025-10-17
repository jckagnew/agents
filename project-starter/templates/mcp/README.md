# 🤖 MCP (Model Context Protocol) Integration

This directory contains MCP integrations that enable AI agents to directly interact with external services and tools, automating full-stack application development.

## What are MCPs?

MCPs (Model Context Protocols) allow AI coding agents like Claude, Cursor, or GPT-4 to directly interact with external services through standardized protocols. This enables:

- **Automated Backend Setup**: Create databases, APIs, and authentication systems
- **UI Component Generation**: Generate and integrate UI components automatically  
- **Payment Processing**: Set up Stripe payments and billing systems
- **Service Integration**: Connect to external APIs and services

## Available MCPs

### 🗄️ **Supabase MCP**
- **Purpose**: Automated database and backend setup
- **Features**: 
  - Create projects and databases
  - Set up authentication
  - Generate API endpoints
  - Configure real-time subscriptions
- **Setup**: Requires Supabase personal access token

### 🎨 **ShadCN MCP** 
- **Purpose**: UI component generation and integration
- **Features**:
  - Generate ShadCN UI components
  - Create responsive layouts
  - Integrate with Tailwind CSS
  - Theme customization
- **Setup**: Works with existing Next.js projects

### 💳 **Stripe MCP**
- **Purpose**: Payment processing automation
- **Features**:
  - Set up payment flows
  - Create products and pricing
  - Handle webhooks
  - Generate invoices
- **Setup**: Requires Stripe secret API key

## Quick Start

1. **Install MCPs**: Run the setup script to install all MCPs
2. **Configure Keys**: Add your API keys to environment variables
3. **Connect to Agent**: Use the provided commands to connect MCPs to your AI agent
4. **Start Building**: Use the prompt templates to build full-stack applications

## Workflow

1. **Plan**: Use our AI planning layer to define requirements
2. **Backend**: Use Supabase MCP to create database and API
3. **Frontend**: Use ShadCN MCP to build UI components
4. **Payments**: Use Stripe MCP to add payment processing
5. **Deploy**: Deploy your complete application

## Examples

See the `examples/` directory for complete application examples built using MCPs.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Supabase MCP](https://github.com/supabase/mcp-server)
- [ShadCN MCP](https://github.com/shadcn/mcp-server)
- [Stripe MCP](https://github.com/stripe/mcp-server)
