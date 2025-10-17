# 🎯 Cursor Best Practices Guide

## 📋 **Overview**

This guide is based on Lee Robinson's proven Cursor workflows and best practices from his role as Head of AI Education at Cursor. It provides comprehensive strategies for maximizing productivity with AI-assisted development.

## 🚀 **Core Principles from Lee Robinson**

### **1. The Three-Panel Interface**
- **Left Panel**: File tree and project structure
- **Middle Panel**: Main code editing area (your primary focus)
- **Right Panel**: AI agent for parallel tasks and assistance

### **2. Parallel Development Strategy**
- **Main work** in the center panel
- **Background tasks** in the agent panel
- Use agent for secondary features while you focus on primary work
- Train yourself to work on multiple things simultaneously

### **3. Context Management**
- **New chat for discrete features** (not one long conversation)
- **Keep context under 80-90%** to maintain quality
- **Separate chats** for one-off questions vs. main workflows
- **Micro-slice** complex tasks into smaller, focused conversations

## 🛠️ **Custom Commands (Lee's Approach)**

### **@code-review**
Lee's signature command that reviews all changes for:
- Security vulnerabilities
- Test coverage adequacy
- Authentication changes
- Offline functionality impact
- Unnecessary additions
- Performance implications

### **@fix-lint-errors**
- Automatically runs appropriate linter
- Fixes all detected issues
- Verifies fixes by re-running linter
- Explains what was changed and why

### **@security-scan**
- Runs bandit (Python) or npm audit (JavaScript)
- Checks for dependency vulnerabilities
- Scans for hardcoded secrets
- Reviews authentication/authorization code

## 📝 **Writing Quality Rules (Anti-AI Patterns)**

### **Banned Words/Phrases**
Based on Lee's approach to eliminating AI-generated patterns:

**Generic Marketing Speak:**
- "game-changing" → "provides specific benefits"
- "innovative" → remove or be specific
- "excited to" → just state the thing
- "revolutionary" → be specific about benefits
- "cutting-edge" → describe actual capabilities
- "next-generation" → describe current features
- "industry-leading" → provide metrics
- "best-in-class" → provide comparisons

**LLM Pattern Detection:**
- Avoid excessive bullet point lists
- Don't use "it's not just X, it's Y" structure
- Avoid "first, second, third" unless truly sequential
- Don't overuse "super", "really", "very"
- Avoid "as you can see" and "obviously"

### **Writing Process (Lee's Method)**
1. **Word vomit** or voice notes to get ideas down
2. **First draft** yourself (maintains human touch)
3. **AI review** to catch banned phrases and improve structure
4. **Human refinement** based on AI suggestions

## 🔧 **Technical Setup (Lee's Recommendations)**

### **Essential Tools**
- **Typed languages** (TypeScript, Python with type hints)
- **Linters** (ESLint, Black, flake8, mypy)
- **Formatters** (Prettier, Black, isort)
- **Tests** (Jest, pytest)
- **Pre-commit hooks** for automated quality checks

### **Why These Tools Matter**
- **AI agents work better** with structured, typed code
- **Linters catch errors** that AI might miss
- **Formatters maintain consistency** across the codebase
- **Tests provide guardrails** for AI-generated code
- **Type checking** helps AI understand code structure

## 🎯 **Workflow Strategies**

### **For Beginners**
1. **Start with simple projects** - don't try to build complex systems
2. **Use agent as pair programmer** - ask "what does this do?"
3. **Read code** even when you don't understand it
4. **Ask questions** - "explain this function", "how does this work?"
5. **Build incrementally** - small, testable changes

### **For Experienced Developers**
1. **Use agent for research** - explore new technologies
2. **Focus on architecture** - let agent handle implementation
3. **Code review everything** - use @code-review command
4. **Optimize workflows** - create custom commands
5. **Share knowledge** - document your learnings

### **Parallel Task Execution**
1. **Main work** in center panel
2. **Agent tasks** in right panel
3. **Don't mix contexts** - keep related work together
4. **Use @mentions** for specific files/functions
5. **Start fresh** for new features

## 🚨 **Error Handling (Lee's Approach)**

### **When AI Gets It Wrong**
1. **Stop and analyze** what went wrong
2. **Be specific** about what you wanted
3. **Provide clear context** about the issue
4. **Don't just say "fix it"** - explain the problem
5. **Use separate chat** for debugging vs. feature work

### **Context Management**
- **Start new chat** for new features
- **Keep related work** in same chat
- **Use @mentions** for specific context
- **Don't let context exceed 80%**
- **Summarize progress** periodically

## 🎓 **Learning Strategies**

### **Code Reading (Lee's Method)**
- **Look at code** even when you don't understand it
- **Ask questions** - "what does this do?"
- **Use agent as teacher** - "explain this function"
- **Learn by doing** - don't just read tutorials
- **Build simple things first** - get the spark

### **Progressive Learning**
1. **Vibe coding** - build prototypes quickly
2. **Learn the code** - understand what you built
3. **Add structure** - types, lints, tests
4. **Optimize workflows** - custom commands, parallel tasks
5. **Share knowledge** - teach others what you learned

## 🔧 **Advanced Techniques**

### **Agent Orchestration**
- **Use multiple agents** for different tasks
- **Chain agent outputs** for complex workflows
- **Use agent for research**, human for implementation
- **Combine agent suggestions** with human judgment

### **Prompt Engineering**
- **Be specific** about what you want
- **Provide examples** when possible
- **Use structured prompts** for consistency
- **Iterate on prompts** based on results
- **Document successful patterns**

### **Context Optimization**
- **Use @mentions** for specific context
- **Summarize long conversations**
- **Start fresh** for new features
- **Keep related work together**
- **Use file references efficiently**

## 🎯 **Project-Specific Rules**

### **AI Agent Development**
- Use structured outputs (Pydantic models)
- Implement error handling and retry logic
- Add logging and tracing
- Write behavior tests
- Document agent capabilities

### **Web Development**
- Use responsive design principles
- Implement proper error boundaries
- Add loading states
- Optimize for performance
- Follow accessibility guidelines

### **Mobile Development**
- Test on multiple devices
- Handle offline scenarios
- Optimize for battery life
- Follow platform guidelines
- Use proper navigation patterns

## 🚀 **Success Metrics**

### **Code Quality**
- Linting passes with no errors
- Test coverage above 80%
- Type checking passes
- Security scans clean
- Performance benchmarks met

### **Development Velocity**
- Features delivered on time
- Bugs caught early
- Code reviews efficient
- Documentation up to date
- Team knowledge sharing

## 🎉 **Key Takeaways from Lee Robinson**

### **1. AI as Pair Programmer**
- **Infinite patience** - ask any question
- **Always available** - 24/7 assistance
- **Never judges** - no stupid questions
- **Explains everything** - how things work

### **2. Code Quality First**
- **Set up guardrails** - types, lints, tests
- **Fix issues immediately** - don't accumulate debt
- **Use agent for cleanup** - maintain quality
- **Review everything** - use @code-review

### **3. Parallel Development**
- **Main work** in center panel
- **Agent tasks** in right panel
- **Don't mix contexts** - separate chats
- **Train the skill** - practice parallel work

### **4. Learning by Doing**
- **Read code** even when confused
- **Ask questions** constantly
- **Build simple things** first
- **Use agent as teacher** - explain everything

### **5. Writing Quality**
- **Ban generic phrases** - be specific
- **Detect AI patterns** - avoid clichés
- **Human first** - write your own drafts
- **AI review** - catch banned phrases

## 🔧 **Implementation Checklist**

### **Initial Setup**
- [ ] Install Cursor
- [ ] Set up typed languages (TypeScript, Python)
- [ ] Configure linters (ESLint, Black, flake8, mypy)
- [ ] Set up formatters (Prettier, isort)
- [ ] Install testing frameworks (Jest, pytest)
- [ ] Configure pre-commit hooks

### **Custom Commands**
- [ ] Create @code-review command
- [ ] Create @fix-lint-errors command
- [ ] Create @security-scan command
- [ ] Create @test-coverage command
- [ ] Create @refactor-suggestions command

### **Writing Rules**
- [ ] Create banned words list
- [ ] Set up LLM pattern detection
- [ ] Create writing quality prompts
- [ ] Test with sample content
- [ ] Refine based on results

### **Workflow Optimization**
- [ ] Practice parallel development
- [ ] Create new chats for features
- [ ] Use @mentions for context
- [ ] Manage context usage
- [ ] Document successful patterns

## 🎯 **Conclusion**

Lee Robinson's approach to Cursor emphasizes:
- **Code quality first** through automated tools
- **Parallel development** with agent assistance
- **Learning by doing** with AI as teacher
- **Writing quality** through anti-AI patterns
- **Context management** for optimal results

The goal is not to replace human judgment, but to augment it with AI capabilities while maintaining high standards of code quality and development practices.

**Remember: The best way to learn coding is to read code, ask questions, and build things. Cursor makes this process more accessible and efficient than ever before.**
