import React from 'react';
import { 
  ZoomIn, 
  ZoomOut, 
  Grid3X3, 
  Ruler, 
  Eye, 
  EyeOff,
  Undo,
  Redo,
  Copy,
  Trash2,
  Group,
  Ungroup,
  AlignLeft,
  AlignCenter,
  AlignRight,
  AlignJustify,
} from 'lucide-react';

import { useCanvasStore } from '../../stores/canvasStore';
import { useComponentStore } from '../../stores/componentStore';

export const CanvasControls: React.FC = () => {
  const {
    zoom,
    gridEnabled,
    snapToGrid,
    showRulers,
    showGuides,
    canUndo,
    canRedo,
    setZoom,
    toggleGrid,
    toggleSnapToGrid,
    toggleRulers,
    toggleGuides,
    undo,
    redo,
  } = useCanvasStore();

  const {
    selectedComponents,
    components,
    duplicateComponent,
    deleteComponent,
    groupComponents,
    ungroupComponent,
    isGrouped,
  } = useComponentStore();

  const handleZoomIn = () => {
    setZoom(Math.min(5, zoom + 0.1));
  };

  const handleZoomOut = () => {
    setZoom(Math.max(0.1, zoom - 0.1));
  };

  const handleZoomReset = () => {
    setZoom(1);
  };

  const handleDuplicate = () => {
    selectedComponents.forEach((componentId: string) => {
      duplicateComponent(componentId);
    });
  };

  const handleDelete = () => {
    selectedComponents.forEach((componentId: string) => {
      deleteComponent(componentId);
    });
  };

  const handleGroup = () => {
    if (selectedComponents.length > 1) {
      groupComponents(selectedComponents);
    }
  };

  const handleUngroup = () => {
    selectedComponents.forEach((componentId: string) => {
      if (isGrouped(componentId)) {
        ungroupComponent(componentId);
      }
    });
  };

  const canGroup = selectedComponents.length > 1;
  const canUngroup = selectedComponents.some((id: string) => isGrouped(id));

  return (
    <div className="canvas-controls">
      {/* Top toolbar */}
      <div className="toolbar">
        {/* Zoom controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={handleZoomOut}
            className="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          
          <span className="text-sm font-medium min-w-[60px] text-center">
            {Math.round(zoom * 100)}%
          </span>
          
          <button
            onClick={handleZoomIn}
            className="p-2 hover:bg-gray-100 rounded transition-colors"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          
          <button
            onClick={handleZoomReset}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded transition-colors"
            title="Reset Zoom"
          >
            Reset
          </button>
        </div>

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300" />

        {/* Grid controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={toggleGrid}
            className={`p-2 rounded transition-colors ${
              gridEnabled ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
            }`}
            title="Toggle Grid"
          >
            <Grid3X3 className="w-4 h-4" />
          </button>
          
          <button
            onClick={toggleSnapToGrid}
            className={`p-2 rounded transition-colors ${
              snapToGrid ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
            }`}
            title="Snap to Grid"
          >
            <Grid3X3 className="w-4 h-4" />
          </button>
        </div>

        {/* View controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={toggleRulers}
            className={`p-2 rounded transition-colors ${
              showRulers ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
            }`}
            title="Toggle Rulers"
          >
            <Ruler className="w-4 h-4" />
          </button>
          
          <button
            onClick={toggleGuides}
            className={`p-2 rounded transition-colors ${
              showGuides ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
            }`}
            title="Toggle Guides"
          >
            <Eye className="w-4 h-4" />
          </button>
        </div>

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300" />

        {/* History controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={undo}
            disabled={!canUndo}
            className="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Undo"
          >
            <Undo className="w-4 h-4" />
          </button>
          
          <button
            onClick={redo}
            disabled={!canRedo}
            className="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Redo"
          >
            <Redo className="w-4 h-4" />
          </button>
        </div>

        {/* Divider */}
        <div className="w-px h-6 bg-gray-300" />

        {/* Selection controls */}
        {selectedComponents.length > 0 && (
          <div className="flex items-center space-x-2">
            <button
              onClick={handleDuplicate}
              className="p-2 hover:bg-gray-100 rounded transition-colors"
              title="Duplicate"
            >
              <Copy className="w-4 h-4" />
            </button>
            
            <button
              onClick={handleDelete}
              className="p-2 hover:bg-red-100 text-red-600 rounded transition-colors"
              title="Delete"
            >
              <Trash2 className="w-4 h-4" />
            </button>
            
            {canGroup && (
              <button
                onClick={handleGroup}
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Group"
              >
                <Group className="w-4 h-4" />
              </button>
            )}
            
            {canUngroup && (
              <button
                onClick={handleUngroup}
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Ungroup"
              >
                <Ungroup className="w-4 h-4" />
              </button>
            )}
          </div>
        )}

        {/* Alignment controls */}
        {selectedComponents.length > 1 && (
          <>
            <div className="w-px h-6 bg-gray-300" />
            <div className="flex items-center space-x-2">
              <button
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Align Left"
              >
                <AlignLeft className="w-4 h-4" />
              </button>
              
              <button
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Align Center"
              >
                <AlignCenter className="w-4 h-4" />
              </button>
              
              <button
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Align Right"
              >
                <AlignRight className="w-4 h-4" />
              </button>
              
              <button
                className="p-2 hover:bg-gray-100 rounded transition-colors"
                title="Justify"
              >
                <AlignJustify className="w-4 h-4" />
              </button>
            </div>
          </>
        )}
      </div>

      {/* Selection info */}
      {selectedComponents.length > 0 && (
        <div className="absolute top-16 left-4 bg-white border border-gray-200 rounded-lg shadow-sm px-3 py-2 text-sm">
          {selectedComponents.length} component{selectedComponents.length !== 1 ? 's' : ''} selected
        </div>
      )}
    </div>
  );
};

export default CanvasControls;
