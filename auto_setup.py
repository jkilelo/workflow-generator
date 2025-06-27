#!/usr/bin/env python3
"""
Auto Setup for Workflow Generator
Automatically generates example workflows and sets up the system post-installation
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from workflow_manager import WorkflowManager
    from workflow_schema import WorkflowSchema
    from workflow_generator import WorkflowGenerator
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("Please ensure all dependencies are installed")
    sys.exit(1)


class AutoSetup:
    """Autonomous setup system for Workflow Generator"""

    def __init__(self):
        self.setup_start_time = time.time()
        self.examples_generated = []
        self.files_created = []

    def print_banner(self):
        """Print setup banner"""
        print("🚀 Workflow Generator - Auto Setup")
        print("==================================")
        print("Generating example workflows and setting up your environment...")
        print()

    def create_directory_structure(self):
        """Create necessary directory structure"""
        print("📁 Creating directory structure...")

        directories = [
            "backend",
            "frontend/src/components/workflows",
            "frontend/src/components/ui",
            "apps",
            "generated_workflows",
            "templates",
            "examples",
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}")

        print()

    def create_ui_components(self):
        """Create basic UI components for React"""
        print("⚛️ Creating base UI components...")

        # Create Button component
        button_component = """import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  size = 'md',
  className = '',
  ...props 
}) => {
  const baseClasses = 'font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-blue-500'
  };
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };
  
  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;
  
  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
};"""

        # Create Input component
        input_component = """import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ 
  label, 
  error, 
  className = '',
  ...props 
}) => {
  const inputClasses = `mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
    focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
    error ? 'border-red-300' : ''
  } ${className}`;
  
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <input className={inputClasses} {...props} />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};"""

        # Create other UI components
        ui_components = {
            "Button.tsx": button_component,
            "Input.tsx": input_component,
            "Select.tsx": """import React from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export const Select: React.FC<SelectProps> = ({ 
  label, 
  error, 
  children,
  className = '',
  ...props 
}) => {
  const selectClasses = `mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
    focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
    error ? 'border-red-300' : ''
  } ${className}`;
  
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <select className={selectClasses} {...props}>
        {children}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};""",
            "TextArea.tsx": """import React from 'react';

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const TextArea: React.FC<TextAreaProps> = ({ 
  label, 
  error, 
  className = '',
  ...props 
}) => {
  const textareaClasses = `mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
    focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
    error ? 'border-red-300' : ''
  } ${className}`;
  
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <textarea className={textareaClasses} {...props} />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};""",
            "FileUpload.tsx": """import React, { useRef } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) -> void;
  accept?: string;
  required?: boolean;
  label?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  accept = "*/*",
  required = false,
  label = "Choose File"
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };
  
  return (
    <div className="mb-4">
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        required={required}
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {label}
      </button>
    </div>
  );
};""",
            "Card.tsx": """import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`bg-white shadow rounded-lg ${className}`}>
      {children}
    </div>
  );
};

export const CardHeader: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`px-6 py-4 border-b border-gray-200 ${className}`}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <h3 className={`text-lg font-medium text-gray-900 ${className}`}>
      {children}
    </h3>
  );
};

export const CardContent: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`px-6 py-4 ${className}`}>
      {children}
    </div>
  );
};""",
        }

        ui_dir = Path("frontend/src/components/ui")
        for filename, content in ui_components.items():
            file_path = ui_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.files_created.append(str(file_path))
            print(f"   ✅ {filename}")

        print()

    def create_example_workflows(self):
        """Create example workflows automatically"""
        print("🔧 Generating example workflows...")

        manager = WorkflowManager()

        # Example 1: Data Processing Pipeline
        data_pipeline_tasks = {
            1: "data input and validation",
            2: "ai-powered data analysis",
            3: "report generation",
            4: "output formatting",
        }

        workflow_id_1 = manager.create_workflow_from_tasks(
            tasks=data_pipeline_tasks,
            workflow_name="Data Processing Pipeline",
            description="Complete data processing workflow with AI analysis",
            category="data_processing",
        )

        # Example 2: Content Generation System
        content_gen_tasks = {
            1: "content input",
            2: "ai content generation",
            3: "quality review",
            4: "publication",
        }

        workflow_id_2 = manager.create_workflow_from_tasks(
            tasks=content_gen_tasks,
            workflow_name="AI Content Generator",
            description="Automated content generation with AI assistance",
            category="content",
        )

        # Example 3: Testing Framework
        testing_tasks = {
            1: "test configuration",
            2: "automated testing",
            3: "result analysis",
            4: "report generation",
        }

        workflow_id_3 = manager.create_workflow_from_tasks(
            tasks=testing_tasks,
            workflow_name="Automated Testing Suite",
            description="Comprehensive automated testing framework",
            category="testing",
        )

        # Deploy all workflows
        workflows = [workflow_id_1, workflow_id_2, workflow_id_3]

        for workflow_id in workflows:
            try:
                paths = manager.deploy_workflow(workflow_id)
                self.examples_generated.append(workflow_id)
                workflow_info = manager.get_workflow_schema(workflow_id)
                print(f"   ✅ {workflow_info.metadata.name} ({workflow_id})")

                # Track created files
                for file_path in paths.values():
                    self.files_created.append(str(file_path))

            except Exception as e:
                print(f"   ❌ Failed to deploy {workflow_id}: {e}")

        print()
        return workflows

    def create_main_server_template(self):
        """Create a basic FastAPI server template"""
        print("🌐 Creating FastAPI server template...")

        server_template = '''#!/usr/bin/env python3
"""
Auto-generated FastAPI Server for Workflow Generator
This server includes all generated workflow plugins
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import importlib.util
import sys

app = FastAPI(
    title="Workflow Generator API",
    description="Auto-generated API server with workflow plugins",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registry for loaded plugins
PLUGINS = {}

@app.get("/")
async def root():
    return {
        "message": "Workflow Generator API Server",
        "version": "1.0.0",
        "plugins": list(PLUGINS.keys())
    }

@app.get("/api/plugins")
async def list_plugins():
    return {
        "plugins": [
            {
                "id": plugin_id,
                "metadata": plugin.metadata.dict() if hasattr(plugin, 'metadata') else {}
            }
            for plugin_id, plugin in PLUGINS.items()
        ]
    }

def load_plugins():
    """Dynamically load all workflow plugins"""
    backend_dir = Path("./backend")
    
    if not backend_dir.exists():
        print("Backend directory not found, skipping plugin loading")
        return
    
    for plugin_file in backend_dir.glob("*_plugin.py"):
        try:
            plugin_name = plugin_file.stem
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'plugin_instance'):
                plugin = module.plugin_instance
                PLUGINS[plugin_name] = plugin
                
                # Register plugin routes
                if hasattr(plugin, 'get_api_routes'):
                    for route_config in plugin.get_api_routes():
                        app.add_api_route(
                            path=f"/api/workflows/{route_config['path']}",
                            endpoint=route_config['handler'],
                            methods=[route_config['method']],
                            response_model=route_config.get('response_model')
                        )
                
                print(f"✅ Loaded plugin: {plugin_name}")
            else:
                print(f"⚠️ Plugin {plugin_name} missing plugin_instance")
                
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_file}: {e}")

# Load plugins on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Loading workflow plugins...")
    load_plugins()
    print(f"📊 Loaded {len(PLUGINS)} plugins")

if __name__ == "__main__":
    print("🌐 Starting Workflow Generator API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''

        server_path = Path("main.py")
        with open(server_path, "w", encoding="utf-8") as f:
            f.write(server_template)

        self.files_created.append(str(server_path))
        print(f"   ✅ main.py")
        print()

    def create_example_configs(self):
        """Create example configuration files"""
        print("⚙️ Creating example configurations...")

        # Create example environment file
        env_example = """# Workflow Generator Environment Configuration
# Copy this file to .env and customize as needed

# Directory paths (relative to project root)
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend/src/components/workflows
APPS_DIR=./apps
BASE_DIR=.

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# LLM Configuration (optional)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# Development settings
DEVELOPMENT=true
LOG_LEVEL=INFO
"""

        with open(".env.example", "w", encoding="utf-8") as f:
            f.write(env_example)

        self.files_created.append(".env.example")
        print(f"   ✅ .env.example")
        print()

    def generate_summary_report(self):
        """Generate setup summary report"""
        setup_time = time.time() - self.setup_start_time

        print("📊 Setup Summary")
        print("===============")
        print(f"⏱️ Setup completed in {setup_time:.2f} seconds")
        print(f"🔧 Generated {len(self.examples_generated)} example workflows:")

        manager = WorkflowManager()
        for workflow_id in self.examples_generated:
            try:
                schema = manager.get_workflow_schema(workflow_id)
                print(f"   • {schema.metadata.name} ({len(schema.steps)} steps)")
            except:
                print(f"   • {workflow_id}")

        print(f"📁 Created {len(self.files_created)} files:")
        for file_path in self.files_created[:10]:  # Show first 10 files
            print(f"   • {file_path}")

        if len(self.files_created) > 10:
            print(f"   ... and {len(self.files_created) - 10} more files")

        print()
        print("🎉 Workflow Generator is ready to use!")
        print()
        print("Next Steps:")
        print("1. Start the API server: python main.py")
        print("2. View generated workflows in ./backend/ and ./frontend/")
        print("3. Create new workflows: python workflow_manager.py --help")
        print("4. Run the demo: python demo_workflow_system.py")
        print()

    def run_setup(self):
        """Run the complete auto setup process"""
        try:
            self.print_banner()
            self.create_directory_structure()
            self.create_ui_components()
            self.create_example_workflows()
            self.create_main_server_template()
            self.create_example_configs()
            self.generate_summary_report()

            return True

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            import traceback

            traceback.print_exc()
            return False


def main():
    """Main entry point for auto setup"""
    setup = AutoSetup()
    success = setup.run_setup()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
