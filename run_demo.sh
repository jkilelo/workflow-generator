#!/bin/bash

# 🚀 Workflow Generator Demo Launcher
# Autonomous FastAPI + React workflow generation system
# This script handles complete environment setup and service management

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
BACKEND_PORT=8003
FRONTEND_PORT=3000
LOG_DIR="$PROJECT_DIR/logs"
PID_FILE="$PROJECT_DIR/.demo_pids"

# Create logs directory
mkdir -p "$LOG_DIR"

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo
    echo -e "${CYAN}=================================${NC}"
    echo -e "${WHITE}  🚀 WORKFLOW GENERATOR DEMO    ${NC}"
    echo -e "${CYAN}=================================${NC}"
    echo
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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to kill existing demo processes
cleanup() {
    print_step "Cleaning up existing processes..."
    
    if [ -f "$PID_FILE" ]; then
        while read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                print_step "Stopping process $pid"
                kill "$pid" 2>/dev/null || true
                sleep 1
                if kill -0 "$pid" 2>/dev/null; then
                    kill -9 "$pid" 2>/dev/null || true
                fi
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi
    
    # Kill any remaining processes on our ports
    pkill -f "live_server.py" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    
    # Wait a moment for cleanup
    sleep 2
    
    print_success "Cleanup completed"
}

# Function to check Python version
check_python() {
    print_step "Checking Python installation..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -lt 8 ]; then
        print_error "Python 3.8+ is required. Found: $($PYTHON_CMD --version)"
        exit 1
    fi
    
    print_success "Python $($PYTHON_CMD --version) detected"
}

# Function to setup virtual environment
setup_venv() {
    print_step "Setting up Python virtual environment..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -d "$VENV_DIR" ]; then
        print_step "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    print_step "Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        print_step "Installing Python dependencies..."
        pip install -r requirements.txt >/dev/null 2>&1
    else
        print_warning "requirements.txt not found, installing core dependencies..."
        pip install fastapi uvicorn pydantic jinja2 requests aiofiles python-multipart >/dev/null 2>&1
    fi
    
    print_success "Virtual environment ready"
}

# Function to run autonomous setup if needed
run_setup() {
    print_step "Checking system setup..."
    
    source "$VENV_DIR/bin/activate"
    
    # Check if we need to run auto_setup
    if [ ! -d "apps" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_step "Running autonomous setup (first-time setup)..."
        $PYTHON_CMD auto_setup.py
        print_success "Auto-setup completed"
    else
        print_success "System already configured"
    fi
}

# Function to start FastAPI backend
start_backend() {
    print_step "Starting FastAPI backend server..."
    
    source "$VENV_DIR/bin/activate"
    cd "$PROJECT_DIR"
    
    # Check if port is available
    if ! check_port $BACKEND_PORT; then
        print_warning "Port $BACKEND_PORT is already in use. Trying to stop existing server..."
        pkill -f "live_server.py" 2>/dev/null || true
        pkill -f "uvicorn.*$BACKEND_PORT" 2>/dev/null || true
        sleep 3
    fi
    
    # Start the server
    print_step "Launching live server on port $BACKEND_PORT..."
    nohup $PYTHON_CMD live_server.py > "$LOG_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID >> "$PID_FILE"
    
    # Wait for server to start
    print_step "Waiting for backend to initialize..."
    for i in {1..30}; do
        if curl -s "http://localhost:$BACKEND_PORT/api/health" >/dev/null 2>&1; then
            print_success "Backend server is running (PID: $BACKEND_PID)"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            print_error "Backend failed to start. Check logs: $LOG_DIR/backend.log"
            exit 1
        fi
    done
}

# Function to open browser
open_browser() {
    print_step "Opening demo in browser..."
    
    # Wait a moment for everything to settle
    sleep 2
    
    local url="http://localhost:$BACKEND_PORT"
    
    # Detect OS and open browser
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists xdg-open; then
            xdg-open "$url" >/dev/null 2>&1 &
        elif command_exists gnome-open; then
            gnome-open "$url" >/dev/null 2>&1 &
        else
            print_warning "Could not auto-open browser. Please navigate to: $url"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$url" >/dev/null 2>&1 &
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        start "$url" >/dev/null 2>&1 &
    else
        print_warning "Could not auto-open browser. Please navigate to: $url"
    fi
    
    print_success "Demo interface should open in your browser"
}

# Function to show status
show_status() {
    echo
    print_header
    print_success "🎉 Workflow Generator Demo is now running!"
    echo
    echo -e "${WHITE}📊 Service Status:${NC}"
    echo -e "  🔹 Backend Server: ${GREEN}http://localhost:$BACKEND_PORT${NC}"
    echo -e "  🔹 Interactive UI: ${GREEN}http://localhost:$BACKEND_PORT${NC}"
    echo -e "  🔹 API Health: ${GREEN}http://localhost:$BACKEND_PORT/api/health${NC}"
    echo
    echo -e "${WHITE}📁 Generated Content:${NC}"
    if [ -d "apps" ]; then
        local workflow_count=$(find apps -maxdepth 1 -type d | wc -l)
        echo -e "  🔹 Workflows: ${CYAN}$((workflow_count - 1)) generated${NC}"
    fi
    if [ -d "backend" ]; then
        local plugin_count=$(find backend -name "*_plugin.py" | wc -l)
        echo -e "  🔹 Backend Plugins: ${CYAN}$plugin_count files${NC}"
    fi
    if [ -d "frontend" ]; then
        local component_count=$(find frontend -name "*.tsx" 2>/dev/null | wc -l)
        echo -e "  🔹 React Components: ${CYAN}$component_count files${NC}"
    fi
    echo
    echo -e "${WHITE}🎯 What to try:${NC}"
    echo -e "  🔹 Click any workflow card to execute it"
    echo -e "  🔹 Fill out dynamic forms and watch real-time execution"
    echo -e "  🔹 View step-by-step progress tracking"
    echo -e "  🔹 Test responsive design on different screen sizes"
    echo
    echo -e "${WHITE}📝 Logs:${NC}"
    echo -e "  🔹 Backend: ${CYAN}$LOG_DIR/backend.log${NC}"
    echo -e "  🔹 All processes: ${CYAN}tail -f $LOG_DIR/*.log${NC}"
    echo
    echo -e "${WHITE}🛑 To stop the demo:${NC}"
    echo -e "  🔹 Press ${RED}Ctrl+C${NC} or run: ${CYAN}./run_demo.sh --stop${NC}"
    echo
    print_message $CYAN "================================="
}

# Function to monitor and keep services running
monitor_services() {
    print_step "Monitoring services... (Press Ctrl+C to stop)"
    
    trap cleanup EXIT INT TERM
    
    while true; do
        # Check if backend is still running
        if ! curl -s "http://localhost:$BACKEND_PORT/api/health" >/dev/null 2>&1; then
            print_warning "Backend service appears to be down. Attempting restart..."
            start_backend
        fi
        
        sleep 30  # Check every 30 seconds
    done
}

# Function to stop all services
stop_services() {
    print_step "Stopping all demo services..."
    cleanup
    print_success "All services stopped"
    exit 0
}

# Function to show logs
show_logs() {
    print_step "Showing service logs..."
    if [ -f "$LOG_DIR/backend.log" ]; then
        echo -e "${CYAN}=== Backend Logs ===${NC}"
        tail -n 50 "$LOG_DIR/backend.log"
    else
        print_warning "No backend logs found"
    fi
}

# Function to show help
show_help() {
    echo "🚀 Workflow Generator Demo Launcher"
    echo
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  --start     Start the demo (default)"
    echo "  --stop      Stop all demo services"
    echo "  --restart   Restart all services"
    echo "  --status    Show service status"
    echo "  --logs      Show service logs"
    echo "  --cleanup   Clean up and reset"
    echo "  --help      Show this help message"
    echo
    echo "Examples:"
    echo "  $0                  # Start the demo"
    echo "  $0 --stop           # Stop all services"
    echo "  $0 --logs           # View logs"
    echo
}

# Main execution
main() {
    case "${1:-start}" in
        "start"|"")
            print_header
            check_python
            cleanup
            setup_venv
            run_setup
            start_backend
            open_browser
            show_status
            monitor_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            print_header
            cleanup
            sleep 2
            start_backend
            print_success "Services restarted"
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "cleanup")
            cleanup
            print_step "Removing generated files..."
            rm -rf apps backend frontend logs
            print_success "Cleanup completed"
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"