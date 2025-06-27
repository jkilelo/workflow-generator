#!/bin/bash

# Autonomous Installation Script for Workflow Generator
# This script handles complete setup including Python, Node.js, and example generation

set -e  # Exit on any error

echo "🚀 Workflow Generator - Autonomous Installation"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python if not available
install_python() {
    log_info "Checking Python installation..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python $PYTHON_VERSION is already installed"
        return 0
    fi
    
    log_info "Installing Python..."
    
    # Detect OS and install Python accordingly
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command_exists yum; then
            sudo yum install -y python3 python3-pip
        elif command_exists dnf; then
            sudo dnf install -y python3 python3-pip
        else
            log_error "Unsupported Linux distribution. Please install Python 3.8+ manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install python3
        else
            log_error "Homebrew not found. Please install Python 3.8+ manually or install Homebrew first."
            exit 1
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        log_error "Windows detected. Please install Python 3.8+ from https://python.org/downloads/ manually."
        exit 1
    else
        log_error "Unsupported operating system. Please install Python 3.8+ manually."
        exit 1
    fi
    
    log_success "Python installation completed"
}

# Install Node.js if not available
install_nodejs() {
    log_info "Checking Node.js installation..."
    
    if command_exists node; then
        NODE_VERSION=$(node --version)
        log_success "Node.js $NODE_VERSION is already installed"
        return 0
    fi
    
    log_info "Installing Node.js..."
    
    # Install Node.js using NodeSource repository
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install node
        else
            log_error "Homebrew not found. Please install Node.js manually or install Homebrew first."
            exit 1
        fi
    else
        log_error "Please install Node.js 16+ manually from https://nodejs.org/"
        exit 1
    fi
    
    log_success "Node.js installation completed"
}

# Create virtual environment
setup_python_env() {
    log_info "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -f "venv/bin/activate" ] && [ ! -f "venv/Scripts/activate" ]; then
        python3 -m venv venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        log_error "Failed to create virtual environment"
        exit 1
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    
    log_success "Python environment setup completed"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Install from requirements.txt if exists, otherwise install directly
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        pip install fastapi uvicorn pydantic jinja2 requests python-multipart
    fi
    
    # Install the package itself in development mode
    pip install -e .
    
    log_success "Python dependencies installed"
}

# Install Node.js dependencies
install_node_deps() {
    log_info "Installing Node.js dependencies..."
    
    if [ -f "package.json" ]; then
        npm install
        log_success "Node.js dependencies installed"
    else
        log_warning "No package.json found, skipping Node.js dependencies"
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    mkdir -p backend
    mkdir -p frontend/src/components/workflows
    mkdir -p frontend/src/components/ui
    mkdir -p apps
    mkdir -p generated_workflows
    mkdir -p templates
    
    log_success "Directory structure created"
}

# Generate example workflows
generate_examples() {
    log_info "Generating example workflows..."
    
    # Run the auto setup script
    if [ -f "auto_setup.py" ]; then
        python auto_setup.py
    else
        # Run demo if auto_setup doesn't exist
        if [ -f "demo_workflow_system.py" ]; then
            python demo_workflow_system.py
        else
            log_warning "No example generation script found"
        fi
    fi
    
    log_success "Example workflows generated"
}

# Create version file
create_version() {
    echo "1.0.0" > VERSION
}

# Main installation process
main() {
    log_info "Starting autonomous installation process..."
    
    # Check if we're in the right directory
    if [ ! -f "workflow_generator.py" ] && [ ! -f "setup.py" ]; then
        log_error "Please run this script from the workflow_generator directory"
        exit 1
    fi
    
    # Install system dependencies
    install_python
    install_nodejs
    
    # Setup Python environment
    setup_python_env
    
    # Create directory structure
    create_directories
    
    # Create version file
    create_version
    
    # Install dependencies
    install_python_deps
    install_node_deps
    
    # Generate examples
    generate_examples
    
    log_success "🎉 Installation completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Run demo: python demo_workflow_system.py"
    echo "3. Create workflows: python workflow_manager.py --help"
    echo "4. Start development server: uvicorn main:app --reload"
    echo ""
    echo "Generated files are in:"
    echo "- Backend: ./backend/"
    echo "- Frontend: ./frontend/src/components/workflows/"
    echo "- Apps: ./apps/"
    echo ""
    log_success "Workflow Generator is ready to use! 🚀"
}

# Run main function
main "$@"