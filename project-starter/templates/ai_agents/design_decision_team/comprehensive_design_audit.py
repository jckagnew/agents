#!/usr/bin/env python3
"""
Comprehensive Design Audit and Improvement System
Uses Design Decision Team to systematically improve all screens
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DesignAuditSystem:
    def __init__(self):
        self.project_path = "/Users/jackagnew/projects/agents/weight-tracker-mobile"
        self.screens_to_audit = [
            "DashboardScreen",
            "ProfileScreen", 
            "LoggingScreen",
            "HistoryScreen",
            "SettingsScreen",
            "PaywallScreen"
        ]
        
    def analyze_current_screens(self):
        """Analyze all current screens and identify design issues"""
        print("🔍 Analyzing Current Screen Designs")
        print("=" * 40)
        
        audit_results = {}
        
        for screen in self.screens_to_audit:
            print(f"\n📱 Analyzing {screen}...")
            
            # Check if screen file exists
            screen_file = f"{self.project_path}/src/screens/{screen}.tsx"
            if os.path.exists(screen_file):
                print(f"✅ {screen} file exists")
                
                # Analyze the screen (simplified analysis)
                analysis = self.analyze_screen_design(screen, screen_file)
                audit_results[screen] = analysis
            else:
                print(f"❌ {screen} file not found")
                audit_results[screen] = {"status": "not_found"}
        
        return audit_results
    
    def analyze_screen_design(self, screen_name, file_path):
        """Analyze a specific screen's design"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            analysis = {
                "screen_name": screen_name,
                "file_path": file_path,
                "analysis_date": datetime.now().isoformat(),
                "issues": [],
                "recommendations": [],
                "design_score": 0
            }
            
            # Check for common design issues
            issues = []
            recommendations = []
            score = 100
            
            # Typography Analysis
            if "fontSize" not in content or "fontWeight" not in content:
                issues.append("Typography not properly defined")
                recommendations.append("Implement consistent typography system")
                score -= 15
            
            # Layout Analysis
            if "flexDirection" not in content and "justifyContent" not in content:
                issues.append("Layout structure needs improvement")
                recommendations.append("Optimize flexbox layout for better screen usage")
                score -= 10
            
            # Color System Analysis
            if "#" not in content and "color" not in content.lower():
                issues.append("Color system not implemented")
                recommendations.append("Implement consistent color palette")
                score -= 10
            
            # Spacing Analysis
            if "margin" not in content and "padding" not in content:
                issues.append("Spacing system not consistent")
                recommendations.append("Implement consistent spacing scale")
                score -= 10
            
            # Accessibility Analysis
            if "accessibilityLabel" not in content:
                issues.append("Accessibility considerations missing")
                recommendations.append("Add accessibility labels and roles")
                score -= 5
            
            # Animation Analysis
            if "Animated" not in content:
                issues.append("No animations or micro-interactions")
                recommendations.append("Add subtle animations for better UX")
                score -= 5
            
            analysis["issues"] = issues
            analysis["recommendations"] = recommendations
            analysis["design_score"] = max(0, score)
            
            print(f"   Design Score: {analysis['design_score']}/100")
            print(f"   Issues Found: {len(issues)}")
            
            return analysis
            
        except Exception as e:
            return {
                "screen_name": screen_name,
                "error": str(e),
                "design_score": 0
            }
    
    def generate_design_improvement_plan(self, audit_results):
        """Generate comprehensive design improvement plan"""
        print("\n🎨 Generating Design Improvement Plan")
        print("=" * 40)
        
        plan = {
            "project": "Weight Tracker Mobile App",
            "audit_date": datetime.now().isoformat(),
            "overall_score": 0,
            "screens": {},
            "global_improvements": [
                "Implement Design System",
                "Typography Scale",
                "Color Palette",
                "Spacing System",
                "Component Library",
                "Animation Guidelines"
            ],
            "priority_actions": []
        }
        
        total_score = 0
        screen_count = 0
        
        for screen_name, analysis in audit_results.items():
            if "design_score" in analysis:
                plan["screens"][screen_name] = {
                    "current_score": analysis["design_score"],
                    "issues": analysis.get("issues", []),
                    "recommendations": analysis.get("recommendations", []),
                    "priority": "high" if analysis["design_score"] < 70 else "medium"
                }
                
                total_score += analysis["design_score"]
                screen_count += 1
        
        if screen_count > 0:
            plan["overall_score"] = total_score / screen_count
        
        # Generate priority actions
        plan["priority_actions"] = [
            "1. Create Design System Foundation",
            "2. Implement Typography Scale",
            "3. Define Color Palette",
            "4. Create Spacing System",
            "5. Build Component Library",
            "6. Add Micro-interactions",
            "7. Improve Screen Layouts",
            "8. Enhance Accessibility"
        ]
        
        print(f"Overall Design Score: {plan['overall_score']:.1f}/100")
        print(f"Screens Analyzed: {screen_count}")
        
        return plan
    
    def create_design_system_foundation(self):
        """Create the foundational design system files"""
        print("\n🏗️ Creating Design System Foundation")
        print("=" * 40)
        
        # Create design system directory
        design_system_dir = f"{self.project_path}/src/design-system"
        os.makedirs(design_system_dir, exist_ok=True)
        
        # Create typography system
        typography_content = '''// Typography System
export const typography = {
  // Font Families
  fontFamily: {
    primary: 'System',
    secondary: 'System',
    mono: 'Courier New',
  },
  
  // Font Sizes
  fontSize: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
  },
  
  // Font Weights
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
  },
  
  // Line Heights
  lineHeight: {
    tight: 1.2,
    normal: 1.4,
    relaxed: 1.6,
    loose: 1.8,
  },
  
  // Letter Spacing
  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
    wider: 1,
  },
};

// Typography Styles
export const textStyles = {
  h1: {
    fontSize: typography.fontSize['4xl'],
    fontWeight: typography.fontWeight.bold,
    lineHeight: typography.lineHeight.tight,
    letterSpacing: typography.letterSpacing.tight,
  },
  h2: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
    lineHeight: typography.lineHeight.tight,
  },
  h3: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.semibold,
    lineHeight: typography.lineHeight.normal,
  },
  body: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.normal,
    lineHeight: typography.lineHeight.normal,
  },
  caption: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.normal,
    lineHeight: typography.lineHeight.normal,
  },
  button: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.semibold,
    lineHeight: typography.lineHeight.tight,
    letterSpacing: typography.letterSpacing.wide,
  },
};
'''
        
        with open(f"{design_system_dir}/typography.ts", 'w') as f:
            f.write(typography_content)
        
        # Create color system
        color_content = '''// Color System
export const colors = {
  // Primary Colors
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    200: '#bae6fd',
    300: '#7dd3fc',
    400: '#38bdf8',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
    800: '#075985',
    900: '#0c4a6e',
  },
  
  // Secondary Colors
  secondary: {
    50: '#f0fdf4',
    100: '#dcfce7',
    200: '#bbf7d0',
    300: '#86efac',
    400: '#4ade80',
    500: '#22c55e',
    600: '#16a34a',
    700: '#15803d',
    800: '#166534',
    900: '#14532d',
  },
  
  // Neutral Colors
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#e5e5e5',
    300: '#d4d4d4',
    400: '#a3a3a3',
    500: '#737373',
    600: '#525252',
    700: '#404040',
    800: '#262626',
    900: '#171717',
  },
  
  // Semantic Colors
  success: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Background Colors
  background: {
    primary: '#ffffff',
    secondary: '#f8fafc',
    tertiary: '#f1f5f9',
  },
  
  // Text Colors
  text: {
    primary: '#171717',
    secondary: '#525252',
    tertiary: '#a3a3a3',
    inverse: '#ffffff',
  },
};

// Color Usage Guidelines
export const colorUsage = {
  primary: colors.primary[600],
  primaryLight: colors.primary[400],
  primaryDark: colors.primary[800],
  secondary: colors.secondary[600],
  background: colors.background.primary,
  surface: colors.background.secondary,
  text: colors.text.primary,
  textSecondary: colors.text.secondary,
  border: colors.neutral[200],
  success: colors.success,
  warning: colors.warning,
  error: colors.error,
};
'''
        
        with open(f"{design_system_dir}/colors.ts", 'w') as f:
            f.write(color_content)
        
        # Create spacing system
        spacing_content = '''// Spacing System
export const spacing = {
  // Base spacing unit (8px)
  unit: 8,
  
  // Spacing scale
  xs: 4,    // 0.5 * unit
  sm: 8,    // 1 * unit
  md: 16,   // 2 * unit
  lg: 24,   // 3 * unit
  xl: 32,   // 4 * unit
  '2xl': 48, // 6 * unit
  '3xl': 64, // 8 * unit
  '4xl': 96, // 12 * unit
};

// Layout spacing
export const layout = {
  // Container padding
  containerPadding: spacing.lg,
  
  // Section spacing
  sectionSpacing: spacing.xl,
  
  // Component spacing
  componentSpacing: spacing.md,
  
  // Card padding
  cardPadding: spacing.lg,
  
  // Button padding
  buttonPadding: {
    horizontal: spacing.lg,
    vertical: spacing.md,
  },
  
  // Input padding
  inputPadding: {
    horizontal: spacing.md,
    vertical: spacing.sm,
  },
};

// Border radius
export const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

// Shadows
export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  xl: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
    elevation: 8,
  },
};
'''
        
        with open(f"{design_system_dir}/spacing.ts", 'w') as f:
            f.write(spacing_content)
        
        # Create component styles
        component_content = '''// Component Styles
import { colors, spacing, borderRadius, shadows, layout } from './index';

export const componentStyles = {
  // Button Styles
  button: {
    primary: {
      backgroundColor: colors.primary[600],
      paddingHorizontal: layout.buttonPadding.horizontal,
      paddingVertical: layout.buttonPadding.vertical,
      borderRadius: borderRadius.lg,
      ...shadows.md,
    },
    secondary: {
      backgroundColor: colors.neutral[100],
      paddingHorizontal: layout.buttonPadding.horizontal,
      paddingVertical: layout.buttonPadding.vertical,
      borderRadius: borderRadius.lg,
      borderWidth: 1,
      borderColor: colors.neutral[300],
    },
  },
  
  // Card Styles
  card: {
    backgroundColor: colors.background.primary,
    padding: layout.cardPadding,
    borderRadius: borderRadius.lg,
    ...shadows.md,
    marginBottom: spacing.md,
  },
  
  // Input Styles
  input: {
    backgroundColor: colors.background.secondary,
    paddingHorizontal: layout.inputPadding.horizontal,
    paddingVertical: layout.inputPadding.vertical,
    borderRadius: borderRadius.md,
    borderWidth: 1,
    borderColor: colors.neutral[200],
    fontSize: 16,
  },
  
  // Container Styles
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
    paddingHorizontal: layout.containerPadding,
  },
  
  // Section Styles
  section: {
    marginBottom: layout.sectionSpacing,
  },
};
'''
        
        with open(f"{design_system_dir}/components.ts", 'w') as f:
            f.write(component_content)
        
        # Create index file
        index_content = '''// Design System Index
export * from './colors';
export * from './typography';
export * from './spacing';
export * from './components';
'''
        
        with open(f"{design_system_dir}/index.ts", 'w') as f:
            f.write(index_content)
        
        print("✅ Design System Foundation Created")
        print(f"📁 Location: {design_system_dir}")
        print("📋 Files Created:")
        print("   • typography.ts - Typography system")
        print("   • colors.ts - Color palette")
        print("   • spacing.ts - Spacing and layout")
        print("   • components.ts - Component styles")
        print("   • index.ts - Main export file")
    
    def run_comprehensive_audit(self):
        """Run the complete design audit and improvement process"""
        print("🎨 Comprehensive Design Audit & Improvement System")
        print("=" * 55)
        
        # Step 1: Analyze current screens
        audit_results = self.analyze_current_screens()
        
        # Step 2: Generate improvement plan
        improvement_plan = self.generate_design_improvement_plan(audit_results)
        
        # Step 3: Create design system foundation
        self.create_design_system_foundation()
        
        # Step 4: Save results
        results = {
            "audit_results": audit_results,
            "improvement_plan": improvement_plan,
            "timestamp": datetime.now().isoformat()
        }
        
        with open("design_audit_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: design_audit_results.json")
        
        # Step 5: Generate next steps
        print(f"\n🚀 Next Steps:")
        print(f"1. Review design audit results")
        print(f"2. Implement design system in components")
        print(f"3. Update each screen with improved design")
        print(f"4. Test and iterate")
        
        return results

def main():
    print("🎨 Design Decision Team - Comprehensive Screen Improvement")
    print("=" * 60)
    
    audit_system = DesignAuditSystem()
    results = audit_system.run_comprehensive_audit()
    
    print(f"\n🎉 Design audit complete!")
    print(f"📊 Overall Score: {results['improvement_plan']['overall_score']:.1f}/100")
    print(f"📱 Screens Analyzed: {len(results['audit_results'])}")

if __name__ == "__main__":
    main()
