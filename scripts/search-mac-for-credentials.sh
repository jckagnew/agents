#!/bin/bash

# ===================================================================
# SEARCH LOCAL MAC FOR EXISTING .ENV FILES
# Run this on your Mac to find all existing credentials
# ===================================================================

set -e

echo "🔍 SEARCHING FOR EXISTING .ENV FILES ON YOUR MAC"
echo "================================================="
echo ""

SEARCH_PATHS=(
    "$HOME/projects"
    "$HOME/Documents"
    "$HOME/Desktop"
    "$HOME/Downloads"
    "$HOME/code"
    "$HOME/dev"
    "$HOME/workspace"
)

MASTER_ENV="$HOME/projects/design-first-software-factory/.env"
TEMP_CONSOLIDATED="/tmp/consolidated_credentials.env"
REPORT_FILE="$HOME/projects/design-first-software-factory/CREDENTIAL_SOURCES.txt"

# Clear temp file
> "$TEMP_CONSOLIDATED"
> "$REPORT_FILE"

echo "# Credential Sources Found" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

FOUND_COUNT=0

echo "Searching in:"
for path in "${SEARCH_PATHS[@]}"; do
    if [ -d "$path" ]; then
        echo "  - $path"
    fi
done
echo ""

# Search for .env files
for search_path in "${SEARCH_PATHS[@]}"; do
    if [ ! -d "$search_path" ]; then
        continue
    fi

    echo "Searching $search_path..."

    while IFS= read -r env_file; do
        if [ ! -f "$env_file" ]; then
            continue
        fi

        # Skip if it's just the example file
        if [[ "$env_file" == *".env.example"* ]] || [[ "$env_file" == *".env.template"* ]]; then
            continue
        fi

        # Skip if in node_modules or .git
        if [[ "$env_file" == *"node_modules"* ]] || [[ "$env_file" == *".git"* ]]; then
            continue
        fi

        FOUND_COUNT=$((FOUND_COUNT + 1))

        echo "  ✅ Found: $env_file"
        echo "## File $FOUND_COUNT: $env_file" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"

        # Extract credentials (hide values in report)
        while IFS= read -r line || [ -n "$line" ]; do
            # Skip comments and empty lines
            if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "$line" ]]; then
                continue
            fi

            # Extract key=value
            if [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)= ]]; then
                KEY=$(echo "$line" | cut -d'=' -f1 | xargs)
                VALUE=$(echo "$line" | cut -d'=' -f2- | xargs)

                # Skip placeholders
                if [[ "$VALUE" =~ your-.*-here ]] || [[ "$VALUE" =~ \<.*\> ]] || [[ "$VALUE" == "" ]]; then
                    continue
                fi

                # Add to consolidated file
                echo "$KEY=$VALUE" >> "$TEMP_CONSOLIDATED"

                # Add key name to report (not value for security)
                echo "- $KEY" >> "$REPORT_FILE"
            fi
        done < "$env_file"

        echo "" >> "$REPORT_FILE"

    done < <(find "$search_path" -maxdepth 5 -type f \( -name ".env" -o -name ".env.*" \) 2>/dev/null)
done

echo ""
echo "📊 SEARCH COMPLETE"
echo "=================="
echo "Found $FOUND_COUNT .env file(s)"
echo ""

if [ $FOUND_COUNT -eq 0 ]; then
    echo "❌ No .env files found in searched locations"
    echo ""
    echo "Searched:"
    for path in "${SEARCH_PATHS[@]}"; do
        if [ -d "$path" ]; then
            echo "  - $path"
        fi
    done
    echo ""
    echo "Try searching manually:"
    echo "  find ~ -name '.env' -type f 2>/dev/null | grep -v node_modules"
    exit 1
fi

# Count unique keys
UNIQUE_KEYS=$(sort -u -t'=' -k1,1 "$TEMP_CONSOLIDATED" | wc -l | xargs)
echo "Total unique credentials: $UNIQUE_KEYS"
echo ""

# Show credential types found
echo "Credential types found:"
grep -E "SUPABASE|OPENAI|ANTHROPIC|GOOGLE|REDIS|STRIPE" "$TEMP_CONSOLIDATED" | cut -d'=' -f1 | sort -u | while read key; do
    echo "  ✅ $key"
done

echo ""
echo "📋 CONSOLIDATION"
echo "================"

if [ -f "$MASTER_ENV" ]; then
    echo "Backing up existing .env..."
    cp "$MASTER_ENV" "$MASTER_ENV.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Consolidate and deduplicate
sort -u -t'=' -k1,1 "$TEMP_CONSOLIDATED" > "$MASTER_ENV"

echo "✅ Consolidated credentials written to:"
echo "   $MASTER_ENV"
echo ""
echo "📄 Detailed report saved to:"
echo "   $REPORT_FILE"
echo ""
echo "🔒 Security Note:"
echo "   - .env file is gitignored (safe)"
echo "   - Report only shows key names, not values"
echo ""
echo "📋 Next steps:"
echo "   1. Review: cat $MASTER_ENV"
echo "   2. Verify: npm run env:validate"
echo "   3. Use in development!"
echo ""

# Show summary in report
echo "" >> "$REPORT_FILE"
echo "## Summary" >> "$REPORT_FILE"
echo "- Files found: $FOUND_COUNT" >> "$REPORT_FILE"
echo "- Unique credentials: $UNIQUE_KEYS" >> "$REPORT_FILE"
echo "- Consolidated to: $MASTER_ENV" >> "$REPORT_FILE"
