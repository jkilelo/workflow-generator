"""
Generic Workflow Schema Definition

Based on research of modern workflow orchestration engines (Prefect 3.0, Airflow, Temporal)
and analysis of existing app_generator implementations, this schema provides a comprehensive
foundation for auto-generating fullstack workflows.

Key Features:
- JSON Schema-based workflow definitions
- Dynamic step types with validation
- LLM integration patterns
- Conditional step execution
- Parameter validation and type safety
- Frontend form auto-generation
- Backend API auto-generation
"""

from typing import Dict, List, Optional, Any, Union, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum
import json


class ParameterType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    FILE = "file"
    SELECT = "select"
    MULTISELECT = "multiselect"
    TEXT_AREA = "textarea"
    JSON = "json"
    DATE = "date"
    URL = "url"
    EMAIL = "email"


class StepType(str, Enum):
    FORM_INPUT = "form_input"
    LLM_PROCESSING = "llm_processing"
    FILE_PROCESSING = "file_processing"
    HTTP_REQUEST = "http_request"
    DATA_TRANSFORMATION = "data_transformation"
    CODE_EXECUTION = "code_execution"
    OUTPUT_GENERATION = "output_generation"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PARALLEL = "parallel"


class ValidationRule(BaseModel):
    type: Literal["required", "min", "max", "pattern", "custom"]
    value: Optional[Union[str, int, float]] = None
    message: str


class ParameterDefinition(BaseModel):
    name: str
    type: ParameterType
    label: Optional[str] = None
    description: Optional[str] = None
    required: bool = False
    default: Optional[Any] = None
    options: Optional[List[Union[str, Dict[str, Any]]]] = None  # For select/multiselect
    validation: Optional[List[ValidationRule]] = None
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    depends_on: Optional[Dict[str, Any]] = None  # Conditional visibility
    
    @validator('options')
    def validate_options(cls, v, values):
        if values.get('type') in [ParameterType.SELECT, ParameterType.MULTISELECT] and not v:
            raise ValueError(f"Options required for {values.get('type')} parameter type")
        return v


class LLMConfiguration(BaseModel):
    template_name: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: str
    template_variables: Optional[List[str]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    response_format: Optional[Literal["text", "json", "structured"]] = "text"
    response_schema: Optional[Dict[str, Any]] = None


class ConditionalLogic(BaseModel):
    condition: str  # Python expression or JSONPath
    true_steps: List[str]  # Step IDs to execute if condition is true
    false_steps: Optional[List[str]] = None  # Step IDs to execute if condition is false


class StepDefinition(BaseModel):
    id: str
    name: str
    type: StepType
    description: Optional[str] = None
    depends_on: Optional[List[str]] = None  # Step IDs this step depends on
    parameters: Optional[List[ParameterDefinition]] = None
    llm_config: Optional[LLMConfiguration] = None
    conditional: Optional[ConditionalLogic] = None
    custom_handler: Optional[str] = None  # Python function name for custom logic
    output_mapping: Optional[Dict[str, str]] = None  # Map outputs to workflow variables
    error_handling: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None  # Timeout in seconds
    retry_config: Optional[Dict[str, Any]] = None
    ui_config: Optional[Dict[str, Any]] = None  # Frontend-specific configuration


class WorkflowMetadata(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class WorkflowConfiguration(BaseModel):
    parallel_execution: bool = False
    max_parallel_steps: int = 3
    default_timeout: int = 300
    auto_advance: bool = True
    save_intermediate_results: bool = True
    enable_rollback: bool = False
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


class WorkflowSchema(BaseModel):
    metadata: WorkflowMetadata
    steps: List[StepDefinition]
    configuration: Optional[WorkflowConfiguration] = WorkflowConfiguration()
    global_parameters: Optional[List[ParameterDefinition]] = None
    global_variables: Optional[Dict[str, Any]] = None
    
    @validator('steps')
    def validate_step_dependencies(cls, v):
        step_ids = {step.id for step in v}
        for step in v:
            if step.depends_on:
                for dep in step.depends_on:
                    if dep not in step_ids:
                        raise ValueError(f"Step {step.id} depends on non-existent step {dep}")
        return v
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Generate JSON Schema for this workflow"""
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "title": self.metadata.name,
            "description": self.metadata.description,
            "properties": {
                "metadata": self.metadata.dict(),
                "steps": [step.dict() for step in self.steps],
                "configuration": self.configuration.dict() if self.configuration else {}
            }
        }
    
    def get_step_by_id(self, step_id: str) -> Optional[StepDefinition]:
        """Get step definition by ID"""
        return next((step for step in self.steps if step.id == step_id), None)
    
    def get_execution_order(self) -> List[List[str]]:
        """Calculate step execution order based on dependencies"""
        # Topological sort implementation
        step_graph = {step.id: step.depends_on or [] for step in self.steps}
        execution_order = []
        processed = set()
        
        while len(processed) < len(self.steps):
            ready_steps = [
                step_id for step_id in step_graph.keys()
                if step_id not in processed and all(dep in processed for dep in step_graph[step_id])
            ]
            
            if not ready_steps:
                remaining = set(step_graph.keys()) - processed
                raise ValueError(f"Circular dependency detected in steps: {remaining}")
            
            execution_order.append(ready_steps)
            processed.update(ready_steps)
        
        return execution_order


# Example workflow schemas based on existing implementations

def create_ai_web_testing_workflow() -> WorkflowSchema:
    """Create schema for AI Web UI Testing Framework"""
    return WorkflowSchema(
        metadata=WorkflowMetadata(
            id="ai_web_testing",
            name="AI Web UI Testing Framework",
            description="AI-powered web UI testing with element extraction and test generation",
            category="testing",
            tags=["ai", "web", "testing", "automation"]
        ),
        steps=[
            StepDefinition(
                id="element_extraction",
                name="Element Extraction",
                type=StepType.HTTP_REQUEST,
                description="Extract interactive elements from web pages",
                parameters=[
                    ParameterDefinition(
                        name="page_url",
                        type=ParameterType.URL,
                        label="Page URL",
                        description="URL of the web page to analyze",
                        required=True,
                        validation=[ValidationRule(type="required", message="Page URL is required")]
                    )
                ],
                custom_handler="crawl_website"
            ),
            StepDefinition(
                id="test_generation",
                name="Test Cases Generation",
                type=StepType.LLM_PROCESSING,
                description="Generate AI-powered test scenarios",
                depends_on=["element_extraction"],
                llm_config=LLMConfiguration(
                    template_name="gherkin_generation",
                    user_prompt_template="Generate comprehensive test scenarios for the following web elements:\n{elements_description}\nPage URL: {page_url}",
                    template_variables=["elements_description", "page_url"],
                    response_format="text"
                ),
                parameters=[
                    ParameterDefinition(
                        name="llm_provider",
                        type=ParameterType.SELECT,
                        label="LLM Provider",
                        required=True,
                        options=["openai", "anthropic", "google"]
                    )
                ]
            ),
            StepDefinition(
                id="code_generation",
                name="Code Generation",
                type=StepType.LLM_PROCESSING,
                description="Generate executable test code",
                depends_on=["test_generation"],
                llm_config=LLMConfiguration(
                    template_name="playwright_generation",
                    user_prompt_template="Generate Playwright test code for:\n{test_scenarios}",
                    template_variables=["test_scenarios"],
                    response_format="text"
                ),
                parameters=[
                    ParameterDefinition(
                        name="llm_provider",
                        type=ParameterType.SELECT,
                        label="LLM Provider",
                        required=True,
                        options=["openai", "anthropic", "google"]
                    )
                ]
            ),
            StepDefinition(
                id="code_execution",
                name="Code Execution",
                type=StepType.CODE_EXECUTION,
                description="Execute generated tests and view results",
                depends_on=["code_generation"],
                custom_handler="execute_test_code"
            )
        ]
    )


def create_dq_testing_workflow() -> WorkflowSchema:
    """Create schema for DQ Testing Framework"""
    return WorkflowSchema(
        metadata=WorkflowMetadata(
            id="dq_testing",
            name="Data Quality Testing Framework",
            description="Comprehensive data quality analysis and testing",
            category="data_quality",
            tags=["data", "quality", "testing", "analysis"]
        ),
        steps=[
            StepDefinition(
                id="schema_analysis",
                name="Schema Analysis",
                type=StepType.LLM_PROCESSING,
                description="Analyze data schema and generate profiling suggestions",
                parameters=[
                    ParameterDefinition(
                        name="data_file",
                        type=ParameterType.FILE,
                        label="Data File",
                        required=True,
                        validation=[ValidationRule(type="required", message="Data file is required")]
                    ),
                    ParameterDefinition(
                        name="llm_provider",
                        type=ParameterType.SELECT,
                        label="LLM Provider",
                        required=True,
                        options=["openai", "anthropic", "google"]
                    )
                ],
                llm_config=LLMConfiguration(
                    template_name="schema_analysis",
                    user_prompt_template="Analyze the following data schema and provide comprehensive profiling suggestions:\n{schema_info}",
                    template_variables=["schema_info"],
                    response_format="structured"
                )
            ),
            StepDefinition(
                id="profile_generation",
                name="Profile Generation",
                type=StepType.LLM_PROCESSING,
                description="Generate data quality profiles",
                depends_on=["schema_analysis"],
                llm_config=LLMConfiguration(
                    template_name="profile_generation",
                    user_prompt_template="Generate data quality profiles based on analysis:\n{analysis_results}",
                    template_variables=["analysis_results"],
                    response_format="json"
                )
            ),
            StepDefinition(
                id="rule_generation",
                name="Rule Generation",
                type=StepType.LLM_PROCESSING,
                description="Generate data quality rules",
                depends_on=["profile_generation"],
                llm_config=LLMConfiguration(
                    template_name="rule_generation",
                    user_prompt_template="Generate data quality rules from profiles:\n{profiles}",
                    template_variables=["profiles"],
                    response_format="structured"
                )
            ),
            StepDefinition(
                id="execution",
                name="Execution",
                type=StepType.CODE_EXECUTION,
                description="Execute data quality tests",
                depends_on=["rule_generation"],
                custom_handler="execute_dq_tests"
            )
        ]
    )


if __name__ == "__main__":
    # Example usage
    ai_workflow = create_ai_web_testing_workflow()
    dq_workflow = create_dq_testing_workflow()
    
    print("AI Web Testing Workflow JSON Schema:")
    print(json.dumps(ai_workflow.to_json_schema(), indent=2))
    
    print("\nExecution Order:", ai_workflow.get_execution_order())