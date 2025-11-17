# 🤖 Agent HQ Setup Guide

This guide will help you set up automated multi-agent PR reviews using GitHub Actions.

## 🔑 Step 1: Add Your Agent Keys to GitHub Secrets

**Important**: You must add your API keys as secrets in your GitHub repository before the workflows can run.

### How to Add Secrets:

1. Go to your repository on GitHub: `https://github.com/jckagnew/agents`
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret** for each of the following keys:

### Required Secrets:

| Secret Name | Description | Value Source |
|------------|-------------|--------------|
| `ANTHROPIC_API_KEY` | Your Claude API key | From `.env`: `ANTHROPIC_API_KEY` |
| `GOOGLE_AI_API_KEY` | Your Gemini/Google AI key | From `.env`: `GOOGLE_AI_API_KEY` |
| `DEEPSEEK_API_KEY` | Your DeepSeek API key | From `.env`: `DEEPSEEK_API_KEY` |
| `XAI_API_KEY` | Your Grok/X.AI key | From `.env`: `GROK_API_KEY` |
| `SERPER_API_KEY` | Your Serper API key | From `.env`: `SERPER_API_KEY` |

### Quick Copy Commands:

To extract your keys from `.env` (run from repository root):

```bash
# Claude
grep "^ANTHROPIC_API_KEY=" .env | cut -d'=' -f2

# Google AI / Gemini
grep "^GOOGLE_AI_API_KEY=" .env | cut -d'=' -f2

# DeepSeek
grep "^DEEPSEEK_API_KEY=" .env | cut -d'=' -f2

# Grok (X.AI)
grep "^GROK_API_KEY=" .env | cut -d'=' -f2

# Serper
grep "^SERPER_API_KEY=" .env | cut -d'=' -f2
```

**⚠️ Security Note**: Never commit your `.env` file or expose API keys in code or logs.

---

## 🚀 Step 2: Verify Workflow File

The workflow file has been created at:
```
.github/workflows/multi_agent_review.yml
```

### What This Workflow Does:

When you open a Pull Request, three AI agents will automatically review it:

1. **🧐 Claude (Architect)** - Reviews for:
   - High-level logic flaws
   - Security vulnerabilities
   - System design adherence
   - Technical debt introduction

2. **🧠 Gemini (Repo Analyst)** - Reviews for:
   - Cross-cutting impacts
   - Regressions
   - Unintended side effects
   - Non-obvious problems

3. **💻 DeepSeek (Coder)** - Reviews for:
   - Code syntax
   - Performance optimizations
   - Best practices adherence
   - Line-by-line suggestions

### How It Works:

- All three agents run **in parallel** when a PR is opened
- Each agent posts its review as a **separate comment** on the PR
- Reviews are posted automatically - no manual trigger needed

---

## ✅ Step 3: Test the Workflow

1. **Commit and push the workflow file**:
   ```bash
   git add .github/workflows/multi_agent_review.yml
   git commit -m "Add multi-agent PR review workflow"
   git push origin develop
   ```

2. **Create a test PR**:
   - Make a small change in a feature branch
   - Open a Pull Request to `develop`
   - Watch the Actions tab - you should see three jobs running

3. **Check the PR comments**:
   - Once the workflows complete, each agent will post its review
   - Look for comments from the GitHub Actions bot

---

## 🔧 Troubleshooting

### Workflow Not Running?

- ✅ Check that secrets are added correctly (Settings > Secrets)
- ✅ Verify the workflow file is in `.github/workflows/` directory
- ✅ Check the Actions tab for any error messages
- ✅ Ensure the PR is targeting a branch that has the workflow file

### Agents Not Posting Comments?

- ✅ Check the Actions logs for each job
- ✅ Verify API keys are correct and have sufficient credits
- ✅ Check that the repository has "Allow GitHub Actions to create and approve pull requests" enabled (Settings > Actions > General)

### Missing Secrets Error?

If you see "Secret not found" errors:
- Go to Settings > Secrets and variables > Actions
- Verify all required secrets are added
- Check that secret names match exactly (case-sensitive)

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Google Gemini CLI Action](https://github.com/google-github-actions/run-gemini-cli)
- [DeepSeek Review Action](https://github.com/hustcer/deepseek-review)

---

## 🎯 Next Steps

After setting up the PR review workflow, you can:

1. **Customize agent prompts** - Edit the `prompt` fields in the workflow file
2. **Add more agents** - Extend the workflow with additional AI services
3. **Set up branch protection** - Require agent reviews before merging
4. **Create issue automation** - Use agents to respond to issues automatically

---

**Status**: ✅ Workflow file created  
**Next**: Add secrets to GitHub repository settings

