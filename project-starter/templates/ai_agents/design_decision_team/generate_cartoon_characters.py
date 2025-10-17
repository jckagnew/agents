#!/usr/bin/env python3
"""
Cartoon Character Generator for Weight Tracker Splash Screen
Generates "Before" and "After" cartoon characters using DALL-E 3
"""

import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class CartoonCharacterGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
    def generate_cartoon_character(self, prompt, filename_prefix):
        """Generate a cartoon character using DALL-E 3"""
        print(f"🎨 Generating cartoon character: {filename_prefix}")
        print(f"📝 Prompt: {prompt}")
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "hd",
            "style": "natural"
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            image_url = data['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Saved: {filename}")
            return filename
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def generate_weight_tracker_characters(self):
        """Generate Before and After cartoon characters for weight tracker"""
        print("🎯 Generating Weight Tracker Cartoon Characters")
        print("=" * 50)
        
        # Before character prompts (overweight, friendly, approachable)
        before_prompts = [
            "A friendly, cheerful cartoon person who is overweight, standing confidently with arms spread wide, wearing casual clothes, bright smile, welcoming expression, clean white background, cartoon style similar to Pixar or Disney, non-threatening and positive",
            "A happy cartoon character who is plus-size, wearing a colorful t-shirt and jeans, giving a thumbs up, warm smile, friendly eyes, standing in a confident pose, white background, modern cartoon art style, encouraging and motivational",
            "A lovable cartoon person who is heavier, wearing workout clothes but in a relaxed pose, friendly face, approachable demeanor, clean background, cartoon style like modern mobile game characters, positive and inspiring"
        ]
        
        # After character prompts (fit, healthy, confident)
        after_prompts = [
            "A confident, healthy cartoon person who is fit and muscular, standing proudly with arms raised in victory, wearing athletic clothes, big smile, strong posture, clean white background, cartoon style similar to Pixar or Disney, inspiring and motivational",
            "A happy cartoon character who is lean and athletic, wearing workout gear, flexing muscles playfully, bright smile, confident expression, standing in a strong pose, white background, modern cartoon art style, energetic and positive",
            "A proud cartoon person who is healthy and fit, wearing sports attire, doing a victory pose, friendly face, confident demeanor, clean background, cartoon style like modern mobile game characters, triumphant and encouraging"
        ]
        
        generated_files = []
        
        # Generate Before characters
        print("\n📸 Generating 'BEFORE' Characters (Overweight, Friendly)")
        print("-" * 40)
        for i, prompt in enumerate(before_prompts, 1):
            filename = self.generate_cartoon_character(prompt, f"before_character_{i}")
            if filename:
                generated_files.append(filename)
        
        # Generate After characters
        print("\n💪 Generating 'AFTER' Characters (Fit, Confident)")
        print("-" * 40)
        for i, prompt in enumerate(after_prompts, 1):
            filename = self.generate_cartoon_character(prompt, f"after_character_{i}")
            if filename:
                generated_files.append(filename)
        
        return generated_files
    
    def create_morphing_animation_plan(self, before_files, after_files):
        """Create a plan for morphing animation"""
        print("\n🎬 Morphing Animation Plan")
        print("=" * 30)
        
        plan = {
            "technique": "Lottie Animation",
            "tools": ["Adobe After Effects", "Bodymovin Plugin", "LottieFiles"],
            "steps": [
                "1. Import Before and After character images",
                "2. Create keyframe animation in After Effects",
                "3. Use Puppet Pin Tool for smooth morphing",
                "4. Add easing and timing adjustments",
                "5. Export as Lottie JSON using Bodymovin",
                "6. Integrate into React Native app"
            ],
            "before_files": before_files,
            "after_files": after_files,
            "estimated_time": "2-4 hours",
            "file_size": "50-500KB"
        }
        
        print(f"🎯 Technique: {plan['technique']}")
        print(f"🛠️ Tools: {', '.join(plan['tools'])}")
        print(f"⏰ Estimated Time: {plan['estimated_time']}")
        print(f"📦 File Size: {plan['file_size']}")
        
        print("\n📋 Implementation Steps:")
        for step in plan['steps']:
            print(f"   {step}")
        
        return plan

def main():
    print("🎨 Cartoon Character Generator for Weight Tracker")
    print("=" * 55)
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API key not found. Please check your .env file.")
        return
    
    generator = CartoonCharacterGenerator()
    
    # Generate characters
    generated_files = generator.generate_weight_tracker_characters()
    
    if generated_files:
        print(f"\n🎉 Successfully generated {len(generated_files)} cartoon characters!")
        
        # Separate before and after files
        before_files = [f for f in generated_files if f.startswith('before_')]
        after_files = [f for f in generated_files if f.startswith('after_')]
        
        # Create morphing plan
        plan = generator.create_morphing_animation_plan(before_files, after_files)
        
        # Save plan to file
        with open('morphing_animation_plan.json', 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"\n💾 Animation plan saved to: morphing_animation_plan.json")
        print(f"📁 Generated files:")
        for file in generated_files:
            print(f"   • {file}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Review the generated cartoon characters")
        print(f"   2. Choose your favorite Before/After pair")
        print(f"   3. Create morphing animation using the plan")
        print(f"   4. Integrate into your weight tracker app!")
        
    else:
        print("❌ No characters were generated. Please check your API key and try again.")

if __name__ == "__main__":
    main()
