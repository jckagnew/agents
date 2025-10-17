import React, { useCallback, useRef, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  ReactFlowProvider,
  ReactFlowInstance,
  NodeTypes,
  EdgeTypes,
} from 'reactflow';
// React Flow styles are handled in index.css

import { useCanvasStore } from '../../stores/canvasStore';
import { useComponentStore } from '../../stores/componentStore';
import { DesignComponent, Position, Size } from '../../types/components';
import { CanvasViewport } from '../../types/canvas';

import { ComponentNode } from './ComponentNode';
import { CanvasControls } from './CanvasControls';
import { CanvasGrid } from './CanvasGrid';

// Custom node types
const nodeTypes: NodeTypes = {
  component: ComponentNode,
};

// Custom edge types (empty for now)
const edgeTypes: EdgeTypes = {};

interface DesignCanvasProps {
  className?: string;
}

export const DesignCanvas: React.FC<DesignCanvasProps> = ({ className = '' }) => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);
  
  const {
    zoom,
    pan,
    selectedComponents,
    gridEnabled,
    snapToGrid,
    gridSize,
    showRulers,
    showGuides,
    setZoom,
    setPan,
    selectComponents,
    deselectAll,
    addAction,
  } = useCanvasStore();

  const {
    components,
    addComponent,
    updateComponent,
    moveComponent,
    resizeComponent,
    getComponent,
  } = useComponentStore();

  // Convert components to React Flow nodes
  const [nodes, setNodes, onNodesChange] = useNodesState(
    components.map(component => ({
      id: component.id,
      type: 'component',
      position: component.position,
      data: { component },
      selected: selectedComponents.includes(component.id),
    }))
  );

  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Handle node changes
  const onNodesChangeHandler = useCallback((changes: any) => {
    onNodesChange(changes);
    
    changes.forEach((change: any) => {
      if (change.type === 'position' && change.position) {
        const component = getComponent(change.id);
        if (component) {
          const newPosition = snapToGrid ? {
            x: Math.round(change.position.x / gridSize) * gridSize,
            y: Math.round(change.position.y / gridSize) * gridSize,
          } : change.position;
          
          moveComponent(change.id, newPosition);
          addAction({
            type: 'move_component',
            data: { componentId: change.id, position: newPosition },
            description: `Moved ${component.name}`,
          });
        }
      }
      
      if (change.type === 'dimensions' && change.dimensions) {
        const component = getComponent(change.id);
        if (component) {
          const newSize: Size = {
            width: change.dimensions.width,
            height: change.dimensions.height,
          };
          
          resizeComponent(change.id, newSize);
          addAction({
            type: 'resize_component',
            data: { componentId: change.id, size: newSize },
            description: `Resized ${component.name}`,
          });
        }
      }
    });
  }, [getComponent, moveComponent, resizeComponent, addAction, snapToGrid, gridSize]);

  // Handle selection changes
  const onSelectionChange = useCallback(({ nodes }: { nodes: Node[] }) => {
    const selectedIds = nodes.map(node => node.id);
    selectComponents(selectedIds);
  }, [selectComponents]);

  // Handle connection creation
  const onConnect = useCallback((params: Connection) => {
    setEdges((eds) => addEdge(params, eds));
  }, [setEdges]);

  // Handle drag over
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // Handle drop
  const onDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();

    if (!reactFlowInstance || !reactFlowWrapper.current) return;

    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });

    const componentData = event.dataTransfer.getData('application/reactflow');
    if (!componentData) return;

    try {
      const componentType = JSON.parse(componentData);
      const newComponent: DesignComponent = {
        id: `comp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        type: componentType.type,
        name: componentType.name,
        position: snapToGrid ? {
          x: Math.round(position.x / gridSize) * gridSize,
          y: Math.round(position.y / gridSize) * gridSize,
        } : position,
        size: componentType.defaultSize || { width: 200, height: 100 },
        properties: componentType.defaultProperties || {},
      };

      addComponent(newComponent);
      addAction({
        type: 'create_component',
        data: { component: newComponent },
        description: `Created ${newComponent.name}`,
      });
    } catch (error) {
      console.error('Error parsing dropped component:', error);
    }
  }, [reactFlowInstance, snapToGrid, gridSize, addComponent, addAction]);

  // Handle viewport changes
  const onViewportChange = useCallback((viewport: CanvasViewport) => {
    setZoom(viewport.zoom);
    setPan({ x: viewport.x, y: viewport.y });
  }, [setZoom, setPan]);

  // Handle double click to deselect all
  const onPaneClick = useCallback(() => {
    deselectAll();
  }, [deselectAll]);

  return (
    <div className={`design-canvas ${className}`} ref={reactFlowWrapper}>
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChangeHandler}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onSelectionChange={onSelectionChange}
          onInit={setReactFlowInstance}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
          fitView
          attributionPosition="bottom-left"
          className="canvas-container"
        >
          <Background 
            color="#e5e7eb" 
            gap={gridEnabled ? gridSize : 0}
            size={1}
          />
          
          <Controls 
            showInteractive={false}
            position="top-right"
          />
          
          <MiniMap
            nodeColor={(node) => {
              const component = getComponent(node.id);
              return component?.type === 'group' ? '#3b82f6' : '#6b7280';
            }}
            nodeStrokeWidth={3}
            zoomable
            pannable
            position="bottom-right"
          />
          
          {showRulers && (
            <div className="rulers">
              {/* Horizontal ruler */}
              <div className="ruler horizontal" />
              {/* Vertical ruler */}
              <div className="ruler vertical" />
            </div>
          )}
          
          {showGuides && (
            <div className="guides">
              {/* Guide lines will be rendered here */}
            </div>
          )}
        </ReactFlow>
        
        <CanvasControls />
        <CanvasGrid enabled={gridEnabled} size={gridSize} />
      </ReactFlowProvider>
    </div>
  );
};

export default DesignCanvas;
