# Workflow System Examples

Practical examples and use cases for the PinkFlow Workflow System.

---

## Table of Contents

- [Basic Examples](#basic-examples)
- [Conditional Routing Examples](#conditional-routing-examples)
- [Environment-Specific Examples](#environment-specific-examples)
- [Real-World Scenarios](#real-world-scenarios)
- [Advanced Patterns](#advanced-patterns)

---

## Basic Examples

### Example 1: Simple Linear Workflow

The simplest workflow with sequential steps:

```python
from core.workflow import WorkflowBuilder, Environment

def step_one(context):
    print("Executing step 1")
    context['step1_done'] = True
    return context

def step_two(context):
    print("Executing step 2")
    context['step2_done'] = True
    return context

workflow = (
    WorkflowBuilder('simple_001', 'Simple Linear Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('step1', 'Step 1', step_one)
    .add_process_node('step2', 'Step 2', step_two)
    .add_end_node('end', 'End')
    .connect('start', 'step1')
    .connect('step1', 'step2')
    .connect('step2', 'end')
    .build()
)

result = workflow.execute()
print(f"Path: {' → '.join(result['execution_path'])}")
```

**Output:**
```
Executing step 1
Executing step 2
Path: start → step1 → step2 → end
```

---

### Example 2: Simple Decision Workflow

Workflow with a basic decision point:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def check_value(context):
    context['value'] = 75  # Simulated value
    return context

def handle_high(context):
    print("Value is high")
    return context

def handle_low(context):
    print("Value is low")
    return context

workflow = (
    WorkflowBuilder('decision_001', 'Decision Workflow')
    .add_start_node('start', 'Start')
    .add_process_node('check', 'Check Value', check_value)
    .add_decision_node('decide', 'Decision Point')
    .add_process_node('high', 'Handle High', handle_high)
    .add_process_node('low', 'Handle Low', handle_low)
    .add_end_node('end', 'End')
    
    .connect('start', 'check')
    .connect('check', 'decide')
    .connect(
        'decide', 'high',
        EdgeCondition(EdgeConditionType.GREATER_THAN, 'value', 50)
    )
    .connect(
        'decide', 'low',
        EdgeCondition(EdgeConditionType.LESS_THAN, 'value', 50)
    )
    .connect('high', 'end')
    .connect('low', 'end')
    .build()
)

result = workflow.execute()
```

---

## Conditional Routing Examples

### Example 3: Multiple Conditions

Workflow with multiple conditional paths:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def evaluate_score(context):
    context['score'] = 85
    context['approved'] = True
    return context

workflow = (
    WorkflowBuilder('multi_cond_001', 'Multiple Conditions')
    .add_start_node('start', 'Start')
    .add_process_node('evaluate', 'Evaluate', evaluate_score)
    .add_decision_node('check', 'Check Conditions')
    .add_process_node('excellent', 'Excellent Path', lambda c: c)
    .add_process_node('good', 'Good Path', lambda c: c)
    .add_process_node('poor', 'Poor Path', lambda c: c)
    .add_end_node('end', 'End')
    
    .connect('start', 'evaluate')
    .connect('evaluate', 'check')
    
    # Excellent: score >= 90 and approved
    .connect(
        'check', 'excellent',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('score', 0) >= 90 and c.get('approved', False)
        ),
        priority=10
    )
    
    # Good: score >= 70 and approved
    .connect(
        'check', 'good',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('score', 0) >= 70 and c.get('approved', False)
        ),
        priority=5
    )
    
    # Poor: everything else
    .connect('check', 'poor', priority=1)
    
    .connect('excellent', 'end')
    .connect('good', 'end')
    .connect('poor', 'end')
    .build()
)
```

---

### Example 4: Loop with Exit Condition

Workflow that loops until a condition is met:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def initialize(context):
    context['counter'] = 0
    context['target'] = 3
    return context

def increment(context):
    context['counter'] = context.get('counter', 0) + 1
    print(f"Counter: {context['counter']}")
    return context

workflow = (
    WorkflowBuilder('loop_001', 'Loop Workflow')
    .add_start_node('start', 'Start', initialize)
    .add_process_node('increment', 'Increment', increment)
    .add_decision_node('check', 'Check Counter')
    .add_end_node('end', 'End')
    
    .connect('start', 'increment')
    .connect('increment', 'check')
    
    # If counter < target, loop back
    .connect(
        'check', 'increment',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('counter', 0) < c.get('target', 0)
        )
    )
    
    # If counter >= target, end
    .connect(
        'check', 'end',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('counter', 0) >= c.get('target', 0)
        )
    )
    .build()
)

result = workflow.execute()
print(f"Final counter: {result['counter']}")
```

---

## Environment-Specific Examples

### Example 5: Environment-Based Configuration

Workflow that behaves differently per environment:

```python
from core.workflow import WorkflowBuilder, Environment, WorkflowManager

def deploy(context):
    env = context.get('environment', 'development')
    
    if env == 'sandbox':
        print("Deploying to sandbox with debug enabled")
        context['debug'] = True
        context['replicas'] = 1
    elif env == 'staging':
        print("Deploying to staging with monitoring")
        context['debug'] = False
        context['replicas'] = 2
    elif env == 'production':
        print("Deploying to production with full redundancy")
        context['debug'] = False
        context['replicas'] = 5
    
    return context

# Create environment-specific workflows
manager = WorkflowManager()

for env in [Environment.SANDBOX, Environment.STAGING, Environment.PRODUCTION]:
    workflow = (
        WorkflowBuilder(f'deploy_{env.value}', f'Deploy to {env.value}', env)
        .add_start_node('start', 'Start')
        .add_process_node('deploy', 'Deploy', deploy)
        .add_end_node('end', 'End')
        .connect('start', 'deploy')
        .connect('deploy', 'end')
        .build()
    )
    manager.register_workflow(workflow)

# Execute for each environment
for env in [Environment.SANDBOX, Environment.STAGING, Environment.PRODUCTION]:
    print(f"\n=== {env.value.upper()} ===")
    result = manager.execute_workflow(f'deploy_{env.value}')
    print(f"Replicas: {result.get('replicas')}")
```

---

## Real-World Scenarios

### Example 6: CI/CD Pipeline

Complete CI/CD pipeline workflow:

```python
from core.workflow import WorkflowBuilder, Environment, EdgeCondition, EdgeConditionType

def checkout_code(context):
    print("Checking out code from repository")
    context['code_checked_out'] = True
    return context

def build(context):
    print("Building application")
    context['build_success'] = True
    return context

def run_unit_tests(context):
    print("Running unit tests")
    context['unit_tests_passed'] = True
    return context

def run_integration_tests(context):
    print("Running integration tests")
    context['integration_tests_passed'] = True
    return context

def security_scan(context):
    print("Running security scan")
    context['security_passed'] = True
    return context

def deploy_staging(context):
    print("Deploying to staging")
    context['staging_deployed'] = True
    return context

def manual_approval(context):
    print("Waiting for manual approval...")
    context['approved'] = True
    return context

def deploy_production(context):
    print("Deploying to production")
    context['production_deployed'] = True
    return context

def notify_failure(context):
    print("Notifying team of failure")
    return context

workflow = (
    WorkflowBuilder('cicd_001', 'CI/CD Pipeline', Environment.STAGING)
    .with_description('Complete CI/CD pipeline with testing and deployment')
    
    .add_start_node('start', 'Start Pipeline')
    .add_process_node('checkout', 'Checkout Code', checkout_code)
    .add_process_node('build', 'Build', build)
    .add_decision_node('check_build', 'Check Build')
    .add_process_node('unit_tests', 'Unit Tests', run_unit_tests)
    .add_decision_node('check_unit', 'Check Unit Tests')
    .add_process_node('integration_tests', 'Integration Tests', run_integration_tests)
    .add_decision_node('check_integration', 'Check Integration Tests')
    .add_process_node('security', 'Security Scan', security_scan)
    .add_decision_node('check_security', 'Check Security')
    .add_process_node('deploy_stg', 'Deploy Staging', deploy_staging)
    .add_process_node('approval', 'Manual Approval', manual_approval)
    .add_decision_node('check_approval', 'Check Approval')
    .add_process_node('deploy_prod', 'Deploy Production', deploy_production)
    .add_process_node('notify_fail', 'Notify Failure', notify_failure)
    .add_end_node('success', 'Success')
    .add_end_node('failure', 'Failure')
    
    # Build flow
    .connect('start', 'checkout')
    .connect('checkout', 'build')
    .connect('build', 'check_build')
    .connect(
        'check_build', 'unit_tests',
        EdgeCondition(EdgeConditionType.EQUALS, 'build_success', True)
    )
    .connect(
        'check_build', 'notify_fail',
        EdgeCondition(EdgeConditionType.EQUALS, 'build_success', False)
    )
    
    # Test flow
    .connect('unit_tests', 'check_unit')
    .connect(
        'check_unit', 'integration_tests',
        EdgeCondition(EdgeConditionType.EQUALS, 'unit_tests_passed', True)
    )
    .connect(
        'check_unit', 'notify_fail',
        EdgeCondition(EdgeConditionType.EQUALS, 'unit_tests_passed', False)
    )
    
    .connect('integration_tests', 'check_integration')
    .connect(
        'check_integration', 'security',
        EdgeCondition(EdgeConditionType.EQUALS, 'integration_tests_passed', True)
    )
    .connect(
        'check_integration', 'notify_fail',
        EdgeCondition(EdgeConditionType.EQUALS, 'integration_tests_passed', False)
    )
    
    # Security and deployment flow
    .connect('security', 'check_security')
    .connect(
        'check_security', 'deploy_stg',
        EdgeCondition(EdgeConditionType.EQUALS, 'security_passed', True)
    )
    .connect(
        'check_security', 'notify_fail',
        EdgeCondition(EdgeConditionType.EQUALS, 'security_passed', False)
    )
    
    .connect('deploy_stg', 'approval')
    .connect('approval', 'check_approval')
    .connect(
        'check_approval', 'deploy_prod',
        EdgeCondition(EdgeConditionType.EQUALS, 'approved', True)
    )
    .connect(
        'check_approval', 'failure',
        EdgeCondition(EdgeConditionType.EQUALS, 'approved', False)
    )
    
    .connect('deploy_prod', 'success')
    .connect('notify_fail', 'failure')
    .build()
)

result = workflow.execute()
print(f"\nPipeline result: {result.get('production_deployed', False)}")
```

---

### Example 7: Data Processing Pipeline

Data processing with validation and error handling:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def load_data(context):
    print("Loading data from source")
    context['data_loaded'] = True
    context['record_count'] = 1000
    return context

def validate_data(context):
    print("Validating data")
    context['data_valid'] = context.get('record_count', 0) > 0
    return context

def transform_data(context):
    print("Transforming data")
    context['data_transformed'] = True
    return context

def enrich_data(context):
    print("Enriching data")
    context['data_enriched'] = True
    return context

def save_data(context):
    print("Saving processed data")
    context['data_saved'] = True
    return context

def handle_error(context):
    print("Handling data error")
    context['error_handled'] = True
    return context

workflow = (
    WorkflowBuilder('data_pipeline_001', 'Data Processing Pipeline')
    .add_start_node('start', 'Start')
    .add_process_node('load', 'Load Data', load_data)
    .add_process_node('validate', 'Validate Data', validate_data)
    .add_decision_node('check_valid', 'Check Validity')
    .add_process_node('transform', 'Transform Data', transform_data)
    .add_process_node('enrich', 'Enrich Data', enrich_data)
    .add_process_node('save', 'Save Data', save_data)
    .add_process_node('error', 'Handle Error', handle_error)
    .add_end_node('success', 'Success')
    .add_end_node('failure', 'Failure')
    
    .connect('start', 'load')
    .connect('load', 'validate')
    .connect('validate', 'check_valid')
    .connect(
        'check_valid', 'transform',
        EdgeCondition(EdgeConditionType.EQUALS, 'data_valid', True)
    )
    .connect(
        'check_valid', 'error',
        EdgeCondition(EdgeConditionType.EQUALS, 'data_valid', False)
    )
    .connect('transform', 'enrich')
    .connect('enrich', 'save')
    .connect('save', 'success')
    .connect('error', 'failure')
    .build()
)
```

---

## Advanced Patterns

### Example 8: Retry Logic

Workflow with automatic retry on failure:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def initialize(context):
    context['max_retries'] = 3
    context['retry_count'] = 0
    return context

def risky_operation(context):
    retry_count = context.get('retry_count', 0)
    # Simulate success on 3rd try
    success = retry_count >= 2
    
    print(f"Attempt {retry_count + 1}: {'Success' if success else 'Failed'}")
    context['operation_success'] = success
    return context

def increment_retry(context):
    context['retry_count'] = context.get('retry_count', 0) + 1
    return context

workflow = (
    WorkflowBuilder('retry_001', 'Retry Pattern')
    .add_start_node('start', 'Start', initialize)
    .add_process_node('operation', 'Risky Operation', risky_operation)
    .add_decision_node('check_result', 'Check Result')
    .add_process_node('retry', 'Increment Retry', increment_retry)
    .add_decision_node('check_retries', 'Check Retry Count')
    .add_end_node('success', 'Success')
    .add_end_node('failure', 'Max Retries Exceeded')
    
    .connect('start', 'operation')
    .connect('operation', 'check_result')
    
    # If successful, end
    .connect(
        'check_result', 'success',
        EdgeCondition(EdgeConditionType.EQUALS, 'operation_success', True)
    )
    
    # If failed, check retry count
    .connect(
        'check_result', 'check_retries',
        EdgeCondition(EdgeConditionType.EQUALS, 'operation_success', False)
    )
    
    # If retries available, retry
    .connect(
        'check_retries', 'retry',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('retry_count', 0) < c.get('max_retries', 0)
        )
    )
    
    # If max retries reached, fail
    .connect(
        'check_retries', 'failure',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('retry_count', 0) >= c.get('max_retries', 0)
        )
    )
    
    # Retry loop
    .connect('retry', 'operation')
    .build()
)

result = workflow.execute()
print(f"Final result: {'Success' if result.get('operation_success') else 'Failure'}")
print(f"Total attempts: {result.get('retry_count', 0) + 1}")
```

---

### Example 9: Feature Flags

Workflow with feature flag-based routing:

```python
from core.workflow import WorkflowBuilder, EdgeCondition, EdgeConditionType

def initialize(context):
    # Simulate feature flags
    context['feature_flags'] = {
        'use_new_algorithm': True,
        'enable_caching': True,
        'send_notifications': False
    }
    return context

def new_algorithm(context):
    print("Using new algorithm")
    context['algorithm'] = 'new'
    return context

def old_algorithm(context):
    print("Using old algorithm")
    context['algorithm'] = 'old'
    return context

def with_cache(context):
    print("Using cached results")
    return context

def without_cache(context):
    print("Computing fresh results")
    return context

workflow = (
    WorkflowBuilder('feature_flags_001', 'Feature Flags Pattern')
    .add_start_node('start', 'Start', initialize)
    .add_decision_node('check_algorithm', 'Check Algorithm Flag')
    .add_process_node('new_algo', 'New Algorithm', new_algorithm)
    .add_process_node('old_algo', 'Old Algorithm', old_algorithm)
    .add_decision_node('check_cache', 'Check Cache Flag')
    .add_process_node('with_cache', 'With Cache', with_cache)
    .add_process_node('no_cache', 'Without Cache', without_cache)
    .add_end_node('end', 'End')
    
    .connect('start', 'check_algorithm')
    .connect(
        'check_algorithm', 'new_algo',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('feature_flags', {}).get('use_new_algorithm', False)
        )
    )
    .connect(
        'check_algorithm', 'old_algo',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: not c.get('feature_flags', {}).get('use_new_algorithm', False)
        )
    )
    
    .connect('new_algo', 'check_cache')
    .connect('old_algo', 'check_cache')
    .connect(
        'check_cache', 'with_cache',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: c.get('feature_flags', {}).get('enable_caching', False)
        )
    )
    .connect(
        'check_cache', 'no_cache',
        EdgeCondition(
            EdgeConditionType.CUSTOM,
            custom_function=lambda c: not c.get('feature_flags', {}).get('enable_caching', False)
        )
    )
    
    .connect('with_cache', 'end')
    .connect('no_cache', 'end')
    .build()
)

result = workflow.execute()
```

---

## Running the Examples

To run any example:

1. Save the example code to a Python file
2. Ensure the workflow system is in your Python path
3. Run the file:

```bash
python your_example.py
```

Or run the built-in examples:

```bash
cd workflow-system
python examples/example_workflows.py
```

---

**Last Updated**: 2025-11-08
