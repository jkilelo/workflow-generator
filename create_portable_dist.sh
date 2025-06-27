#!/bin/bash

# 🚀 Workflow Generator Portable Distribution Creator
# Creates a portable directory with all necessary files for fresh environment deployment

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="workflow_generator_portable"
VERSION=$(date +"%Y%m%d_%H%M%S")

print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo
    echo -e "${CYAN}================================================${NC}"
    echo -e "${WHITE}  📦 CREATING PORTABLE DISTRIBUTION            ${NC}"
    echo -e "${WHITE}  Version: $VERSION                            ${NC}"
    echo -e "${CYAN}================================================${NC}"
    echo
}

# Function to create distribution structure
create_dist_structure() {
    print_step "Creating distribution directory structure..."
    
    cd "$SCRIPT_DIR"
    
    # Remove existing dist if it exists
    if [ -d "$DIST_DIR" ]; then
        rm -rf "$DIST_DIR"
    fi
    
    # Create main directories
    mkdir -p "$DIST_DIR"/{templates,examples,docs}
    
    print_success "Distribution structure created"
}

# Function to copy core files
copy_core_files() {
    print_step "Copying core workflow generator files..."
    
    # Essential Python files
    cp workflow_manager.py "$DIST_DIR/"
    cp workflow_generator.py "$DIST_DIR/"
    cp workflow_schema.py "$DIST_DIR/"
    cp base_plugin.py "$DIST_DIR/"
    cp llm_manager.py "$DIST_DIR/"
    cp auto_setup.py "$DIST_DIR/"
    
    # Server files
    cp live_server.py "$DIST_DIR/"
    cp main.py "$DIST_DIR/"
    
    # Web interface
    cp interactive_demo.html "$DIST_DIR/"
    cp demo.html "$DIST_DIR/"
    
    # Demo scripts
    cp demo_hello_workflow.sh "$DIST_DIR/"
    cp run_demo.sh "$DIST_DIR/"
    cp run_demo.bat "$DIST_DIR/"
    
    # Configuration files
    cp requirements.txt "$DIST_DIR/"
    cp setup.py "$DIST_DIR/"
    
    print_success "Core files copied"
}

# Function to copy templates
copy_templates() {
    print_step "Copying code generation templates..."
    
    if [ -d "templates" ] && [ "$(ls -A templates)" ]; then
        cp -r templates/* "$DIST_DIR/templates/"
        print_success "Templates copied"
    else
        print_warning "Templates directory is empty or not found - creating basic templates"
        
        # Create basic templates for the portable distribution
        cat > "$DIST_DIR/templates/basic_info.txt" << 'EOF'
This templates directory will be populated automatically when you run:
python auto_setup.py

The auto_setup.py script creates all necessary Jinja2 templates for:
- FastAPI plugin generation
- React component generation  
- Configuration file generation
- Schema file generation
EOF
        print_success "Basic template info created"
    fi
}

# Function to copy testing files
copy_testing_files() {
    print_step "Copying testing and validation files..."
    
    cp test_e2e.py "$DIST_DIR/"
    cp test_ui_interactive.py "$DIST_DIR/"
    
    print_success "Testing files copied"
}

# Function to create documentation
create_documentation() {
    print_step "Creating portable distribution documentation..."
    
    cat > "$DIST_DIR/README_PORTABLE.md" << 'EOF'
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
EOF
    
    print_success "Documentation created"
}

# Function to create installation script
create_install_script() {
    print_step "Creating installation script..."
    
    cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash

# 🚀 Workflow Generator Installation Script
# One-command installation for fresh environments

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo
    echo -e "${CYAN}================================================${NC}"
    echo -e "${WHITE}  🚀 WORKFLOW GENERATOR INSTALLATION           ${NC}"
    echo -e "${CYAN}================================================${NC}"
    echo
}

main() {
    print_header
    
    # Check Python
    if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
        print_error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    PYTHON_CMD="python3"
    if ! command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python"
    fi
    
    print_success "Python detected"
    
    # Make scripts executable
    print_step "Making scripts executable..."
    chmod +x *.sh
    
    # Run autonomous setup
    print_step "Running autonomous setup..."
    $PYTHON_CMD auto_setup.py
    
    print_success "🎉 Installation complete!"
    echo
    echo "Next steps:"
    echo "  1. Run the demo: ./run_demo.sh"
    echo "  2. Or try hello workflow: ./demo_hello_workflow.sh"
    echo "  3. Access UI at: http://localhost:8003"
    echo
}

main "$@"
EOF
    
    chmod +x "$DIST_DIR/install.sh"
    print_success "Installation script created"
}

# Function to create Windows installation script
create_windows_install() {
    print_step "Creating Windows installation script..."
    
    cat > "$DIST_DIR/install.bat" << 'EOF'
@echo off
REM 🚀 Workflow Generator Installation Script for Windows

echo.
echo =================================================
echo   🚀 WORKFLOW GENERATOR INSTALLATION
echo =================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [SUCCESS] Python detected

REM Run autonomous setup
echo [STEP] Running autonomous setup...
python auto_setup.py

echo [SUCCESS] 🎉 Installation complete!
echo.
echo Next steps:
echo   1. Run the demo: run_demo.bat
echo   2. Access UI at: http://localhost:8003
echo.
pause
EOF
    
    print_success "Windows installation script created"
}

# Function to create version info
create_version_info() {
    print_step "Creating version information..."
    
    cat > "$DIST_DIR/VERSION" << EOF
WORKFLOW_GENERATOR_VERSION=$VERSION
BUILD_DATE=$(date)
PLATFORM=portable
PYTHON_MIN_VERSION=3.8
FEATURES=fastapi,react,ai,testing,ui
EOF
    
    print_success "Version information created"
}

# Function to create file list
create_file_manifest() {
    print_step "Creating file manifest..."
    
    cd "$DIST_DIR"
    find . -type f | sort > FILE_MANIFEST.txt
    cd ..
    
    print_success "File manifest created"
}

# Function to create archive
create_archive() {
    print_step "Creating distribution archive..."
    
    tar -czf "${DIST_DIR}_${VERSION}.tar.gz" "$DIST_DIR"
    zip -r "${DIST_DIR}_${VERSION}.zip" "$DIST_DIR" >/dev/null 2>&1
    
    print_success "Distribution archives created"
}

# Function to show completion summary
show_completion() {
    echo
    print_message $CYAN "================================================"
    print_success "📦 Portable Distribution Created Successfully!"
    echo
    echo -e "${WHITE}📁 Distribution Directory:${NC} ${CYAN}$DIST_DIR${NC}"
    echo -e "${WHITE}📄 Files Count:${NC} $(find "$DIST_DIR" -type f | wc -l) files"
    echo -e "${WHITE}💾 Directory Size:${NC} $(du -sh "$DIST_DIR" | cut -f1)"
    echo
    echo -e "${WHITE}📦 Archives:${NC}"
    if [ -f "${DIST_DIR}_${VERSION}.tar.gz" ]; then
        echo -e "  🔹 ${CYAN}${DIST_DIR}_${VERSION}.tar.gz${NC} ($(du -sh "${DIST_DIR}_${VERSION}.tar.gz" | cut -f1))"
    fi
    if [ -f "${DIST_DIR}_${VERSION}.zip" ]; then
        echo -e "  🔹 ${CYAN}${DIST_DIR}_${VERSION}.zip${NC} ($(du -sh "${DIST_DIR}_${VERSION}.zip" | cut -f1))"
    fi
    echo
    echo -e "${WHITE}🚀 To use in fresh environment:${NC}"
    echo -e "  1. Copy ${CYAN}$DIST_DIR${NC} directory to target system"
    echo -e "  2. Run: ${CYAN}./install.sh${NC} (Linux/Mac) or ${CYAN}install.bat${NC} (Windows)"
    echo -e "  3. Start demo: ${CYAN}./run_demo.sh${NC}"
    echo
    echo -e "${WHITE}📋 Contents:${NC}"
    echo -e "  🔹 Complete workflow generator system"
    echo -e "  🔹 All templates and dependencies"
    echo -e "  🔹 Demo scripts and examples" 
    echo -e "  🔹 Testing and validation tools"
    echo -e "  🔹 Documentation and setup guides"
    echo
    print_message $CYAN "================================================"
}

# Main execution
main() {
    print_header
    
    create_dist_structure
    copy_core_files
    copy_templates
    copy_testing_files
    create_documentation
    create_install_script
    create_windows_install
    create_version_info
    create_file_manifest
    create_archive
    
    show_completion
}

main "$@"