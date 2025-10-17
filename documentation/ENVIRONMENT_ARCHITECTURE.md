# Environment Variable Architecture

## 🏗️ Architecture Overview

Your project uses a **centralized environment variable management** system:

```
env.master (Single Source of Truth)
    ↓
Individual Project .env files
```

## 📁 File Structure

```
agents/
├── env.master                    # 🎯 Master file with ALL API keys
├── sync-env.sh                   # 🔄 Script to sync to all projects
├── clevel-sales-guy/
│   └── .env                      # 📋 Project-specific env
├── business-name-generator/
│   └── app/.env.local            # 📋 Next.js project env
└── other-projects/
    └── .env                      # 📋 Project-specific env
```

## 🔄 How It Works

### 1. **env.master** - Single Source of Truth
- Contains ALL API keys and environment variables
- Never committed to version control
- Updated when you get new API keys (like Serper)

### 2. **Project .env files** - Project-Specific
- Copied from `env.master` for each project
- Can be customized per project needs
- Contains only variables needed by that project

### 3. **sync-env.sh** - Synchronization Script
- Copies `env.master` to all known projects
- Maintains consistency across projects
- Run when you add new API keys

## 🚀 Usage

### Adding New API Keys
1. Add to `env.master`
2. Run `./sync-env.sh` to update all projects

### For New Projects
```bash
# Copy master env to new project
cp env.master my-new-project/.env

# Or use the sync script
./sync-env.sh
```

### For Existing Projects
```bash
# Sync all projects
./sync-env.sh

# Or sync specific project
cp env.master specific-project/.env
```

## 📋 Current API Keys in env.master

- **OpenAI**: `sk-proj-...` (AI generation)
- **Anthropic**: `sk-ant-...` (Claude AI)
- **Google**: `AIzaSyCzv...` (Gemini AI)
- **Serper**: `4d7237480b1009d11c895f2b9dc757dba924e36e` (Web search)
- **Supabase**: Database and auth
- **Stripe**: Payment processing
- **SendGrid**: Email services
- **GitHub**: Development tools

## ⚠️ Security Notes

- Never commit `.env` files to version control
- Rotate API keys regularly
- Use different keys for development/production
- Keep `env.master` secure and backed up

## 🔧 Maintenance

### When to Run sync-env.sh
- After adding new API keys to `env.master`
- When setting up new projects
- When updating existing project environments

### Project-Specific Variables
Some projects may need additional variables not in `env.master`:
- Add them to the project's `.env` file
- Consider adding common ones back to `env.master`

## 📝 Example Workflow

```bash
# 1. Add new API key to master
echo "NEW_API_KEY=your_key_here" >> env.master

# 2. Sync to all projects
./sync-env.sh

# 3. Verify in a project
cat clevel-sales-guy/.env | grep NEW_API_KEY
```

This architecture ensures consistency while allowing project-specific customization! 🎯
