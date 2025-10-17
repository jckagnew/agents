import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { DesignComponent, ComponentDefinition, Position, Size } from '../types/components';

interface ComponentStore {
  components: DesignComponent[];
  componentLibrary: ComponentDefinition[];
  selectedComponent: DesignComponent | null;
  selectedComponents: string[];
  hoveredComponent: string | null;
  
  // Actions
  addComponent: (component: DesignComponent) => void;
  updateComponent: (id: string, updates: Partial<DesignComponent>) => void;
  deleteComponent: (id: string) => void;
  duplicateComponent: (id: string) => void;
  moveComponent: (id: string, position: Position) => void;
  resizeComponent: (id: string, size: Size) => void;
  setSelectedComponent: (component: DesignComponent | null) => void;
  setSelectedComponents: (ids: string[]) => void;
  addSelectedComponent: (id: string) => void;
  removeSelectedComponent: (id: string) => void;
  clearSelectedComponents: () => void;
  setHoveredComponent: (id: string | null) => void;
  getComponent: (id: string) => DesignComponent | undefined;
  getComponentsByParent: (parentId: string) => DesignComponent[];
  clearComponents: () => void;
  loadComponents: (components: DesignComponent[]) => void;
  
  // Component Library
  loadComponentLibrary: (library: ComponentDefinition[]) => void;
  getComponentDefinition: (type: string) => ComponentDefinition | undefined;
  searchComponents: (query: string) => ComponentDefinition[];
  getComponentsByCategory: (category: string) => ComponentDefinition[];
  
  // Grouping
  groupComponents: (componentIds: string[]) => string;
  ungroupComponent: (groupId: string) => void;
  isGrouped: (componentId: string) => boolean;
  getGroupChildren: (groupId: string) => DesignComponent[];
}

export const useComponentStore = create<ComponentStore>()(
  devtools(
    (set, get) => ({
      components: [],
      componentLibrary: [],
      selectedComponent: null,
      selectedComponents: [],
      hoveredComponent: null,

      addComponent: (component: DesignComponent) => {
        const { components } = get();
        set({ 
          components: [...components, component],
        });
      },

      updateComponent: (id: string, updates: Partial<DesignComponent>) => {
        const { components } = get();
        set({
          components: components.map(comp => 
            comp.id === id ? { ...comp, ...updates } : comp
          ),
        });
      },

      deleteComponent: (id: string) => {
        const { components } = get();
        const component = components.find(comp => comp.id === id);
        
        if (!component) return;

        // If it's a group, delete all children
        if (component.children && component.children.length > 0) {
          const childIds = component.children.map(child => child.id);
          set({
            components: components.filter(comp => 
              comp.id !== id && !childIds.includes(comp.id)
            ),
          });
        } else {
          set({
            components: components.filter(comp => comp.id !== id),
          });
        }
      },

      duplicateComponent: (id: string) => {
        const { components } = get();
        const component = components.find(comp => comp.id === id);
        
        if (!component) return;

        const duplicated: DesignComponent = {
          ...component,
          id: `comp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          position: {
            x: component.position.x + 20,
            y: component.position.y + 20,
          },
          children: component.children?.map(child => ({
            ...child,
            id: `comp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            parentId: `comp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          })),
        };

        set({
          components: [...components, duplicated],
        });
      },

      moveComponent: (id: string, position: Position) => {
        const { components } = get();
        set({
          components: components.map(comp => 
            comp.id === id ? { ...comp, position } : comp
          ),
        });
      },

      resizeComponent: (id: string, size: Size) => {
        const { components } = get();
        set({
          components: components.map(comp => 
            comp.id === id ? { ...comp, size } : comp
          ),
        });
      },

      setSelectedComponent: (component: DesignComponent | null) => {
        set({ selectedComponent: component });
      },

      setSelectedComponents: (ids: string[]) => {
        set({ selectedComponents: ids });
      },

      addSelectedComponent: (id: string) => {
        const { selectedComponents } = get();
        if (!selectedComponents.includes(id)) {
          set({ selectedComponents: [...selectedComponents, id] });
        }
      },

      removeSelectedComponent: (id: string) => {
        const { selectedComponents } = get();
        set({ selectedComponents: selectedComponents.filter(compId => compId !== id) });
      },

      clearSelectedComponents: () => {
        set({ selectedComponents: [] });
      },

      setHoveredComponent: (id: string | null) => {
        set({ hoveredComponent: id });
      },

      getComponent: (id: string) => {
        const { components } = get();
        return components.find(comp => comp.id === id);
      },

      getComponentsByParent: (parentId: string) => {
        const { components } = get();
        return components.filter(comp => comp.parentId === parentId);
      },

      clearComponents: () => {
        set({ 
          components: [],
          selectedComponent: null,
          hoveredComponent: null,
        });
      },

      loadComponents: (components: DesignComponent[]) => {
        set({ components });
      },

      loadComponentLibrary: (library: ComponentDefinition[]) => {
        set({ componentLibrary: library });
      },

      getComponentDefinition: (type: string) => {
        const { componentLibrary } = get();
        return componentLibrary.find(comp => comp.id === type);
      },

      searchComponents: (query: string) => {
        const { componentLibrary } = get();
        const lowercaseQuery = query.toLowerCase();
        return componentLibrary.filter(comp => 
          comp.name.toLowerCase().includes(lowercaseQuery) ||
          comp.description.toLowerCase().includes(lowercaseQuery) ||
          comp.tags.some(tag => tag.toLowerCase().includes(lowercaseQuery))
        );
      },

      getComponentsByCategory: (category: string) => {
        const { componentLibrary } = get();
        return componentLibrary.filter(comp => comp.category === category);
      },

      groupComponents: (componentIds: string[]) => {
        const { components } = get();
        const groupId = `group_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        // Find bounds of selected components
        const selectedComponents = components.filter(comp => componentIds.includes(comp.id));
        if (selectedComponents.length === 0) return groupId;

        const minX = Math.min(...selectedComponents.map(comp => comp.position.x));
        const minY = Math.min(...selectedComponents.map(comp => comp.position.y));
        const maxX = Math.max(...selectedComponents.map(comp => comp.position.x + comp.size.width));
        const maxY = Math.max(...selectedComponents.map(comp => comp.position.y + comp.size.height));

        const groupComponent: DesignComponent = {
          id: groupId,
          type: 'group',
          name: 'Group',
          position: { x: minX, y: minY },
          size: { width: maxX - minX, height: maxY - minY },
          properties: {},
          children: selectedComponents.map(comp => ({
            ...comp,
            parentId: groupId,
            position: {
              x: comp.position.x - minX,
              y: comp.position.y - minY,
            },
          })),
        };

        // Update components
        const updatedComponents = components.map(comp => {
          if (componentIds.includes(comp.id)) {
            return {
              ...comp,
              parentId: groupId,
              position: {
                x: comp.position.x - minX,
                y: comp.position.y - minY,
              },
            };
          }
          return comp;
        });

        set({
          components: [...updatedComponents, groupComponent],
        });

        return groupId;
      },

      ungroupComponent: (groupId: string) => {
        const { components } = get();
        const groupComponent = components.find(comp => comp.id === groupId);
        
        if (!groupComponent || !groupComponent.children) return;

        // Move children back to root level
        const ungroupedChildren = groupComponent.children.map(child => ({
          ...child,
          parentId: undefined,
          position: {
            x: child.position.x + groupComponent.position.x,
            y: child.position.y + groupComponent.position.y,
          },
        }));

        set({
          components: [
            ...components.filter(comp => comp.id !== groupId),
            ...ungroupedChildren,
          ],
        });
      },

      isGrouped: (componentId: string) => {
        const { components } = get();
        const component = components.find(comp => comp.id === componentId);
        return component?.parentId !== undefined;
      },

      getGroupChildren: (groupId: string) => {
        const { components } = get();
        return components.filter(comp => comp.parentId === groupId);
      },
    }),
    {
      name: 'component-store',
    }
  )
);
