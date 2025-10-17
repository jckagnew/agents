// Canvas and design area types
import { Position, Size, DesignComponent } from './components';

export interface CanvasState {
  zoom: number;
  pan: Position;
  selectedComponents: string[];
  clipboard: DesignComponent[];
  history: HistoryState;
  isDirty: boolean;
  gridEnabled: boolean;
  snapToGrid: boolean;
  gridSize: number;
  showRulers: boolean;
  showGuides: boolean;
}

export interface HistoryState {
  past: CanvasAction[];
  present: CanvasAction | null;
  future: CanvasAction[];
  maxHistorySize: number;
}

export interface CanvasAction {
  id: string;
  type: CanvasActionType;
  data: any;
  timestamp: Date;
  description: string;
}

export type CanvasActionType = 
  | 'create_component'
  | 'delete_component'
  | 'move_component'
  | 'resize_component'
  | 'update_properties'
  | 'group_components'
  | 'ungroup_components'
  | 'duplicate_component'
  | 'paste_component'
  | 'select_component'
  | 'deselect_component'
  | 'select_all'
  | 'deselect_all';

export interface CanvasViewport {
  x: number;
  y: number;
  width: number;
  height: number;
  zoom: number;
}

export interface CanvasSelection {
  componentIds: string[];
  bounds: SelectionBounds;
  isMultiSelect: boolean;
}

export interface SelectionBounds {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface CanvasTool {
  id: string;
  name: string;
  icon: string;
  cursor: string;
  isActive: boolean;
  shortcut?: string;
}

export interface CanvasGuide {
  id: string;
  type: 'horizontal' | 'vertical';
  position: number;
  color: string;
  opacity: number;
}

export interface CanvasRuler {
  type: 'horizontal' | 'vertical';
  position: number;
  size: number;
  unit: 'px' | 'rem' | 'em' | '%';
  marks: RulerMark[];
}

export interface RulerMark {
  position: number;
  value: number;
  isMajor: boolean;
  label?: string;
}

export interface CanvasGrid {
  enabled: boolean;
  size: number;
  color: string;
  opacity: number;
  snapThreshold: number;
}

export interface CanvasSettings {
  grid: CanvasGrid;
  rulers: {
    enabled: boolean;
    unit: 'px' | 'rem' | 'em' | '%';
  };
  guides: {
    enabled: boolean;
    color: string;
    opacity: number;
  };
  zoom: {
    min: number;
    max: number;
    step: number;
    default: number;
  };
  pan: {
    enabled: boolean;
    momentum: boolean;
  };
  selection: {
    multiSelect: boolean;
    showBounds: boolean;
    showHandles: boolean;
  };
}
