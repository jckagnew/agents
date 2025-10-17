import React, { useState, useCallback } from 'react';
import { 
  Globe, 
  Search, 
  Download, 
  Eye, 
  Palette, 
  Type, 
  Layout, 
  Smartphone,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { useComponentStore } from '../../stores/componentStore';

interface WebsiteAnalysis {
  url: string;
  title: string;
  status: 'idle' | 'analyzing' | 'completed' | 'error';
  designElements: Array<{
    type: string;
    selector: string;
    properties: Record<string, any>;
    screenshot?: string;
  }>;
  colorPalette: string[];
  typographyScale: Record<string, string>;
  componentPatterns: Array<{
    name: string;
    pattern: string;
    elements: string[];
  }>;
  recommendations: string[];
  extractedComponents: Array<{
    id: string;
    name: string;
    category: string;
    code: {
      react: string;
      css: string;
    };
  }>;
}

export const WebsiteAnalyzer: React.FC = () => {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState<WebsiteAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { addComponent } = useComponentStore();

  const analyzeWebsite = useCallback(async () => {
    if (!url.trim()) return;

    setIsAnalyzing(true);
    setError(null);
    setAnalysis(null);

    try {
      // Mock analysis - in real implementation, this would call the Vision Design Agent
      const mockAnalysis: WebsiteAnalysis = {
        url,
        title: 'Sample Website Analysis',
        status: 'analyzing',
        designElements: [],
        colorPalette: [],
        typographyScale: {},
        componentPatterns: [],
        recommendations: [],
        extractedComponents: []
      };

      setAnalysis(mockAnalysis);

      // Simulate analysis delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Mock completed analysis
      const completedAnalysis: WebsiteAnalysis = {
        url,
        title: 'Sample Website Analysis',
        status: 'completed',
        designElements: [
          {
            type: 'hero_section',
            selector: '.hero',
            properties: {
              background_color: '#3B82F6',
              text_color: '#FFFFFF',
              font_family: 'Inter, sans-serif',
              font_size: '3rem',
              padding: '80px 0'
            }
          },
          {
            type: 'cta_button',
            selector: '.cta-button',
            properties: {
              background_color: '#F59E0B',
              text_color: '#FFFFFF',
              border_radius: '8px',
              padding: '16px 32px',
              font_weight: '600'
            }
          }
        ],
        colorPalette: ['#3B82F6', '#F59E0B', '#6B7280', '#F9FAFB'],
        typographyScale: {
          'h1': '3rem',
          'h2': '2.25rem',
          'h3': '1.875rem',
          'h4': '1.5rem',
          'h5': '1.25rem',
          'h6': '1rem',
          'body': '1rem'
        },
        componentPatterns: [
          {
            name: 'Hero Section',
            pattern: 'centered_text_with_cta',
            elements: ['headline', 'subheadline', 'cta_button']
          },
          {
            name: 'Feature Cards',
            pattern: 'three_column_grid',
            elements: ['icon', 'title', 'description']
          }
        ],
        recommendations: [
          'Consider adding more visual hierarchy with better typography scaling',
          'Increase contrast ratio for better accessibility',
          'Add more conversion elements throughout the page',
          'Implement a more systematic color palette approach'
        ],
        extractedComponents: [
          {
            id: 'hero-section-extracted',
            name: 'Hero Section',
            category: 'extracted',
            code: {
              react: `const HeroSection = ({ headline, subheadline, ctaText }) => (
  <section className="hero-section">
    <div className="hero-content">
      <h1 className="hero-headline">{headline}</h1>
      <p className="hero-subheadline">{subheadline}</p>
      <button className="cta-button">{ctaText}</button>
    </div>
  </section>
);`,
              css: `.hero-section {
  padding: 80px 0;
  text-align: center;
  background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
  color: white;
}

.hero-headline {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subheadline {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  padding: 16px 32px;
  font-size: 1.125rem;
  font-weight: 600;
  background: #F59E0B;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.cta-button:hover {
  background: #D97706;
  transform: translateY(-2px);
}`
            }
          }
        ]
      };

      setAnalysis(completedAnalysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
      setAnalysis({
        url,
        title: 'Analysis Failed',
        status: 'error',
        designElements: [],
        colorPalette: [],
        typographyScale: {},
        componentPatterns: [],
        recommendations: [],
        extractedComponents: []
      });
    } finally {
      setIsAnalyzing(false);
    }
  }, [url]);

  const addExtractedComponent = useCallback((component: any) => {
    addComponent(component);
  }, [addComponent]);

  return (
    <div className="website-analyzer p-6 bg-white rounded-lg shadow-sm border">
      <div className="flex items-center gap-3 mb-6">
        <Globe className="w-6 h-6 text-blue-600" />
        <h2 className="text-xl font-semibold text-gray-900">Website Analyzer</h2>
      </div>

      {/* URL Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Website URL
        </label>
        <div className="flex gap-2">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isAnalyzing}
          />
          <button
            onClick={analyzeWebsite}
            disabled={!url.trim() || isAnalyzing}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isAnalyzing ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Search className="w-4 h-4" />
            )}
            Analyze
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Status */}
          <div className="flex items-center gap-2">
            {analysis.status === 'completed' && <CheckCircle className="w-5 h-5 text-green-500" />}
            {analysis.status === 'error' && <AlertCircle className="w-5 h-5 text-red-500" />}
            {analysis.status === 'analyzing' && <Loader2 className="w-5 h-5 animate-spin text-blue-500" />}
            <span className="font-medium">
              {analysis.status === 'completed' && 'Analysis Complete'}
              {analysis.status === 'error' && 'Analysis Failed'}
              {analysis.status === 'analyzing' && 'Analyzing...'}
            </span>
          </div>

          {analysis.status === 'completed' && (
            <>
              {/* Color Palette */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Palette className="w-5 h-5" />
                  Color Palette
                </h3>
                <div className="flex gap-2 flex-wrap">
                  {analysis.colorPalette.map((color, index) => (
                    <div
                      key={index}
                      className="w-12 h-12 rounded-lg border border-gray-200 flex items-center justify-center text-xs font-mono"
                      style={{ backgroundColor: color }}
                      title={color}
                    >
                      {color}
                    </div>
                  ))}
                </div>
              </div>

              {/* Typography Scale */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Type className="w-5 h-5" />
                  Typography Scale
                </h3>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(analysis.typographyScale).map(([element, size]) => (
                    <div key={element} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="font-medium">{element}</span>
                      <span className="text-sm text-gray-600">{size}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Component Patterns */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Layout className="w-5 h-5" />
                  Component Patterns
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {analysis.componentPatterns.map((pattern, index) => (
                    <div key={index} className="p-3 border border-gray-200 rounded-lg">
                      <h4 className="font-medium text-gray-900">{pattern.name}</h4>
                      <p className="text-sm text-gray-600 mb-2">{pattern.pattern}</p>
                      <div className="flex flex-wrap gap-1">
                        {pattern.elements.map((element, elIndex) => (
                          <span
                            key={elIndex}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                          >
                            {element}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Extracted Components */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Download className="w-5 h-5" />
                  Extracted Components
                </h3>
                <div className="space-y-3">
                  {analysis.extractedComponents.map((component) => (
                    <div key={component.id} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-900">{component.name}</h4>
                        <button
                          onClick={() => addExtractedComponent(component)}
                          className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                        >
                          Add to Library
                        </button>
                      </div>
                      <div className="text-sm text-gray-600 mb-3">
                        Category: {component.category}
                      </div>
                      <div className="bg-gray-50 p-3 rounded text-xs font-mono overflow-x-auto">
                        <pre>{component.code.react}</pre>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center gap-2">
                  <Eye className="w-5 h-5" />
                  Recommendations
                </h3>
                <ul className="space-y-2">
                  {analysis.recommendations.map((recommendation, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}

          {analysis.status === 'error' && error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default WebsiteAnalyzer;
