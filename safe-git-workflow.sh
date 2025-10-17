#!/bin/bash
# Safe Git Workflow Script
# Forces verification before any git operations

echo "🛡️ SAFE GIT WORKFLOW ACTIVATED"
echo "================================"
echo ""

# Function to show current state
show_state() {
    echo "📊 CURRENT STATE:"
    echo "Branch: $(git branch --show-current)"
    echo "Status:"
    git status --short
    echo ""
}

# Function to show what would change
show_changes() {
    echo "📝 CHANGES TO BE MADE:"
    if [ "$1" = "commit" ]; then
        echo "Files to commit:"
        git diff --cached --name-only
        echo ""
        echo "Lines to commit:"
        git diff --cached --stat
    elif [ "$1" = "push" ]; then
        echo "Files to push:"
        git diff --name-only HEAD~1 HEAD
        echo ""
        echo "Lines to push:"
        git diff --stat HEAD~1 HEAD
    fi
    echo ""
}

# Function to get approval
get_approval() {
    echo "❓ Do you want to proceed? (y/N)"
    read -p "> " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operation cancelled."
        exit 1
    fi
    echo "✅ Operation approved. Proceeding..."
}

# Main workflow
case "$1" in
    "commit")
        show_state
        show_changes "commit"
        get_approval
        git commit "${@:2}"
        ;;
    "push")
        show_state
        show_changes "push"
        get_approval
        git push "${@:2}"
        ;;
    "status")
        show_state
        ;;
    *)
        echo "Usage: $0 {commit|push|status} [git-options]"
        echo ""
        echo "Examples:"
        echo "  $0 commit -m 'message'"
        echo "  $0 push origin branch-name"
        echo "  $0 status"
        exit 1
        ;;
esac
