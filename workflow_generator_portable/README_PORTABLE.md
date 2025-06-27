# 🚀 Workflow Generator - Portable Distribution

**Autonomous FastAPI + React workflow generation system**

This portable distribution contains everything needed to run the workflow generator in a completely fresh environment.

## 📦 What's Included

### Core Components
- `workflow_manager.py` - Main workflow management system
- `workflow_generator.py` - Code generation engine using Jinja2
- `workflow_schema.py` - Pydantic models for workflow definitions
- `base_plugin.py` - Base class for all generated plugins
- `llm_manager.py` - AI/LLM integration manager
- `auto_setup.py` - Autonomous setup system

### Server Components
- `live_server.py` - Interactive FastAPI server
- `main.py` - Alternative server entry point
- `interactive_demo.html` - Full-featured web interface
- `demo.html` - Static demo showcase

### Demo Scripts
- `demo_hello_workflow.sh` - Standalone hello workflow demo
- `run_demo.sh` - Main demo launcher (Linux/Mac)
- `run_demo.bat` - Demo launcher for Windows

### Templates
- `templates/` - Jinja2 templates for code generation
  - FastAPI plugin templates
  - React component templates
  - Configuration file templates

### Testing
- `test_e2e.py` - End-to-end testing suite
- `test_ui_interactive.py` - Playwright UI testing

## 🚀 Quick Start

### Option 1: One-Command Setup
```bash
# Make scripts executable
chmod +x *.sh

# Run the main demo
./run_demo.sh
```

### Option 2: Hello Workflow Demo
```bash
# Generate a standalone hello workflow project
./demo_hello_workflow.sh

# Access at http://localhost:8004
```

### Option 3: Manual Setup
```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt

# Run autonomous setup
python auto_setup.py

# Start server
python live_server.py

# Access at http://localhost:8003
```

## 🎯 What You Can Do

### Generate Workflows from CLI
```bash
python workflow_manager.py --create "data input" "ai processing" "report generation" --name "my_workflow"
```

### Use Interactive Web Interface
1. Start the server: `./run_demo.sh`
2. Open http://localhost:8003
3. Click workflow cards to execute step-by-step
4. Fill dynamic forms and watch real-time execution

### Create Custom Workflows
```python
from workflow_manager import WorkflowManager

manager = WorkflowManager()
tasks = {
    1: "user input collection",
    2: "data processing", 
    3: "ai analysis",
    4: "result presentation"
}

workflow_id = manager.create_workflow_from_tasks(
    tasks=tasks,
    workflow_name="Custom Workflow",
    category="business"
)

manager.deploy_workflow(workflow_id)
```

## 📁 Generated Structure

Each workflow creates:
```
apps/my_workflow/
├── config.json                    # Workflow configuration
└── schema.json                    # Parameter validation

backend/
└── my_workflow_plugin.py          # FastAPI plugin

frontend/src/components/workflows/
└── my_workflow_workflow.tsx       # React component
```

## 🔧 System Requirements

- **Python 3.8+**
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 512MB RAM minimum
- **Disk Space**: 100MB for installation + generated files
- **Network**: Internet connection for initial dependency installation

## 🎮 Demo Features

### Hello Workflow Demo
- Complete standalone project generation
- Interactive 4-step workflow execution
- Real-time progress tracking
- Personalized greeting system
- Teardown capabilities

### Main Demo System
- Multiple pre-built workflow examples
- AI Content Generator
- Data Processing Pipeline  
- Automated Testing Suite
- Real-time execution with API calls

## 🔌 AI Integration

Built-in support for:
- **OpenAI GPT-4**
- **Anthropic Claude**
- **Google Gemini**

```bash
# Optional: Set API keys
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

## 🧪 Testing

```bash
# Run comprehensive tests
python test_e2e.py

# Run UI tests with Playwright
python test_ui_interactive.py

# Test workflow generation
python workflow_manager.py --test
```

## 🚦 Production Deployment

### Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN python auto_setup.py
EXPOSE 8003
CMD ["python", "live_server.py"]
```

### Systemd Service
```ini
[Unit]
Description=Workflow Generator
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/workflow_generator
ExecStart=/path/to/venv/bin/python live_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using the port
lsof -i :8003
# Kill the process
pkill -f live_server.py
```

**Python version issues:**
```bash
# Check Python version
python --version
# Must be 3.8 or higher
```

**Virtual environment issues:**
```bash
# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📄 License

MIT License - Free for personal and commercial use.

## 🤝 Support

- **Issues**: Create GitHub issues for bugs
- **Documentation**: Check README.md for detailed info
- **Community**: Join discussions for help and ideas

---

**Ready to generate workflows? Run `./run_demo.sh` to get started!** 🚀
