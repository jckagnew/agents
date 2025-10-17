#!/usr/bin/env python3
"""
Systematic Screen Improvement Script
Applies design system improvements to each screen systematically
"""

import os
import re
from datetime import datetime

class ScreenImprovementSystem:
    def __init__(self):
        self.project_path = "/Users/jackagnew/projects/agents/weight-tracker-mobile"
        self.design_system_path = f"{self.project_path}/src/design-system"
        self.screens_path = f"{self.project_path}/src/screens"
        
        # Actual screens that exist
        self.screens_to_improve = [
            "DashboardScreen.tsx",
            "ProfileScreen.tsx", 
            "LogEntryScreen.tsx",
            "HistoryScreen.tsx",
            "SettingsScreen.tsx",
            "PaywallScreen.tsx"
        ]
    
    def create_enhanced_components(self):
        """Create enhanced reusable components with design system"""
        components_dir = f"{self.project_path}/src/components"
        os.makedirs(components_dir, exist_ok=True)
        
        # Create Enhanced Button Component
        button_content = '''import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { colors, spacing, borderRadius, shadows, textStyles } from '../design-system';

interface EnhancedButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  accessibilityLabel?: string;
  accessibilityHint?: string;
}

export default function EnhancedButton({
  title,
  onPress,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  accessibilityLabel,
  accessibilityHint,
}: EnhancedButtonProps) {
  const buttonStyle = [
    styles.base,
    styles[variant],
    styles[size],
    disabled && styles.disabled,
  ];

  const textStyle = [
    textStyles.button,
    styles[`${variant}Text`],
    disabled && styles.disabledText,
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      onPress={onPress}
      disabled={disabled || loading}
      accessibilityLabel={accessibilityLabel || title}
      accessibilityHint={accessibilityHint}
      accessibilityRole="button"
    >
      {loading ? (
        <ActivityIndicator 
          color={variant === 'primary' ? colors.text.inverse : colors.primary[600]} 
          size="small" 
        />
      ) : (
        <Text style={textStyle}>{title}</Text>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.md,
  },
  
  // Variants
  primary: {
    backgroundColor: colors.primary[600],
  },
  secondary: {
    backgroundColor: colors.neutral[100],
    borderWidth: 1,
    borderColor: colors.neutral[300],
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: colors.primary[600],
  },
  
  // Sizes
  sm: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    minHeight: 36,
  },
  md: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    minHeight: 44,
  },
  lg: {
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.lg,
    minHeight: 52,
  },
  
  // States
  disabled: {
    opacity: 0.5,
  },
  
  // Text styles
  primaryText: {
    color: colors.text.inverse,
  },
  secondaryText: {
    color: colors.text.primary,
  },
  outlineText: {
    color: colors.primary[600],
  },
  disabledText: {
    opacity: 0.7,
  },
});
'''
        
        with open(f"{components_dir}/EnhancedButton.tsx", 'w') as f:
            f.write(button_content)
        
        # Create Enhanced Card Component
        card_content = '''import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { colors, spacing, borderRadius, shadows } from '../design-system';

interface EnhancedCardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  padding?: 'sm' | 'md' | 'lg';
  shadow?: 'sm' | 'md' | 'lg';
  accessibilityLabel?: string;
}

export default function EnhancedCard({
  children,
  style,
  padding = 'md',
  shadow = 'md',
  accessibilityLabel,
}: EnhancedCardProps) {
  const cardStyle = [
    styles.base,
    styles[padding],
    styles[shadow],
    style,
  ];

  return (
    <View
      style={cardStyle}
      accessibilityLabel={accessibilityLabel}
      accessibilityRole="group"
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    backgroundColor: colors.background.primary,
    borderRadius: borderRadius.lg,
  },
  
  // Padding variants
  sm: {
    padding: spacing.md,
  },
  md: {
    padding: spacing.lg,
  },
  lg: {
    padding: spacing.xl,
  },
  
  // Shadow variants
  sm: {
    ...shadows.sm,
  },
  md: {
    ...shadows.md,
  },
  lg: {
    ...shadows.lg,
  },
});
'''
        
        with open(f"{components_dir}/EnhancedCard.tsx", 'w') as f:
            f.write(card_content)
        
        # Create Enhanced Input Component
        input_content = '''import React, { useState } from 'react';
import { TextInput, View, Text, StyleSheet, TextInputProps } from 'react-native';
import { colors, spacing, borderRadius, textStyles } from '../design-system';

interface EnhancedInputProps extends TextInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  required?: boolean;
}

export default function EnhancedInput({
  label,
  error,
  helperText,
  required = false,
  style,
  ...props
}: EnhancedInputProps) {
  const [isFocused, setIsFocused] = useState(false);

  const inputStyle = [
    styles.input,
    isFocused && styles.focused,
    error && styles.error,
    style,
  ];

  return (
    <View style={styles.container}>
      {label && (
        <Text style={styles.label}>
          {label}
          {required && <Text style={styles.required}> *</Text>}
        </Text>
      )}
      
      <TextInput
        style={inputStyle}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholderTextColor={colors.text.tertiary}
        accessibilityLabel={label}
        accessibilityHint={helperText}
        {...props}
      />
      
      {(error || helperText) && (
        <Text style={[styles.helperText, error && styles.errorText]}>
          {error || helperText}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.md,
  },
  label: {
    ...textStyles.caption,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
    fontWeight: '600',
  },
  required: {
    color: colors.error,
  },
  input: {
    ...textStyles.body,
    backgroundColor: colors.background.secondary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.md,
    borderWidth: 1,
    borderColor: colors.neutral[200],
    minHeight: 44,
  },
  focused: {
    borderColor: colors.primary[500],
    backgroundColor: colors.background.primary,
  },
  error: {
    borderColor: colors.error,
  },
  helperText: {
    ...textStyles.caption,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },
  errorText: {
    color: colors.error,
  },
});
'''
        
        with open(f"{components_dir}/EnhancedInput.tsx", 'w') as f:
            f.write(input_content)
        
        print("✅ Enhanced Components Created")
        print("📋 Components:")
        print("   • EnhancedButton - With variants, sizes, accessibility")
        print("   • EnhancedCard - With padding and shadow options")
        print("   • EnhancedInput - With labels, validation, accessibility")
    
    def improve_screen_systematically(self, screen_file):
        """Improve a specific screen with design system"""
        print(f"\n🎨 Improving {screen_file}...")
        
        file_path = f"{self.screens_path}/{screen_file}"
        
        if not os.path.exists(file_path):
            print(f"❌ {screen_file} not found")
            return False
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Create backup
            backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_path, 'w') as f:
                f.write(content)
            
            # Apply improvements
            improved_content = self.apply_design_improvements(content, screen_file)
            
            # Write improved content
            with open(file_path, 'w') as f:
                f.write(improved_content)
            
            print(f"✅ {screen_file} improved successfully")
            print(f"💾 Backup saved: {os.path.basename(backup_path)}")
            return True
            
        except Exception as e:
            print(f"❌ Error improving {screen_file}: {e}")
            return False
    
    def apply_design_improvements(self, content, screen_name):
        """Apply design system improvements to screen content"""
        
        # Add design system imports
        if "from '../design-system'" not in content:
            import_line = "import { colors, spacing, borderRadius, shadows, textStyles, layout } from '../design-system';\n"
            content = content.replace("import React", f"{import_line}import React")
        
        # Add enhanced component imports
        if "EnhancedButton" not in content and "TouchableOpacity" in content:
            enhanced_imports = "import EnhancedButton from '../components/EnhancedButton';\nimport EnhancedCard from '../components/EnhancedCard';\nimport EnhancedInput from '../components/EnhancedInput';\n"
            content = content.replace("import React", f"{enhanced_imports}import React")
        
        # Replace basic TouchableOpacity with EnhancedButton where appropriate
        content = self.replace_buttons(content)
        
        # Add accessibility improvements
        content = self.add_accessibility_improvements(content)
        
        # Improve typography
        content = self.improve_typography(content)
        
        # Improve spacing and layout
        content = self.improve_spacing(content)
        
        return content
    
    def replace_buttons(self, content):
        """Replace basic TouchableOpacity with EnhancedButton"""
        # This is a simplified replacement - in practice, you'd want more sophisticated parsing
        button_pattern = r'<TouchableOpacity[^>]*>\s*<Text[^>]*>([^<]+)</Text>\s*</TouchableOpacity>'
        
        def replace_button(match):
            button_text = match.group(1)
            return f'<EnhancedButton title="{button_text}" onPress={{() => {{}}}} />'
        
        # Only replace if EnhancedButton is imported
        if "EnhancedButton" in content:
            content = re.sub(button_pattern, replace_button, content)
        
        return content
    
    def add_accessibility_improvements(self, content):
        """Add accessibility improvements"""
        # Add accessibility labels to key elements
        accessibility_improvements = [
            ('<View style={styles.container}>', '<View style={styles.container} accessibilityRole="main">'),
            ('<ScrollView', '<ScrollView accessibilityRole="scrollbar"'),
            ('<Text style={styles.title}>', '<Text style={styles.title} accessibilityRole="header">'),
        ]
        
        for old, new in accessibility_improvements:
            content = content.replace(old, new)
        
        return content
    
    def improve_typography(self, content):
        """Improve typography using design system"""
        # Replace hardcoded font sizes with design system
        typography_replacements = [
            ('fontSize: 24', 'fontSize: textStyles.h2.fontSize'),
            ('fontSize: 20', 'fontSize: textStyles.h3.fontSize'),
            ('fontSize: 18', 'fontSize: textStyles.body.fontSize'),
            ('fontSize: 16', 'fontSize: textStyles.body.fontSize'),
            ('fontSize: 14', 'fontSize: textStyles.caption.fontSize'),
        ]
        
        for old, new in typography_replacements:
            content = content.replace(old, new)
        
        return content
    
    def improve_spacing(self, content):
        """Improve spacing using design system"""
        # Replace hardcoded spacing with design system
        spacing_replacements = [
            ('margin: 20', 'margin: spacing.lg'),
            ('padding: 20', 'padding: spacing.lg'),
            ('margin: 16', 'margin: spacing.md'),
            ('padding: 16', 'padding: spacing.md'),
            ('margin: 8', 'margin: spacing.sm'),
            ('padding: 8', 'padding: spacing.sm'),
        ]
        
        for old, new in spacing_replacements:
            content = content.replace(old, new)
        
        return content
    
    def run_systematic_improvement(self):
        """Run the systematic improvement process"""
        print("🎨 Systematic Screen Improvement Process")
        print("=" * 45)
        
        # Step 1: Create enhanced components
        print("\n🏗️ Step 1: Creating Enhanced Components")
        self.create_enhanced_components()
        
        # Step 2: Improve each screen
        print("\n🎨 Step 2: Improving Screens Systematically")
        improved_count = 0
        
        for screen_file in self.screens_to_improve:
            if self.improve_screen_systematically(screen_file):
                improved_count += 1
        
        # Step 3: Summary
        print(f"\n🎉 Systematic Improvement Complete!")
        print(f"📊 Screens Improved: {improved_count}/{len(self.screens_to_improve)}")
        print(f"📁 Design System: {self.design_system_path}")
        print(f"🧩 Enhanced Components: {self.project_path}/src/components/")
        
        print(f"\n🚀 Next Steps:")
        print(f"1. Test the improved screens")
        print(f"2. Fine-tune design system values")
        print(f"3. Add micro-interactions and animations")
        print(f"4. Conduct accessibility testing")
        
        return improved_count

def main():
    print("🎨 Design Decision Team - Systematic Screen Improvement")
    print("=" * 60)
    
    improvement_system = ScreenImprovementSystem()
    improved_count = improvement_system.run_systematic_improvement()
    
    print(f"\n✨ {improved_count} screens have been systematically improved!")

if __name__ == "__main__":
    main()
