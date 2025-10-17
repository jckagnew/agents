import React from 'react';
import { useComponentStore } from '../../stores/componentStore';
import { ColorPicker } from './ColorPicker';
import { TypographyEditor } from './TypographyEditor';

export const PropertiesPanel: React.FC = () => {
  const { selectedComponent, updateComponent } = useComponentStore();

  if (!selectedComponent) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Properties</h2>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <div className="w-16 h-16 bg-gray-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">⚙️</span>
            </div>
            <p className="text-sm">Select a component to edit its properties</p>
          </div>
        </div>
      </div>
    );
  }

  const handlePropertyChange = (propertyName: string, value: any) => {
    updateComponent(selectedComponent.id, {
      properties: {
        ...selectedComponent.properties,
        [propertyName]: value,
      },
    });
  };

  const renderPropertyEditor = (propertyName: string, value: any, type: string) => {
    switch (type) {
      case 'color':
        return (
          <ColorPicker
            value={value}
            onChange={(color) => handlePropertyChange(propertyName, color)}
          />
        );
      
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handlePropertyChange(propertyName, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {/* Options will be populated based on component definition */}
            <option value="primary">Primary</option>
            <option value="secondary">Secondary</option>
            <option value="outline">Outline</option>
          </select>
        );
      
      case 'boolean':
        return (
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={value}
              onChange={(e) => handlePropertyChange(propertyName, e.target.checked)}
              className="mr-2"
            />
            <span className="text-sm text-gray-700">Enabled</span>
          </label>
        );
      
      case 'number':
        return (
          <input
            type="number"
            value={value}
            onChange={(e) => handlePropertyChange(propertyName, parseFloat(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
      
      default:
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => handlePropertyChange(propertyName, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
    }
  };

  return (
    <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Properties</h2>
        <p className="text-sm text-gray-500 mt-1">{selectedComponent.name}</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Position & Size */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-900">Position & Size</h3>
          
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">X</label>
              <input
                type="number"
                value={selectedComponent.position.x}
                onChange={(e) => updateComponent(selectedComponent.id, {
                  position: {
                    ...selectedComponent.position,
                    x: parseFloat(e.target.value) || 0,
                  },
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Y</label>
              <input
                type="number"
                value={selectedComponent.position.y}
                onChange={(e) => updateComponent(selectedComponent.id, {
                  position: {
                    ...selectedComponent.position,
                    y: parseFloat(e.target.value) || 0,
                  },
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Width</label>
              <input
                type="number"
                value={selectedComponent.size.width}
                onChange={(e) => updateComponent(selectedComponent.id, {
                  size: {
                    ...selectedComponent.size,
                    width: parseFloat(e.target.value) || 0,
                  },
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Height</label>
              <input
                type="number"
                value={selectedComponent.size.height}
                onChange={(e) => updateComponent(selectedComponent.id, {
                  size: {
                    ...selectedComponent.size,
                    height: parseFloat(e.target.value) || 0,
                  },
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              />
            </div>
          </div>
        </div>

        {/* Component Properties */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-900">Properties</h3>
          
          <div className="space-y-3">
            {Object.entries(selectedComponent.properties).map(([key, value]) => (
              <div key={key}>
                <label className="block text-xs font-medium text-gray-700 mb-1 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').trim()}
                </label>
                {renderPropertyEditor(key, value, typeof value)}
              </div>
            ))}
          </div>
        </div>

        {/* Style Properties */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-900">Style</h3>
          
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Background Color</label>
              <ColorPicker
                value={selectedComponent.properties.backgroundColor || '#ffffff'}
                onChange={(color) => handlePropertyChange('backgroundColor', color)}
              />
            </div>
            
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Text Color</label>
              <ColorPicker
                value={selectedComponent.properties.color || '#000000'}
                onChange={(color) => handlePropertyChange('color', color)}
              />
            </div>
            
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Border Radius</label>
              <input
                type="number"
                value={selectedComponent.properties.borderRadius || 0}
                onChange={(e) => handlePropertyChange('borderRadius', parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                min="0"
                step="1"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertiesPanel;
