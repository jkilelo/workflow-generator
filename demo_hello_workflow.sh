#!/bin/bash

# 🚀 Workflow Generator Demo - Hello Workflow
# Demonstrates autonomous workflow generation with complete setup
# Creates a standalone workflow project in ./hello_workflow

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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="./hello_workflow"
WORKFLOW_NAME="hello_workflow"
SERVER_PORT=8004

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo
    echo -e "${CYAN}================================================${NC}"
    echo -e "${WHITE}  🚀 WORKFLOW GENERATOR DEMONSTRATION          ${NC}"
    echo -e "${WHITE}  Creating: Hello Workflow Project             ${NC}"
    echo -e "${CYAN}================================================${NC}"
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

# Function to check if directory exists and handle user choice
check_target_directory() {
    print_step "Checking target directory: $TARGET_DIR"
    
    if [ -d "$TARGET_DIR" ]; then
        print_warning "Directory '$TARGET_DIR' already exists!"
        echo
        echo "Options:"
        echo "  1) Overwrite existing directory"
        echo "  2) Keep existing directory and exit"
        echo "  3) Cancel"
        echo
        read -p "Choose option (1-3): " choice
        
        case $choice in
            1)
                print_step "Removing existing directory..."
                rm -rf "$TARGET_DIR"
                print_success "Directory removed"
                ;;
            2)
                print_success "Keeping existing directory. Exiting."
                exit 0
                ;;
            3|*)
                print_success "Operation cancelled."
                exit 0
                ;;
        esac
    fi
    
    print_success "Target directory is ready"
}

# Function to check Python installation
check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
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

# Function to create project structure
create_project_structure() {
    print_step "Creating project structure..."
    
    mkdir -p "$TARGET_DIR"
    cd "$TARGET_DIR"
    
    # Create essential directories
    mkdir -p apps backend frontend/src/components/{ui,workflows} templates logs
    
    print_success "Project structure created"
}

# Function to copy generator files
copy_generator_files() {
    print_step "Copying workflow generator core files..."
    
    # Copy essential generator files
    cp "$SCRIPT_DIR/workflow_manager.py" .
    cp "$SCRIPT_DIR/workflow_generator.py" .
    cp "$SCRIPT_DIR/workflow_schema.py" .
    cp "$SCRIPT_DIR/base_plugin.py" .
    cp "$SCRIPT_DIR/llm_manager.py" .
    cp "$SCRIPT_DIR/requirements.txt" .
    
    # Copy templates directory
    cp -r "$SCRIPT_DIR/templates" .
    
    print_success "Generator files copied"
}

# Function to create custom hello workflow generator
create_hello_generator() {
    print_step "Creating Hello Workflow generator script..."
    
    cat > generate_hello_workflow.py << 'EOF'
#!/usr/bin/env python3
"""
Hello Workflow Generator
Demonstrates the workflow generator by creating a simple greeting workflow
"""

import os
import sys
from workflow_manager import WorkflowManager

def main():
    print("🚀 Generating Hello Workflow...")
    
    # Initialize workflow manager
    manager = WorkflowManager()
    
    # Define hello workflow tasks
    tasks = {
        1: "user name input",
        2: "greeting message generation", 
        3: "personalized response creation",
        4: "message display"
    }
    
    # Create the workflow
    print("📝 Creating workflow definition...")
    workflow_id = manager.create_workflow_from_tasks(
        tasks=tasks,
        workflow_name="Hello Workflow",
        category="demo",
        description="A simple greeting workflow to demonstrate the system"
    )
    
    print(f"✅ Created workflow: {workflow_id}")
    
    # Deploy the workflow (generate all files)
    print("🔧 Generating FastAPI backend and React frontend...")
    success = manager.deploy_workflow(workflow_id)
    
    if success:
        print("🎉 Hello Workflow generated successfully!")
        print(f"📁 Files created in: apps/{workflow_id}/")
        print(f"🐍 Backend plugin: backend/{workflow_id}_plugin.py")
        print(f"⚛️ React component: frontend/src/components/workflows/{workflow_id}_workflow.tsx")
        return True
    else:
        print("❌ Failed to generate workflow")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF
    
    chmod +x generate_hello_workflow.py
    print_success "Hello Workflow generator created"
}

# Function to create FastAPI server
create_server() {
    print_step "Creating FastAPI server..."
    
    cat > server.py << 'EOF'
#!/usr/bin/env python3
"""
Hello Workflow Server
Autonomous FastAPI server for the generated hello workflow
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import importlib.util
import sys
import json
import uvicorn

app = FastAPI(
    title="Hello Workflow Demo",
    description="Generated workflow demonstration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def root():
    """Serve the demo interface"""
    return FileResponse("demo_interface.html")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Hello Workflow Server is running",
        "workflows": ["hello_workflow"]
    }

@app.get("/api/workflows")
async def list_workflows():
    """List available workflows"""
    workflows = []
    
    # Load hello_workflow config
    config_path = Path("apps/hello_workflow/config.json")
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            workflows.append(config)
    
    return {"workflows": workflows}

# Auto-register generated plugin routes
def register_workflow_routes():
    """Automatically register routes from generated plugins"""
    backend_dir = Path("backend")
    if backend_dir.exists():
        for plugin_file in backend_dir.glob("*_plugin.py"):
            try:
                # Import the plugin module
                spec = importlib.util.spec_from_file_location(
                    plugin_file.stem, plugin_file
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_file.stem] = module
                spec.loader.exec_module(module)
                
                # Get plugin instance and register routes
                if hasattr(module, 'plugin_instance'):
                    plugin = module.plugin_instance
                    routes = plugin.get_api_routes()
                    
                    for route_config in routes:
                        app.add_api_route(
                            route_config["path"],
                            route_config["handler"],
                            methods=[route_config["method"]]
                        )
                    
                    print(f"✅ Registered routes for {plugin_file.stem}")
                    
            except Exception as e:
                print(f"⚠️ Could not register {plugin_file}: {e}")

# Register routes on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Hello Workflow Server starting...")
    register_workflow_routes()
    print("✅ Server ready!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=False)
EOF
    
    chmod +x server.py
    print_success "FastAPI server created"
}

# Function to create demo interface
create_demo_interface() {
    print_step "Creating demo web interface..."
    
    cat > demo_interface.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello Workflow Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        function HelloWorkflowDemo() {
            const [userName, setUserName] = useState('');
            const [greeting, setGreeting] = useState('');
            const [isLoading, setIsLoading] = useState(false);
            const [step, setStep] = useState(1);

            const executeStep = async (stepNum) => {
                setIsLoading(true);
                
                // Simulate workflow execution
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                switch(stepNum) {
                    case 2:
                        setGreeting(`Hello, ${userName}! 👋`);
                        setStep(3);
                        break;
                    case 3:
                        setGreeting(`${greeting}\n\nWelcome to the Workflow Generator demo!\nThis workflow was auto-generated from simple task descriptions.`);
                        setStep(4);
                        break;
                    case 4:
                        setStep(5);
                        break;
                }
                
                setIsLoading(false);
            };

            const resetWorkflow = () => {
                setUserName('');
                setGreeting('');
                setStep(1);
            };

            return (
                <div className="container mx-auto px-4 py-8 max-w-4xl">
                    {/* Header */}
                    <div className="text-center mb-12">
                        <h1 className="text-5xl font-bold text-gray-800 mb-4">
                            👋 Hello Workflow Demo
                        </h1>
                        <p className="text-xl text-gray-600 mb-6">
                            Generated automatically by the Workflow Generator system
                        </p>
                        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg inline-block">
                            ✅ Status: <span className="font-semibold">Auto-Generated & Running</span>
                        </div>
                    </div>

                    {/* Workflow Steps */}
                    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
                        <h2 className="text-2xl font-bold text-gray-800 mb-6">Workflow Execution</h2>
                        
                        {/* Step 1: Name Input */}
                        {step >= 1 && (
                            <div className={`p-6 rounded-lg border-2 mb-4 ${step === 1 ? 'border-blue-400 bg-blue-50' : 'border-green-400 bg-green-50'}`}>
                                <h3 className="text-lg font-semibold mb-3">
                                    Step 1: User Name Input {step > 1 && '✅'}
                                </h3>
                                {step === 1 ? (
                                    <div>
                                        <input
                                            type="text"
                                            value={userName}
                                            onChange={(e) => setUserName(e.target.value)}
                                            placeholder="Enter your name"
                                            className="w-full p-3 border border-gray-300 rounded-lg mb-4"
                                        />
                                        <button
                                            onClick={() => userName && setStep(2)}
                                            disabled={!userName}
                                            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
                                        >
                                            Continue to Greeting Generation
                                        </button>
                                    </div>
                                ) : (
                                    <p className="text-green-700">Name collected: <strong>{userName}</strong></p>
                                )}
                            </div>
                        )}

                        {/* Step 2: Greeting Generation */}
                        {step >= 2 && (
                            <div className={`p-6 rounded-lg border-2 mb-4 ${step === 2 ? 'border-blue-400 bg-blue-50' : 'border-green-400 bg-green-50'}`}>
                                <h3 className="text-lg font-semibold mb-3">
                                    Step 2: Greeting Message Generation {step > 2 && '✅'}
                                </h3>
                                {step === 2 ? (
                                    <button
                                        onClick={() => executeStep(2)}
                                        disabled={isLoading}
                                        className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
                                    >
                                        {isLoading ? 'Generating greeting...' : 'Generate Greeting'}
                                    </button>
                                ) : (
                                    <p className="text-green-700">Greeting generated successfully</p>
                                )}
                            </div>
                        )}

                        {/* Step 3: Personalized Response */}
                        {step >= 3 && (
                            <div className={`p-6 rounded-lg border-2 mb-4 ${step === 3 ? 'border-blue-400 bg-blue-50' : 'border-green-400 bg-green-50'}`}>
                                <h3 className="text-lg font-semibold mb-3">
                                    Step 3: Personalized Response Creation {step > 3 && '✅'}
                                </h3>
                                {step === 3 ? (
                                    <button
                                        onClick={() => executeStep(3)}
                                        disabled={isLoading}
                                        className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300"
                                    >
                                        {isLoading ? 'Creating response...' : 'Create Personalized Response'}
                                    </button>
                                ) : (
                                    <p className="text-green-700">Personalized response created</p>
                                )}
                            </div>
                        )}

                        {/* Step 4: Message Display */}
                        {step >= 4 && (
                            <div className={`p-6 rounded-lg border-2 mb-4 ${step === 4 ? 'border-blue-400 bg-blue-50' : 'border-green-400 bg-green-50'}`}>
                                <h3 className="text-lg font-semibold mb-3">
                                    Step 4: Message Display {step > 4 && '✅'}
                                </h3>
                                {step === 4 ? (
                                    <div>
                                        <div className="bg-white p-4 rounded-lg border mb-4">
                                            <pre className="text-lg whitespace-pre-wrap">{greeting}</pre>
                                        </div>
                                        <button
                                            onClick={() => executeStep(4)}
                                            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                                        >
                                            Complete Workflow
                                        </button>
                                    </div>
                                ) : step === 5 && (
                                    <div className="text-center">
                                        <div className="text-6xl mb-4">🎉</div>
                                        <h3 className="text-2xl font-bold text-green-800 mb-2">Workflow Completed!</h3>
                                        <p className="text-green-700 mb-4">The hello workflow has been executed successfully.</p>
                                        <button
                                            onClick={resetWorkflow}
                                            className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600"
                                        >
                                            Run Again
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Info Panel */}
                    <div className="bg-white rounded-xl shadow-lg p-8">
                        <h2 className="text-2xl font-bold text-gray-800 mb-6">🚀 What Just Happened?</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h3 className="font-semibold text-gray-800 mb-2">Generated Files:</h3>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    <li>✅ FastAPI backend plugin</li>
                                    <li>✅ React TypeScript component</li>
                                    <li>✅ JSON configuration files</li>
                                    <li>✅ Server and interface</li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="font-semibold text-gray-800 mb-2">Capabilities:</h3>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    <li>✅ Step-by-step execution</li>
                                    <li>✅ Dynamic form generation</li>
                                    <li>✅ Real-time progress tracking</li>
                                    <li>✅ Responsive design</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }

        ReactDOM.render(<HelloWorkflowDemo />, document.getElementById('root'));
    </script>
</body>
</html>
EOF
    
    print_success "Demo interface created"
}

# Function to create run script
create_run_script() {
    print_step "Creating startup script..."
    
    cat > run_hello_workflow.sh << 'EOF'
#!/bin/bash

# Hello Workflow Runner
# Activates environment and starts the server

echo "🚀 Starting Hello Workflow Demo..."

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "Starting server on http://localhost:8004"
python server.py
EOF
    
    chmod +x run_hello_workflow.sh
    print_success "Startup script created"
}

# Function to setup Python environment
setup_python_environment() {
    print_step "Setting up Python virtual environment..."
    
    # Create virtual environment
    $PYTHON_CMD -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip >/dev/null 2>&1
    
    # Install requirements
    print_step "Installing Python dependencies..."
    pip install -r requirements.txt >/dev/null 2>&1
    
    print_success "Python environment ready"
}

# Function to generate the workflow
generate_workflow() {
    print_step "Generating Hello Workflow..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run the workflow generator
    $PYTHON_CMD generate_hello_workflow.py
    
    if [ $? -eq 0 ]; then
        print_success "Workflow generated successfully"
        return 0
    else
        print_error "Failed to generate workflow"
        return 1
    fi
}

# Function to start the server
start_server() {
    print_step "Starting Hello Workflow server..."
    
    # Check if port is available
    if lsof -Pi :$SERVER_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $SERVER_PORT is in use. Trying to stop existing process..."
        pkill -f "server.py" 2>/dev/null || true
        sleep 2
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Start server in background
    echo "🌐 Starting server on http://localhost:$SERVER_PORT"
    nohup $PYTHON_CMD server.py > logs/server.log 2>&1 &
    SERVER_PID=$!
    
    # Wait for server to start
    print_step "Waiting for server to initialize..."
    for i in {1..15}; do
        if curl -s "http://localhost:$SERVER_PORT/api/health" >/dev/null 2>&1; then
            print_success "Server is running (PID: $SERVER_PID)"
            return 0
        fi
        sleep 1
    done
    
    print_error "Server failed to start. Check logs/server.log"
    return 1
}

# Function to open browser
open_browser() {
    print_step "Opening demo in browser..."
    
    sleep 2
    local url="http://localhost:$SERVER_PORT"
    
    # Detect OS and open browser
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v xdg-open >/dev/null 2>&1; then
            xdg-open "$url" >/dev/null 2>&1 &
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open "$url" >/dev/null 2>&1 &
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        start "$url" >/dev/null 2>&1 &
    fi
    
    print_success "Demo should open in your browser"
}

# Function to show completion message
show_completion() {
    echo
    print_message $CYAN "================================================"
    print_success "🎉 Hello Workflow Demo is ready!"
    echo
    echo -e "${WHITE}🌐 Access the demo:${NC}"
    echo -e "  🔹 URL: ${GREEN}http://localhost:$SERVER_PORT${NC}"
    echo -e "  🔹 Health check: ${GREEN}http://localhost:$SERVER_PORT/api/health${NC}"
    echo
    echo -e "${WHITE}📁 Generated files in: ${CYAN}$TARGET_DIR${NC}"
    echo -e "  🔹 Backend: ${CYAN}backend/hello_workflow_plugin.py${NC}"
    echo -e "  🔹 Frontend: ${CYAN}frontend/src/components/workflows/hello_workflow_workflow.tsx${NC}"
    echo -e "  🔹 Config: ${CYAN}apps/hello_workflow/config.json${NC}"
    echo
    echo -e "${WHITE}🎯 Try the demo:${NC}"
    echo -e "  🔹 Enter your name in step 1"
    echo -e "  🔹 Watch the workflow execute step by step"
    echo -e "  🔹 See the auto-generated greeting"
    echo
    echo -e "${WHITE}🛑 To stop:${NC}"
    echo -e "  🔹 Press ${RED}Ctrl+C${NC} or run: ${CYAN}pkill -f server.py${NC}"
    echo
    print_message $CYAN "================================================"
    echo
}

# Main execution
main() {
    print_header
    
    # Check prerequisites
    check_python
    check_target_directory
    
    # Create project
    create_project_structure
    copy_generator_files
    create_hello_generator
    create_server
    create_demo_interface
    create_run_script
    
    # Setup and generate
    setup_python_environment
    
    if ! generate_workflow; then
        print_error "Failed to generate workflow. Exiting."
        exit 1
    fi
    
    # Start services
    if ! start_server; then
        print_error "Failed to start server. Exiting."
        exit 1
    fi
    
    open_browser
    show_completion
    
    # Keep script running
    trap 'pkill -f server.py 2>/dev/null; echo; print_success "Demo stopped. Goodbye!"; exit 0' INT TERM
    
    print_step "Demo is running. Press Ctrl+C to stop."
    wait
}

# Run main function
main "$@"