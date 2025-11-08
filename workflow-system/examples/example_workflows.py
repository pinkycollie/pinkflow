"""
PinkFlow Workflow System - Example Workflows

This module provides example workflows demonstrating various use cases
and patterns for the PinkFlow workflow system.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.workflow import (
    WorkflowBuilder,
    Environment,
    EdgeCondition,
    EdgeConditionType,
    NodeType
)


def create_development_cycle_workflow():
    """
    Create a complete development cycle workflow.
    
    This workflow demonstrates:
    - Code development
    - Testing
    - Code review
    - Deployment decision based on test results
    """
    
    def start_development(context):
        """Initialize development phase."""
        context['phase'] = 'development'
        context['code_quality'] = 0
        context['tests_passed'] = False
        print(f"[{context['environment']}] Starting development cycle...")
        return context
    
    def write_code(context):
        """Simulate code writing."""
        context['code_quality'] = 85  # Simulated quality score
        print(f"[{context['environment']}] Code written with quality score: {context['code_quality']}")
        return context
    
    def run_tests(context):
        """Run automated tests."""
        # Tests pass if code quality is above 70
        context['tests_passed'] = context.get('code_quality', 0) > 70
        test_status = "PASSED" if context['tests_passed'] else "FAILED"
        print(f"[{context['environment']}] Tests {test_status}")
        return context
    
    def code_review(context):
        """Perform code review."""
        context['review_approved'] = context.get('code_quality', 0) > 75
        review_status = "APPROVED" if context['review_approved'] else "REJECTED"
        print(f"[{context['environment']}] Code review {review_status}")
        return context
    
    def deploy_to_staging(context):
        """Deploy to staging environment."""
        context['deployed_to'] = 'staging'
        print(f"[{context['environment']}] Deployed to staging")
        return context
    
    def fix_issues(context):
        """Fix identified issues."""
        print(f"[{context['environment']}] Fixing issues...")
        context['code_quality'] = min(100, context.get('code_quality', 0) + 20)
        return context
    
    def complete_cycle(context):
        """Complete the development cycle."""
        print(f"[{context['environment']}] Development cycle completed")
        return context
    
    # Build the workflow
    workflow = (
        WorkflowBuilder(
            workflow_id='dev_cycle_001',
            name='Complete Development Cycle',
            environment=Environment.DEVELOPMENT
        )
        .with_description('End-to-end development workflow from code to deployment')
        .with_metadata('version', '1.0.0')
        .with_metadata('owner', 'PinkFlow Team')
        
        # Add nodes
        .add_start_node('start', 'Start Development', start_development)
        .add_process_node('write_code', 'Write Code', write_code)
        .add_process_node('run_tests', 'Run Tests', run_tests)
        .add_decision_node('check_tests', 'Check Test Results')
        .add_process_node('code_review', 'Code Review', code_review)
        .add_decision_node('check_review', 'Check Review')
        .add_process_node('deploy', 'Deploy to Staging', deploy_to_staging)
        .add_process_node('fix_issues', 'Fix Issues', fix_issues)
        .add_end_node('end', 'Complete', complete_cycle)
        
        # Connect nodes with conditional routing
        .connect('start', 'write_code')
        .connect('write_code', 'run_tests')
        .connect('run_tests', 'check_tests')
        
        # If tests pass, go to code review
        .connect(
            'check_tests', 'code_review',
            EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', True),
            priority=10
        )
        
        # If tests fail, fix issues
        .connect(
            'check_tests', 'fix_issues',
            EdgeCondition(EdgeConditionType.EQUALS, 'tests_passed', False),
            priority=5
        )
        
        # After fixing, run tests again
        .connect('fix_issues', 'run_tests')
        
        # After code review, check if approved
        .connect('code_review', 'check_review')
        
        # If approved, deploy
        .connect(
            'check_review', 'deploy',
            EdgeCondition(EdgeConditionType.EQUALS, 'review_approved', True),
            priority=10
        )
        
        # If not approved, fix issues
        .connect(
            'check_review', 'fix_issues',
            EdgeCondition(EdgeConditionType.EQUALS, 'review_approved', False),
            priority=5
        )
        
        # After deployment, complete
        .connect('deploy', 'end')
        
        .build()
    )
    
    return workflow


def create_sandbox_workflow():
    """
    Create a sandbox environment workflow for experimentation.
    
    This workflow is designed for safe experimentation with automatic rollback.
    """
    
    def initialize_sandbox(context):
        """Initialize sandbox environment."""
        context['sandbox_id'] = 'sandbox_001'
        context['experiment_count'] = 0
        print(f"[SANDBOX] Initialized sandbox: {context['sandbox_id']}")
        return context
    
    def run_experiment(context):
        """Run an experiment in sandbox."""
        context['experiment_count'] = context.get('experiment_count', 0) + 1
        context['experiment_success'] = context['experiment_count'] <= 3
        print(f"[SANDBOX] Running experiment #{context['experiment_count']}")
        return context
    
    def validate_results(context):
        """Validate experiment results."""
        context['results_valid'] = context.get('experiment_success', False)
        print(f"[SANDBOX] Results validation: {'VALID' if context['results_valid'] else 'INVALID'}")
        return context
    
    def promote_to_staging(context):
        """Promote successful experiments to staging."""
        print(f"[SANDBOX] Promoting to staging environment")
        context['promoted'] = True
        return context
    
    def rollback_changes(context):
        """Rollback failed experiments."""
        print(f"[SANDBOX] Rolling back changes")
        context['rolled_back'] = True
        return context
    
    def cleanup_sandbox(context):
        """Cleanup sandbox resources."""
        print(f"[SANDBOX] Cleaning up sandbox: {context.get('sandbox_id', 'unknown')}")
        return context
    
    workflow = (
        WorkflowBuilder(
            workflow_id='sandbox_exp_001',
            name='Sandbox Experimentation',
            environment=Environment.SANDBOX
        )
        .with_description('Safe experimentation workflow with automatic rollback')
        
        .add_start_node('init', 'Initialize Sandbox', initialize_sandbox)
        .add_process_node('experiment', 'Run Experiment', run_experiment)
        .add_process_node('validate', 'Validate Results', validate_results)
        .add_decision_node('check_results', 'Check Results')
        .add_process_node('promote', 'Promote to Staging', promote_to_staging)
        .add_process_node('rollback', 'Rollback Changes', rollback_changes)
        .add_process_node('cleanup', 'Cleanup', cleanup_sandbox)
        .add_end_node('end', 'Complete')
        
        .connect('init', 'experiment')
        .connect('experiment', 'validate')
        .connect('validate', 'check_results')
        
        # If results are valid, promote
        .connect(
            'check_results', 'promote',
            EdgeCondition(EdgeConditionType.EQUALS, 'results_valid', True)
        )
        
        # If results are invalid, rollback
        .connect(
            'check_results', 'rollback',
            EdgeCondition(EdgeConditionType.EQUALS, 'results_valid', False)
        )
        
        .connect('promote', 'cleanup')
        .connect('rollback', 'cleanup')
        .connect('cleanup', 'end')
        
        .build()
    )
    
    return workflow


def create_staging_deployment_workflow():
    """
    Create a staging deployment workflow with quality gates.
    
    This workflow includes:
    - Pre-deployment checks
    - Deployment to staging
    - Smoke tests
    - Decision to promote to production
    """
    
    def pre_deployment_checks(context):
        """Run pre-deployment checks."""
        context['checks_passed'] = True
        context['security_scan'] = 'passed'
        context['dependencies'] = 'up_to_date'
        print(f"[STAGING] Pre-deployment checks completed")
        return context
    
    def deploy_to_staging(context):
        """Deploy to staging environment."""
        print(f"[STAGING] Deploying to staging environment")
        context['staging_url'] = 'https://staging.pinkflow.dev'
        context['deployed'] = True
        return context
    
    def run_smoke_tests(context):
        """Run smoke tests."""
        context['smoke_tests_passed'] = True
        print(f"[STAGING] Smoke tests completed")
        return context
    
    def performance_tests(context):
        """Run performance tests."""
        context['performance_score'] = 92
        context['performance_acceptable'] = context['performance_score'] > 80
        print(f"[STAGING] Performance score: {context['performance_score']}")
        return context
    
    def ready_for_production(context):
        """Mark as ready for production."""
        context['production_ready'] = True
        print(f"[STAGING] Approved for production deployment")
        return context
    
    def requires_tuning(context):
        """Mark as requiring tuning."""
        context['needs_tuning'] = True
        print(f"[STAGING] Requires performance tuning")
        return context
    
    workflow = (
        WorkflowBuilder(
            workflow_id='staging_deploy_001',
            name='Staging Deployment with Quality Gates',
            environment=Environment.STAGING
        )
        .with_description('Staging deployment workflow with automated quality gates')
        
        .add_start_node('start', 'Start Deployment')
        .add_process_node('pre_checks', 'Pre-deployment Checks', pre_deployment_checks)
        .add_process_node('deploy', 'Deploy to Staging', deploy_to_staging)
        .add_process_node('smoke_tests', 'Smoke Tests', run_smoke_tests)
        .add_process_node('perf_tests', 'Performance Tests', performance_tests)
        .add_decision_node('check_performance', 'Check Performance')
        .add_process_node('prod_ready', 'Production Ready', ready_for_production)
        .add_process_node('needs_tuning', 'Needs Tuning', requires_tuning)
        .add_end_node('end', 'Complete')
        
        .connect('start', 'pre_checks')
        .connect('pre_checks', 'deploy')
        .connect('deploy', 'smoke_tests')
        .connect('smoke_tests', 'perf_tests')
        .connect('perf_tests', 'check_performance')
        
        .connect(
            'check_performance', 'prod_ready',
            EdgeCondition(EdgeConditionType.EQUALS, 'performance_acceptable', True)
        )
        
        .connect(
            'check_performance', 'needs_tuning',
            EdgeCondition(EdgeConditionType.EQUALS, 'performance_acceptable', False)
        )
        
        .connect('prod_ready', 'end')
        .connect('needs_tuning', 'end')
        
        .build()
    )
    
    return workflow


def create_production_deployment_workflow():
    """
    Create a production deployment workflow with strict controls.
    
    This workflow includes:
    - Multiple approval gates
    - Canary deployment
    - Monitoring and validation
    - Automatic rollback on failure
    """
    
    def verify_approvals(context):
        """Verify all required approvals."""
        context['approvals'] = ['tech_lead', 'security', 'product_owner']
        context['all_approved'] = len(context['approvals']) >= 3
        print(f"[PRODUCTION] Approvals verified: {context['approvals']}")
        return context
    
    def backup_current_state(context):
        """Backup current production state."""
        context['backup_id'] = 'backup_20250108_001'
        print(f"[PRODUCTION] Created backup: {context['backup_id']}")
        return context
    
    def canary_deployment(context):
        """Deploy to canary instances (10% traffic)."""
        context['canary_deployed'] = True
        context['canary_traffic_percent'] = 10
        print(f"[PRODUCTION] Canary deployment: {context['canary_traffic_percent']}% traffic")
        return context
    
    def monitor_canary(context):
        """Monitor canary deployment."""
        context['canary_error_rate'] = 0.5  # 0.5% error rate
        context['canary_healthy'] = context['canary_error_rate'] < 1.0
        print(f"[PRODUCTION] Canary error rate: {context['canary_error_rate']}%")
        return context
    
    def full_deployment(context):
        """Deploy to all production instances."""
        context['deployment_complete'] = True
        print(f"[PRODUCTION] Full deployment completed")
        return context
    
    def rollback_deployment(context):
        """Rollback to previous version."""
        print(f"[PRODUCTION] Rolling back to backup: {context.get('backup_id', 'unknown')}")
        context['rolled_back'] = True
        return context
    
    def notify_success(context):
        """Send success notifications."""
        print(f"[PRODUCTION] Deployment successful - notifications sent")
        return context
    
    def notify_failure(context):
        """Send failure notifications."""
        print(f"[PRODUCTION] Deployment failed - notifications sent")
        return context
    
    workflow = (
        WorkflowBuilder(
            workflow_id='prod_deploy_001',
            name='Production Deployment with Canary',
            environment=Environment.PRODUCTION
        )
        .with_description('Production deployment with canary and automatic rollback')
        
        .add_start_node('start', 'Start Production Deployment')
        .add_process_node('verify', 'Verify Approvals', verify_approvals)
        .add_process_node('backup', 'Backup Current State', backup_current_state)
        .add_process_node('canary', 'Canary Deployment', canary_deployment)
        .add_process_node('monitor', 'Monitor Canary', monitor_canary)
        .add_decision_node('check_canary', 'Check Canary Health')
        .add_process_node('full_deploy', 'Full Deployment', full_deployment)
        .add_process_node('rollback', 'Rollback', rollback_deployment)
        .add_process_node('success', 'Notify Success', notify_success)
        .add_process_node('failure', 'Notify Failure', notify_failure)
        .add_end_node('end', 'Complete')
        
        .connect('start', 'verify')
        .connect('verify', 'backup')
        .connect('backup', 'canary')
        .connect('canary', 'monitor')
        .connect('monitor', 'check_canary')
        
        .connect(
            'check_canary', 'full_deploy',
            EdgeCondition(EdgeConditionType.EQUALS, 'canary_healthy', True)
        )
        
        .connect(
            'check_canary', 'rollback',
            EdgeCondition(EdgeConditionType.EQUALS, 'canary_healthy', False)
        )
        
        .connect('full_deploy', 'success')
        .connect('rollback', 'failure')
        .connect('success', 'end')
        .connect('failure', 'end')
        
        .build()
    )
    
    return workflow


def main():
    """
    Main function to demonstrate example workflows.
    """
    print("=" * 80)
    print("PinkFlow Workflow System - Example Workflows")
    print("=" * 80)
    print()
    
    # Create workflows
    dev_workflow = create_development_cycle_workflow()
    sandbox_workflow = create_sandbox_workflow()
    staging_workflow = create_staging_deployment_workflow()
    prod_workflow = create_production_deployment_workflow()
    
    workflows = [dev_workflow, sandbox_workflow, staging_workflow, prod_workflow]
    
    # Execute each workflow
    for workflow in workflows:
        print(f"\n{'=' * 80}")
        print(f"Executing: {workflow.name}")
        print(f"Environment: {workflow.environment.value}")
        print(f"Description: {workflow.description}")
        print(f"{'=' * 80}\n")
        
        try:
            result = workflow.execute()
            print(f"\n✓ Workflow completed successfully")
            print(f"  - Iterations: {result.get('iterations', 0)}")
            print(f"  - Path: {' → '.join(result.get('execution_path', []))}")
            print(f"  - Status: {result.get('execution_status', 'unknown')}")
        except Exception as e:
            print(f"\n✗ Workflow failed: {str(e)}")
    
    print(f"\n{'=' * 80}")
    print("All workflows completed")
    print(f"{'=' * 80}")


if __name__ == '__main__':
    main()
