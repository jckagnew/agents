# 🎨 ShadCN/UI Development Workflow

A comprehensive workflow for building UI components using shadcn/ui with MCP agents. This workflow works with both Claude and Cursor.

## 🚀 Quick Start

### For Complex UI Features:
1. **Requirements Analysis** → 2. **Component Research** → 3. **Implementation**

### For Quick Component Additions:
1. **Express Agent** → Ready to use!

## 📋 Prerequisites

1. **MCP Server**: Ensure shadcn MCP server is running
2. **shadcn/ui Setup**: Run `npx shadcn@latest init` in your project
3. **TypeScript**: Ensure your project has TypeScript configured
4. **React/Next.js**: These agents work with React-based projects

## 🤖 Agent Workflows

### Workflow 1: Complex UI Feature Development

#### Step 1: Requirements Analysis
Use **Agent 1** to analyze your feature request:

```
I need a complete user dashboard with:
- User profile section
- Recent activity table
- Quick action buttons
- Settings modal
```

**Agent 1 Output:**
- Breaks down into required components
- Creates component hierarchy
- Verifies components exist in registries
- Generates `design-docs/dashboard/requirements.md`

#### Step 2: Component Research
Use **Agent 2** to research all components:

**Input:** `design-docs/dashboard/requirements.md`

**Agent 2 Output:**
- Gets implementation details for each component
- Finds best examples and demos
- Generates installation commands
- Creates `design-docs/dashboard/component-research.md`

#### Step 3: Implementation
Use **Agent 3** to build the complete feature:

**Input:** 
- `design-docs/dashboard/requirements.md`
- `design-docs/dashboard/component-research.md`

**Agent 3 Output:**
- Complete TypeScript/React implementation
- Proper imports and type definitions
- State management and error handling
- Ready-to-use component

### Workflow 2: Quick Component Addition

#### Express Agent
For single components or quick additions:

```
Add a date picker to my form
```

**Express Agent Output:**
- Installation command: `npx shadcn@latest add calendar`
- Complete implementation code
- Setup instructions
- Ready to paste and use

## 🛠️ Implementation Examples

### Example 1: Login Form (Complex Feature)

#### Agent 1 - Requirements Analysis:
```markdown
## Feature: Login Form
## Components Required:
- form (validation and submission)
- input (email and password fields)
- button (submit action)
- card (form container)
- alert (error display)

## Component Hierarchy:
Card
└── Form
    ├── Label + Input (email)
    ├── Label + Input (password)
    ├── Button (submit)
    └── Alert (errors)
```

#### Agent 2 - Component Research:
```markdown
## Installation Commands:
```bash
npx shadcn@latest add form input button card alert label
```

Component: Form
Implementation: [form component code]
Best Example: [form-with-validation-demo]
Key Props: onSubmit, form control

Component: Input
Implementation: [input component code]
Best Example: [email/password example]
Key Props: type, placeholder, required
```

#### Agent 3 - Implementation:
```tsx
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function LoginForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const form = useForm()

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      // Login logic
    } catch (err) {
      setError("Login failed")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input type="email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Signing in..." : "Sign In"}
            </Button>
            {error && (
              <Alert>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}
```

### Example 2: Date Picker (Quick Addition)

#### Express Agent:
```bash
# Install command
npx shadcn@latest add calendar
```

```tsx
// Quick implementation for calendar
import { Calendar } from "@/components/ui/calendar"

export function CalendarComponent() {
  return (
    <Calendar>
      {/* Add your content here */}
    </Calendar>
  )
}

// Example usage:
// <CalendarComponent />
```

## 🔧 Cursor Integration

### Setting up MCP in Cursor:

1. **Install MCP Server**:
   ```bash
   npm install -g @modelcontextprotocol/server-shadcn
   ```

2. **Configure Cursor**:
   - Open Cursor settings
   - Add MCP server configuration
   - Enable shadcn MCP server

3. **Verify Setup**:
   - Run `npx shadcn@latest init` in your project
   - Check that `components.json` is created
   - Test MCP connection

### Using Agents in Cursor:

1. **Open Chat Panel** in Cursor
2. **Paste Agent Prompt** from the agent files
3. **Follow the Workflow** step by step
4. **Copy Generated Code** to your project

## 📁 Project Structure

```
your-project/
├── components/
│   └── ui/                 # shadcn/ui components
├── design-docs/            # Generated by agents
│   └── [feature-name]/
│       ├── requirements.md
│       └── component-research.md
├── src/
│   └── components/         # Your custom components
└── components.json         # shadcn/ui config
```

## 🎯 Best Practices

### 1. Always Start with Requirements
- Use Agent 1 for complex features
- Break down into clear components
- Verify components exist before proceeding

### 2. Research Before Implementing
- Use Agent 2 to understand components
- Get examples and best practices
- Understand dependencies and props

### 3. Follow the Hierarchy
- Use Agent 3's structured approach
- Maintain proper component hierarchy
- Add proper TypeScript types

### 4. Use Express Agent for Quick Wins
- Single components and simple additions
- Quick prototypes and experiments
- Learning new components

### 5. Verify and Test
- Always test generated code
- Check for TypeScript errors
- Verify component functionality

## 🚨 Common Issues and Solutions

### Issue: MCP Server Not Running
**Solution**: 
```bash
# Install and start MCP server
npm install -g @modelcontextprotocol/server-shadcn
mcp-server-shadcn
```

### Issue: Components Not Found
**Solution**: 
```bash
# Initialize shadcn/ui
npx shadcn@latest init
```

### Issue: TypeScript Errors
**Solution**: 
- Check imports are correct
- Verify component props
- Add proper type definitions

### Issue: Styling Issues
**Solution**: 
- Ensure Tailwind CSS is configured
- Check component CSS variables
- Verify shadcn/ui theme setup

## 📚 Additional Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Agent Templates](templates/agents/shadcn_ui_agents.md)
- [Python Implementation](templates/python/shadcn_ui_agents.py)

---

*This workflow is designed to work seamlessly with both Claude and Cursor, providing a powerful development experience for shadcn/ui components.*
