#!/bin/bash

# Test script for ntfy.sh migration
echo "🧪 Testing ntfy.sh migration..."

# Test basic notification
curl -d "Migration test successful! 🎉" http://192.168.0.146:8080/mytopic

# Test with title and priority
curl -d "High priority test" \
  -H "X-Title: Migration Test" \
  -H "X-Priority: 5" \
  http://192.168.0.146:8080/mytopic

echo "✅ Test notifications sent!"
