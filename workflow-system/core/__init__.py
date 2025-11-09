"""
PinkFlow Workflow System - Core Module

This module provides the core functionality for creating and managing
dynamic workflows with node-based routing and conditional logic.
"""

from .workflow import (
    Workflow,
    WorkflowBuilder,
    Node,
    Edge,
    EdgeCondition,
    NodeType,
    Environment,
    EdgeConditionType,
    NodeMetadata
)
from .workflow_manager import (
    WorkflowManager,
    WorkflowRegistry
)

__all__ = [
    'Workflow',
    'WorkflowBuilder',
    'Node',
    'Edge',
    'EdgeCondition',
    'NodeType',
    'Environment',
    'EdgeConditionType',
    'NodeMetadata',
    'WorkflowManager',
    'WorkflowRegistry',
]

__version__ = '1.0.0'
