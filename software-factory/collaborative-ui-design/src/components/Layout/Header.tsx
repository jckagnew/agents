import React from 'react';
import { 
  Save, 
  Download, 
  Upload, 
  Share2, 
  Settings, 
  User,
  Menu,
  Play,
  Square,
  RotateCcw,
  BookOpen,
  Globe, // Added Globe icon for Website Analyzer
} from 'lucide-react';

import { useCanvasStore } from '../../stores/canvasStore';

interface HeaderProps {
  onToggleDesignSkills?: () => void;
  onToggleWebsiteAnalyzer?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleDesignSkills, onToggleWebsiteAnalyzer }) => {
  const { isDirty, canUndo, canRedo, undo, redo } = useCanvasStore();

  const handleSave = () => {
    // TODO: Implement save functionality
    console.log('Saving project...');
  };

  const handleExport = () => {
    // TODO: Implement export functionality
    console.log('Exporting project...');
  };

  const handleImport = () => {
    // TODO: Implement import functionality
    console.log('Importing project...');
  };

  const handleShare = () => {
    // TODO: Implement share functionality
    console.log('Sharing project...');
  };

  const handlePreview = () => {
    // TODO: Implement preview functionality
    console.log('Previewing project...');
  };

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left side - Logo and project info */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">UI</span>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-gray-900">Collaborative UI Design</h1>
              <p className="text-xs text-gray-500">Untitled Project {isDirty && '• Unsaved'}</p>
            </div>
          </div>
        </div>

        {/* Center - Project controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={undo}
            disabled={!canUndo}
            className="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Undo"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          
          <button
            onClick={redo}
            disabled={!canRedo}
            className="p-2 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Redo"
          >
            <RotateCcw className="w-4 h-4 transform rotate-180" />
          </button>

          <div className="w-px h-6 bg-gray-300" />

          <button
            onClick={handlePreview}
            className="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Play className="w-4 h-4" />
            <span className="text-sm font-medium">Preview</span>
          </button>

          <button
            onClick={onToggleDesignSkills}
            className="flex items-center space-x-2 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            title="Design Skills Guide"
          >
            <BookOpen className="w-4 h-4" />
            <span className="text-sm font-medium">Skills</span>
          </button>

          <button
            onClick={onToggleWebsiteAnalyzer}
            className="flex items-center space-x-2 px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            title="Website Analyzer"
          >
            <Globe className="w-4 h-4" />
            <span className="text-sm font-medium">Analyze</span>
          </button>
        </div>

        {/* Right side - Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={handleSave}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              isDirty
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Save className="w-4 h-4" />
            <span className="text-sm font-medium">Save</span>
          </button>

          <button
            onClick={handleExport}
            className="flex items-center space-x-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span className="text-sm font-medium">Export</span>
          </button>

          <button
            onClick={handleImport}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded transition-colors"
            title="Import"
          >
            <Upload className="w-4 h-4" />
          </button>

          <button
            onClick={handleShare}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded transition-colors"
            title="Share"
          >
            <Share2 className="w-4 h-4" />
          </button>

          <div className="w-px h-6 bg-gray-300" />

          <button
            className="p-2 text-gray-600 hover:bg-gray-100 rounded transition-colors"
            title="Settings"
          >
            <Settings className="w-4 h-4" />
          </button>

          <button
            className="p-2 text-gray-600 hover:bg-gray-100 rounded transition-colors"
            title="Account"
          >
            <User className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
