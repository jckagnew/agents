#!/bin/bash

# Migration script from Pushover to ntfy.sh
# This script helps you convert Pushover API calls to ntfy.sh

echo "🔄 Pushover to ntfy.sh Migration Helper"
echo "======================================"

# Your ntfy.sh server details
NTFY_SERVER="http://192.168.0.128:8080"
DEFAULT_TOPIC="mytopic"

echo ""
echo "📋 Migration Examples:"
echo ""

echo "1. Basic Message:"
echo "   Pushover: curl -s --form-string \"token=YOUR_TOKEN\" --form-string \"user=YOUR_USER\" --form-string \"message=Hello\" https://api.pushover.net/1/messages.json"
echo "   ntfy.sh:  curl -d \"Hello\" $NTFY_SERVER/$DEFAULT_TOPIC"
echo ""

echo "2. Message with Title:"
echo "   Pushover: curl -s --form-string \"token=YOUR_TOKEN\" --form-string \"user=YOUR_USER\" --form-string \"message=Hello\" --form-string \"title=Test\" https://api.pushover.net/1/messages.json"
echo "   ntfy.sh:  curl -d \"Hello\" -H \"X-Title: Test\" $NTFY_SERVER/$DEFAULT_TOPIC"
echo ""

echo "3. High Priority Message:"
echo "   Pushover: curl -s --form-string \"token=YOUR_TOKEN\" --form-string \"user=YOUR_USER\" --form-string \"message=Alert!\" --form-string \"priority=1\" https://api.pushover.net/1/messages.json"
echo "   ntfy.sh:  curl -d \"Alert!\" -H \"X-Priority: 5\" $NTFY_SERVER/$DEFAULT_TOPIC"
echo ""

echo "4. Message with URL:"
echo "   Pushover: curl -s --form-string \"token=YOUR_TOKEN\" --form-string \"user=YOUR_USER\" --form-string \"message=Check this\" --form-string \"url=https://example.com\" https://api.pushover.net/1/messages.json"
echo "   ntfy.sh:  curl -d \"Check this\" -H \"X-Actions: view, Open Link, https://example.com\" $NTFY_SERVER/$DEFAULT_TOPIC"
echo ""

echo "🔧 Priority Mapping:"
echo "   Pushover Priority 1 (Emergency) → ntfy.sh Priority 5 (Max)"
echo "   Pushover Priority 2 (High)      → ntfy.sh Priority 4 (High)"
echo "   Pushover Priority 0 (Normal)    → ntfy.sh Priority 3 (Normal)"
echo "   Pushover Priority -1 (Low)      → ntfy.sh Priority 2 (Low)"
echo "   Pushover Priority -2 (Lowest)   → ntfy.sh Priority 1 (Min)"
echo ""

echo "📱 Test your migration:"
echo "   curl -d \"Migration test!\" $NTFY_SERVER/$DEFAULT_TOPIC"
echo ""

echo "✅ Migration complete! Your iPhone should receive notifications from ntfy.sh"
