#!/bin/bash
# Example usage of Agentic Image Selector

echo "🎯 Agentic Image Selector - Example Usage"
echo "========================================="

# Example 1: Fitness app
echo "1. Creating splash screens for a fitness app..."
python agents/orchestration-agent.py --init \
  --project-type fitness \
  --app-name "MyFitnessApp" \
  --theme "transformation"

python agents/orchestration-agent.py --run

# Example 2: Finance app
echo "2. Creating splash screens for a finance app..."
python agents/orchestration-agent.py --init \
  --project-type finance \
  --app-name "WealthBuilder" \
  --theme "wealth-building" \
  --colors "blue-to-gold"

python agents/orchestration-agent.py --run

# Example 3: Custom project
echo "3. Creating splash screens for a custom project..."
python agents/orchestration-agent.py --init \
  --project-type custom \
  --app-name "MyCustomApp" \
  --theme "innovation" \
  --colors "purple-to-pink" \
  --animation "fade" \
  --cta-primary "Get Started" \
  --cta-secondary "Learn More"

python agents/orchestration-agent.py --run

echo "✅ All examples completed!"
