# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Generic Workflow Generator system that auto-generates FastAPI backend and React frontend code from workflow schema definitions. The system creates production-ready code that integrates with existing app_generator architectures while being completely generic and extensible.

## Core Architecture

The system consists of three main components:

- **workflow_schema.py**: Defines the schema structure for workflows using Pydantic models with comprehensive parameter types and step definitions
- **workflow_generator.py**: Generates FastAPI plugins and React TypeScript components from workflow schemas using Jinja2 templates
- **workflow_manager.py**: Manages workflow creation, integration, and deployment with automatic step type inference

## Environment Configuration

The system uses environment variables for path configuration to avoid hardcoded paths:

- `BACKEND_DIR`: Backend directory (default: `./backend`)  
- `FRONTEND_DIR`: Frontend components directory (default: `./frontend/src/components/workflows`)
- `APPS_DIR`: Apps configuration directory (default: `./apps`)
- `BASE_DIR`: Base project directory (default: current working directory)

## Common Commands

### Running the Demo System
```bash
python demo_workflow_system.py
```

### Running Integration Tests
```bash
python integration_test_summary.py
```

### Creating a Workflow from Command Line
```bash
python workflow_manager.py --create "data input" "ai processing" "output generation" --name "My Workflow"
```

### Deploying a Workflow
```bash
python workflow_manager.py --deploy workflow_id
```

### Listing All Workflows
```bash
python workflow_manager.py --list
```

### Creating Example Workflow
```bash
python workflow_manager.py --example
```

## Key Features

### Auto-Generation Capabilities
- FastAPI plugin generation with proper type hints and validation
- React TypeScript component generation with dynamic forms
- LLM integration with configurable providers (OpenAI, Anthropic, Google)
- Automatic step type inference from task descriptions
- Parameter validation and error handling
- State management integration

### Supported Step Types
- **FORM_INPUT**: Dynamic form generation based on parameter schemas
- **LLM_PROCESSING**: AI processing with template system and provider selection
- **FILE_PROCESSING**: File upload and processing capabilities
- **HTTP_REQUEST**: Web crawling and API integration
- **CODE_EXECUTION**: Custom code execution with handlers
- **DATA_TRANSFORMATION**: Generic data processing steps

### Parameter Types
- STRING, NUMBER, BOOLEAN, FILE, SELECT, MULTISELECT
- TEXT_AREA, JSON, DATE, URL, EMAIL
- Validation rules and conditional visibility support

## File Generation

Each workflow generates 4 files:
- `{workflow_id}_plugin.py`: FastAPI backend plugin
- `{workflow_id}_workflow.tsx`: React TypeScript component  
- `config.json`: App configuration for integration
- `schema.json`: Complete workflow schema definition

## Integration Pattern

Generated plugins follow the BasePlugin interface and integrate with:
- LLMManager for AI processing
- Existing API route registration
- Frontend state management stores
- Standard validation and error handling patterns

## Development Workflow

1. Define tasks as simple dictionary: `{1: "task description", 2: "another task"}`
2. Use WorkflowManager to create workflow from tasks
3. System automatically infers step types and parameters
4. Deploy generates all necessary files
5. Integration code provided for main API server

## Testing

The system includes comprehensive integration testing that validates:
- Generated code syntax and compilation
- API endpoint registration and responses
- File generation and structure
- Schema validation and workflow execution order
- Frontend/backend integration