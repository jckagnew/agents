#!/bin/bash
# Convenience wrapper for the future upgrades tracker

# Usage: ./scripts/upgrade-tracker.sh add "Tool Name" "Keep Watching" "Description"
#        ./scripts/upgrade-tracker.sh update "Tool Name" "Prototype" "New Description"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

case "$1" in
  "add")
    shift
    python3 "$SCRIPT_DIR/add_future_upgrade.py" \
      --name "$1" \
      --status "$2" \
      --summary "$3" \
      --triggers "${4:-Define trigger conditions before next review.}" \
      --owner "${5:-Unassigned}" \
      --notes "${6:-}"
    ;;
  "update")
    shift
    python3 "$SCRIPT_DIR/add_future_upgrade.py" \
      --name "$1" \
      --status "$2" \
      --summary "$3" \
      --triggers "${4:-Define trigger conditions before next review.}" \
      --owner "${5:-Unassigned}" \
      --notes "${6:-}"
    ;;
  "list")
    echo "📋 Current Future Upgrades:"
    echo ""
    if [ -f "$PROJECT_ROOT/docs/potential-factory-upgrades.md" ]; then
      cat "$PROJECT_ROOT/docs/potential-factory-upgrades.md"
    else
      echo "No upgrades tracked yet. Add one with:"
      echo "  ./scripts/upgrade-tracker.sh add \"Tool Name\" \"Keep Watching\" \"Description\""
    fi
    ;;
  *)
    echo "Usage:"
    echo "  $0 add \"Tool Name\" \"Status\" \"Summary\" [triggers] [owner] [notes]"
    echo "  $0 update \"Tool Name\" \"Status\" \"Summary\" [triggers] [owner] [notes]"
    echo "  $0 list"
    echo ""
    echo "Status options: Keep Watching, Prototype, Adopt, Parked"
    echo ""
    echo "Examples:"
    echo "  $0 add \"New Tool\" \"Keep Watching\" \"Interesting capability\""
    echo "  $0 update \"Existing Tool\" \"Prototype\" \"Ready for testing\""
    echo "  $0 list"
    exit 1
    ;;
esac
