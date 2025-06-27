# Workflow Generator 🚀

**Autonomous workflow generation system for FastAPI and React applications**

Generate production-ready FastAPI backend plugins and React TypeScript components from simple task definitions. The system automatically handles dependency installation, example generation, and complete project setup.

## 🎯 Key Features

- **🤖 Autonomous Setup**: Installs all dependencies and generates examples automatically
- **⚡ Instant Generation**: Create full-stack workflows from simple task lists
- **🔧 FastAPI Integration**: Auto-generates FastAPI plugins with proper type hints
- **⚛️ React Components**: Creates TypeScript components with dynamic forms
- **🧠 LLM Integration**: Built-in support for OpenAI, Anthropic, and Google AI
- **📦 Zero Configuration**: Works out-of-the-box with sensible defaults
- **🎨 UI Components**: Includes complete UI component library
- **📊 Real-time Execution**: Step-by-step workflow execution with progress tracking

## 🚀 Quick Start

### **One-Command Demo (Recommended)**
```bash
# Clone the repository
git clone https://github.com/yourusername/workflow-generator.git
cd workflow-generator

# Linux/Mac: Run the demo script
./run_demo.sh

# Windows: Run the demo script
run_demo.bat
```

The demo script automatically:
- ✅ Sets up Python virtual environment
- ✅ Installs all dependencies  
- ✅ Runs autonomous setup
- ✅ Starts FastAPI server
- ✅ Opens browser to http://localhost:8003
- ✅ Monitors services and provides logging

### **Hello Workflow Demo (Standalone)**
```bash
# Generate a complete standalone workflow project
./demo_hello_workflow.sh

# This creates ./hello_workflow/ with:
# - Complete FastAPI backend
# - React frontend interface  
# - Auto-generated workflow files
# - Standalone server on http://localhost:8004
```

### **Manual Setup**
```bash
# Clone and setup manually
git clone https://github.com/yourusername/workflow-generator.git
cd workflow-generator
python auto_setup.py

# Start the interactive server
source venv/bin/activate
python live_server.py

# Open browser to http://localhost:8003
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/workflow-generator.git
cd workflow-generator

# Run autonomous setup (installs everything automatically)
python auto_setup.py
```

### Python Package Installation

```bash
# Install from PyPI (when available)
pip install workflow-generator

# Or install from source
pip install -e .
```

That's it! The system will automatically:
- ✅ Install Python and Node.js dependencies
- ✅ Create directory structure
- ✅ Generate 3 example workflows
- ✅ Set up FastAPI server
- ✅ Create React UI components
- ✅ Start the development server

## 📖 Usage Examples

### Creating Workflows from Task Lists

```python
from workflow_manager import WorkflowManager

manager = WorkflowManager()

# Define your workflow as simple tasks
tasks = {
    1: "data input and validation",
    2: "ai-powered analysis", 
    3: "report generation",
    4: "email notification"
}

# Auto-generate complete workflow
workflow_id = manager.create_workflow_from_tasks(
    tasks=tasks,
    workflow_name="Business Intelligence Pipeline",
    category="business"
)

# Deploy to generate all files
manager.deploy_workflow(workflow_id)
```

### Command Line Usage

```bash
# Create workflow from command line
workflow-generator --create "data analysis" "ai processing" "report generation" --name "Analytics Pipeline"

# Deploy existing workflow
workflow-generator --deploy analytics_pipeline

# List all workflows
workflow-generator --list

# Generate comprehensive example
workflow-generator --example

# Run demo system
workflow-demo
```

### Generated File Structure

```
your-project/
├── backend/
│   ├── analytics_pipeline_plugin.py      # FastAPI plugin
│   └── main.py                           # Auto-generated server
├── frontend/src/components/
│   ├── workflows/
│   │   └── analytics_pipeline_workflow.tsx  # React component
│   └── ui/                               # UI component library
├── apps/analytics_pipeline/
│   ├── config.json                       # App configuration
│   └── schema.json                       # Workflow schema
└── generated_workflows/                   # Generated artifacts
```

## 🏗️ Architecture

### Core Components

- **`workflow_schema.py`**: Pydantic models for workflow definitions
- **`workflow_generator.py`**: Jinja2-based code generation engine
- **`workflow_manager.py`**: High-level workflow management and deployment
- **`auto_setup.py`**: Autonomous setup and example generation

### Supported Step Types

| Step Type | Description | Auto-Generated Features |
|-----------|-------------|-------------------------|
| `FORM_INPUT` | User input forms | Dynamic form validation, file uploads |
| `LLM_PROCESSING` | AI/LLM integration | Provider selection, prompt templates |
| `HTTP_REQUEST` | Web scraping/APIs | URL validation, response handling |
| `CODE_EXECUTION` | Custom code | Error handling, timeout management |
| `FILE_PROCESSING` | File operations | Upload handling, format validation |
| `DATA_TRANSFORMATION` | Data processing | Schema validation, type conversion |

### Parameter Types

- **Basic**: `STRING`, `NUMBER`, `BOOLEAN`, `DATE`
- **Advanced**: `SELECT`, `MULTISELECT`, `TEXT_AREA`, `JSON`
- **Special**: `FILE`, `URL`, `EMAIL`
- **Validation**: Custom rules, conditional visibility

## ⚙️ Configuration

### Environment Variables

```bash
# Directory paths (auto-configured)
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend/src/components/workflows
APPS_DIR=./apps

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# LLM providers (optional)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

### Custom Configuration

```python
# Custom directory setup
manager = WorkflowManager(
    backend_dir="./my-backend",
    frontend_dir="./my-frontend/components",
    apps_dir="./my-apps"
)
```

## 🎨 Generated Code Examples

### FastAPI Plugin

```python
# Auto-generated backend plugin
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from base_plugin import BasePlugin

class DataAnalysisPlugin(BasePlugin):
    async def step_1(self, request: Step1Request):
        # Auto-generated with proper validation
        return Step1Response(success=True, data=result)
```

### React Component

```tsx
// Auto-generated React component
import React, { useState } from 'react';
import { Button, Input, Select } from '../ui';

const DataAnalysisWorkflow: React.FC<Props> = ({ appId }) => {
  // Auto-generated form handling
  const [step1Form, setStep1Form] = useState({});
  
  return (
    <div className="workflow-container">
      {/* Auto-generated step forms */}
    </div>
  );
};
```

## 🛠️ Development

### Running the Development Server

```bash
# Start FastAPI backend
python main.py

# Start React development (if using Vite)
cd frontend && npm run dev
```

### Creating Custom Step Types

```python
# Add to workflow_schema.py
class CustomStepType(str, Enum):
    CUSTOM_PROCESSING = "custom_processing"

# Extend generator templates
# Templates automatically include your custom types
```

### Testing Generated Code

```bash
# Run integration tests
python integration_test_summary.py

# Test specific workflow
python -m pytest tests/test_workflows.py
```

## 📊 Example Workflows

The system includes three pre-built examples:

1. **Data Processing Pipeline**
   - Data input and validation
   - AI-powered analysis
   - Report generation
   - Output formatting

2. **AI Content Generator**
   - Content input
   - AI content generation
   - Quality review
   - Publication

3. **Automated Testing Suite**
   - Test configuration
   - Automated testing
   - Result analysis
   - Report generation

## 🎮 Demo Script Options

The `run_demo.sh` script includes several useful commands:

```bash
./run_demo.sh              # Start the complete demo
./run_demo.sh --stop       # Stop all services  
./run_demo.sh --restart    # Restart all services
./run_demo.sh --status     # Show service status
./run_demo.sh --logs       # View service logs
./run_demo.sh --cleanup    # Clean up generated files
./run_demo.sh --help       # Show help message
```

**Service Management:**
- ✅ Automatic port conflict detection and resolution
- ✅ Process monitoring and auto-restart
- ✅ Comprehensive logging to `logs/` directory
- ✅ Graceful shutdown on Ctrl+C
- ✅ Browser auto-opening
- ✅ Cross-platform support (Linux, macOS, Windows)

## 🔧 Advanced Features

### LLM Integration

```python
# Auto-configured LLM processing
llm_config = LLMConfiguration(
    user_prompt_template="Analyze this data: {input_data}",
    template_variables=["input_data"],
    response_format="json"
)
```

### Conditional Logic

```python
# Dynamic step execution
conditional = ConditionalLogic(
    condition="data_quality > 0.8",
    true_steps=["advanced_analysis"],
    false_steps=["data_cleaning"]
)
```

### Custom Handlers

```python
# Custom business logic
async def custom_data_handler(self, request):
    # Your custom implementation
    return {"processed": True}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: [workflow-generator.readthedocs.io](https://workflow-generator.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/workflow-generator/workflow-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/workflow-generator/workflow-generator/discussions)

## 🎉 What's Next?

After installation, you'll have:
- ✅ 3 fully functional example workflows
- ✅ Complete FastAPI backend with auto-generated plugins
- ✅ React frontend with TypeScript components
- ✅ Integrated development server
- ✅ UI component library
- ✅ LLM integration ready

Start creating your own workflows:

```bash
# Create your first custom workflow
workflow-generator --create "your task 1" "your task 2" --name "My Workflow"
```

**Happy workflow building! 🚀**