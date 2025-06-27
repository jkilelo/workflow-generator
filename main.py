#!/usr/bin/env python3
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
