# PinkFlow Workflow System Documentation

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

The PinkFlow Workflow System is a powerful, flexible framework for creating and managing dynamic workflows with node-based routing and conditional logic. It's designed to support complete development cycles across multiple environments (sandbox, staging, production).

### What is the Workflow System?

The Workflow System provides:

- **Node-based Architecture**: Create workflows as directed graphs of interconnected nodes
- **Conditional Routing**: Dynamic edge traversal based on runtime conditions
- **Environment Support**: Built-in support for sandbox, staging, production, and development environments
- **Execution Management**: Track and manage workflow executions with detailed history
- **Extensibility**: Easy to extend with custom nodes, conditions, and actions

### When to Use This System

Use the PinkFlow Workflow System when you need to:

- Orchestrate complex multi-step processes
- Implement conditional logic in your workflows
- Manage deployments across multiple environments
- Create repeatable, auditable processes
- Build dynamic routing based on runtime data

---

## Key Features

### 1. Dynamic Node Connections

Connect nodes dynamically with configurable edges:

```python
workflow.connect_nodes(
    from_node_id='build',
    to_node_id='test',
    condition=EdgeCondition(EdgeConditionType.ALWAYS)
)
```

### 2. Conditional Routing

Route execution based on runtime conditions:

```python
# Route to different nodes based on test results
workflow.connect(
    'check_tests', 'deploy',
    EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', True)
)

workflow.connect(
    'check_tests', 'fix_issues',
    EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', False)
)
```

### 3. Environment-Aware Execution

Workflows are environment-aware:

```python
workflow = WorkflowBuilder(
    workflow_id='deploy_001',
    name='Deployment Workflow',
    environment=Environment.PRODUCTION
).build()
```

### 4. Execution History

Track all workflow executions:

```python
history = manager.get_execution_history(workflow_id='deploy_001')
for execution in history:
    print(f"Executed at: {execution['started_at']}")
    print(f"Status: {execution['status']}")
```

---

## Architecture

### Component Overview

```
workflow-system/
├── core/                          # Core workflow components
│   ├── __init__.py               # Module exports
│   ├── workflow.py               # Workflow, Node, Edge classes
│   └── workflow_manager.py       # Manager and registry
├── examples/                      # Example workflows
│   └── example_workflows.py      # Ready-to-use examples
└── docs/                         # Documentation
    ├── README.md                 # This file
    ├── API_REFERENCE.md          # Detailed API docs
    └── EXAMPLES.md               # Usage examples
```

### Core Classes

1. **Workflow**: Main orchestrator for managing nodes and edges
2. **Node**: Represents a step in the workflow with executable action
3. **Edge**: Represents a connection between nodes with conditions
4. **WorkflowBuilder**: Fluent interface for building workflows
5. **WorkflowManager**: High-level interface for workflow management
6. **WorkflowRegistry**: Registry for storing and retrieving workflows

### Data Flow

```
Start Node → Process Node → Decision Node → [Conditional Routing] → End Node
     ↓            ↓              ↓                     ↓                ↓
  Execute      Execute        Execute            Evaluate          Execute
  Action       Action         Action            Conditions         Action
     ↓            ↓              ↓                     ↓                ↓
  Update       Update         Update              Select           Final
  Context      Context        Context            Next Node         Result
```

---

## Getting Started

### Installation

The workflow system is self-contained and requires only Python 3.8+:

```bash
# No external dependencies required
python3 --version  # Ensure Python 3.8+
```

### Quick Start

Here's a simple workflow to get started:

```python
from core.workflow import WorkflowBuilder, Environment, EdgeCondition, EdgeConditionType

# Define node actions
def start_task(context):
    context['task_started'] = True
    return context

def process_task(context):
    context['task_completed'] = True
    return context

# Build workflow
workflow = (
    WorkflowBuilder('quick_start', 'Quick Start Workflow')
    .add_start_node('start', 'Start', start_task)
    .add_process_node('process', 'Process', process_task)
    .add_end_node('end', 'End')
    .connect('start', 'process')
    .connect('process', 'end')
    .build()
)

# Execute workflow
result = workflow.execute()
print(f"Completed: {result.get('completed')}")
print(f"Path: {result.get('execution_path')}")
```

### Your First Workflow

Let's create a more realistic workflow:

```python
from core.workflow import WorkflowBuilder, Environment, EdgeCondition, EdgeConditionType

def build_code(context):
    """Build the code."""
    context['build_success'] = True
    return context

def run_tests(context):
    """Run automated tests."""
    context['tests_passed'] = True
    return context

def deploy(context):
    """Deploy the application."""
    context['deployed'] = True
    return context

# Create workflow
workflow = (
    WorkflowBuilder('ci_cd_001', 'CI/CD Pipeline', Environment.STAGING)
    .with_description('Basic CI/CD workflow')
    
    .add_start_node('start', 'Start Pipeline')
    .add_process_node('build', 'Build Code', build_code)
    .add_process_node('test', 'Run Tests', run_tests)
    .add_decision_node('check_tests', 'Check Tests')
    .add_process_node('deploy', 'Deploy', deploy)
    .add_end_node('success', 'Success')
    .add_end_node('failure', 'Failure')
    
    .connect('start', 'build')
    .connect('build', 'test')
    .connect('test', 'check_tests')
    .connect(
        'check_tests', 'deploy',
        EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', True)
    )
    .connect(
        'check_tests', 'failure',
        EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', False)
    )
    .connect('deploy', 'success')
    
    .build()
)

# Execute
result = workflow.execute()
print(f"Status: {'Success' if result.get('deployed') else 'Failed'}")
```

---

## Core Concepts

### 1. Nodes

Nodes are the building blocks of workflows. Each node has:

- **ID**: Unique identifier
- **Name**: Human-readable name
- **Type**: START, PROCESS, DECISION, END, PARALLEL, MERGE
- **Action**: Function to execute (optional)
- **Config**: Configuration parameters

**Node Types:**

- **START**: Entry point of the workflow
- **PROCESS**: Performs an action or computation
- **DECISION**: Makes decisions but doesn't execute logic
- **END**: Terminal node marking completion
- **PARALLEL**: Splits execution into parallel paths
- **MERGE**: Merges parallel paths back together

### 2. Edges

Edges connect nodes and define the flow:

- **Source Node**: Starting point
- **Destination Node**: Endpoint
- **Condition**: When the edge can be traversed
- **Priority**: For selecting among multiple edges

**Condition Types:**

- **ALWAYS**: Always traverse (default)
- **EQUALS**: Field equals value
- **NOT_EQUALS**: Field doesn't equal value
- **GREATER_THAN**: Field greater than value
- **LESS_THAN**: Field less than value
- **CONTAINS**: Value contained in field
- **CUSTOM**: Custom function for complex logic

### 3. Context

The context is a dictionary passed through the workflow:

```python
context = {
    'environment': 'staging',
    'workflow_id': 'deploy_001',
    'execution_path': ['start', 'build', 'test'],
    'custom_field': 'custom_value'
}
```

Context is updated by each node and used for conditional routing.

### 4. Environments

Four built-in environments with different configurations:

- **SANDBOX**: Experimentation (max 100 iterations, 60s timeout)
- **STAGING**: Pre-production testing (max 500 iterations, 300s timeout)
- **PRODUCTION**: Live deployment (max 1000 iterations, 600s timeout)
- **DEVELOPMENT**: Local development (max 50 iterations, 30s timeout)

---

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for detailed API documentation.

### Quick Reference

**Creating Workflows:**

```python
workflow = WorkflowBuilder(id, name, environment).build()
```

**Adding Nodes:**

```python
builder.add_start_node(id, name, action)
builder.add_process_node(id, name, action, config)
builder.add_decision_node(id, name, action)
builder.add_end_node(id, name, action)
```

**Connecting Nodes:**

```python
builder.connect(from_id, to_id, condition, priority)
```

**Executing Workflows:**

```python
result = workflow.execute(initial_context)
```

**Managing Workflows:**

```python
manager = WorkflowManager()
manager.register_workflow(workflow)
result = manager.execute_workflow(workflow_id, context)
```

---

## Examples

### Example 1: Development Cycle

Complete development workflow with testing and deployment:

```python
from examples.example_workflows import create_development_cycle_workflow

workflow = create_development_cycle_workflow()
result = workflow.execute()
```

See `examples/example_workflows.py` for the full implementation.

### Example 2: Sandbox Experimentation

Safe experimentation with automatic rollback:

```python
from examples.example_workflows import create_sandbox_workflow

workflow = create_sandbox_workflow()
result = workflow.execute()
```

### Example 3: Staging Deployment

Staging deployment with quality gates:

```python
from examples.example_workflows import create_staging_deployment_workflow

workflow = create_staging_deployment_workflow()
result = workflow.execute()
```

### Example 4: Production Deployment

Production deployment with canary and rollback:

```python
from examples.example_workflows import create_production_deployment_workflow

workflow = create_production_deployment_workflow()
result = workflow.execute()
```

---

## Advanced Usage

### Custom Conditions

Create custom conditions for complex logic:

```python
def custom_condition(context):
    """Complex condition logic."""
    return (
        context.get('quality_score', 0) > 80 and
        context.get('security_scan') == 'passed' and
        len(context.get('approvals', [])) >= 3
    )

edge = Edge(
    edge_id='custom_edge',
    from_node='check',
    to_node='deploy',
    condition=EdgeCondition(
        EdgeConditionType.CUSTOM,
        custom_function=custom_condition
    )
)
```

### Parallel Execution

Create workflows with parallel paths:

```python
builder = WorkflowBuilder('parallel_001', 'Parallel Workflow')

# Create parallel branches
builder.add_parallel_node('parallel_split', 'Split')
builder.add_process_node('branch_a', 'Branch A', action_a)
builder.add_process_node('branch_b', 'Branch B', action_b)
builder.add_merge_node('merge', 'Merge')

# Connect parallel paths
builder.connect('start', 'parallel_split')
builder.connect('parallel_split', 'branch_a')
builder.connect('parallel_split', 'branch_b')
builder.connect('branch_a', 'merge')
builder.connect('branch_b', 'merge')
builder.connect('merge', 'end')
```

### Exporting Workflows

Export workflows to JSON for storage or sharing:

```python
# Export single workflow
json_str = workflow.to_json()
with open('workflow.json', 'w') as f:
    f.write(json_str)

# Export all workflows from manager
manager.export_to_file(Path('all_workflows.json'))
```

### Workflow Statistics

Get insights about workflow executions:

```python
stats = manager.get_statistics()
print(f"Total workflows: {stats['total_workflows']}")
print(f"Total executions: {stats['total_executions']}")
print(f"Success rate: {stats['successful_executions'] / stats['total_executions']}")
```

---

## Best Practices

### 1. Node Design

- **Single Responsibility**: Each node should do one thing well
- **Idempotent Actions**: Node actions should be repeatable safely
- **Error Handling**: Handle errors gracefully in node actions
- **Clear Naming**: Use descriptive names for nodes and edges

### 2. Conditional Logic

- **Simple Conditions**: Keep conditions simple and testable
- **Priority Order**: Use priorities for multiple edges from same node
- **Default Paths**: Always provide a default path for decision nodes
- **Validation**: Validate context data before making decisions

### 3. Environment Management

- **Environment-Specific Config**: Use environment configs for different settings
- **Gradual Rollout**: Test in sandbox → staging → production
- **Rollback Plans**: Always have rollback capability in production
- **Monitoring**: Monitor workflow executions in production

### 4. Testing

- **Unit Test Nodes**: Test node actions independently
- **Integration Test Workflows**: Test complete workflow execution
- **Mock External Dependencies**: Use mocks for external services
- **Test All Paths**: Ensure all conditional paths are tested

### 5. Performance

- **Limit Iterations**: Set appropriate max_iterations to prevent infinite loops
- **Optimize Actions**: Keep node actions fast and efficient
- **Batch Operations**: Group related operations in single nodes
- **Async Operations**: Consider async for long-running operations

---

## Troubleshooting

### Common Issues

#### Issue: Workflow Validation Fails

**Symptom**: `ValueError: Workflow validation failed`

**Solutions:**
- Ensure workflow has start and end nodes
- Check all edges reference existing nodes
- Verify no unreachable nodes exist

#### Issue: Infinite Loop

**Symptom**: `ValueError: Workflow exceeded maximum iterations`

**Solutions:**
- Check for cycles in your workflow graph
- Ensure decision nodes have exit conditions
- Increase max_iterations if legitimately needed

#### Issue: Node Action Fails

**Symptom**: Exception during workflow execution

**Solutions:**
- Add error handling in node actions
- Validate context data before using it
- Use try-except blocks in actions
- Log errors for debugging

#### Issue: Condition Not Working

**Symptom**: Wrong path taken in workflow

**Solutions:**
- Verify field name exists in context
- Check condition type matches data type
- Use priority to order multiple conditions
- Test condition logic independently

### Debugging Tips

1. **Print Execution Path**:
   ```python
   result = workflow.execute()
   print(result.get('execution_path'))
   ```

2. **Add Logging to Actions**:
   ```python
   def my_action(context):
       print(f"Current context: {context}")
       # ... action logic
       return context
   ```

3. **Validate Workflow**:
   ```python
   errors = workflow.validate()
   if errors:
       print(f"Validation errors: {errors}")
   ```

4. **Check Execution History**:
   ```python
   history = manager.get_execution_history(workflow_id)
   for execution in history:
       print(f"Status: {execution['status']}")
   ```

---

## Support and Contributing

### Getting Help

- Check the [examples](../examples/example_workflows.py)
- Review the [API Reference](API_REFERENCE.md)
- Check [EXAMPLES.md](EXAMPLES.md) for more use cases

### Contributing

Contributions are welcome! To extend the workflow system:

1. Add new node types in `workflow.py`
2. Implement new condition types in `EdgeCondition`
3. Create reusable workflow templates in `examples/`
4. Add documentation and tests

### Version

Current version: **1.0.0**

---

**Last Updated**: 2025-11-08
**Maintained by**: PinkFlow Team
