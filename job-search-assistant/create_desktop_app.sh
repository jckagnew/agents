#!/bin/bash
# Create macOS Desktop App for Job Search Assistant

APP_NAME="Job Search Assistant"
APP_DIR="$HOME/Applications/$APP_NAME.app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "�� Creating macOS Desktop App for Job Search Assistant..."

# Create app bundle structure
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'INFO_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>job_search_assistant</string>
    <key>CFBundleIdentifier</key>
    <string>com.clevelsalesguy.jobsearchassistant</string>
    <key>CFBundleName</key>
    <string>Job Search Assistant</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
INFO_EOF

# Create the executable script
cat > "$APP_DIR/Contents/MacOS/job_search_assistant" << 'EXEC_EOF'
#!/bin/bash
# Job Search Assistant - Desktop App Launcher

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")")/job-search-assistant"

# Change to project directory
cd "$PROJECT_DIR"

# Check if project exists
if [ ! -f "pyproject.toml" ]; then
    osascript -e 'display dialog "Job Search Assistant project not found. Please ensure it is installed correctly." buttons {"OK"} default button "OK"'
    exit 1
fi

# Start the server
osascript -e 'display notification "Starting Job Search Assistant..." with title "Job Search Assistant"'

# Run the startup script
./start_job_search.sh
EXEC_EOF

# Make executable
chmod +x "$APP_DIR/Contents/MacOS/job_search_assistant"

echo "✅ Desktop app created at: $APP_DIR"
echo "🎯 You can now find 'Job Search Assistant' in your Applications folder"
echo "📱 Double-click to start the server and open your browser automatically"

# Create a simple icon (optional)
echo "🎨 Creating app icon..."
# You can add an icon here if you have one

echo "�� Desktop app setup complete!"
