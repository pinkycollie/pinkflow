"""
Simple tests to verify the workflow system functionality.
Run with: python3 test_workflow.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow import (
    WorkflowBuilder,
    Environment,
    EdgeCondition,
    EdgeConditionType,
    NodeType
)
from core.workflow_manager import WorkflowManager


def test_simple_workflow():
    """Test a simple linear workflow."""
    print("Testing simple workflow...")
    
    def action(context):
        context['executed'] = True
        return context
    
    workflow = (
        WorkflowBuilder('test_001', 'Test Workflow')
        .add_start_node('start', 'Start')
        .add_process_node('process', 'Process', action)
        .add_end_node('end', 'End')
        .connect('start', 'process')
        .connect('process', 'end')
        .build()
    )
    
    result = workflow.execute()
    
    assert result['completed'] == True
    assert result['executed'] == True
    assert 'start' in result['execution_path']
    assert 'process' in result['execution_path']
    assert 'end' in result['execution_path']
    
    print("✓ Simple workflow test passed")


def test_conditional_workflow():
    """Test workflow with conditional routing."""
    print("Testing conditional workflow...")
    
    def set_value(context):
        context['value'] = 75
        return context
    
    def high_path(context):
        context['path'] = 'high'
        return context
    
    def low_path(context):
        context['path'] = 'low'
        return context
    
    workflow = (
        WorkflowBuilder('test_002', 'Conditional Test')
        .add_start_node('start', 'Start')
        .add_process_node('set_value', 'Set Value', set_value)
        .add_decision_node('decide', 'Decide')
        .add_process_node('high', 'High Path', high_path)
        .add_process_node('low', 'Low Path', low_path)
        .add_end_node('end', 'End')
        
        .connect('start', 'set_value')
        .connect('set_value', 'decide')
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
    
    assert result['completed'] == True
    assert result['value'] == 75
    assert result['path'] == 'high'
    assert 'high' in result['execution_path']
    assert 'low' not in result['execution_path']
    
    print("✓ Conditional workflow test passed")


def test_environment_workflow():
    """Test workflows with different environments."""
    print("Testing environment-specific workflows...")
    
    def check_env(context):
        context['env_checked'] = context['environment']
        return context
    
    for env in [Environment.SANDBOX, Environment.STAGING, Environment.PRODUCTION]:
        workflow = (
            WorkflowBuilder(f'env_test_{env.value}', f'Env Test {env.value}', env)
            .add_start_node('start', 'Start')
            .add_process_node('check', 'Check Env', check_env)
            .add_end_node('end', 'End')
            .connect('start', 'check')
            .connect('check', 'end')
            .build()
        )
        
        result = workflow.execute()
        
        assert result['completed'] == True
        assert result['environment'] == env.value
        assert result['env_checked'] == env.value
    
    print("✓ Environment workflow test passed")


def test_workflow_manager():
    """Test workflow manager functionality."""
    print("Testing workflow manager...")
    
    manager = WorkflowManager()
    
    workflow = (
        WorkflowBuilder('manager_test', 'Manager Test')
        .add_start_node('start', 'Start')
        .add_end_node('end', 'End')
        .connect('start', 'end')
        .build()
    )
    
    # Register workflow
    manager.register_workflow(workflow)
    
    # Execute workflow
    result = manager.execute_workflow('manager_test')
    
    assert result['completed'] == True
    
    # Check execution history
    history = manager.get_execution_history('manager_test')
    assert len(history) == 1
    assert history[0]['workflow_id'] == 'manager_test'
    assert history[0]['status'] == 'success'
    
    # Get statistics
    stats = manager.get_statistics()
    assert stats['total_workflows'] == 1
    assert stats['total_executions'] == 1
    assert stats['successful_executions'] == 1
    
    print("✓ Workflow manager test passed")


def test_custom_condition():
    """Test custom condition functionality."""
    print("Testing custom conditions...")
    
    def complex_condition(context):
        return (
            context.get('score', 0) > 80 and
            context.get('approved', False) == True
        )
    
    def set_values(context):
        context['score'] = 90
        context['approved'] = True
        return context
    
    workflow = (
        WorkflowBuilder('custom_cond_test', 'Custom Condition Test')
        .add_start_node('start', 'Start')
        .add_process_node('set_values', 'Set Values', set_values)
        .add_decision_node('check', 'Check')
        .add_process_node('success', 'Success', lambda c: {**c, 'result': 'success'})
        .add_process_node('failure', 'Failure', lambda c: {**c, 'result': 'failure'})
        .add_end_node('end', 'End')
        
        .connect('start', 'set_values')
        .connect('set_values', 'check')
        .connect(
            'check', 'success',
            EdgeCondition(EdgeConditionType.CUSTOM, custom_function=complex_condition)
        )
        .connect(
            'check', 'failure',
            EdgeCondition(
                EdgeConditionType.CUSTOM,
                custom_function=lambda c: not complex_condition(c)
            )
        )
        .connect('success', 'end')
        .connect('failure', 'end')
        .build()
    )
    
    result = workflow.execute()
    
    assert result['completed'] == True
    assert result['result'] == 'success'
    
    print("✓ Custom condition test passed")


def test_workflow_validation():
    """Test workflow validation."""
    print("Testing workflow validation...")
    
    # Test valid workflow
    workflow = (
        WorkflowBuilder('valid_test', 'Valid Test')
        .add_start_node('start', 'Start')
        .add_end_node('end', 'End')
        .connect('start', 'end')
        .build()
    )
    
    errors = workflow.validate()
    assert len(errors) == 0
    
    # Test invalid workflow (no start node)
    try:
        workflow = (
            WorkflowBuilder('invalid_test', 'Invalid Test')
            .add_end_node('end', 'End')
            .build()
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "start node" in str(e).lower()
    
    print("✓ Workflow validation test passed")


def test_workflow_export():
    """Test workflow export to JSON."""
    print("Testing workflow export...")
    
    workflow = (
        WorkflowBuilder('export_test', 'Export Test', Environment.STAGING)
        .with_description('Test workflow export')
        .with_metadata('version', '1.0')
        .add_start_node('start', 'Start')
        .add_process_node('process', 'Process')
        .add_end_node('end', 'End')
        .connect('start', 'process')
        .connect('process', 'end')
        .build()
    )
    
    # Export to dict
    data = workflow.to_dict()
    assert data['workflow_id'] == 'export_test'
    assert data['name'] == 'Export Test'
    assert data['environment'] == 'staging'
    assert data['description'] == 'Test workflow export'
    assert data['metadata']['version'] == '1.0'
    assert len(data['nodes']) == 3
    assert len(data['edges']) == 2
    
    # Export to JSON
    json_str = workflow.to_json()
    assert 'export_test' in json_str
    assert 'staging' in json_str
    
    print("✓ Workflow export test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("Running Workflow System Tests")
    print("=" * 80)
    print()
    
    tests = [
        test_simple_workflow,
        test_conditional_workflow,
        test_environment_workflow,
        test_workflow_manager,
        test_custom_condition,
        test_workflow_validation,
        test_workflow_export,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            failed += 1
        print()
    
    print("=" * 80)
    if failed == 0:
        print(f"All {len(tests)} tests passed! ✓")
    else:
        print(f"{failed} of {len(tests)} tests failed ✗")
    print("=" * 80)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
