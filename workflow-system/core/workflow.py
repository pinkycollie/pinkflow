"""
PinkFlow Workflow System - Core Workflow Module

This module provides the core workflow orchestration system for dynamically
connecting nodes, edges, and implementing conditional routing for complete
development cycles.

Features:
- Dynamic node connection management
- Edge-based routing with conditions
- Environment-aware workflow execution (sandbox, staging, production)
- Modular and extensible design
"""

from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json


class NodeType(Enum):
    """Defines the types of nodes in the workflow."""
    START = "start"
    PROCESS = "process"
    DECISION = "decision"
    END = "end"
    PARALLEL = "parallel"
    MERGE = "merge"


class Environment(Enum):
    """Defines the deployment environments."""
    SANDBOX = "sandbox"
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class EdgeConditionType(Enum):
    """Defines types of conditions for edge routing."""
    ALWAYS = "always"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    CUSTOM = "custom"


@dataclass
class NodeMetadata:
    """Metadata for workflow nodes."""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    description: str = ""
    owner: str = ""


@dataclass
class EdgeCondition:
    """
    Represents a condition for edge traversal.
    
    Attributes:
        condition_type: Type of condition to evaluate
        field: Field name to check (for data-based conditions)
        value: Expected value for comparison
        custom_function: Custom function for complex conditions
    """
    condition_type: EdgeConditionType
    field: Optional[str] = None
    value: Any = None
    custom_function: Optional[Callable[[Dict], bool]] = None
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate the condition against the provided context.
        
        Args:
            context: Dictionary containing workflow execution context
            
        Returns:
            True if condition is met, False otherwise
        """
        if self.condition_type == EdgeConditionType.ALWAYS:
            return True
        
        if self.condition_type == EdgeConditionType.CUSTOM:
            if self.custom_function:
                return self.custom_function(context)
            return False
        
        if self.field is None or self.field not in context:
            return False
        
        field_value = context[self.field]
        
        if self.condition_type == EdgeConditionType.EQUALS:
            return field_value == self.value
        elif self.condition_type == EdgeConditionType.NOT_EQUALS:
            return field_value != self.value
        elif self.condition_type == EdgeConditionType.GREATER_THAN:
            return field_value > self.value
        elif self.condition_type == EdgeConditionType.LESS_THAN:
            return field_value < self.value
        elif self.condition_type == EdgeConditionType.CONTAINS:
            return self.value in field_value
        
        return False


@dataclass
class Edge:
    """
    Represents a directed edge between two nodes.
    
    Attributes:
        edge_id: Unique identifier for the edge
        from_node: Source node ID
        to_node: Destination node ID
        condition: Condition for edge traversal
        priority: Priority for edge selection (higher = more priority)
        metadata: Additional edge metadata
    """
    edge_id: str
    from_node: str
    to_node: str
    condition: EdgeCondition = field(default_factory=lambda: EdgeCondition(EdgeConditionType.ALWAYS))
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def can_traverse(self, context: Dict[str, Any]) -> bool:
        """Check if this edge can be traversed given the context."""
        return self.condition.evaluate(context)


@dataclass
class Node:
    """
    Represents a node in the workflow.
    
    Attributes:
        node_id: Unique identifier for the node
        name: Human-readable name
        node_type: Type of node
        action: Function to execute when node is visited
        config: Configuration parameters for the node
        metadata: Additional node metadata
    """
    node_id: str
    name: str
    node_type: NodeType
    action: Optional[Callable[[Dict], Dict]] = None
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: NodeMetadata = field(default_factory=NodeMetadata)
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the node's action with the given context.
        
        Args:
            context: Current workflow execution context
            
        Returns:
            Updated context after node execution
        """
        if self.action:
            return self.action(context)
        return context


class Workflow:
    """
    Main workflow orchestrator that manages nodes, edges, and execution.
    
    This class provides the core functionality for creating and executing
    dynamic workflows with conditional routing.
    """
    
    def __init__(
        self,
        workflow_id: str,
        name: str,
        environment: Environment = Environment.DEVELOPMENT,
        description: str = ""
    ):
        """
        Initialize a new workflow.
        
        Args:
            workflow_id: Unique identifier for the workflow
            name: Human-readable workflow name
            environment: Target environment for execution
            description: Optional description of the workflow
        """
        self.workflow_id = workflow_id
        self.name = name
        self.environment = environment
        self.description = description
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.start_node: Optional[str] = None
        self.end_nodes: List[str] = []
        self.created_at = datetime.now()
        self.metadata: Dict[str, Any] = {}
    
    def add_node(self, node: Node) -> None:
        """
        Add a node to the workflow.
        
        Args:
            node: Node to add
            
        Raises:
            ValueError: If node with same ID already exists
        """
        if node.node_id in self.nodes:
            raise ValueError(f"Node with ID '{node.node_id}' already exists")
        
        self.nodes[node.node_id] = node
        
        # Automatically set start and end nodes based on type
        if node.node_type == NodeType.START and self.start_node is None:
            self.start_node = node.node_id
        elif node.node_type == NodeType.END:
            if node.node_id not in self.end_nodes:
                self.end_nodes.append(node.node_id)
    
    def add_edge(self, edge: Edge) -> None:
        """
        Add an edge to the workflow.
        
        Args:
            edge: Edge to add
            
        Raises:
            ValueError: If source or destination node doesn't exist
        """
        if edge.from_node not in self.nodes:
            raise ValueError(f"Source node '{edge.from_node}' does not exist")
        if edge.to_node not in self.nodes:
            raise ValueError(f"Destination node '{edge.to_node}' does not exist")
        
        self.edges.append(edge)
    
    def connect_nodes(
        self,
        from_node_id: str,
        to_node_id: str,
        condition: Optional[EdgeCondition] = None,
        priority: int = 0
    ) -> Edge:
        """
        Create and add an edge between two nodes.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Destination node ID
            condition: Optional condition for edge traversal
            priority: Edge priority for selection
            
        Returns:
            The created edge
        """
        edge_id = f"{from_node_id}_to_{to_node_id}_{len(self.edges)}"
        edge = Edge(
            edge_id=edge_id,
            from_node=from_node_id,
            to_node=to_node_id,
            condition=condition or EdgeCondition(EdgeConditionType.ALWAYS),
            priority=priority
        )
        self.add_edge(edge)
        return edge
    
    def get_outgoing_edges(self, node_id: str) -> List[Edge]:
        """
        Get all outgoing edges from a node.
        
        Args:
            node_id: Node ID to get edges for
            
        Returns:
            List of outgoing edges, sorted by priority (descending)
        """
        outgoing = [e for e in self.edges if e.from_node == node_id]
        return sorted(outgoing, key=lambda e: e.priority, reverse=True)
    
    def get_next_nodes(self, current_node_id: str, context: Dict[str, Any]) -> List[str]:
        """
        Determine the next nodes to visit based on conditions.
        
        Args:
            current_node_id: Current node ID
            context: Current execution context
            
        Returns:
            List of next node IDs that can be traversed
        """
        outgoing_edges = self.get_outgoing_edges(current_node_id)
        next_nodes = []
        
        for edge in outgoing_edges:
            if edge.can_traverse(context):
                next_nodes.append(edge.to_node)
        
        return next_nodes
    
    def execute(
        self,
        initial_context: Optional[Dict[str, Any]] = None,
        max_iterations: int = 1000
    ) -> Dict[str, Any]:
        """
        Execute the workflow starting from the start node.
        
        Args:
            initial_context: Initial context for workflow execution
            max_iterations: Maximum number of node visits to prevent infinite loops
            
        Returns:
            Final execution context
            
        Raises:
            ValueError: If workflow has no start node or exceeds max iterations
        """
        if self.start_node is None:
            raise ValueError("Workflow has no start node")
        
        context = initial_context or {}
        context['environment'] = self.environment.value
        context['workflow_id'] = self.workflow_id
        context['execution_path'] = []
        
        current_nodes = [self.start_node]
        iterations = 0
        
        while current_nodes and iterations < max_iterations:
            iterations += 1
            next_nodes = []
            
            for node_id in current_nodes:
                if node_id not in self.nodes:
                    continue
                
                node = self.nodes[node_id]
                context['execution_path'].append(node_id)
                
                # Execute node action
                context = node.execute(context)
                
                # Check if we've reached an end node
                if node.node_type == NodeType.END:
                    continue
                
                # Determine next nodes
                next_node_ids = self.get_next_nodes(node_id, context)
                next_nodes.extend(next_node_ids)
            
            current_nodes = next_nodes
        
        if iterations >= max_iterations:
            raise ValueError(f"Workflow exceeded maximum iterations ({max_iterations})")
        
        context['completed'] = True
        context['iterations'] = iterations
        return context
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export workflow to dictionary format.
        
        Returns:
            Dictionary representation of the workflow
        """
        return {
            'workflow_id': self.workflow_id,
            'name': self.name,
            'environment': self.environment.value,
            'description': self.description,
            'start_node': self.start_node,
            'end_nodes': self.end_nodes,
            'nodes': {
                node_id: {
                    'node_id': node.node_id,
                    'name': node.name,
                    'type': node.node_type.value,
                    'config': node.config,
                    'metadata': {
                        'description': node.metadata.description,
                        'tags': node.metadata.tags,
                        'owner': node.metadata.owner
                    }
                }
                for node_id, node in self.nodes.items()
            },
            'edges': [
                {
                    'edge_id': edge.edge_id,
                    'from': edge.from_node,
                    'to': edge.to_node,
                    'condition_type': edge.condition.condition_type.value,
                    'priority': edge.priority,
                    'metadata': edge.metadata
                }
                for edge in self.edges
            ],
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Export workflow to JSON string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation of the workflow
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    def validate(self) -> List[str]:
        """
        Validate the workflow structure.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.start_node:
            errors.append("Workflow has no start node")
        
        if not self.end_nodes:
            errors.append("Workflow has no end nodes")
        
        # Check for unreachable nodes
        reachable = set()
        if self.start_node:
            to_visit = [self.start_node]
            while to_visit:
                current = to_visit.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                for edge in self.get_outgoing_edges(current):
                    to_visit.append(edge.to_node)
        
        unreachable = set(self.nodes.keys()) - reachable
        if unreachable:
            errors.append(f"Unreachable nodes: {', '.join(unreachable)}")
        
        return errors


class WorkflowBuilder:
    """
    Builder class for creating workflows with a fluent interface.
    
    This provides a more convenient way to construct workflows programmatically.
    """
    
    def __init__(self, workflow_id: str, name: str, environment: Environment = Environment.DEVELOPMENT):
        """
        Initialize a new workflow builder.
        
        Args:
            workflow_id: Unique workflow identifier
            name: Workflow name
            environment: Target environment
        """
        self.workflow = Workflow(workflow_id, name, environment)
    
    def with_description(self, description: str) -> 'WorkflowBuilder':
        """Add description to the workflow."""
        self.workflow.description = description
        return self
    
    def with_metadata(self, key: str, value: Any) -> 'WorkflowBuilder':
        """Add metadata to the workflow."""
        self.workflow.metadata[key] = value
        return self
    
    def add_start_node(self, node_id: str, name: str, action: Optional[Callable] = None) -> 'WorkflowBuilder':
        """Add a start node to the workflow."""
        node = Node(node_id=node_id, name=name, node_type=NodeType.START, action=action)
        self.workflow.add_node(node)
        return self
    
    def add_process_node(
        self,
        node_id: str,
        name: str,
        action: Optional[Callable] = None,
        config: Optional[Dict] = None
    ) -> 'WorkflowBuilder':
        """Add a process node to the workflow."""
        node = Node(
            node_id=node_id,
            name=name,
            node_type=NodeType.PROCESS,
            action=action,
            config=config or {}
        )
        self.workflow.add_node(node)
        return self
    
    def add_decision_node(
        self,
        node_id: str,
        name: str,
        action: Optional[Callable] = None
    ) -> 'WorkflowBuilder':
        """Add a decision node to the workflow."""
        node = Node(node_id=node_id, name=name, node_type=NodeType.DECISION, action=action)
        self.workflow.add_node(node)
        return self
    
    def add_end_node(self, node_id: str, name: str, action: Optional[Callable] = None) -> 'WorkflowBuilder':
        """Add an end node to the workflow."""
        node = Node(node_id=node_id, name=name, node_type=NodeType.END, action=action)
        self.workflow.add_node(node)
        return self
    
    def connect(
        self,
        from_node: str,
        to_node: str,
        condition: Optional[EdgeCondition] = None,
        priority: int = 0
    ) -> 'WorkflowBuilder':
        """Connect two nodes with an edge."""
        self.workflow.connect_nodes(from_node, to_node, condition, priority)
        return self
    
    def build(self) -> Workflow:
        """
        Build and return the workflow.
        
        Returns:
            The constructed workflow
            
        Raises:
            ValueError: If workflow validation fails
        """
        errors = self.workflow.validate()
        if errors:
            raise ValueError(f"Workflow validation failed: {'; '.join(errors)}")
        return self.workflow
