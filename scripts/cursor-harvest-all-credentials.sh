#!/bin/bash

# ===================================================================
# COMPREHENSIVE CREDENTIAL HARVESTING SCRIPT
# For Cursor to consolidate ALL credentials into master .env
# ===================================================================
# This script searches the entire workspace for .env files and
# consolidates ALL credentials into the master .env file
# ===================================================================

set -e

MASTER_ENV="/home/user/agents/.env"
BACKUP_ENV="/home/user/agents/.env.backup.$(date +%Y%m%d_%H%M%S)"
HARVEST_REPORT="/home/user/agents/HARVEST_REPORT.txt"

echo "🔍 COMPREHENSIVE CREDENTIAL HARVESTING"
echo "======================================="
echo ""
echo "This script will:"
echo "  1. Search for ALL .env files in /home/user/"
echo "  2. Extract ALL key-value pairs"
echo "  3. Consolidate into master .env at: $MASTER_ENV"
echo "  4. Create backup of existing .env"
echo "  5. Generate report of what was found"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled by user"
    exit 0
fi

# Backup existing master .env
if [ -f "$MASTER_ENV" ]; then
    echo "💾 Backing up existing .env to: $BACKUP_ENV"
    cp "$MASTER_ENV" "$BACKUP_ENV"
fi

# Initialize report
echo "# CREDENTIAL HARVEST REPORT" > "$HARVEST_REPORT"
echo "Generated: $(date)" >> "$HARVEST_REPORT"
echo "" >> "$HARVEST_REPORT"

# Create temporary file for consolidation
TEMP_CONSOLIDATED="/tmp/consolidated_env_$$"
touch "$TEMP_CONSOLIDATED"

# Copy existing master .env as base
if [ -f "$MASTER_ENV" ]; then
    cat "$MASTER_ENV" > "$TEMP_CONSOLIDATED"
fi

echo ""
echo "🔍 Step 1: Searching for .env files..."
echo "======================================="

# Find all .env files (excluding node_modules, .git)
ENV_FILES=$(find /home/user -type f \( \
    -name ".env" -o \
    -name ".env.*" -o \
    -name "*.env" -o \
    -name "env" -o \
    -name "secrets.*" -o \
    -name "config.env" \
\) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" ! -path "*/build/*" 2>/dev/null || true)

if [ -z "$ENV_FILES" ]; then
    echo "❌ No .env files found"
    echo "" >> "$HARVEST_REPORT"
    echo "## Search Results" >> "$HARVEST_REPORT"
    echo "No .env files found in /home/user/" >> "$HARVEST_REPORT"
    exit 0
fi

# Count files
FILE_COUNT=$(echo "$ENV_FILES" | wc -l)
echo "✅ Found $FILE_COUNT .env file(s)"
echo ""

echo "## Files Found" >> "$HARVEST_REPORT"
echo "$ENV_FILES" >> "$HARVEST_REPORT"
echo "" >> "$HARVEST_REPORT"

echo "🔄 Step 2: Extracting credentials..."
echo "======================================="
echo "" >> "$HARVEST_REPORT"
echo "## Credentials Extracted" >> "$HARVEST_REPORT"
echo "" >> "$HARVEST_REPORT"

# Track statistics
TOTAL_KEYS=0
NEW_KEYS=0
UPDATED_KEYS=0
SKIPPED_KEYS=0

# Process each .env file
while IFS= read -r env_file; do
    echo ""
    echo "📄 Processing: $env_file"
    echo "### From: $env_file" >> "$HARVEST_REPORT"
    echo "" >> "$HARVEST_REPORT"

    FILE_KEYS=0

    # Read file line by line
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip comments and empty lines
        if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "$line" ]]; then
            continue
        fi

        # Extract key=value pairs
        if [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)= ]]; then
            KEY=$(echo "$line" | cut -d'=' -f1 | xargs)
            VALUE=$(echo "$line" | cut -d'=' -f2- | xargs)

            # Skip placeholder values
            if [[ "$VALUE" =~ your-.*-here ]] || [[ "$VALUE" =~ \<.*\> ]] || [[ "$VALUE" == "" ]]; then
                echo "  ⏭️  Skipping placeholder: $KEY"
                SKIPPED_KEYS=$((SKIPPED_KEYS + 1))
                continue
            fi

            # Check if key exists in consolidated file
            if grep -q "^$KEY=" "$TEMP_CONSOLIDATED"; then
                # Key exists - check if value is different
                EXISTING_VALUE=$(grep "^$KEY=" "$TEMP_CONSOLIDATED" | head -1 | cut -d'=' -f2-)

                if [ "$VALUE" != "$EXISTING_VALUE" ]; then
                    # Update with new value (assuming newer is better)
                    sed -i "s|^$KEY=.*|$KEY=$VALUE|" "$TEMP_CONSOLIDATED"
                    echo "  ✏️  Updated: $KEY"
                    echo "- $KEY (updated)" >> "$HARVEST_REPORT"
                    UPDATED_KEYS=$((UPDATED_KEYS + 1))
                else
                    echo "  ✓ Exists: $KEY"
                fi
            else
                # New key - add it
                echo "$KEY=$VALUE" >> "$TEMP_CONSOLIDATED"
                echo "  ✅ Added: $KEY"
                echo "- $KEY (new)" >> "$HARVEST_REPORT"
                NEW_KEYS=$((NEW_KEYS + 1))
            fi

            FILE_KEYS=$((FILE_KEYS + 1))
            TOTAL_KEYS=$((TOTAL_KEYS + 1))
        fi
    done < "$env_file"

    echo "  → Extracted $FILE_KEYS key(s) from this file"
    echo "" >> "$HARVEST_REPORT"

done <<< "$ENV_FILES"

echo ""
echo "📊 Step 3: Consolidation Summary"
echo "======================================="
echo "Total credentials found: $TOTAL_KEYS"
echo "New credentials added: $NEW_KEYS"
echo "Existing credentials updated: $UPDATED_KEYS"
echo "Placeholder values skipped: $SKIPPED_KEYS"
echo ""

echo "" >> "$HARVEST_REPORT"
echo "## Summary Statistics" >> "$HARVEST_REPORT"
echo "- Total credentials found: $TOTAL_KEYS" >> "$HARVEST_REPORT"
echo "- New credentials added: $NEW_KEYS" >> "$HARVEST_REPORT"
echo "- Existing credentials updated: $UPDATED_KEYS" >> "$HARVEST_REPORT"
echo "- Placeholder values skipped: $SKIPPED_KEYS" >> "$HARVEST_REPORT"

# Sort and deduplicate
echo "🔧 Step 4: Sorting and deduplicating..."
echo "======================================="

# Sort by key name, keep only last occurrence of each key
sort -u -t'=' -k1,1 "$TEMP_CONSOLIDATED" > "${TEMP_CONSOLIDATED}.sorted"
mv "${TEMP_CONSOLIDATED}.sorted" "$TEMP_CONSOLIDATED"

# Move consolidated file to master location
mv "$TEMP_CONSOLIDATED" "$MASTER_ENV"

echo "✅ Master .env updated at: $MASTER_ENV"
echo ""

echo "📝 Step 5: Validation"
echo "======================================="

# Count keys in final file
FINAL_KEY_COUNT=$(grep -c "^[A-Za-z_]" "$MASTER_ENV" || echo "0")
echo "Final credential count: $FINAL_KEY_COUNT"
echo ""

# List all keys (without values for security)
echo "Keys in master .env:"
echo "-------------------"
grep "^[A-Za-z_]" "$MASTER_ENV" | cut -d'=' -f1 | sort | while read key; do
    echo "  ✓ $key"
done

echo "" >> "$HARVEST_REPORT"
echo "## Final Master .env Keys" >> "$HARVEST_REPORT"
grep "^[A-Za-z_]" "$MASTER_ENV" | cut -d'=' -f1 | sort | while read key; do
    echo "- $key" >> "$HARVEST_REPORT"
done

echo ""
echo "📄 Step 6: Report Generated"
echo "======================================="
echo "Detailed report saved to: $HARVEST_REPORT"
echo ""

echo "✅ HARVEST COMPLETE!"
echo ""
echo "📋 Next Steps:"
echo "  1. Review master .env: nano $MASTER_ENV"
echo "  2. Read harvest report: cat $HARVEST_REPORT"
echo "  3. Backup saved at: $BACKUP_ENV"
echo "  4. Validate: npm run env:validate"
echo "  5. Commit to git (DO NOT commit .env itself!)"
echo ""
echo "🔒 Security Reminder:"
echo "  - .env file is gitignored (credentials safe)"
echo "  - Backup contains old credentials (review and delete when ready)"
echo "  - Report file contains key names only (safe to commit)"
echo ""
