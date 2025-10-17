"""
Web-based Developer UI for AI Agent Project Generation

This module provides a Flask-based web interface for generating AI agent projects
using our data-driven frameworks with a modern, interactive UI.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import zipfile
import tempfile

# Add parent directories to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from schemas.agent_schemas import AgentSchemaGenerator
from mcp.mcp_framework import MCPFramework
from prompting.structured_prompts import PromptFramework, PromptType
from test_data.data_generator import TestDataGenerator, DataContext
from configuration.subject_setting_style import SubjectSettingStyleFramework, SubjectType, SettingType, StyleType


app = Flask(__name__)
app.secret_key = 'ai_agent_project_generator_secret_key'

# Initialize frameworks
schema_generator = AgentSchemaGenerator()
mcp_framework = MCPFramework()
prompt_framework = PromptFramework()
data_generator = TestDataGenerator()
config_framework = SubjectSettingStyleFramework()

# Global project state
current_projects = {}


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/patterns')
def get_patterns():
    """Get available agent patterns"""
    patterns = schema_generator.get_pattern_schemas()
    pattern_list = []
    
    for pattern_id, schema in patterns.items():
        pattern_list.append({
            'id': pattern_id,
            'name': schema['pattern_name'],
            'description': schema['description'],
            'agent_type': schema['agent_type'],
            'domain': schema['domain']
        })
    
    return jsonify(pattern_list)


@app.route('/api/templates')
def get_templates():
    """Get available agent templates"""
    templates = config_framework.get_available_templates()
    template_list = []
    
    for template_name in templates:
        template_info = config_framework.templates[template_name]
        template_list.append({
            'id': template_name,
            'name': template_name.replace('_', ' ').title(),
            'description': template_info['description'],
            'subject': template_info['subject']['primary'],
            'setting': template_info['setting']['primary'],
            'style': template_info['style']['primary']
        })
    
    return jsonify(template_list)


@app.route('/api/domains')
def get_domains():
    """Get available domains"""
    domains = [
        {'id': 'customer_service', 'name': 'Customer Service', 'description': 'Customer support and service'},
        {'id': 'healthcare', 'name': 'Healthcare', 'description': 'Medical and health-related services'},
        {'id': 'e_commerce', 'name': 'E-commerce', 'description': 'Online retail and shopping'},
        {'id': 'technology', 'name': 'Technology', 'description': 'Software and tech development'},
        {'id': 'education', 'name': 'Education', 'description': 'Learning and educational services'},
        {'id': 'finance', 'name': 'Finance', 'description': 'Financial services and banking'},
        {'id': 'other', 'name': 'Other', 'description': 'Custom domain'}
    ]
    return jsonify(domains)


@app.route('/api/project/create', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    project = {
        'id': project_id,
        'name': data.get('name', 'Untitled Project'),
        'description': data.get('description', ''),
        'domain': data.get('domain', 'technology'),
        'patterns': data.get('patterns', []),
        'template': data.get('template', 'customer_service_agent'),
        'capabilities': data.get('capabilities', []),
        'communication_style': data.get('communication_style', 'professional'),
        'integrations': data.get('integrations', []),
        'test_requirements': data.get('test_requirements', {}),
        'created_at': datetime.now().isoformat(),
        'status': 'created'
    }
    
    current_projects[project_id] = project
    
    return jsonify({
        'success': True,
        'project_id': project_id,
        'project': project
    })


@app.route('/api/project/<project_id>')
def get_project(project_id):
    """Get project details"""
    if project_id not in current_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify(current_projects[project_id])


@app.route('/api/project/<project_id>/update', methods=['POST'])
def update_project(project_id):
    """Update project details"""
    if project_id not in current_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    current_projects[project_id].update(data)
    
    return jsonify({
        'success': True,
        'project': current_projects[project_id]
    })


@app.route('/api/project/<project_id>/preview')
def preview_project(project_id):
    """Preview project configuration"""
    if project_id not in current_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    project = current_projects[project_id]
    
    # Generate agent configuration
    agent_config_id = config_framework.create_from_template(
        project['template'], 
        {
            'name': f"{project['name']} Agent",
            'description': project['description']
        }
    )
    
    # Get agent details
    agent_config = config_framework.get_agent_by_id(agent_config_id)
    photographic_prompt = config_framework.generate_photographic_prompt(agent_config_id)
    instructions = config_framework.generate_agent_instructions(agent_config_id)
    
    # Generate pattern schemas
    pattern_schemas = {}
    for pattern_id in project['patterns']:
        schema = schema_generator.generate_schema_for_pattern(pattern_id)
        if schema:
            pattern_schemas[pattern_id] = schema
    
    preview = {
        'agent_config': agent_config.dict() if agent_config else None,
        'photographic_prompt': photographic_prompt,
        'instructions': instructions,
        'pattern_schemas': pattern_schemas,
        'project_structure': _generate_project_structure_preview(project)
    }
    
    return jsonify(preview)


@app.route('/api/project/<project_id>/generate', methods=['POST'])
def generate_project(project_id):
    """Generate the complete project"""
    if project_id not in current_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    project = current_projects[project_id]
    
    try:
        # Create project directory
        project_name = project['name'].replace(' ', '_').lower()
        project_dir = Path(f"generated_projects/{project_name}")
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate all project files
        _generate_project_files(project, project_dir)
        
        # Create zip file
        zip_path = _create_project_zip(project_dir, project_name)
        
        project['status'] = 'generated'
        project['zip_path'] = zip_path
        
        return jsonify({
            'success': True,
            'message': 'Project generated successfully',
            'zip_path': zip_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/project/<project_id>/download')
def download_project(project_id):
    """Download generated project"""
    if project_id not in current_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    project = current_projects[project_id]
    
    if 'zip_path' not in project:
        return jsonify({'error': 'Project not generated yet'}), 400
    
    return send_file(project['zip_path'], as_attachment=True)


def _generate_project_structure_preview(project):
    """Generate project structure preview"""
    structure = {
        'directories': [
            'agents/',
            'configs/',
            'schemas/',
            'prompts/',
            'test_data/',
            'tests/',
            'docs/',
            'scripts/'
        ],
        'files': [
            'main.py',
            'requirements.txt',
            'README.md',
            '.env.example',
            'configs/agent_config.json',
            'configs/mcp_config.json',
            'schemas/selected_patterns.json',
            'prompts/agent_instructions.md'
        ]
    }
    
    # Add pattern-specific files
    for pattern_id in project['patterns']:
        structure['files'].extend([
            f'configs/{pattern_id}_config.json',
            f'prompts/{pattern_id}_prompt.txt'
        ])
    
    # Add test data files
    for data_type in project['test_requirements'].get('data_types', []):
        structure['files'].append(f'test_data/{data_type}.json')
    
    return structure


def _generate_project_files(project, project_dir):
    """Generate all project files"""
    # Generate project structure
    _generate_project_structure(project_dir)
    
    # Generate agent configurations
    _generate_agent_configs(project, project_dir)
    
    # Generate schemas
    _generate_schemas(project, project_dir)
    
    # Generate prompts
    _generate_prompts(project, project_dir)
    
    # Generate test data
    _generate_test_data(project, project_dir)
    
    # Generate MCP configurations
    _generate_mcp_configs(project, project_dir)
    
    # Generate documentation
    _generate_documentation(project, project_dir)
    
    # Generate setup files
    _generate_setup_files(project, project_dir)


def _generate_project_structure(project_dir):
    """Generate basic project structure"""
    dirs = [
        "agents",
        "configs", 
        "schemas",
        "prompts",
        "test_data",
        "tests",
        "docs",
        "scripts"
    ]
    
    for dir_name in dirs:
        (project_dir / dir_name).mkdir(exist_ok=True)
        
        # Create __init__.py files
        init_file = project_dir / dir_name / "__init__.py"
        init_file.write_text('"""Generated AI Agent Project"""\n')


def _generate_agent_configs(project, project_dir):
    """Generate agent configuration files"""
    config_dir = project_dir / "configs"
    
    # Generate main agent config
    agent_config_id = config_framework.create_from_template(
        project['template'],
        {
            'name': f"{project['name']} Agent",
            'description': project['description']
        }
    )
    
    agent_config = config_framework.get_agent_by_id(agent_config_id)
    if agent_config:
        config_data = {
            'agent': agent_config.dict(),
            'capabilities': project.get('capabilities', []),
            'communication_style': project.get('communication_style', 'professional'),
            'integrations': project.get('integrations', [])
        }
        
        with open(config_dir / "agent_config.json", "w") as f:
            json.dump(config_data, f, indent=2, default=str)


def _generate_schemas(project, project_dir):
    """Generate JSON schemas"""
    schema_dir = project_dir / "schemas"
    
    # Generate selected pattern schemas
    selected_schemas = {}
    for pattern_id in project['patterns']:
        schema = schema_generator.generate_schema_for_pattern(pattern_id)
        if schema:
            selected_schemas[pattern_id] = schema
    
    with open(schema_dir / "selected_patterns.json", "w") as f:
        json.dump(selected_schemas, f, indent=2, default=str)


def _generate_prompts(project, project_dir):
    """Generate structured prompts"""
    prompt_dir = project_dir / "prompts"
    
    # Generate agent instructions
    agent_config_id = config_framework.create_from_template(
        project['template'],
        {
            'name': f"{project['name']} Agent",
            'description': project['description']
        }
    )
    
    instructions = config_framework.generate_agent_instructions(agent_config_id)
    with open(prompt_dir / "agent_instructions.md", "w") as f:
        f.write(instructions)


def _generate_test_data(project, project_dir):
    """Generate test data"""
    test_dir = project_dir / "test_data"
    test_requirements = project.get('test_requirements', {})
    
    if not test_requirements:
        return
    
    # Generate test data for each type
    for data_type in test_requirements.get('data_types', []):
        volume = test_requirements.get('volume', 1000)
        context = DataContext.TECHNOLOGY  # Default context
        
        if data_type == "user_profiles":
            data = data_generator.generate_user_profiles(volume // 10, context)
        elif data_type == "conversations":
            users = data_generator.generate_user_profiles(10, context)
            data = data_generator.generate_conversations(volume // 5, users, context)
        elif data_type == "tasks":
            data = data_generator.generate_tasks(volume // 20, context)
        elif data_type == "events":
            users = data_generator.generate_user_profiles(10, context)
            data = data_generator.generate_events(volume // 10, users, context)
        elif data_type == "metrics":
            data = data_generator.generate_metrics(volume // 50, context)
        elif data_type == "documents":
            data = data_generator.generate_documents(volume // 100, context)
        else:
            continue
        
        # Save test data
        with open(test_dir / f"{data_type}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)


def _generate_mcp_configs(project, project_dir):
    """Generate MCP configurations"""
    config_dir = project_dir / "configs"
    
    mcp_config = {
        'tools': project.get('integrations', []),
        'settings': {
            'timeout': 30,
            'retry_attempts': 3,
            'concurrent_requests': 10
        }
    }
    
    with open(config_dir / "mcp_config.json", "w") as f:
        json.dump(mcp_config, f, indent=2)


def _generate_documentation(project, project_dir):
    """Generate project documentation"""
    # Generate README
    readme_content = f"""# {project['name']}

## Description
{project['description']}

## Domain
{project['domain'].replace('_', ' ').title()}

## Agent Patterns
{chr(10).join([f"- {pattern_id}" for pattern_id in project['patterns']])}

## Capabilities
{chr(10).join([f"- {cap}" for cap in project.get('capabilities', [])])}

## Communication Style
{project.get('communication_style', 'Professional')}

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Testing

Run tests with:
```bash
python -m pytest tests/
```
"""
    
    with open(project_dir / "README.md", "w") as f:
        f.write(readme_content)


def _generate_setup_files(project, project_dir):
    """Generate setup and configuration files"""
    # Generate requirements.txt
    requirements = [
        "pydantic>=2.0.0",
        "asyncio",
        "requests",
        "flask",
        "pathlib",
        "datetime",
        "uuid",
        "json",
        "typing"
    ]
    
    with open(project_dir / "requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    # Generate .env.example
    env_example = f"""# Agent Configuration
AGENT_NAME={project['name']}
AGENT_DESCRIPTION={project['description']}
AGENT_DOMAIN={project['domain']}

# Database Configuration
DATABASE_URL=sqlite:///agent_data.db

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# MCP Configuration
MCP_TIMEOUT=30
MCP_RETRY_ATTEMPTS=3
"""
    
    with open(project_dir / ".env.example", "w") as f:
        f.write(env_example)
    
    # Generate main.py
    main_py = f'''"""
{project['name']} - AI Agent Project
Generated by AI Agent Project Generator
"""

import asyncio
import json
from pathlib import Path

async def main():
    """Main entry point for the agent"""
    print("🤖 Starting {project['name']} Agent")
    print("=" * 50)
    
    print(f"Agent: {project['name']}")
    print(f"Description: {project['description']}")
    print(f"Domain: {project['domain']}")
    print(f"Capabilities: {', '.join(project.get('capabilities', []))}")
    
    print("\\n🚀 Agent is ready!")

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open(project_dir / "main.py", "w") as f:
        f.write(main_py)


def _create_project_zip(project_dir, project_name):
    """Create a zip file of the generated project"""
    zip_path = f"generated_projects/{project_name}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(project_dir)
                zipf.write(file_path, arcname)
    
    return zip_path


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create basic HTML template
    html_template = templates_dir / 'index.html'
    if not html_template.exists():
        html_template.write_text('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Project Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .step { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .step h3 { margin-top: 0; color: #333; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .form-group textarea { height: 100px; resize: vertical; }
        .checkbox-group { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .checkbox-item { display: flex; align-items: center; }
        .checkbox-item input { width: auto; margin-right: 8px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #545b62; }
        .preview { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 15px; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Agent Project Generator</h1>
            <p>Create sophisticated AI agent projects using our data-driven frameworks</p>
        </div>
        
        <form id="projectForm">
            <div class="step">
                <h3>📋 Basic Information</h3>
                <div class="form-group">
                    <label for="projectName">Project Name</label>
                    <input type="text" id="projectName" name="name" required>
                </div>
                <div class="form-group">
                    <label for="projectDescription">Description</label>
                    <textarea id="projectDescription" name="description" required></textarea>
                </div>
                <div class="form-group">
                    <label for="domain">Domain</label>
                    <select id="domain" name="domain" required>
                        <option value="technology">Technology</option>
                        <option value="customer_service">Customer Service</option>
                        <option value="healthcare">Healthcare</option>
                        <option value="e_commerce">E-commerce</option>
                        <option value="education">Education</option>
                        <option value="finance">Finance</option>
                    </select>
                </div>
            </div>
            
            <div class="step">
                <h3>🤖 Agent Patterns</h3>
                <div class="checkbox-group" id="patternsContainer">
                    <!-- Patterns will be loaded dynamically -->
                </div>
            </div>
            
            <div class="step">
                <h3>🎭 Agent Configuration</h3>
                <div class="form-group">
                    <label for="template">Agent Template</label>
                    <select id="template" name="template" required>
                        <option value="customer_service_agent">Customer Service Agent</option>
                        <option value="technical_analyst">Technical Analyst</option>
                        <option value="creative_writer">Creative Writer</option>
                        <option value="project_manager">Project Manager</option>
                        <option value="healthcare_assistant">Healthcare Assistant</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="capabilities">Capabilities (comma-separated)</label>
                    <input type="text" id="capabilities" name="capabilities" placeholder="e.g., problem solving, data analysis, customer support">
                </div>
                <div class="form-group">
                    <label for="communicationStyle">Communication Style</label>
                    <select id="communicationStyle" name="communication_style">
                        <option value="professional">Professional and formal</option>
                        <option value="friendly">Friendly and casual</option>
                        <option value="technical">Technical and precise</option>
                        <option value="empathetic">Empathetic and supportive</option>
                        <option value="creative">Creative and engaging</option>
                    </select>
                </div>
            </div>
            
            <div class="step">
                <h3>🔗 External Integrations</h3>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="database" name="integrations" value="database">
                        <label for="database">Database Integration</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="api" name="integrations" value="api">
                        <label for="api">API Integration</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="fileProcessing" name="integrations" value="file_processing">
                        <label for="fileProcessing">File Processing</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="imageProcessing" name="integrations" value="image_processing">
                        <label for="imageProcessing">Image Processing</label>
                    </div>
                </div>
            </div>
            
            <div class="step">
                <h3>🧪 Testing Requirements</h3>
                <div class="form-group">
                    <label for="testDataTypes">Test Data Types</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="userProfiles" name="test_data_types" value="user_profiles" checked>
                            <label for="userProfiles">User Profiles</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="conversations" name="test_data_types" value="conversations" checked>
                            <label for="conversations">Conversations</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="tasks" name="test_data_types" value="tasks">
                            <label for="tasks">Tasks</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="events" name="test_data_types" value="events">
                            <label for="events">Events</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="metrics" name="test_data_types" value="metrics">
                            <label for="metrics">Metrics</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="documents" name="test_data_types" value="documents">
                            <label for="documents">Documents</label>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label for="testVolume">Test Data Volume</label>
                    <select id="testVolume" name="test_volume">
                        <option value="100">Small (100 records)</option>
                        <option value="500" selected>Medium (500 records)</option>
                        <option value="1000">Large (1000 records)</option>
                        <option value="5000">Very Large (5000 records)</option>
                    </select>
                </div>
            </div>
            
            <div class="step">
                <h3>📊 Preview & Generate</h3>
                <button type="button" class="btn btn-secondary" onclick="previewProject()">Preview Project</button>
                <button type="button" class="btn" onclick="generateProject()">Generate Project</button>
                <div id="preview" class="preview hidden"></div>
            </div>
        </form>
    </div>
    
    <script>
        let currentProjectId = null;
        
        // Load patterns on page load
        window.onload = function() {
            loadPatterns();
        };
        
        async function loadPatterns() {
            try {
                const response = await fetch('/api/patterns');
                const patterns = await response.json();
                
                const container = document.getElementById('patternsContainer');
                patterns.forEach(pattern => {
                    const checkboxItem = document.createElement('div');
                    checkboxItem.className = 'checkbox-item';
                    checkboxItem.innerHTML = `
                        <input type="checkbox" id="${pattern.id}" name="patterns" value="${pattern.id}">
                        <label for="${pattern.id}">${pattern.name}</label>
                    `;
                    container.appendChild(checkboxItem);
                });
            } catch (error) {
                console.error('Error loading patterns:', error);
            }
        }
        
        async function previewProject() {
            const formData = new FormData(document.getElementById('projectForm'));
            const projectData = {
                name: formData.get('name'),
                description: formData.get('description'),
                domain: formData.get('domain'),
                patterns: formData.getAll('patterns'),
                template: formData.get('template'),
                capabilities: formData.get('capabilities').split(',').map(c => c.trim()).filter(c => c),
                communication_style: formData.get('communication_style'),
                integrations: formData.getAll('integrations'),
                test_requirements: {
                    data_types: formData.getAll('test_data_types'),
                    volume: parseInt(formData.get('test_volume'))
                }
            };
            
            try {
                const response = await fetch('/api/project/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(projectData)
                });
                
                const result = await response.json();
                if (result.success) {
                    currentProjectId = result.project_id;
                    await showPreview(result.project_id);
                }
            } catch (error) {
                console.error('Error creating project:', error);
                alert('Error creating project: ' + error.message);
            }
        }
        
        async function showPreview(projectId) {
            try {
                const response = await fetch(`/api/project/${projectId}/preview`);
                const preview = await response.json();
                
                const previewDiv = document.getElementById('preview');
                previewDiv.innerHTML = `
                    <h4>Project Preview</h4>
                    <p><strong>Agent:</strong> ${preview.agent_config?.name || 'N/A'}</p>
                    <p><strong>Photographic Description:</strong> ${preview.photographic_prompt || 'N/A'}</p>
                    <p><strong>Patterns:</strong> ${Object.keys(preview.pattern_schemas || {}).length} selected</p>
                    <p><strong>Files to be generated:</strong> ${preview.project_structure?.files?.length || 0} files</p>
                `;
                previewDiv.classList.remove('hidden');
            } catch (error) {
                console.error('Error loading preview:', error);
            }
        }
        
        async function generateProject() {
            if (!currentProjectId) {
                alert('Please preview the project first');
                return;
            }
            
            try {
                const response = await fetch(`/api/project/${currentProjectId}/generate`, {
                    method: 'POST'
                });
                
                const result = await response.json();
                if (result.success) {
                    alert('Project generated successfully!');
                    // Download the project
                    window.location.href = `/api/project/${currentProjectId}/download`;
                } else {
                    alert('Error generating project: ' + result.error);
                }
            } catch (error) {
                console.error('Error generating project:', error);
                alert('Error generating project: ' + error.message);
            }
        }
    </script>
</body>
</html>
        ''')
    
    app.run(debug=True, host='0.0.0.0', port=5000)





