import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { WebsiteAnalyzer } from '../WebsiteAnalyzer';
import { useComponentStore } from '../../../stores/componentStore';

// Mock the component store
jest.mock('../../../stores/componentStore');
const mockUseComponentStore = useComponentStore as jest.MockedFunction<typeof useComponentStore>;

describe('WebsiteAnalyzer', () => {
  const mockAddComponent = jest.fn();
  
  beforeEach(() => {
    mockUseComponentStore.mockReturnValue({
      addComponent: mockAddComponent,
      // Add other required properties with default values
      components: [],
      loadComponentLibrary: jest.fn(),
      updateComponent: jest.fn(),
      deleteComponent: jest.fn(),
      selectedComponent: null,
      setSelectedComponent: jest.fn(),
    });
    jest.clearAllMocks();
  });

  it('renders the website analyzer component', () => {
    render(<WebsiteAnalyzer />);
    
    expect(screen.getByText('Website Analyzer')).toBeInTheDocument();
    expect(screen.getByLabelText('Website URL')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument();
  });

  it('disables analyze button when URL is empty', () => {
    render(<WebsiteAnalyzer />);
    
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    expect(analyzeButton).toBeDisabled();
  });

  it('enables analyze button when URL is provided', () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    
    expect(analyzeButton).not.toBeDisabled();
  });

  it('shows loading state during analysis', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /analyze/i })).toBeDisabled();
  });

  it('displays analysis results after successful analysis', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for analysis sections
    expect(screen.getByText('Color Palette')).toBeInTheDocument();
    expect(screen.getByText('Typography Scale')).toBeInTheDocument();
    expect(screen.getByText('Component Patterns')).toBeInTheDocument();
    expect(screen.getByText('Extracted Components')).toBeInTheDocument();
    expect(screen.getByText('Recommendations')).toBeInTheDocument();
  });

  it('displays color palette correctly', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for color palette items
    const colorItems = screen.getAllByText(/#[0-9A-F]{6}/i);
    expect(colorItems.length).toBeGreaterThan(0);
  });

  it('displays typography scale correctly', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for typography scale items
    expect(screen.getByText('h1')).toBeInTheDocument();
    expect(screen.getByText('body')).toBeInTheDocument();
  });

  it('displays component patterns correctly', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for component patterns
    expect(screen.getByText('Hero Section')).toBeInTheDocument();
    expect(screen.getByText('Feature Cards')).toBeInTheDocument();
  });

  it('displays extracted components correctly', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for extracted components
    expect(screen.getByText('Hero Section')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add to library/i })).toBeInTheDocument();
  });

  it('calls addComponent when Add to Library is clicked', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    const addButton = screen.getByRole('button', { name: /add to library/i });
    fireEvent.click(addButton);
    
    expect(mockAddComponent).toHaveBeenCalledWith(
      expect.objectContaining({
        id: 'hero-section-extracted',
        name: 'Hero Section',
        category: 'extracted'
      })
    );
  });

  it('displays recommendations correctly', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Check for recommendations
    expect(screen.getByText(/Consider adding more visual hierarchy/)).toBeInTheDocument();
    expect(screen.getByText(/Increase contrast ratio/)).toBeInTheDocument();
  });

  it('handles analysis errors gracefully', async () => {
    // Mock console.error to avoid error logs in test output
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    fireEvent.change(urlInput, { target: { value: 'https://invalid-url.com' } });
    fireEvent.click(analyzeButton);
    
    // The component should handle errors gracefully
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    consoleSpy.mockRestore();
  });

  it('resets form state when new analysis is started', async () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    // First analysis
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Complete')).toBeInTheDocument();
    });
    
    // Start new analysis
    fireEvent.change(urlInput, { target: { value: 'https://another-site.com' } });
    fireEvent.click(analyzeButton);
    
    // Should show loading state
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();
  });

  it('displays proper accessibility attributes', () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    expect(urlInput).toHaveAttribute('type', 'url');
    expect(urlInput).toHaveAttribute('placeholder', 'https://example.com');
    expect(analyzeButton).toHaveAttribute('title', 'Website Analyzer');
  });

  it('handles keyboard navigation', () => {
    render(<WebsiteAnalyzer />);
    
    const urlInput = screen.getByLabelText('Website URL');
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    
    // Tab navigation should work
    urlInput.focus();
    expect(urlInput).toHaveFocus();
    
    // Enter key should trigger analysis
    fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
    fireEvent.keyDown(urlInput, { key: 'Enter', code: 'Enter' });
    
    // Button should be enabled
    expect(analyzeButton).not.toBeDisabled();
  });
});
