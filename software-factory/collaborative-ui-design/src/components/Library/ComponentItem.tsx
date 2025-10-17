import React from 'react';
import { ComponentDefinition } from '../../types/components';

interface ComponentItemProps {
  component: ComponentDefinition;
  viewMode: 'grid' | 'list';
}

export const ComponentItem: React.FC<ComponentItemProps> = ({ component, viewMode }) => {
  const handleDragStart = (event: React.DragEvent) => {
    const componentData = {
      type: component.id,
      name: component.name,
      defaultSize: { width: 200, height: 100 },
      defaultProperties: component.properties.reduce((acc, prop) => {
        acc[prop.name] = prop.value;
        return acc;
      }, {} as Record<string, any>),
    };

    event.dataTransfer.setData('application/reactflow', JSON.stringify(componentData));
    event.dataTransfer.effectAllowed = 'move';
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      atom: 'bg-blue-100 text-blue-700',
      molecule: 'bg-green-100 text-green-700',
      organism: 'bg-purple-100 text-purple-700',
      template: 'bg-orange-100 text-orange-700',
      layout: 'bg-gray-100 text-gray-700',
      form: 'bg-pink-100 text-pink-700',
      navigation: 'bg-indigo-100 text-indigo-700',
      content: 'bg-yellow-100 text-yellow-700',
      feedback: 'bg-red-100 text-red-700',
      overlay: 'bg-teal-100 text-teal-700',
    };
    return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-700';
  };

  if (viewMode === 'list') {
    return (
      <div
        draggable
        onDragStart={handleDragStart}
        className="component-library-item flex items-center space-x-3 p-3 hover:bg-blue-50 transition-colors cursor-move"
      >
        {/* Icon */}
        <div className="flex-shrink-0 w-8 h-8 bg-gray-100 rounded flex items-center justify-center">
          <span className="text-sm font-medium text-gray-600">
            {component.name.charAt(0).toUpperCase()}
          </span>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-1">
            <h3 className="text-sm font-medium text-gray-900 truncate">
              {component.name}
            </h3>
            <span className={`px-2 py-1 text-xs rounded-full ${getCategoryColor(component.category)}`}>
              {component.category}
            </span>
          </div>
          <p className="text-xs text-gray-500 truncate">
            {component.description}
          </p>
          {component.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-1">
              {component.tags.slice(0, 3).map(tag => (
                <span
                  key={tag}
                  className="px-1 py-0.5 text-xs bg-gray-100 text-gray-600 rounded"
                >
                  {tag}
                </span>
              ))}
              {component.tags.length > 3 && (
                <span className="text-xs text-gray-400">
                  +{component.tags.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>

        {/* Variants indicator */}
        {component.variants.length > 0 && (
          <div className="flex-shrink-0 text-xs text-gray-400">
            {component.variants.length} variant{component.variants.length !== 1 ? 's' : ''}
          </div>
        )}
      </div>
    );
  }

  return (
    <div
      draggable
      onDragStart={handleDragStart}
      className="component-library-item group"
    >
      {/* Preview */}
      <div className="aspect-square bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-center mb-2 group-hover:border-blue-300 transition-colors">
        {component.preview ? (
          <img
            src={component.preview}
            alt={component.name}
            className="max-w-full max-h-full object-contain"
          />
        ) : (
          <div className="text-2xl text-gray-400">
            {component.name.charAt(0).toUpperCase()}
          </div>
        )}
      </div>

      {/* Info */}
      <div className="space-y-1">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-gray-900 truncate">
            {component.name}
          </h3>
          <span className={`px-2 py-1 text-xs rounded-full ${getCategoryColor(component.category)}`}>
            {component.category}
          </span>
        </div>
        
        <p className="text-xs text-gray-500 line-clamp-2">
          {component.description}
        </p>

        {component.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {component.tags.slice(0, 2).map(tag => (
              <span
                key={tag}
                className="px-1 py-0.5 text-xs bg-gray-100 text-gray-600 rounded"
              >
                {tag}
              </span>
            ))}
            {component.tags.length > 2 && (
              <span className="text-xs text-gray-400">
                +{component.tags.length - 2}
              </span>
            )}
          </div>
        )}

        {component.variants.length > 0 && (
          <div className="text-xs text-gray-400">
            {component.variants.length} variant{component.variants.length !== 1 ? 's' : ''}
          </div>
        )}
      </div>
    </div>
  );
};

export default ComponentItem;
