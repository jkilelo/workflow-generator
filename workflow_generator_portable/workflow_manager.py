"""
Workflow Manager

Integrates the generic workflow generator with the existing app_generator system.
Provides a comprehensive interface for:
- Auto-generating workflows from simple task lists
- Dynamic plugin registration
- Frontend component integration
- Runtime workflow execution

Usage:
    manager = WorkflowManager()
    workflow_id = manager.create_workflow_from_tasks({
        1: "schema analysis",
        2: "profile generation", 
        3: "rule generation",
        4: "code execution"
    })
    manager.deploy_workflow(workflow_id)
"""

import os
import json
import importlib.util
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from workflow_schema import (
    WorkflowSchema, WorkflowMetadata, StepDefinition, ParameterDefinition,
    StepType, ParameterType, LLMConfiguration
)
from workflow_generator import WorkflowGenerator


class WorkflowManager:
    """Manages auto-generated workflows and their integration with the app_generator system"""
    
    def __init__(self, 
                 backend_dir: str = None,
                 frontend_dir: str = None,
                 apps_dir: str = None):
        # Set default paths relative to current working directory or environment
        if backend_dir is None:
            backend_dir = os.environ.get('BACKEND_DIR', './backend')
        if frontend_dir is None:
            frontend_dir = os.environ.get('FRONTEND_DIR', './frontend/src/components/workflows')
        if apps_dir is None:
            apps_dir = os.environ.get('APPS_DIR', './apps')
            
        self.backend_dir = Path(backend_dir)
        self.frontend_dir = Path(frontend_dir)
        self.apps_dir = Path(apps_dir)
        self.generator = WorkflowGenerator()
        self.workflows_registry = {}
        
        # Ensure directories exist
        self.frontend_dir.mkdir(parents=True, exist_ok=True)
        self.apps_dir.mkdir(parents=True, exist_ok=True)
    
    def create_workflow_from_tasks(self, 
                                 tasks: Dict[int, str],
                                 workflow_name: str = None,
                                 workflow_id: str = None,
                                 description: str = None,
                                 category: str = "auto_generated") -> str:
        """
        Create a workflow from a simple task list.
        
        Args:
            tasks: Dictionary mapping step numbers to task descriptions
            workflow_name: Optional name for the workflow
            workflow_id: Optional ID for the workflow
            description: Optional description
            category: Workflow category
            
        Returns:
            The generated workflow ID
            
        Example:
            tasks = {
                1: "data input", 
                2: "ai processing",
                3: "output generation"
            }
        """
        if not workflow_id:
            workflow_id = "_".join(workflow_name.lower().split() if workflow_name else ["auto", "workflow"])
            workflow_id = workflow_id.replace("-", "_")
        
        if not workflow_name:
            workflow_name = " ".join(workflow_id.split("_")).title()
        
        # Auto-detect step types and generate parameters
        steps = []
        for step_num, task_desc in sorted(tasks.items()):
            step_id = f"step_{step_num}"
            step_name = task_desc.title()
            
            # Auto-detect step type based on keywords
            step_type, parameters, llm_config, custom_handler = self._infer_step_configuration(task_desc)
            
            step = StepDefinition(
                id=step_id,
                name=step_name,
                type=step_type,
                description=f"Execute {task_desc}",
                depends_on=[f"step_{step_num-1}"] if step_num > 1 else None,
                parameters=parameters,
                llm_config=llm_config,
                custom_handler=custom_handler
            )
            steps.append(step)
        
        # Create workflow schema
        workflow = WorkflowSchema(
            metadata=WorkflowMetadata(
                id=workflow_id,
                name=workflow_name,
                description=description or f"Auto-generated workflow for {workflow_name}",
                category=category,
                version="1.0.0",
                author="Workflow Manager Auto-Generator"
            ),
            steps=steps
        )
        
        # Store in registry
        self.workflows_registry[workflow_id] = workflow
        
        return workflow_id
    
    def _infer_step_configuration(self, task_desc: str) -> Tuple[StepType, List[ParameterDefinition], Optional[LLMConfiguration], Optional[str]]:
        """Infer step configuration based on task description keywords"""
        task_lower = task_desc.lower()
        
        # LLM processing keywords
        llm_keywords = ['ai', 'generate', 'analysis', 'analyze', 'process', 'llm', 'gpt', 'claude', 'create', 'write']
        
        # Input keywords  
        input_keywords = ['input', 'upload', 'file', 'data', 'schema']
        
        # Execution keywords
        execution_keywords = ['execute', 'run', 'test', 'code']
        
        # HTTP/API keywords
        http_keywords = ['crawl', 'fetch', 'api', 'request', 'extract', 'scrape']
        
        parameters = []
        llm_config = None
        custom_handler = None
        
        if any(keyword in task_lower for keyword in llm_keywords):
            # LLM Processing Step
            step_type = StepType.LLM_PROCESSING
            
            # Add LLM provider parameter
            parameters.append(ParameterDefinition(
                name="llm_provider",
                type=ParameterType.SELECT,
                label="LLM Provider",
                required=True,
                options=["openai", "anthropic", "google"],
                default="openai"
            ))
            
            # Create LLM configuration
            llm_config = LLMConfiguration(
                user_prompt_template=f"Execute the following task: {task_desc}\n\nInput data: {{input_data}}",
                template_variables=["input_data"],
                response_format="text"
            )
            
        elif any(keyword in task_lower for keyword in input_keywords):
            # Form Input Step
            step_type = StepType.FORM_INPUT
            
            if 'file' in task_lower or 'upload' in task_lower:
                parameters.append(ParameterDefinition(
                    name="data_file",
                    type=ParameterType.FILE,
                    label="Data File",
                    required=True,
                    description="Upload the data file to process"
                ))
            
            if 'schema' in task_lower:
                parameters.append(ParameterDefinition(
                    name="schema_info",
                    type=ParameterType.TEXT_AREA,
                    label="Schema Information",
                    required=False,
                    placeholder="Optional schema information"
                ))
                
        elif any(keyword in task_lower for keyword in execution_keywords):
            # Code Execution Step
            step_type = StepType.CODE_EXECUTION
            custom_handler = f"execute_{task_desc.lower().replace(' ', '_')}"
            
        elif any(keyword in task_lower for keyword in http_keywords):
            # HTTP Request Step
            step_type = StepType.HTTP_REQUEST
            
            if 'url' in task_lower or 'page' in task_lower or 'crawl' in task_lower:
                parameters.append(ParameterDefinition(
                    name="page_url",
                    type=ParameterType.URL,
                    label="Page URL",
                    required=True,
                    description="URL of the page to process"
                ))
            
            custom_handler = f"handle_{task_desc.lower().replace(' ', '_')}"
            
        else:
            # Generic step
            step_type = StepType.DATA_TRANSFORMATION
            
            parameters.append(ParameterDefinition(
                name="input_data",
                type=ParameterType.TEXT_AREA,
                label="Input Data",
                required=False,
                placeholder="Enter input data for this step"
            ))
        
        return step_type, parameters, llm_config, custom_handler
    
    def generate_workflow(self, workflow_id: str) -> Dict[str, str]:
        """Generate code files for a workflow"""
        if workflow_id not in self.workflows_registry:
            raise ValueError(f"Workflow {workflow_id} not found in registry")
        
        workflow = self.workflows_registry[workflow_id]
        return self.generator.generate_workflow_files(workflow)
    
    def deploy_workflow(self, workflow_id: str) -> Dict[str, Path]:
        """Deploy a workflow to the app_generator system"""
        if workflow_id not in self.workflows_registry:
            raise ValueError(f"Workflow {workflow_id} not found in registry")
        
        workflow = self.workflows_registry[workflow_id]
        
        # Generate files
        files = self.generator.generate_workflow_files(workflow)
        
        # Save backend plugin
        backend_plugin_path = self.backend_dir / f"{workflow_id}_plugin.py"
        with open(backend_plugin_path, 'w') as f:
            f.write(files[f"{workflow_id}_plugin.py"])
        
        # Save frontend component
        frontend_component_path = self.frontend_dir / f"{workflow_id}_workflow.tsx"
        with open(frontend_component_path, 'w') as f:
            f.write(files[f"{workflow_id}_workflow.tsx"])
        
        # Save app configuration
        app_config_path = self.apps_dir / workflow_id / "config.json"
        app_config_path.parent.mkdir(exist_ok=True)
        with open(app_config_path, 'w') as f:
            f.write(files[f"{workflow_id}_config.json"])
        
        # Save workflow schema
        schema_path = self.apps_dir / workflow_id / "schema.json"
        with open(schema_path, 'w') as f:
            f.write(files[f"{workflow_id}_schema.json"])
        
        return {
            "backend_plugin": backend_plugin_path,
            "frontend_component": frontend_component_path,
            "app_config": app_config_path,
            "schema": schema_path
        }
    
    def integrate_with_main_api(self, workflow_id: str) -> str:
        """Generate integration code for main_api_server.py"""
        if workflow_id not in self.workflows_registry:
            raise ValueError(f"Workflow {workflow_id} not found in registry")
        
        workflow = self.workflows_registry[workflow_id]
        
        steps_list = []
        for step in workflow.steps:
            steps_list.append(f'''        {{
            "id": "{step.id}",
            "name": "{step.name}",
            "description": "{step.description or ''}"
        }}''')
        
        steps_str = ",\n".join(steps_list)
        
        integration_code = f'''
# Auto-generated integration for {workflow.metadata.name}
from {workflow_id}_plugin import plugin_instance as {workflow_id}_plugin

# Add to APPS dictionary
APPS["{workflow_id}"] = {{
    "id": "{workflow_id}",
    "name": "{workflow.metadata.name}",
    "description": "{workflow.metadata.description}",
    "category": "{workflow.metadata.category}",
    "plugin": {workflow_id}_plugin,
    "steps": [
{steps_str}
    ]
}}

# Register plugin routes
async def register_{workflow_id}_routes():
    for route_config in {workflow_id}_plugin.get_api_routes():
        app.add_api_route(
            path=f"/api/apps/{workflow_id}/{{route_config['path']}}",
            endpoint=route_config['handler'],
            methods=[route_config['method']],
            response_model=route_config['response_model']
        )
'''
        return integration_code
    
    def create_comprehensive_workflow_example(self) -> str:
        """Create a comprehensive example workflow showcasing all features"""
        tasks = {
            1: "data input and validation",
            2: "ai-powered analysis", 
            3: "report generation",
            4: "code execution and testing",
            5: "output formatting"
        }
        
        workflow_id = self.create_workflow_from_tasks(
            tasks=tasks,
            workflow_name="Comprehensive AI Data Pipeline",
            description="A full-featured workflow demonstrating all step types and capabilities",
            category="example"
        )
        
        return workflow_id
    
    def list_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List all registered workflows"""
        return {
            workflow_id: {
                "name": workflow.metadata.name,
                "description": workflow.metadata.description,
                "category": workflow.metadata.category,
                "steps": len(workflow.steps),
                "version": workflow.metadata.version
            }
            for workflow_id, workflow in self.workflows_registry.items()
        }
    
    def get_workflow_schema(self, workflow_id: str) -> WorkflowSchema:
        """Get workflow schema by ID"""
        if workflow_id not in self.workflows_registry:
            raise ValueError(f"Workflow {workflow_id} not found in registry")
        return self.workflows_registry[workflow_id]


# CLI Interface for easy testing
def main():
    """Command-line interface for workflow management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Workflow Manager CLI")
    parser.add_argument("--create", nargs="+", help="Create workflow from task list")
    parser.add_argument("--name", help="Workflow name")
    parser.add_argument("--deploy", help="Deploy workflow by ID")
    parser.add_argument("--list", action="store_true", help="List all workflows")
    parser.add_argument("--example", action="store_true", help="Create comprehensive example")
    
    args = parser.parse_args()
    
    manager = WorkflowManager()
    
    if args.create:
        tasks = {i+1: task for i, task in enumerate(args.create)}
        workflow_id = manager.create_workflow_from_tasks(
            tasks=tasks, 
            workflow_name=args.name
        )
        print(f"Created workflow: {workflow_id}")
        
        # Auto-deploy
        paths = manager.deploy_workflow(workflow_id)
        print("Deployed files:")
        for file_type, path in paths.items():
            print(f"  {file_type}: {path}")
    
    elif args.deploy:
        paths = manager.deploy_workflow(args.deploy)
        print("Deployed files:")
        for file_type, path in paths.items():
            print(f"  {file_type}: {path}")
    
    elif args.list:
        workflows = manager.list_workflows()
        print("Registered workflows:")
        for workflow_id, info in workflows.items():
            print(f"  {workflow_id}: {info['name']} ({info['steps']} steps)")
    
    elif args.example:
        workflow_id = manager.create_comprehensive_workflow_example()
        paths = manager.deploy_workflow(workflow_id)
        print(f"Created and deployed example workflow: {workflow_id}")
        print("Deployed files:")
        for file_type, path in paths.items():
            print(f"  {file_type}: {path}")


# Check for first-time setup
def check_first_run():
    """Check if this is the first run and auto-setup if needed"""
    setup_marker = Path('.workflow_generator_setup')
    
    if not setup_marker.exists():
        print("🚀 First-time setup detected!")
        print("Running auto-setup to generate example workflows...")
        
        try:
            import auto_setup
            success = auto_setup.main()
            
            if success:
                # Create setup marker
                setup_marker.touch()
                print("✅ Auto-setup completed successfully!")
                return True
            else:
                print("❌ Auto-setup failed")
                return False
                
        except ImportError:
            print("⚠️ Auto-setup module not found, skipping...")
            setup_marker.touch()  # Mark as setup to avoid repeated attempts
            return False
        except Exception as e:
            print(f"❌ Auto-setup error: {e}")
            return False
    
    return True


if __name__ == "__main__":
    # Run first-time setup check
    check_first_run()
    
    # Run main CLI
    main()