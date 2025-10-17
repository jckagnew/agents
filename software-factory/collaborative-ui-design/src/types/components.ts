// Core component types for the collaborative UI design app

export interface Position {
  x: number;
  y: number;
}

export interface Size {
  width: number;
  height: number;
}

export interface ComponentProperty {
  id: string;
  name: string;
  type: 'string' | 'number' | 'boolean' | 'color' | 'spacing' | 'select' | 'font';
  value: any;
  options?: any[];
  required?: boolean;
  description?: string;
}

export interface ComponentVariant {
  id: string;
  name: string;
  properties: Record<string, any>;
  preview?: string;
}

export interface ComponentDefinition {
  id: string;
  name: string;
  category: ComponentCategory;
  icon: string;
  description: string;
  properties: ComponentProperty[];
  variants: ComponentVariant[];
  code: {
    react: string;
    css: string;
    storybook?: string;
  };
  preview: string;
  tags: string[];
}

export type ComponentCategory = 
  | 'atom' 
  | 'molecule' 
  | 'organism' 
  | 'template' 
  | 'layout' 
  | 'form' 
  | 'navigation' 
  | 'content' 
  | 'feedback' 
  | 'overlay'
  | 'conversion'
  | 'typography'
  | 'color'
  | 'extracted';

export interface DesignComponent {
  id: string;
  type: string;
  name: string;
  position: Position;
  size: Size;
  properties: Record<string, any>;
  children?: DesignComponent[];
  parentId?: string;
  locked?: boolean;
  visible?: boolean;
  zIndex?: number;
}

export interface DesignToken {
  id: string;
  name: string;
  category: 'color' | 'typography' | 'spacing' | 'shadow' | 'border';
  value: any;
  description?: string;
  usage?: string[];
}

export interface DesignSystem {
  id: string;
  name: string;
  description: string;
  tokens: DesignToken[];
  components: ComponentDefinition[];
  version: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  components: DesignComponent[];
  designSystem: DesignSystem;
  collaborators: Collaborator[];
  settings: ProjectSettings;
  createdAt: Date;
  updatedAt: Date;
}

export interface Collaborator {
  id: string;
  name: string;
  email: string;
  role: 'owner' | 'editor' | 'viewer' | 'client';
  permissions: Permission[];
  avatar?: string;
  lastActive?: Date;
}

export interface Permission {
  action: 'read' | 'write' | 'comment' | 'approve' | 'export';
  resource: 'project' | 'components' | 'designSystem' | 'comments';
}

export interface ProjectSettings {
  canvasSize: Size;
  gridEnabled: boolean;
  snapToGrid: boolean;
  gridSize: number;
  zoom: number;
  theme: 'light' | 'dark';
  autoSave: boolean;
  autoSaveInterval: number;
}

export interface Comment {
  id: string;
  componentId: string;
  userId: string;
  content: string;
  position: Position;
  replies: Comment[];
  status: 'open' | 'resolved';
  createdAt: Date;
  updatedAt: Date;
}

export interface Annotation {
  id: string;
  componentId: string;
  userId: string;
  type: 'highlight' | 'arrow' | 'rectangle' | 'freehand';
  coordinates: Position[];
  color: string;
  opacity: number;
  createdAt: Date;
}

export interface ChangeEvent {
  id: string;
  type: 'create' | 'update' | 'delete' | 'move' | 'resize';
  componentId: string;
  userId: string;
  data: any;
  timestamp: Date;
}

export interface ExportOptions {
  format: 'react' | 'html' | 'css' | 'figma' | 'sketch';
  includeAssets: boolean;
  optimizeCode: boolean;
  generateStorybook: boolean;
  includeTests: boolean;
}

export interface ExportResult {
  files: ExportFile[];
  metadata: {
    exportedAt: Date;
    exportedBy: string;
    version: string;
    format: string;
  };
}

export interface ExportFile {
  name: string;
  content: string;
  type: 'component' | 'style' | 'asset' | 'config';
  path: string;
}
