# PinkFlow Workflow System

A powerful, flexible workflow orchestration system for managing dynamic node-based workflows with conditional routing across multiple environments.

## 🚀 Quick Start

```python
from core.workflow import WorkflowBuilder, Environment, EdgeCondition, EdgeConditionType

# Create a simple workflow
workflow = (
    WorkflowBuilder('my_workflow', 'My First Workflow', Environment.DEVELOPMENT)
    .add_start_node('start', 'Start')
    .add_process_node('process', 'Process Data', lambda ctx: {**ctx, 'processed': True})
    .add_end_node('end', 'End')
    .connect('start', 'process')
    .connect('process', 'end')
    .build()
)

# Execute the workflow
result = workflow.execute()
print(f"Completed: {result['completed']}")
print(f"Path: {' → '.join(result['execution_path'])}")
```

## 📋 Features

- **🔗 Dynamic Node Connections**: Build complex workflows by connecting nodes with conditional edges
- **🔀 Conditional Routing**: Route execution based on runtime conditions and data
- **🌍 Environment Support**: Built-in support for sandbox, staging, production, and development environments
- **📊 Execution Tracking**: Comprehensive execution history and statistics
- **🔧 Extensible**: Easy to extend with custom nodes, conditions, and actions
- **🎯 Type-Safe**: Built with Python type hints for better code quality
- **📖 Well-Documented**: Extensive documentation and examples

## 📁 Project Structure

```
workflow-system/
├── core/                          # Core workflow components
│   ├── __init__.py               # Module exports
│   ├── workflow.py               # Workflow, Node, Edge classes
│   └── workflow_manager.py       # Manager and registry
├── examples/                      # Example workflows
│   └── example_workflows.py      # Ready-to-use examples
└── docs/                         # Documentation
    ├── README.md                 # Main documentation
    ├── API_REFERENCE.md          # Detailed API docs
    └── EXAMPLES.md               # Usage examples
```

## 🎯 Use Cases

### Development Cycles
- Code → Build → Test → Review → Deploy workflows
- Automated CI/CD pipelines with quality gates
- Multi-stage deployment processes

### Environment Management
- Sandbox experimentation with rollback
- Staging validation and testing
- Production deployment with canary releases

### Data Processing
- ETL pipelines with validation
- Data transformation workflows
- Batch processing with error handling

### Business Processes
- Approval workflows
- Multi-step processes with conditions
- Event-driven automation

## 🛠️ Installation

No external dependencies required! Just Python 3.8+:

```bash
# Ensure you have Python 3.8 or higher
python3 --version

# The workflow system is self-contained
cd workflow-system
```

## 📚 Documentation

- **[Main Documentation](docs/README.md)**: Complete guide to the workflow system
- **[API Reference](docs/API_REFERENCE.md)**: Detailed API documentation
- **[Examples](docs/EXAMPLES.md)**: Practical examples and use cases

## 🎓 Examples

### Development Cycle Workflow

```python
from examples.example_workflows import create_development_cycle_workflow

workflow = create_development_cycle_workflow()
result = workflow.execute()
```

This creates a complete development workflow with:
- Code writing
- Automated testing
- Code review
- Conditional deployment based on quality

### Sandbox Experimentation

```python
from examples.example_workflows import create_sandbox_workflow

workflow = create_sandbox_workflow()
result = workflow.execute()
```

Safe experimentation with automatic rollback on failure.

### Production Deployment

```python
from examples.example_workflows import create_production_deployment_workflow

workflow = create_production_deployment_workflow()
result = workflow.execute()
```

Production deployment with canary releases and automatic rollback.

### Run All Examples

```bash
cd workflow-system
python3 examples/example_workflows.py
```

## 🔑 Key Concepts

### Nodes
Building blocks of workflows. Types include:
- **START**: Entry point
- **PROCESS**: Performs actions
- **DECISION**: Makes decisions
- **END**: Terminal node

### Edges
Connections between nodes with conditions:
- **ALWAYS**: Always traverse
- **EQUALS**: Field equals value
- **CUSTOM**: Complex custom logic

### Environments
- **SANDBOX**: Safe experimentation
- **STAGING**: Pre-production testing
- **PRODUCTION**: Live deployment
- **DEVELOPMENT**: Local development

## 🎨 Advanced Features

### Conditional Routing

```python
workflow.connect(
    'check_tests', 'deploy',
    EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', True),
    priority=10
)
```

### Custom Conditions

```python
def complex_condition(context):
    return (
        context.get('quality_score', 0) > 80 and
        context.get('security_scan') == 'passed'
    )

condition = EdgeCondition(
    EdgeConditionType.CUSTOM,
    custom_function=complex_condition
)
```

### Workflow Management

```python
from core.workflow import WorkflowManager

manager = WorkflowManager()
manager.register_workflow(workflow)
result = manager.execute_workflow('workflow_id', initial_context)

# Get statistics
stats = manager.get_statistics()
print(f"Total executions: {stats['total_executions']}")
print(f"Success rate: {stats['successful_executions'] / stats['total_executions']}")
```

## 🧪 Testing

Test the workflow system:

```bash
# Run example workflows
python3 examples/example_workflows.py

# Create and test your own workflow
python3 your_workflow.py
```

## 📊 Execution Context

Every workflow execution maintains a context dictionary:

```python
{
    'workflow_id': 'my_workflow',
    'environment': 'staging',
    'execution_path': ['start', 'process', 'end'],
    'iterations': 5,
    'completed': True,
    # Your custom fields
    'custom_data': 'value'
}
```

## 🔒 Best Practices

1. **Keep nodes simple**: Each node should have a single responsibility
2. **Use meaningful names**: Clear names for nodes and edges improve readability
3. **Handle errors gracefully**: Add error handling in node actions
4. **Test thoroughly**: Test all conditional paths
5. **Monitor executions**: Track workflow execution history
6. **Start with sandbox**: Test in sandbox before deploying to production

## 🤝 Integration with PinkFlow

This workflow system integrates seamlessly with the PinkFlow ecosystem:

- **DeafAuth**: Use for authentication in workflow actions
- **PinkSync**: Real-time workflow status updates
- **FibonRose**: Trust-based approval workflows
- **360Magicians**: AI-driven workflow orchestration

## 🌟 Real-World Example

Complete CI/CD pipeline:

```python
from core.workflow import WorkflowBuilder, Environment, EdgeCondition, EdgeConditionType

workflow = (
    WorkflowBuilder('cicd_001', 'CI/CD Pipeline', Environment.STAGING)
    .add_start_node('start', 'Start')
    .add_process_node('build', 'Build', build_action)
    .add_process_node('test', 'Test', test_action)
    .add_decision_node('check_tests', 'Check Tests')
    .add_process_node('deploy', 'Deploy', deploy_action)
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

result = workflow.execute()
```

## 📈 Statistics and Monitoring

Track workflow executions:

```python
manager = WorkflowManager()

# Register and execute workflows
manager.register_workflow(workflow)
result = manager.execute_workflow('workflow_id')

# Get execution history
history = manager.get_execution_history('workflow_id')
for execution in history:
    print(f"Started: {execution['started_at']}")
    print(f"Duration: {execution['duration_seconds']}s")
    print(f"Status: {execution['status']}")

# Get statistics
stats = manager.get_statistics()
print(f"Total workflows: {stats['total_workflows']}")
print(f"Success rate: {stats['successful_executions'] / stats['total_executions']:.2%}")
```

## 🔧 Configuration

Configure environment-specific settings:

```python
manager = WorkflowManager()

manager.configure_environment(
    Environment.PRODUCTION,
    {
        'max_iterations': 2000,
        'timeout_seconds': 900,
        'auto_rollback': False
    }
)
```

## 📦 Export and Import

Export workflows to JSON:

```python
# Export single workflow
json_str = workflow.to_json()

# Export all workflows
manager.export_to_file(Path('workflows.json'))
```

## 🆘 Troubleshooting

### Common Issues

**Validation fails**: Ensure all nodes are connected and reachable
```python
errors = workflow.validate()
if errors:
    print(f"Errors: {errors}")
```

**Infinite loop**: Check for cycles and set appropriate max_iterations
```python
result = workflow.execute(max_iterations=100)
```

**Condition not working**: Verify field names and use custom conditions for complex logic
```python
condition = EdgeCondition(
    EdgeConditionType.CUSTOM,
    custom_function=lambda c: c.get('field') == 'value'
)
```

## 📝 Version

**Version**: 1.0.0  
**Last Updated**: 2025-11-08  
**Python**: 3.8+

## 🤝 Contributing

Contributions welcome! To extend the workflow system:

1. Add new node types in `core/workflow.py`
2. Implement new condition types
3. Create reusable workflow templates
4. Add documentation and examples

## 📞 Support

- **Documentation**: See [docs/](docs/)
- **Examples**: See [examples/](examples/)
- **Issues**: Report issues to the PinkFlow repository

## 📄 License

Part of the PinkFlow project. See main repository LICENSE.

---

**Built with ❤️ for the PinkFlow Deaf-First Innovation Ecosystem**
