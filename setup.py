#!/usr/bin/env python3
"""
Setup script for Workflow Generator
Autonomous installation with automatic dependency management and example generation
"""

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess
import json

class PostInstallCommand(install):
    """Post-installation command to set up examples and run initial setup"""
    
    def run(self):
        install.run(self)
        
        # Run post-install setup
        try:
            print("🚀 Running post-installation setup...")
            
            # Create default directories
            self.create_default_structure()
            
            # Run auto setup
            import auto_setup
            auto_setup.main()
            
            print("✅ Workflow Generator installation complete!")
            print("🎉 Example workflows have been generated and are ready to use!")
            
        except Exception as e:
            print(f"⚠️ Post-install setup encountered an issue: {e}")
            print("You can manually run: python auto_setup.py")
    
    def create_default_structure(self):
        """Create default directory structure"""
        dirs = [
            'backend',
            'frontend/src/components/workflows',
            'apps',
            'generated_workflows'
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 Created directory: {dir_path}")

# Read version from version file
def get_version():
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return '1.0.0'

# Read requirements
def get_requirements():
    try:
        with open('requirements.txt', 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return [
            'fastapi>=0.104.0',
            'pydantic>=2.0.0',
            'jinja2>=3.1.0',
            'requests>=2.31.0',
            'uvicorn>=0.24.0',
            'python-multipart>=0.0.6'
        ]

# Read long description
def get_long_description():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
# Workflow Generator

An autonomous system for generating FastAPI backend and React frontend workflows from simple task definitions.

## Features

- Auto-generates FastAPI plugins with proper type hints
- Creates React TypeScript components with dynamic forms  
- Supports LLM integration with multiple providers
- Automatic dependency management and setup
- Production-ready code generation
- Complete project structure creation

## Quick Start

```bash
pip install workflow-generator
# System will auto-setup and generate examples!
```
"""

setup(
    name="workflow-generator",
    version=get_version(),
    author="Workflow Generator Team",
    author_email="contact@workflow-generator.dev",
    description="Autonomous workflow generation system for FastAPI and React applications",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/workflow-generator/workflow-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'llm': [
            'openai>=1.0.0',
            'anthropic>=0.7.0',
            'google-generativeai>=0.3.0',
        ]
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'workflow-generator=workflow_manager:main',
            'wfgen=workflow_manager:main',
            'workflow-demo=demo_workflow_system:main',
        ],
    },
    include_package_data=True,
    package_data={
        'workflow_generator': [
            'templates/*.j2',
            'examples/*.json',
            'VERSION',
        ],
    },
    zip_safe=False,
    keywords="workflow fastapi react generator automation ai llm",
    project_urls={
        "Bug Reports": "https://github.com/workflow-generator/workflow-generator/issues",
        "Source": "https://github.com/workflow-generator/workflow-generator",
        "Documentation": "https://workflow-generator.readthedocs.io/",
    },
)