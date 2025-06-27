"""
Generic Workflow Generator

Auto-generates FastAPI backend and React frontend code from workflow schema definitions.
This system creates production-ready code that integrates with the existing app_generator
architecture while being completely generic and extensible.

Key Features:
- FastAPI plugin generation with proper type hints
- React TypeScript component generation
- Dynamic form generation based on parameter schemas
- LLM integration with template system
- Error handling and validation
- State management integration
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, BaseLoader
from workflow_schema import (
    WorkflowSchema,
    StepDefinition,
    ParameterDefinition,
    ParameterType,
    StepType,
)


class WorkflowGenerator:
    """Generates FastAPI backend and React frontend code from workflow schemas"""

    def __init__(self, output_dir: str = "./generated_workflows"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.setup_templates()

    def setup_templates(self):
        """Setup Jinja2 templates for code generation"""
        # Store templates as separate strings to avoid Python string formatting conflicts
        self.fastapi_template_content = '''from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
import asyncio
import logging
from base_plugin import BasePlugin, PluginMetadata
from llm_manager import LLMManager

{% for param in global_parameters %}
class {{ param.name|title }}Model(BaseModel):
    {% if param.type.value == 'string' %}
    {{ param.name }}: str{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field("{{ param.default or '' }}", description="{{ param.description or '' }}"){% endif %}
    {% elif param.type.value == 'number' %}
    {{ param.name }}: float{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field({{ param.default or 0 }}, description="{{ param.description or '' }}"){% endif %}
    {% elif param.type.value == 'boolean' %}
    {{ param.name }}: bool{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field({{ param.default or 'False' }}, description="{{ param.description or '' }}"){% endif %}
    {% elif param.type.value == 'file' %}
    {{ param.name }}: UploadFile = File(...)
    {% endif %}

{% endfor %}

{% for step in steps %}
class {{ step.id|title }}Request(BaseModel):
{%- if step.parameters and step.parameters|length > 0 %}
{%- for param in step.parameters %}
    {%- if param.type.value == 'string' or param.type.value == 'url' or param.type.value == 'textarea' %}
    {{ param.name }}: str{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field("{{ param.default or '' }}", description="{{ param.description or '' }}"){% endif %}
    {%- elif param.type.value == 'number' %}
    {{ param.name }}: float{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field({{ param.default or 0 }}, description="{{ param.description or '' }}"){% endif %}
    {%- elif param.type.value == 'boolean' %}
    {{ param.name }}: bool{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field({{ param.default or 'False' }}, description="{{ param.description or '' }}"){% endif %}
    {%- elif param.type.value == 'select' %}
    {{ param.name }}: str{% if param.required %} = Field(..., description="{{ param.description or '' }}"){% else %} = Field("{{ param.options[0] if param.options else '' }}", description="{{ param.description or '' }}"){% endif %}
    {%- elif param.type.value == 'file' %}
    {{ param.name }}: Optional[str] = Field(None, description="{{ param.description or '' }}")
    {%- endif %}
{%- endfor %}
{%- else %}
    pass  # No parameters for this step
{%- endif %}

class {{ step.id|title }}Response(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    execution_id: Optional[str] = None

{% endfor %}

class {{ class_name }}Plugin(BasePlugin):
    """Auto-generated plugin for {{ workflow_name }}"""
    
    def __init__(self):
        super().__init__()
        self.llm_manager: Optional[LLMManager] = None
        self.logger = logging.getLogger(__name__)
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{{ workflow_id }}",
            version="{{ version }}",
            description="{{ description }}",
            author="{{ author or 'Auto-generated' }}",
            category="{{ category or 'general' }}"
        )
    
    async def initialize(self) -> bool:
        """Initialize the plugin"""
        try:
            self.llm_manager = LLMManager()
            await self.llm_manager.initialize()
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize {{ class_name }}Plugin: {e}")
            return False
    
    async def cleanup(self) -> bool:
        """Clean up plugin resources"""
        if self.llm_manager:
            await self.llm_manager.cleanup()
        return True
    
    def get_api_routes(self) -> List[Dict[str, Any]]:
        """Return API routes for this plugin"""
        return [
            {% for step in steps %}
            {
                "path": "/{{ workflow_id }}/{{ step.id }}",
                "method": "POST",
                "handler": self.{{ step.id }},
                "request_model": {{ step.id|title }}Request,
                "response_model": {{ step.id|title }}Response
            },
            {% endfor %}
        ]
    
    {% for step in steps %}
    async def {{ step.id }}(self, request: {{ step.id|title }}Request) -> {{ step.id|title }}Response:
        """{{ step.description or 'Execute ' + step.name }}"""
        try:
            self.logger.info(f"Executing step: {{ step.id }}")
            
            {% if step.type.value == 'llm_processing' %}
            # LLM Processing Step
            if not self.llm_manager:
                raise HTTPException(status_code=500, detail="LLM Manager not initialized")
            
            # Prepare template variables
            template_vars = {}
            {% if step.llm_config and step.llm_config.template_variables %}
            {% for var in step.llm_config.template_variables %}
            template_vars["{{ var }}"] = getattr(request, "{{ var }}", "")
            {% endfor %}
            {% endif %}
            
            # Generate LLM response
            prompt_text = """{{ step.llm_config.user_prompt_template if step.llm_config else 'Process the request' }}""".format(**template_vars)
            response = await self.llm_manager.generate(
                provider_name=getattr(request, 'llm_provider', 'openai'),
                messages=[{
                    "role": "user", 
                    "content": prompt_text
                }],
                {% if step.llm_config and step.llm_config.max_tokens %}
                max_tokens={{ step.llm_config.max_tokens }},
                {% endif %}
                {% if step.llm_config and step.llm_config.temperature %}
                temperature={{ step.llm_config.temperature }}
                {% endif %}
            )
            
            result_data = {
                "llm_response": response,
                "template_vars": template_vars,
                "step_id": "{{ step.id }}"
            }
            
            {% elif step.type.value == 'form_input' %}
            # Form Input Step - just return the input data
            result_data = request.dict()
            
            {% elif step.type.value == 'file_processing' %}
            # File Processing Step
            result_data = {
                "message": "File processing completed",
                "step_id": "{{ step.id }}"
            }
            
            {% elif step.type.value == 'http_request' %}
            # HTTP Request Step
            {% if step.custom_handler %}
            result_data = await self.{{ step.custom_handler }}(request)
            {% else %}
            result_data = {
                "message": "HTTP request completed",
                "step_id": "{{ step.id }}"
            }
            {% endif %}
            
            {% elif step.type.value == 'code_execution' %}
            # Code Execution Step
            {% if step.custom_handler %}
            result_data = await self.{{ step.custom_handler }}(request)
            {% else %}
            result_data = {
                "message": "Code execution completed",
                "execution_id": f"exec_{{ step.id }}_{hash(str(request.dict()))}",
                "step_id": "{{ step.id }}"
            }
            {% endif %}
            
            {% else %}
            # Generic Step Processing
            result_data = {
                "message": "Step {{ step.id }} completed successfully",
                "step_id": "{{ step.id }}",
                "request_data": request.dict()
            }
            {% endif %}
            
            return {{ step.id|title }}Response(
                success=True,
                data=result_data,
                message="{{ step.name }} completed successfully"
            )
            
        except Exception as e:
            self.logger.error(f"Error in {{ step.id }}: {str(e)}")
            return {{ step.id|title }}Response(
                success=False,
                message=f"Error in {{ step.name }}: {str(e)}"
            )
    
    {% endfor %}
    
    {% if custom_handlers %}
    # Custom handler methods (implement these based on your specific needs)
    {% for handler in custom_handlers %}
    async def {{ handler }}(self, request) -> Dict[str, Any]:
        """Custom handler: {{ handler }}"""
        # TODO: Implement custom logic for {{ handler }}
        return {"message": "{{ handler }} completed", "custom": True}
    
    {% endfor %}
    {% endif %}

# Plugin instance for registration
plugin_instance = {{ class_name }}Plugin()
'''

        self.react_template = """
import React, { useState, useEffect } from 'react';
import { useWorkflowStore } from '../store/workflowStore';
import { appApiService } from '../services/appApiService';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { FileUpload } from '../components/ui/FileUpload';
import { TextArea } from '../components/ui/TextArea';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { CheckCircle, Clock, AlertCircle, Play } from 'lucide-react';

interface {{ component_name }}Props {
  appId: string;
}

interface StepState {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  result?: any;
  error?: string;
}

const {{ component_name }}: React.FC<{{ component_name }}Props> = ({ appId }) => {
  const { updateWorkflowStep } = useWorkflowStore();
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isExecuting, setIsExecuting] = useState(false);
  
  // Step states
  const [steps, setSteps] = useState<StepState[]>([
    {% for step in steps %}
    {
      id: '{{ step.id }}',
      name: '{{ step.name }}',
      status: 'pending'
    },
    {% endfor %}
  ]);
  
  // Form states for each step
  {% for step in steps %}
  const [{{ step.id }}Form, set{{ step.id|title }}Form] = useState({
    {% for param in step.parameters or [] %}
    {{ param.name }}: {{ param.default|tojson if param.default else ('""' if param.type.value == 'string' else ('false' if param.type.value == 'boolean' else '0')) }},
    {% endfor %}
  });
  
  {% endfor %}
  
  const currentStep = steps[currentStepIndex];
  
  const updateStepStatus = (stepId: string, status: StepState['status'], result?: any, error?: string) => {
    setSteps(prev => prev.map(step => 
      step.id === stepId 
        ? { ...step, status, result, error }
        : step
    ));
  };
  
  {% for step in steps %}
  const execute{{ step.id|title }} = async () => {
    setIsExecuting(true);
    updateStepStatus('{{ step.id }}', 'running');
    
    try {
      const response = await appApiService.executeStep(
        appId,
        '{{ step.id }}',
        {{ step.id }}Form
      );
      
      if (response.success) {
        updateStepStatus('{{ step.id }}', 'completed', response.data);
        updateWorkflowStep(appId, '{{ step.id }}', response.data);
        
        // Auto-advance to next step if available
        if (currentStepIndex < steps.length - 1) {
          setCurrentStepIndex(prev => prev + 1);
        }
      } else {
        updateStepStatus('{{ step.id }}', 'error', null, response.message);
      }
    } catch (error) {
      updateStepStatus('{{ step.id }}', 'error', null, error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setIsExecuting(false);
    }
  };
  
  {% endfor %}
  
  const getStepIcon = (status: StepState['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'running':
        return <Clock className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <div className="w-5 h-5 rounded-full border-2 border-gray-300" />;
    }
  };
  
  const renderStepForm = () => {
    if (!currentStep) return null;
    
    switch (currentStep.id) {
      {% for step in steps %}
      case '{{ step.id }}':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">{{ step.name }}</h3>
            {% if step.description %}
            <p className="text-gray-600">{{ step.description }}</p>
            {% endif %}
            
            {% for param in step.parameters or [] %}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {{ param.label or param.name|title }}
                {% if param.required %}<span className="text-red-500">*</span>{% endif %}
              </label>
              
              {% if param.type.value == 'string' %}
              <Input
                type="text"
                value={ {{ step.id }}Form.{{ param.name }} }
                onChange={(e) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: e.target.value}))}
                placeholder="{{ param.placeholder or '' }}"
                required={ {{ param.required|lower }} }
              />
              {% elif param.type.value == 'number' %}
              <Input
                type="number"
                value={ {{ step.id }}Form.{{ param.name }} }
                onChange={(e) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: parseFloat(e.target.value) || 0}))}
                placeholder="{{ param.placeholder or '' }}"
                required={ {{ param.required|lower }} }
              />
              {% elif param.type.value == 'boolean' %}
              <input
                type="checkbox"
                checked={ {{ step.id }}Form.{{ param.name }} }
                onChange={(e) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: e.target.checked}))}
                className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              {% elif param.type.value == 'select' %}
              <Select
                value={ {{ step.id }}Form.{{ param.name }} }
                onChange={(value) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: value}))}
                required={ {{ param.required|lower }} }
              >
                {% if param.options %}
                {% for option in param.options %}
                <option value="{{ option }}">{{ option }}</option>
                {% endfor %}
                {% endif %}
              </Select>
              {% elif param.type.value == 'textarea' %}
              <TextArea
                value={ {{ step.id }}Form.{{ param.name }} }
                onChange={(e) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: e.target.value}))}
                placeholder="{{ param.placeholder or '' }}"
                required={ {{ param.required|lower }} }
                rows={4}
              />
              {% elif param.type.value == 'file' %}
              <FileUpload
                onFileSelect={(file) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: file}))}
                accept="*/*"
                required={ {{ param.required|lower }} }
              />
              {% elif param.type.value == 'url' %}
              <Input
                type="url"
                value={ {{ step.id }}Form.{{ param.name }} }
                onChange={(e) => set{{ step.id|title }}Form(prev => ({...prev, {{ param.name }}: e.target.value}))}
                placeholder="{{ param.placeholder or 'https://example.com' }}"
                required={ {{ param.required|lower }} }
              />
              {% endif %}
              
              {% if param.help_text %}
              <p className="text-xs text-gray-500 mt-1">{{ param.help_text }}</p>
              {% endif %}
            </div>
            {% endfor %}
            
            <Button
              onClick={execute{{ step.id|title }}}
              disabled={isExecuting}
              className="w-full"
            >
              {isExecuting ? (
                <>
                  <Clock className="w-4 h-4 mr-2 animate-spin" />
                  Running {{ step.name }}...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Start {{ step.name }}
                </>
              )}
            </Button>
            
            {currentStep.result && (
              <Card className="mt-4">
                <CardHeader>
                  <CardTitle className="text-sm">Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto max-h-64">
                    {JSON.stringify(currentStep.result, null, 2)}
                  </pre>
                </CardContent>
              </Card>
            )}
            
            {currentStep.error && (
              <div className="bg-red-50 border border-red-200 rounded p-3">
                <p className="text-red-800 text-sm">Error: {currentStep.error}</p>
              </div>
            )}
          </div>
        );
      {% endfor %}
      default:
        return <div>Unknown step</div>;
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">{{ workflow_name }}</h1>
      
      {/* Step Progress */}
      <div className="mb-8">
        <div className="flex items-center space-x-4">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div className={`flex items-center space-x-2 p-2 rounded ${
                index === currentStepIndex ? 'bg-blue-50 border border-blue-200' : ''
              }`}>
                {getStepIcon(step.status)}
                <span className={`text-sm ${
                  index === currentStepIndex ? 'font-semibold' : ''
                }`}>
                  {step.name}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div className="w-8 h-px bg-gray-300 mx-2" />
              )}
            </div>
          ))}
        </div>
      </div>
      
      {/* Current Step Form */}
      <Card>
        <CardContent className="p-6">
          {renderStepForm()}
        </CardContent>
      </Card>
      
      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <Button
          variant="outline"
          onClick={() => setCurrentStepIndex(prev => Math.max(0, prev - 1))}
          disabled={currentStepIndex === 0}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          onClick={() => setCurrentStepIndex(prev => Math.min(steps.length - 1, prev + 1))}
          disabled={currentStepIndex === steps.length - 1}
        >
          Next
        </Button>
      </div>
    </div>
  );
};

export default {{ component_name }};
"""

    def generate_fastapi_plugin(self, workflow: WorkflowSchema) -> str:
        """Generate FastAPI plugin code from workflow schema"""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.fastapi_template_content)

        # Extract custom handlers
        custom_handlers = set()
        for step in workflow.steps:
            if step.custom_handler:
                custom_handlers.add(step.custom_handler)

        return template.render(
            workflow_id=workflow.metadata.id,
            workflow_name=workflow.metadata.name,
            class_name="".join(
                word.capitalize() for word in workflow.metadata.id.split("_")
            ),
            description=workflow.metadata.description or "",
            version=workflow.metadata.version,
            author=workflow.metadata.author,
            category=workflow.metadata.category,
            steps=workflow.steps,
            global_parameters=workflow.global_parameters or [],
            custom_handlers=list(custom_handlers),
        )

    def generate_react_component(self, workflow: WorkflowSchema) -> str:
        """Generate React component code from workflow schema"""
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.react_template)

        component_name = (
            "".join(word.capitalize() for word in workflow.metadata.id.split("_"))
            + "Workflow"
        )

        return template.render(
            workflow_id=workflow.metadata.id,
            workflow_name=workflow.metadata.name,
            component_name=component_name,
            steps=workflow.steps,
        )

    def generate_app_config(self, workflow: WorkflowSchema) -> Dict[str, Any]:
        """Generate app configuration for main_api_server.py integration"""
        return {
            "id": workflow.metadata.id,
            "name": workflow.metadata.name,
            "description": workflow.metadata.description or "",
            "category": workflow.metadata.category or "general",
            "plugin_class": f"{workflow.metadata.id}_plugin.plugin_instance",
            "steps": [
                {
                    "id": step.id,
                    "name": step.name,
                    "description": step.description or "",
                }
                for step in workflow.steps
            ],
        }

    def generate_workflow_files(self, workflow: WorkflowSchema) -> Dict[str, str]:
        """Generate all files for a workflow"""
        files = {}

        # Generate FastAPI plugin
        plugin_code = self.generate_fastapi_plugin(workflow)
        files[f"{workflow.metadata.id}_plugin.py"] = plugin_code

        # Generate React component
        component_code = self.generate_react_component(workflow)
        files[f"{workflow.metadata.id}_workflow.tsx"] = component_code

        # Generate configuration
        config = self.generate_app_config(workflow)
        files[f"{workflow.metadata.id}_config.json"] = json.dumps(config, indent=2)

        # Generate workflow schema file
        files[f"{workflow.metadata.id}_schema.json"] = json.dumps(
            workflow.model_dump(), indent=2
        )

        return files

    def save_workflow_files(
        self,
        workflow: WorkflowSchema,
        output_backend_dir: str = None,
        output_frontend_dir: str = None,
    ):
        """Save generated workflow files to filesystem"""
        files = self.generate_workflow_files(workflow)

        # Save backend plugin
        if output_backend_dir:
            backend_path = Path(output_backend_dir)
            backend_path.mkdir(exist_ok=True)
            with open(backend_path / f"{workflow.metadata.id}_plugin.py", "w") as f:
                f.write(files[f"{workflow.metadata.id}_plugin.py"])

        # Save frontend component
        if output_frontend_dir:
            frontend_path = Path(output_frontend_dir)
            frontend_path.mkdir(exist_ok=True)
            with open(frontend_path / f"{workflow.metadata.id}_workflow.tsx", "w") as f:
                f.write(files[f"{workflow.metadata.id}_workflow.tsx"])

        # Save to output directory
        workflow_dir = self.output_dir / workflow.metadata.id
        workflow_dir.mkdir(exist_ok=True)

        for filename, content in files.items():
            with open(workflow_dir / filename, "w") as f:
                f.write(content)

        return workflow_dir


# Example usage and testing
if __name__ == "__main__":
    from workflow_schema import (
        create_ai_web_testing_workflow,
        create_dq_testing_workflow,
    )

    generator = WorkflowGenerator()

    # Generate AI Web Testing workflow
    ai_workflow = create_ai_web_testing_workflow()
    ai_files = generator.generate_workflow_files(ai_workflow)
    generator.save_workflow_files(ai_workflow)

    # Generate DQ Testing workflow
    dq_workflow = create_dq_testing_workflow()
    dq_files = generator.generate_workflow_files(dq_workflow)
    generator.save_workflow_files(dq_workflow)

    print("Generated workflows:")
    print(f"- AI Web Testing: {len(ai_files)} files")
    print(f"- DQ Testing: {len(dq_files)} files")
    print(f"Output directory: {generator.output_dir}")
