import React, { useState } from 'react';
import { TypographyEditor } from '../Properties/TypographyEditor';
import { ColorPicker } from '../Properties/ColorPicker';

interface DesignSkillsPanelProps {
  className?: string;
}

export const DesignSkillsPanel: React.FC<DesignSkillsPanelProps> = ({ className = '' }) => {
  const [activeSkill, setActiveSkill] = useState<string>('typography');

  const skills = [
    {
      id: 'typography',
      title: 'Typography',
      subtitle: 'The Foundation of Great Web Design',
      icon: '📝',
      description: 'Master font selection and type scale systems',
      principles: [
        {
          title: 'Font Selection',
          description: 'Find unique fonts from FontShare.com and Uncut.wtf instead of overused free fonts',
          tips: [
            'Use FontShare.com for clean, high-quality free fonts',
            'Try Uncut.wtf for experimental, personality-packed fonts',
            'Avoid the same free fonts everyone else uses'
          ]
        },
        {
          title: 'Type Scale System',
          description: 'Create consistent, intentional typography with Major Third Scale',
          tips: [
            'Start with 16px base font size for paragraphs',
            'Use Major Third Scale (25% increase) for headings',
            'Use REM values instead of pixels for automatic calculations',
            'Visit type-scale.net for instant type scale generation'
          ]
        },
        {
          title: 'Letter Spacing & Line Height',
          description: 'Optimize readability and visual impact',
          tips: [
            'Keep letter spacing default for body text',
            'Tighten letter spacing for larger headings',
            'Use 150% line height for paragraphs (1.5x font size)',
            'Tighten line height for headings to feel more impactful'
          ]
        }
      ]
    },
    {
      id: 'layout',
      title: 'Layout',
      subtitle: 'Structure, Spacing, and Visual Hierarchy',
      icon: '📐',
      description: 'Create systematic layouts that guide the eye',
      principles: [
        {
          title: 'Grid System',
          description: 'Use flexible column grids for consistent structure',
          tips: [
            'Desktop: 12 columns, Tablet: 8 columns, Mobile: 4 columns',
            '12 columns divide evenly (2x6, 3x4, 4x3)',
            'Set up in Figma: Frame → Layout Guide → Add Grid → Columns'
          ]
        },
        {
          title: '8-Point Spacing System',
          description: 'Use multiples of 8 for consistent rhythm',
          tips: [
            'Spacing: 8, 16, 24, 32, 40, 48px etc.',
            'Used by Google Material Design and Apple',
            'Set up in Figma: Layout Guide → Grid → Change size to 8px'
          ]
        },
        {
          title: 'Visual Hierarchy',
          description: 'Guide users through scanning, not reading',
          tips: [
            'Proximity: Keep related elements close together',
            'Size: Larger = more important',
            'Contrast: Use size, weight, or color differences',
            'Alignment: Clean lines create clear structure'
          ]
        }
      ]
    },
    {
      id: 'color',
      title: 'Color Theory',
      subtitle: 'Using Color Intentionally',
      icon: '🎨',
      description: 'Create purposeful color palettes that convert',
      principles: [
        {
          title: '60-30-10 Rule',
          description: 'Limit your palette with specific jobs for each color',
          tips: [
            '60% Neutral colors (whites, blacks) for backgrounds and text',
            '30% Secondary colors for cards, headers, visuals',
            '10% Accent colors for CTAs and important actions',
            'Use opacity variations instead of adding more colors'
          ]
        },
        {
          title: 'Contrast Priority',
          description: 'Ensure readability over aesthetics',
          tips: [
            'Large text: 3:1 contrast ratio minimum',
            'Small text: 4.5:1 contrast ratio minimum',
            'Use Figma contrast checker: Text → Fill → Contrast icon',
            'Test with Chrome CSS Overview tool'
          ]
        },
        {
          title: 'Borrow & Refine',
          description: 'Start with proven palettes, then customize',
          tips: [
            'Use Chrome DevTools → CSS Overview to extract site colors',
            'Find inspiration from successful websites',
            'One good color used well beats five random colors',
            'Focus on intentional color usage over variety'
          ]
        }
      ]
    },
    {
      id: 'coding',
      title: 'Coding Basics',
      subtitle: 'Essential Skills for Web Designers',
      icon: '💻',
      description: 'Get comfortable with code to stand out',
      principles: [
        {
          title: 'Essential Languages',
          description: 'Master the core web technologies',
          tips: [
            'HTML: Structure and content',
            'CSS: Styling and layout',
            'JavaScript: Interactions and behavior',
            'PHP: WordPress and dynamic content'
          ]
        },
        {
          title: '80% Solution Strategy',
          description: 'Find solutions that are mostly done, then customize',
          tips: [
            'Use CodePen, snippets, or ChatGPT for starting points',
            'Learn by doing on real projects',
            'Tweak existing code until it works for your needs',
            "Don't try to build everything from scratch"
          ]
        },
        {
          title: 'Learning Resources',
          description: 'Start with free courses, then learn by doing',
          tips: [
            'Codecademy for free structured learning',
            'Learn additional skills as projects require them',
            'Focus on practical application over theory',
            'Use tools available to you (AI, templates, etc.)'
          ]
        }
      ]
    },
    {
      id: 'conversion',
      title: 'Conversion Skills',
      subtitle: 'Designing for Action',
      icon: '🎯',
      description: 'Design for user action, not just aesthetics',
      principles: [
        {
          title: 'One Goal Per Page',
          description: 'Focus on a single, clear objective',
          tips: [
            'Buy a product, sign up for a call, or get a lead magnet',
            'Avoid trying to do too much at once',
            'Clear goals prevent user confusion',
            'Measure success by goal completion'
          ]
        },
        {
          title: 'Strategic CTAs',
          description: 'Place clear calls-to-action strategically',
          tips: [
            'Visible within seconds of landing',
            'Hero section, navigation, and every 2-3 scroll sections',
            'Make CTAs stand out with color and size',
            'Use action-oriented language'
          ]
        },
        {
          title: 'Trust & Emotion',
          description: 'Build know, like, trust, and feel',
          tips: [
            'Speak to real user motivations',
            'Clearly explain what users get',
            'Show they are not alone (testimonials, reviews)',
            'Create emotional connection through design'
          ]
        }
      ]
    }
  ];

  const activeSkillData = skills.find(skill => skill.id === activeSkill);

  return (
    <div className={`bg-white border-l border-gray-200 w-80 flex flex-col ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">
          Design Skills Guide
        </h2>
        <p className="text-sm text-gray-600">
          Master the 5 essential web design skills
        </p>
      </div>

      {/* Skill Navigation */}
      <div className="p-4 border-b border-gray-200">
        <div className="grid grid-cols-2 gap-2">
          {skills.map((skill) => (
            <button
              key={skill.id}
              onClick={() => setActiveSkill(skill.id)}
              className={`p-3 rounded-lg text-left transition-colors ${
                activeSkill === skill.id
                  ? 'bg-blue-50 border-2 border-blue-200'
                  : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
              }`}
            >
              <div className="text-2xl mb-1">{skill.icon}</div>
              <div className="text-sm font-medium text-gray-900">{skill.title}</div>
              <div className="text-xs text-gray-600">{skill.subtitle}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Active Skill Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeSkillData && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {activeSkillData.title}
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                {activeSkillData.description}
              </p>
            </div>

            <div className="space-y-4">
              {activeSkillData.principles.map((principle, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">
                    {principle.title}
                  </h4>
                  <p className="text-sm text-gray-600 mb-3">
                    {principle.description}
                  </p>
                  <ul className="space-y-1">
                    {principle.tips.map((tip, tipIndex) => (
                      <li key={tipIndex} className="text-sm text-gray-700 flex items-start">
                        <span className="text-blue-500 mr-2">•</span>
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Interactive Tools */}
            {activeSkill === 'typography' && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Typography Tools</h4>
                <div className="space-y-2">
                  <a
                    href="https://type-scale.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    → Type Scale Generator
                  </a>
                  <a
                    href="https://fontshare.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    → FontShare (Free Fonts)
                  </a>
                  <a
                    href="https://uncut.wtf"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    → Uncut (Experimental Fonts)
                  </a>
                </div>
              </div>
            )}

            {activeSkill === 'color' && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Color Tools</h4>
                <div className="space-y-2">
                  <p className="text-sm text-gray-700">
                    Chrome DevTools → CSS Overview for color extraction
                  </p>
                  <p className="text-sm text-gray-700">
                    Figma contrast checker for accessibility
                  </p>
                </div>
              </div>
            )}

            {activeSkill === 'layout' && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Layout Tools</h4>
                <div className="space-y-2">
                  <p className="text-sm text-gray-700">
                    Figma: Frame → Layout Guide → Add Grid
                  </p>
                  <p className="text-sm text-gray-700">
                    Use 8px grid system for consistent spacing
                  </p>
                </div>
              </div>
            )}

            {activeSkill === 'coding' && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Learning Resources</h4>
                <div className="space-y-2">
                  <a
                    href="https://codecademy.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    → Codecademy (Free Courses)
                  </a>
                  <a
                    href="https://codepen.io"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-blue-600 hover:text-blue-800"
                  >
                    → CodePen (Code Snippets)
                  </a>
                </div>
              </div>
            )}

            {activeSkill === 'conversion' && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Conversion Checklist</h4>
                <div className="space-y-2">
                  <label className="flex items-center text-sm text-gray-700">
                    <input type="checkbox" className="mr-2" />
                    One clear goal per page
                  </label>
                  <label className="flex items-center text-sm text-gray-700">
                    <input type="checkbox" className="mr-2" />
                    CTA visible within seconds
                  </label>
                  <label className="flex items-center text-sm text-gray-700">
                    <input type="checkbox" className="mr-2" />
                    Social proof elements
                  </label>
                  <label className="flex items-center text-sm text-gray-700">
                    <input type="checkbox" className="mr-2" />
                    Clear value proposition
                  </label>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
