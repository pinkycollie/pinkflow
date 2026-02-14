"""
PinkFlow Workflow System - Workflow Manager

This module provides the workflow management system for registering, executing,
and managing multiple workflows across different environments.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path

from .workflow import Workflow, Environment


class WorkflowRegistry:
    """
    Registry for managing multiple workflows.
    
    Provides functionality to register, retrieve, and manage workflow instances
    across different environments and use cases.
    """
    
    def __init__(self):
        """Initialize a new workflow registry."""
        self.workflows: Dict[str, Workflow] = {}
        self.execution_history: List[Dict[str, Any]] = []
    
    def register(self, workflow: Workflow) -> None:
        """
        Register a workflow in the registry.
        
        Args:
            workflow: Workflow to register
            
        Raises:
            ValueError: If workflow with same ID already registered
        """
        if workflow.workflow_id in self.workflows:
            raise ValueError(f"Workflow '{workflow.workflow_id}' is already registered")
        
        # Validate workflow before registration
        errors = workflow.validate()
        if errors:
            raise ValueError(f"Cannot register invalid workflow: {'; '.join(errors)}")
        
        self.workflows[workflow.workflow_id] = workflow
    
    def unregister(self, workflow_id: str) -> None:
        """
        Unregister a workflow from the registry.
        
        Args:
            workflow_id: ID of workflow to unregister
        """
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
    
    def get(self, workflow_id: str) -> Optional[Workflow]:
        """
        Retrieve a workflow by ID.
        
        Args:
            workflow_id: ID of workflow to retrieve
            
        Returns:
            Workflow instance or None if not found
        """
        return self.workflows.get(workflow_id)
    
    def list(self, environment: Optional[Environment] = None) -> List[Workflow]:
        """
        List all registered workflows, optionally filtered by environment.
        
        Args:
            environment: Optional environment filter
            
        Returns:
            List of workflows
        """
        if environment:
            return [w for w in self.workflows.values() if w.environment == environment]
        return list(self.workflows.values())
    
    def execute(
        self,
        workflow_id: str,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a registered workflow.
        
        Args:
            workflow_id: ID of workflow to execute
            initial_context: Initial execution context
            
        Returns:
            Final execution context
            
        Raises:
            ValueError: If workflow not found
        """
        workflow = self.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        execution_start = datetime.now()
        
        try:
            result = workflow.execute(initial_context)
            result['execution_status'] = 'success'
        except Exception as e:
            result = {
                'execution_status': 'failed',
                'error': str(e),
                'workflow_id': workflow_id
            }
        
        execution_end = datetime.now()
        
        # Record execution history
        self.execution_history.append({
            'workflow_id': workflow_id,
            'started_at': execution_start.isoformat(),
            'completed_at': execution_end.isoformat(),
            'duration_seconds': (execution_end - execution_start).total_seconds(),
            'status': result.get('execution_status', 'unknown'),
            'environment': workflow.environment.value
        })
        
        return result
    
    def get_execution_history(
        self,
        workflow_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get execution history for workflows.
        
        Args:
            workflow_id: Optional workflow ID to filter by
            limit: Maximum number of records to return
            
        Returns:
            List of execution records
        """
        history = self.execution_history
        
        if workflow_id:
            history = [h for h in history if h['workflow_id'] == workflow_id]
        
        return history[-limit:]
    
    def export_workflows(self, filepath: Path) -> None:
        """
        Export all workflows to a JSON file.
        
        Args:
            filepath: Path to save the JSON file
        """
        data = {
            'workflows': [w.to_dict() for w in self.workflows.values()],
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear(self) -> None:
        """Clear all workflows from the registry."""
        self.workflows.clear()


class WorkflowManager:
    """
    High-level workflow management interface.
    
    Provides convenience methods for managing workflows across different
    environments and development stages.
    """
    
    def __init__(self):
        """Initialize a new workflow manager."""
        self.registry = WorkflowRegistry()
        self.environment_configs: Dict[Environment, Dict[str, Any]] = {
            Environment.SANDBOX: {
                'max_iterations': 100,
                'timeout_seconds': 60,
                'auto_rollback': True
            },
            Environment.STAGING: {
                'max_iterations': 500,
                'timeout_seconds': 300,
                'auto_rollback': True
            },
            Environment.PRODUCTION: {
                'max_iterations': 1000,
                'timeout_seconds': 600,
                'auto_rollback': False
            },
            Environment.DEVELOPMENT: {
                'max_iterations': 50,
                'timeout_seconds': 30,
                'auto_rollback': True
            }
        }
    
    def register_workflow(self, workflow: Workflow) -> None:
        """
        Register a workflow with the manager.
        
        Args:
            workflow: Workflow to register
        """
        self.registry.register(workflow)
    
    def execute_workflow(
        self,
        workflow_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
        override_environment: Optional[Environment] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow with environment-specific configurations.
        
        Args:
            workflow_id: ID of workflow to execute
            initial_context: Initial execution context
            override_environment: Optional environment override
            
        Returns:
            Final execution context
        """
        workflow = self.registry.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        # Determine environment
        environment = override_environment or workflow.environment
        config = self.environment_configs.get(environment, {})
        
        # Merge environment config into context
        context = initial_context or {}
        context['environment_config'] = config
        
        return self.registry.execute(workflow_id, context)
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID."""
        return self.registry.get(workflow_id)
    
    def list_workflows(self, environment: Optional[Environment] = None) -> List[Workflow]:
        """List all workflows, optionally filtered by environment."""
        return self.registry.list(environment)
    
    def get_execution_history(
        self,
        workflow_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.registry.get_execution_history(workflow_id)
    
    def configure_environment(
        self,
        environment: Environment,
        config: Dict[str, Any]
    ) -> None:
        """
        Configure settings for a specific environment.
        
        Args:
            environment: Target environment
            config: Configuration dictionary
        """
        if environment in self.environment_configs:
            self.environment_configs[environment].update(config)
        else:
            self.environment_configs[environment] = config
    
    def get_environment_config(self, environment: Environment) -> Dict[str, Any]:
        """Get configuration for an environment."""
        return self.environment_configs.get(environment, {}).copy()
    
    def export_to_file(self, filepath: Path) -> None:
        """Export all workflows to a file."""
        self.registry.export_workflows(filepath)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about workflows and executions.
        
        Returns:
            Dictionary with workflow statistics
        """
        workflows = self.registry.list()
        history = self.registry.execution_history
        
        return {
            'total_workflows': len(workflows),
            'workflows_by_environment': {
                env.value: len([w for w in workflows if w.environment == env])
                for env in Environment
            },
            'total_executions': len(history),
            'successful_executions': len([h for h in history if h['status'] == 'success']),
            'failed_executions': len([h for h in history if h['status'] == 'failed']),
            'executions_by_environment': {
                env.value: len([h for h in history if h['environment'] == env.value])
                for env in Environment
            }
        }
