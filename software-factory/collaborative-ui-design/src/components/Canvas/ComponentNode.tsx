import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { DesignComponent } from '../../types/components';

interface ComponentNodeData {
  component: DesignComponent;
}

export const ComponentNode: React.FC<NodeProps<ComponentNodeData>> = ({ data, selected }) => {
  const { component } = data;

  const renderComponent = () => {
    switch (component.type) {
      case 'button':
        return (
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            {component.properties.text || 'Button'}
          </button>
        );
      
      case 'text':
        return (
          <div
            className="text-gray-900"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            {component.properties.text || 'Text'}
          </div>
        );
      
      case 'input':
        return (
          <input
            type="text"
            placeholder={component.properties.placeholder || 'Enter text...'}
            className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          />
        );
      
      case 'card':
        return (
          <div
            className="bg-white border border-gray-200 rounded-lg shadow-sm p-4"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            <div className="text-lg font-semibold mb-2">
              {component.properties.title || 'Card Title'}
            </div>
            <div className="text-gray-600">
              {component.properties.content || 'Card content goes here...'}
            </div>
          </div>
        );
      
      case 'image':
        return (
          <div
            className="bg-gray-100 border border-gray-300 rounded flex items-center justify-center"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            {component.properties.src ? (
              <img
                src={component.properties.src}
                alt={component.properties.alt || 'Image'}
                className="max-w-full max-h-full object-contain"
              />
            ) : (
              <span className="text-gray-500 text-sm">Image</span>
            )}
          </div>
        );
      
      case 'container':
        return (
          <div
            className="border border-dashed border-gray-300 rounded bg-gray-50"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            <div className="flex items-center justify-center h-full text-gray-500 text-sm">
              Container
            </div>
          </div>
        );
      
      case 'group':
        return (
          <div
            className="border-2 border-blue-300 rounded bg-blue-50"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            <div className="flex items-center justify-center h-full text-blue-600 text-sm font-medium">
              Group ({component.children?.length || 0} items)
            </div>
          </div>
        );
      
      default:
        return (
          <div
            className="bg-gray-100 border border-gray-300 rounded flex items-center justify-center"
            style={{
              width: component.size.width,
              height: component.size.height,
              ...component.properties,
            }}
          >
            <span className="text-gray-500 text-sm">{component.name}</span>
          </div>
        );
    }
  };

  return (
    <div
      className={`component-node ${selected ? 'selected' : ''}`}
      style={{
        width: component.size.width,
        height: component.size.height,
      }}
    >
      {/* Input handle */}
      <Handle
        type="target"
        position={Position.Top}
        id="input"
        className="w-3 h-3 bg-blue-500 border-2 border-white"
      />
      
      {/* Component content */}
      <div className="w-full h-full">
        {renderComponent()}
      </div>
      
      {/* Output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="output"
        className="w-3 h-3 bg-blue-500 border-2 border-white"
      />
      
      {/* Left handle */}
      <Handle
        type="source"
        position={Position.Left}
        id="left"
        className="w-3 h-3 bg-green-500 border-2 border-white"
      />
      
      {/* Right handle */}
      <Handle
        type="source"
        position={Position.Right}
        id="right"
        className="w-3 h-3 bg-green-500 border-2 border-white"
      />
    </div>
  );
};

export default memo(ComponentNode);
