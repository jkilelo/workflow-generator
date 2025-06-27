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
