#!/bin/bash

# US Date Input Components Setup Script
# Adds smooth US date input components to new projects

set -e

echo "📅 Setting up US Date Input Components..."

# Function to copy components to mobile project
setup_mobile_components() {
    local project_path="$1"
    
    if [ -d "$project_path/src" ]; then
        echo "📱 Setting up mobile date components..."
        
        # Create components directory if it doesn't exist
        mkdir -p "$project_path/src/components"
        mkdir -p "$project_path/src/services"
        
        # Copy SmoothDateInput component
        if [ -f "templates/mobile/components/SmoothDateInput.tsx" ]; then
            cp "templates/mobile/components/SmoothDateInput.tsx" "$project_path/src/components/"
            echo "✅ Added SmoothDateInput.tsx"
        fi
        
        # Copy DateUtilityService
        if [ -f "templates/mobile/services/DateUtilityService.ts" ]; then
            cp "templates/mobile/services/DateUtilityService.ts" "$project_path/src/services/"
            echo "✅ Added DateUtilityService.ts"
        fi
        
        # Copy documentation
        if [ -f "templates/components/US_DATE_INPUT_GUIDE.md" ]; then
            cp "templates/components/US_DATE_INPUT_GUIDE.md" "$project_path/"
            echo "✅ Added US_DATE_INPUT_GUIDE.md"
        fi
    fi
}

# Function to copy components to web project
setup_web_components() {
    local project_path="$1"
    
    if [ -d "$project_path/src" ] || [ -d "$project_path/app" ]; then
        echo "🌐 Setting up web date components..."
        
        # Determine if it's Next.js or other framework
        if [ -f "$project_path/next.config.js" ] || [ -f "$project_path/next.config.ts" ]; then
            # Next.js project
            mkdir -p "$project_path/src/components"
            mkdir -p "$project_path/src/services"
            
            # Copy Next.js components
            if [ -f "templates/web-frameworks/nextjs/src/components/SmoothDateInput.tsx" ]; then
                cp "templates/web-frameworks/nextjs/src/components/SmoothDateInput.tsx" "$project_path/src/components/"
                echo "✅ Added SmoothDateInput.tsx (Next.js)"
            fi
            
            if [ -f "templates/web-frameworks/nextjs/src/services/DateUtilityService.ts" ]; then
                cp "templates/web-frameworks/nextjs/src/services/DateUtilityService.ts" "$project_path/src/services/"
                echo "✅ Added DateUtilityService.ts (Next.js)"
            fi
        else
            # Other web frameworks - copy generic versions
            mkdir -p "$project_path/components"
            mkdir -p "$project_path/services"
            
            # Copy generic components (can be adapted)
            if [ -f "templates/web-frameworks/nextjs/src/components/SmoothDateInput.tsx" ]; then
                cp "templates/web-frameworks/nextjs/src/components/SmoothDateInput.tsx" "$project_path/components/"
                echo "✅ Added SmoothDateInput.tsx (Generic)"
            fi
            
            if [ -f "templates/web-frameworks/nextjs/src/services/DateUtilityService.ts" ]; then
                cp "templates/web-frameworks/nextjs/src/services/DateUtilityService.ts" "$project_path/services/"
                echo "✅ Added DateUtilityService.ts (Generic)"
            fi
        fi
        
        # Copy documentation
        if [ -f "templates/components/US_DATE_INPUT_GUIDE.md" ]; then
            cp "templates/components/US_DATE_INPUT_GUIDE.md" "$project_path/"
            echo "✅ Added US_DATE_INPUT_GUIDE.md"
        fi
    fi
}

# Main setup function
setup_date_components() {
    local project_path="$1"
    
    if [ -z "$project_path" ]; then
        echo "❌ Please provide a project path"
        echo "Usage: $0 <project-path>"
        exit 1
    fi
    
    if [ ! -d "$project_path" ]; then
        echo "❌ Project path does not exist: $project_path"
        exit 1
    fi
    
    echo "🚀 Setting up US Date Input Components for: $project_path"
    
    # Check if it's a mobile project
    if [ -f "$project_path/package.json" ] && grep -q "react-native\|expo" "$project_path/package.json"; then
        setup_mobile_components "$project_path"
    fi
    
    # Check if it's a web project
    if [ -f "$project_path/package.json" ] && grep -q "next\|react\|vue\|angular" "$project_path/package.json"; then
        setup_web_components "$project_path"
    fi
    
    # Check if it's a Python project
    if [ -f "$project_path/requirements.txt" ] || [ -f "$project_path/pyproject.toml" ]; then
        echo "🐍 Python project detected - date components can be added to frontend"
        if [ -f "templates/components/US_DATE_INPUT_GUIDE.md" ]; then
            cp "templates/components/US_DATE_INPUT_GUIDE.md" "$project_path/"
            echo "✅ Added US_DATE_INPUT_GUIDE.md for reference"
        fi
    fi
    
    echo ""
    echo "🎉 US Date Input Components setup complete!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Review the US_DATE_INPUT_GUIDE.md for usage instructions"
    echo "2. Import the components in your forms:"
    echo "   - Mobile: import SmoothDateInput from './src/components/SmoothDateInput'"
    echo "   - Web: import SmoothDateInput from '@/components/SmoothDateInput'"
    echo "3. Use DateUtilityService for date validation and conversion"
    echo "4. Test the components with your existing forms"
    echo ""
    echo "✨ Enjoy smooth, non-jumpy date inputs with US format!"
}

# Run setup if called directly
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    setup_date_components "$@"
fi
