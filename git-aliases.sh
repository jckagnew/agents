#!/bin/bash
# Safe Git Aliases
# Source this file to get safe git commands

# Safe commit - shows changes before committing
alias safe-commit='./safe-git-workflow.sh commit'

# Safe push - shows changes before pushing
alias safe-push='./safe-git-workflow.sh push'

# Safe status - shows current state
alias safe-status='./safe-git-workflow.sh status'

# Safe PR creation - shows changes before creating PR
safe-pr() {
    echo "🛡️ SAFE PR CREATION"
    echo "==================="
    echo ""
    echo "Files to be included in PR:"
    git diff --name-only HEAD~1 HEAD
    echo ""
    echo "Lines to be included in PR:"
    git diff --stat HEAD~1 HEAD
    echo ""
    echo "This will create a PR. Continue? (y/N)"
    read -p "> " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ PR creation cancelled."
        return 1
    fi
    echo "✅ PR creation approved. Proceeding..."
    gh pr create "$@"
}

echo "🛡️ Safe git aliases loaded!"
echo "Available commands:"
echo "  safe-commit    - Safe commit with verification"
echo "  safe-push      - Safe push with verification"
echo "  safe-status    - Show current state"
echo "  safe-pr        - Safe PR creation with verification"
