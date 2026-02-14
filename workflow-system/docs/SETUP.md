# Workflow System Setup and Integration Guide

This guide provides detailed instructions for setting up and integrating the PinkFlow Workflow System into your projects.

---

## Table of Contents

- [Quick Setup](#quick-setup)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Integration with PinkFlow](#integration-with-pinkflow)
- [Extending the System](#extending-the-system)
- [Migration Guide](#migration-guide)
- [Troubleshooting](#troubleshooting)

---

## Quick Setup

### 1. Basic Setup

The workflow system is self-contained with no external dependencies:

```bash
# Navigate to the workflow system
cd workflow-system

# Verify Python version
python3 --version  # Should be 3.8 or higher

# Test the installation by running examples
python3 examples/example_workflows.py
```

### 2. Using in Your Project

Add the workflow system to your Python path:

```python
import sys
from pathlib import Path

# Add workflow-system to path
sys.path.insert(0, str(Path(__file__).parent / 'workflow-system'))

# Import and use
from core.workflow import WorkflowBuilder, Environment

workflow = (
    WorkflowBuilder('my_workflow', 'My Workflow')
    .add_start_node('start', 'Start')
    .add_end_node('end', 'End')
    .connect('start', 'end')
    .build()
)

result = workflow.execute()
```

---

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Any OS with Python support (Linux, macOS, Windows)
- **Memory**: Minimal (workflows run in-memory)
- **Storage**: Minimal (source code only)

### Recommended Setup

- **Python**: 3.10+
- **Environment**: Virtual environment for isolation
- **IDE**: VS Code, PyCharm, or similar with Python support
- **Linting**: flake8, black, mypy for code quality

---

## Installation

### Option 1: Direct Usage (Recommended)

Copy the workflow-system directory to your project:

```bash
# Copy to your project
cp -r workflow-system /path/to/your/project/

# Or use as a submodule
git submodule add <repo-url> workflow-system
```

### Option 2: System-Wide Installation

Create a symbolic link for system-wide access:

```bash
# Create a directory for custom Python modules
mkdir -p ~/python-modules

# Link workflow system
ln -s /path/to/workflow-system ~/python-modules/workflow_system

# Add to PYTHONPATH in ~/.bashrc or ~/.zshrc
echo 'export PYTHONPATH="${PYTHONPATH}:${HOME}/python-modules"' >> ~/.bashrc
source ~/.bashrc
```

### Option 3: Package Installation

Create a setup.py for pip installation:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='pinkflow-workflow-system',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>=3.8',
    description='PinkFlow Workflow Orchestration System',
    author='PinkFlow Team',
    license='TBD',
)
```

Install:

```bash
cd workflow-system
pip install -e .
```

---

## Configuration

### Environment Configuration

Configure settings for each environment:

```python
from core.workflow import WorkflowManager, Environment

manager = WorkflowManager()

# Configure sandbox environment
manager.configure_environment(
    Environment.SANDBOX,
    {
        'max_iterations': 100,
        'timeout_seconds': 60,
        'auto_rollback': True,
        'debug_mode': True
    }
)

# Configure staging environment
manager.configure_environment(
    Environment.STAGING,
    {
        'max_iterations': 500,
        'timeout_seconds': 300,
        'auto_rollback': True,
        'notification_url': 'https://staging.notify.example.com'
    }
)

# Configure production environment
manager.configure_environment(
    Environment.PRODUCTION,
    {
        'max_iterations': 1000,
        'timeout_seconds': 600,
        'auto_rollback': False,
        'monitoring_enabled': True,
        'notification_url': 'https://prod.notify.example.com'
    }
)
```

### Using Configuration Files

Store configuration in JSON:

```json
{
  "environments": {
    "sandbox": {
      "max_iterations": 100,
      "timeout_seconds": 60,
      "auto_rollback": true
    },
    "staging": {
      "max_iterations": 500,
      "timeout_seconds": 300,
      "auto_rollback": true
    },
    "production": {
      "max_iterations": 1000,
      "timeout_seconds": 600,
      "auto_rollback": false
    }
  }
}
```

Load configuration:

```python
import json
from pathlib import Path

# Load config
config_path = Path('workflow-config.json')
with open(config_path) as f:
    config = json.load(f)

# Apply to manager
for env_name, env_config in config['environments'].items():
    env = Environment[env_name.upper()]
    manager.configure_environment(env, env_config)
```

---

## Integration with PinkFlow

### Integration with DeafAuth

Use DeafAuth for authentication in workflows:

```python
def authenticate_user(context):
    """Authenticate user with DeafAuth."""
    # Integration with DeafAuth
    user_token = context.get('auth_token')
    
    # Validate with DeafAuth service
    # auth_result = deafauth_client.validate(user_token)
    
    context['authenticated'] = True
    context['user_id'] = 'user123'
    return context

workflow = (
    WorkflowBuilder('auth_workflow', 'Authentication Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('auth', 'Authenticate', authenticate_user)
    .add_end_node('end', 'End')
    .connect('start', 'auth')
    .connect('auth', 'end')
    .build()
)
```

### Integration with PinkSync

Real-time workflow status updates:

```python
def notify_progress(context):
    """Send progress updates via PinkSync."""
    # Integration with PinkSync
    current_node = context['execution_path'][-1]
    
    # Send WebSocket update
    # pinksync_client.send_update({
    #     'workflow_id': context['workflow_id'],
    #     'node': current_node,
    #     'status': 'in_progress'
    # })
    
    return context

# Add to all process nodes
workflow = (
    WorkflowBuilder('sync_workflow', 'Synced Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('process', 'Process', notify_progress)
    .add_end_node('end', 'End')
    .connect('start', 'process')
    .connect('process', 'end')
    .build()
)
```

### Integration with FibonRose

Trust-based approval workflows:

```python
from core.workflow import EdgeCondition, EdgeConditionType

def check_trust_score(context):
    """Check user's FibonRose trust score."""
    user_id = context.get('user_id')
    
    # Get trust score from FibonRose
    # trust_score = fibonrose_client.get_trust_score(user_id)
    trust_score = 85  # Example
    
    context['trust_score'] = trust_score
    return context

def requires_approval(context):
    """Check if approval is required based on trust."""
    return context.get('trust_score', 0) < 80

workflow = (
    WorkflowBuilder('approval_workflow', 'Approval Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('check_trust', 'Check Trust', check_trust_score)
    .add_decision_node('decide_approval', 'Decide Approval')
    .add_process_node('auto_approve', 'Auto Approve', lambda c: {**c, 'approved': True})
    .add_process_node('manual_review', 'Manual Review', lambda c: c)
    .add_end_node('end', 'End')
    
    .connect('start', 'check_trust')
    .connect('check_trust', 'decide_approval')
    .connect(
        'decide_approval', 'auto_approve',
        EdgeCondition(EdgeConditionType.GREATER_THAN, 'trust_score', 80)
    )
    .connect(
        'decide_approval', 'manual_review',
        EdgeCondition(EdgeConditionType.LESS_THAN, 'trust_score', 80)
    )
    .connect('auto_approve', 'end')
    .connect('manual_review', 'end')
    .build()
)
```

### Integration with 360Magicians

AI-driven workflow orchestration:

```python
def ai_decide(context):
    """Use AI to make workflow decisions."""
    input_data = context.get('data')
    
    # Call 360Magicians AI service
    # decision = magicians_client.analyze(input_data)
    decision = 'approve'  # Example
    
    context['ai_decision'] = decision
    return context

workflow = (
    WorkflowBuilder('ai_workflow', 'AI-Driven Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('ai_analyze', 'AI Analysis', ai_decide)
    .add_decision_node('check_decision', 'Check Decision')
    .add_process_node('approve', 'Approve', lambda c: c)
    .add_process_node('reject', 'Reject', lambda c: c)
    .add_end_node('end', 'End')
    
    .connect('start', 'ai_analyze')
    .connect('ai_analyze', 'check_decision')
    .connect(
        'check_decision', 'approve',
        EdgeCondition(EdgeConditionType.EQUALS, 'ai_decision', 'approve')
    )
    .connect(
        'check_decision', 'reject',
        EdgeCondition(EdgeConditionType.EQUALS, 'ai_decision', 'reject')
    )
    .connect('approve', 'end')
    .connect('reject', 'end')
    .build()
)
```

---

## Extending the System

### Adding Custom Node Types

Extend the NodeType enum:

```python
# In workflow.py, extend NodeType
class NodeType(Enum):
    START = "start"
    PROCESS = "process"
    DECISION = "decision"
    END = "end"
    PARALLEL = "parallel"
    MERGE = "merge"
    # Add custom types
    WEBHOOK = "webhook"
    NOTIFICATION = "notification"
    API_CALL = "api_call"
```

### Adding Custom Conditions

Create custom condition types:

```python
class CustomConditions:
    @staticmethod
    def time_based(context):
        """Condition based on time of day."""
        from datetime import datetime
        hour = datetime.now().hour
        return 9 <= hour <= 17  # Business hours
    
    @staticmethod
    def data_quality(context):
        """Condition based on data quality metrics."""
        quality_score = context.get('quality_score', 0)
        completeness = context.get('completeness', 0)
        return quality_score > 80 and completeness > 95
    
    @staticmethod
    def resource_available(context):
        """Condition based on resource availability."""
        # Check if required resources are available
        return True

# Use custom conditions
condition = EdgeCondition(
    EdgeConditionType.CUSTOM,
    custom_function=CustomConditions.time_based
)
```

### Creating Reusable Workflow Templates

Create templates for common patterns:

```python
class WorkflowTemplates:
    @staticmethod
    def create_approval_workflow(workflow_id, name):
        """Template for approval workflows."""
        return (
            WorkflowBuilder(workflow_id, name)
            .add_start_node('start', 'Start')
            .add_process_node('validate', 'Validate')
            .add_decision_node('check', 'Check')
            .add_process_node('approve', 'Approve')
            .add_process_node('reject', 'Reject')
            .add_end_node('end', 'End')
            # Add standard connections
            .connect('start', 'validate')
            .connect('validate', 'check')
            # Caller adds specific conditions
        )
    
    @staticmethod
    def create_deployment_workflow(workflow_id, name, environment):
        """Template for deployment workflows."""
        return (
            WorkflowBuilder(workflow_id, name, environment)
            .add_start_node('start', 'Start')
            .add_process_node('build', 'Build')
            .add_process_node('test', 'Test')
            .add_process_node('deploy', 'Deploy')
            .add_end_node('end', 'End')
            .connect('start', 'build')
            .connect('build', 'test')
            .connect('test', 'deploy')
            .connect('deploy', 'end')
        )

# Use template
workflow = WorkflowTemplates.create_approval_workflow('approval_001', 'My Approval')
# Add custom logic
workflow.connect('check', 'approve', custom_condition)
workflow = workflow.build()
```

### Adding Middleware

Add middleware for logging, monitoring, or modification:

```python
class WorkflowMiddleware:
    def __init__(self, workflow):
        self.workflow = workflow
        self.original_execute = workflow.execute
        workflow.execute = self._wrapped_execute
    
    def _wrapped_execute(self, initial_context=None, max_iterations=1000):
        """Wrapped execute with middleware."""
        print(f"[MIDDLEWARE] Starting workflow: {self.workflow.workflow_id}")
        
        try:
            result = self.original_execute(initial_context, max_iterations)
            print(f"[MIDDLEWARE] Workflow completed successfully")
            return result
        except Exception as e:
            print(f"[MIDDLEWARE] Workflow failed: {str(e)}")
            raise

# Use middleware
workflow = create_my_workflow()
middleware = WorkflowMiddleware(workflow)
result = workflow.execute()
```

---

## Migration Guide

### From Manual Process Orchestration

If you're currently using manual process orchestration:

```python
# Before: Manual orchestration
def run_process():
    step1()
    if check_condition():
        step2a()
    else:
        step2b()
    step3()

# After: Using workflow system
workflow = (
    WorkflowBuilder('process', 'My Process')
    .add_start_node('start', 'Start')
    .add_process_node('step1', 'Step 1', step1)
    .add_decision_node('check', 'Check')
    .add_process_node('step2a', 'Step 2A', step2a)
    .add_process_node('step2b', 'Step 2B', step2b)
    .add_process_node('step3', 'Step 3', step3)
    .add_end_node('end', 'End')
    .connect('start', 'step1')
    .connect('step1', 'check')
    .connect('check', 'step2a', condition_true)
    .connect('check', 'step2b', condition_false)
    .connect('step2a', 'step3')
    .connect('step2b', 'step3')
    .connect('step3', 'end')
    .build()
)

result = workflow.execute()
```

### From Other Workflow Systems

Key differences and migration tips:

| Feature | Other Systems | PinkFlow Workflow |
|---------|---------------|-------------------|
| Node Definition | YAML/JSON | Python code |
| Conditions | String expressions | Python functions |
| Execution | Background tasks | In-process |
| State | External storage | Context dict |
| Extensions | Plugins | Python code |

---

## Troubleshooting

### Issue: Import Errors

**Problem**: Cannot import workflow modules

**Solution**:
```python
# Add to Python path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'workflow-system'))
```

### Issue: Workflow Validation Fails

**Problem**: Validation errors when building workflow

**Solution**:
```python
# Check validation errors
workflow_builder = WorkflowBuilder('test', 'Test')
# ... add nodes and edges
try:
    workflow = workflow_builder.build()
except ValueError as e:
    print(f"Validation failed: {e}")
```

### Issue: Performance Concerns

**Problem**: Workflows running slowly

**Solutions**:
- Reduce max_iterations
- Optimize node actions
- Use async operations for I/O
- Profile slow operations

```python
import time

def optimized_action(context):
    start = time.time()
    # Your logic here
    duration = time.time() - start
    if duration > 1.0:
        print(f"Warning: Slow operation ({duration:.2f}s)")
    return context
```

---

## Best Practices

### 1. Organize Workflows

```
project/
├── workflows/
│   ├── __init__.py
│   ├── deployment.py
│   ├── data_processing.py
│   └── approval.py
└── workflow-system/
```

### 2. Use Type Hints

```python
from typing import Dict, Any

def my_action(context: Dict[str, Any]) -> Dict[str, Any]:
    context['processed'] = True
    return context
```

### 3. Add Logging

```python
import logging

logger = logging.getLogger(__name__)

def logged_action(context):
    logger.info(f"Processing: {context.get('item_id')}")
    # ... action logic
    return context
```

### 4. Test Workflows

```python
def test_my_workflow():
    workflow = create_my_workflow()
    
    # Test happy path
    result = workflow.execute({'input': 'valid'})
    assert result['completed'] == True
    
    # Test error path
    result = workflow.execute({'input': 'invalid'})
    assert 'error' in result
```

---

**Last Updated**: 2025-11-08  
**Version**: 1.0.0
