import React from 'react';

interface TypographyEditorProps {
  value: {
    fontFamily?: string;
    fontSize?: number;
    fontWeight?: string;
    lineHeight?: number;
    letterSpacing?: number;
  };
  onChange: (value: any) => void;
}

const fontFamilies = [
  'Inter',
  'Arial',
  'Helvetica',
  'Times New Roman',
  'Georgia',
  'Verdana',
  'Courier New',
  'Monaco',
];

const fontWeights = [
  { value: '300', label: 'Light' },
  { value: '400', label: 'Normal' },
  { value: '500', label: 'Medium' },
  { value: '600', label: 'Semi Bold' },
  { value: '700', label: 'Bold' },
  { value: '800', label: 'Extra Bold' },
];

export const TypographyEditor: React.FC<TypographyEditorProps> = ({ value, onChange }) => {
  const handleChange = (key: string, newValue: any) => {
    onChange({
      ...value,
      [key]: newValue,
    });
  };

  return (
    <div className="space-y-3">
      {/* Font Family */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">Font Family</label>
        <select
          value={value.fontFamily || 'Inter'}
          onChange={(e) => handleChange('fontFamily', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        >
          {fontFamilies.map((font) => (
            <option key={font} value={font}>
              {font}
            </option>
          ))}
        </select>
      </div>

      {/* Font Size */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">Font Size</label>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            value={value.fontSize || 16}
            onChange={(e) => handleChange('fontSize', parseFloat(e.target.value) || 16)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            min="8"
            max="72"
            step="1"
          />
          <span className="text-xs text-gray-500">px</span>
        </div>
      </div>

      {/* Font Weight */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">Font Weight</label>
        <select
          value={value.fontWeight || '400'}
          onChange={(e) => handleChange('fontWeight', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        >
          {fontWeights.map((weight) => (
            <option key={weight.value} value={weight.value}>
              {weight.label}
            </option>
          ))}
        </select>
      </div>

      {/* Line Height */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">Line Height</label>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            value={value.lineHeight || 1.5}
            onChange={(e) => handleChange('lineHeight', parseFloat(e.target.value) || 1.5)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            min="0.5"
            max="3"
            step="0.1"
          />
          <span className="text-xs text-gray-500">em</span>
        </div>
      </div>

      {/* Letter Spacing */}
      <div>
        <label className="block text-xs font-medium text-gray-700 mb-1">Letter Spacing</label>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            value={value.letterSpacing || 0}
            onChange={(e) => handleChange('letterSpacing', parseFloat(e.target.value) || 0)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            min="-2"
            max="5"
            step="0.1"
          />
          <span className="text-xs text-gray-500">px</span>
        </div>
      </div>

      {/* Preview */}
      <div className="mt-4 p-3 bg-gray-50 rounded-md">
        <div className="text-xs font-medium text-gray-700 mb-2">Preview</div>
        <div
          style={{
            fontFamily: value.fontFamily || 'Inter',
            fontSize: `${value.fontSize || 16}px`,
            fontWeight: value.fontWeight || '400',
            lineHeight: value.lineHeight || 1.5,
            letterSpacing: `${value.letterSpacing || 0}px`,
          }}
          className="text-gray-900"
        >
          The quick brown fox jumps over the lazy dog
        </div>
      </div>
    </div>
  );
};

export default TypographyEditor;
