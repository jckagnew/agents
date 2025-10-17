import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { CanvasState, CanvasAction, CanvasActionType } from '../types/canvas';
import { DesignComponent, Position, Size } from '../types/components';

interface CanvasStore extends CanvasState {
  // Actions
  setZoom: (zoom: number) => void;
  setPan: (pan: Position) => void;
  selectComponent: (componentId: string) => void;
  selectComponents: (componentIds: string[]) => void;
  deselectComponent: (componentId: string) => void;
  deselectAll: () => void;
  addToClipboard: (components: DesignComponent[]) => void;
  clearClipboard: () => void;
  addAction: (action: Omit<CanvasAction, 'id' | 'timestamp'>) => void;
  undo: () => void;
  redo: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;
  setDirty: (isDirty: boolean) => void;
  toggleGrid: () => void;
  toggleSnapToGrid: () => void;
  setGridSize: (size: number) => void;
  toggleRulers: () => void;
  toggleGuides: () => void;
  reset: () => void;
}

const initialState: CanvasState = {
  zoom: 1,
  pan: { x: 0, y: 0 },
  selectedComponents: [],
  clipboard: [],
  history: {
    past: [],
    present: null,
    future: [],
    maxHistorySize: 50,
  },
  isDirty: false,
  gridEnabled: true,
  snapToGrid: true,
  gridSize: 20,
  showRulers: true,
  showGuides: true,
};

export const useCanvasStore = create<CanvasStore>()(
  devtools(
    (set, get) => ({
      ...initialState,

      setZoom: (zoom: number) => {
        set({ zoom: Math.max(0.1, Math.min(5, zoom)) });
      },

      setPan: (pan: Position) => {
        set({ pan });
      },

      selectComponent: (componentId: string) => {
        const { selectedComponents } = get();
        if (!selectedComponents.includes(componentId)) {
          set({ selectedComponents: [...selectedComponents, componentId] });
        }
      },

      selectComponents: (componentIds: string[]) => {
        set({ selectedComponents: componentIds });
      },

      deselectComponent: (componentId: string) => {
        const { selectedComponents } = get();
        set({ 
          selectedComponents: selectedComponents.filter(id => id !== componentId) 
        });
      },

      deselectAll: () => {
        set({ selectedComponents: [] });
      },

      addToClipboard: (components: DesignComponent[]) => {
        set({ clipboard: components });
      },

      clearClipboard: () => {
        set({ clipboard: [] });
      },

      addAction: (actionData) => {
        const { history } = get();
        const action: CanvasAction = {
          ...actionData,
          id: `action_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          timestamp: new Date(),
        };

        const newHistory = {
          ...history,
          past: [...history.past, history.present].filter((item): item is CanvasAction => item !== null),
          present: action,
          future: [], // Clear future when new action is added
        };

        // Limit history size
        if (newHistory.past.length > history.maxHistorySize) {
          newHistory.past = newHistory.past.slice(-history.maxHistorySize);
        }

        set({ 
          history: newHistory,
          isDirty: true 
        });
      },

      undo: () => {
        const { history } = get();
        if (history.past.length === 0) return;

        const previous = history.past[history.past.length - 1];
        const newPast = history.past.slice(0, -1);

        set({
          history: {
            ...history,
            past: newPast,
            present: previous,
            future: [history.present, ...history.future].filter((item): item is CanvasAction => item !== null),
          },
          isDirty: true,
        });
      },

      redo: () => {
        const { history } = get();
        if (history.future.length === 0) return;

        const next = history.future[0];
        const newFuture = history.future.slice(1);

        set({
          history: {
            ...history,
            past: [...history.past, history.present].filter((item): item is CanvasAction => item !== null),
            present: next,
            future: newFuture,
          },
          isDirty: true,
        });
      },

      canUndo: () => {
        const { history } = get();
        return history.past.length > 0;
      },

      canRedo: () => {
        const { history } = get();
        return history.future.length > 0;
      },

      setDirty: (isDirty: boolean) => {
        set({ isDirty });
      },

      toggleGrid: () => {
        const { gridEnabled } = get();
        set({ gridEnabled: !gridEnabled });
      },

      toggleSnapToGrid: () => {
        const { snapToGrid } = get();
        set({ snapToGrid: !snapToGrid });
      },

      setGridSize: (size: number) => {
        set({ gridSize: Math.max(5, Math.min(100, size)) });
      },

      toggleRulers: () => {
        const { showRulers } = get();
        set({ showRulers: !showRulers });
      },

      toggleGuides: () => {
        const { showGuides } = get();
        set({ showGuides: !showGuides });
      },

      reset: () => {
        set(initialState);
      },
    }),
    {
      name: 'canvas-store',
    }
  )
);
