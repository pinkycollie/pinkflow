# API Reference

Complete API reference for the PinkFlow Workflow System.

---

## Table of Contents

- [Core Classes](#core-classes)
  - [Workflow](#workflow)
  - [WorkflowBuilder](#workflowbuilder)
  - [Node](#node)
  - [Edge](#edge)
  - [EdgeCondition](#edgecondition)
- [Manager Classes](#manager-classes)
  - [WorkflowManager](#workflowmanager)
  - [WorkflowRegistry](#workflowregistry)
- [Enums](#enums)
  - [NodeType](#nodetype)
  - [Environment](#environment)
  - [EdgeConditionType](#edgeconditiontype)
- [Data Classes](#data-classes)
  - [NodeMetadata](#nodemetadata)

---

## Core Classes

### Workflow

Main orchestrator for managing nodes, edges, and execution.

#### Constructor

```python
Workflow(
    workflow_id: str,
    name: str,
    environment: Environment = Environment.DEVELOPMENT,
    description: str = ""
)
```

**Parameters:**
- `workflow_id`: Unique identifier for the workflow
- `name`: Human-readable workflow name
- `environment`: Target environment for execution
- `description`: Optional description

#### Methods

##### `add_node(node: Node) -> None`

Add a node to the workflow.

**Raises:**
- `ValueError`: If node with same ID already exists

**Example:**
```python
node = Node(node_id='process_1', name='Process', node_type=NodeType.PROCESS)
workflow.add_node(node)
```

##### `add_edge(edge: Edge) -> None`

Add an edge to the workflow.

**Raises:**
- `ValueError`: If source or destination node doesn't exist

##### `connect_nodes(from_node_id: str, to_node_id: str, condition: Optional[EdgeCondition] = None, priority: int = 0) -> Edge`

Create and add an edge between two nodes.

**Parameters:**
- `from_node_id`: Source node ID
- `to_node_id`: Destination node ID
- `condition`: Optional condition for edge traversal
- `priority`: Edge priority (higher = more priority)

**Returns:** The created edge

**Example:**
```python
workflow.connect_nodes(
    'node_a', 'node_b',
    EdgeCondition(EdgeConditionType.EQUALS, 'status', 'success'),
    priority=10
)
```

##### `get_outgoing_edges(node_id: str) -> List[Edge]`

Get all outgoing edges from a node, sorted by priority.

**Returns:** List of edges sorted by priority (descending)

##### `get_next_nodes(current_node_id: str, context: Dict[str, Any]) -> List[str]`

Determine the next nodes to visit based on conditions.

**Parameters:**
- `current_node_id`: Current node ID
- `context`: Current execution context

**Returns:** List of next node IDs that can be traversed

##### `execute(initial_context: Optional[Dict[str, Any]] = None, max_iterations: int = 1000) -> Dict[str, Any]`

Execute the workflow starting from the start node.

**Parameters:**
- `initial_context`: Initial context for workflow execution
- `max_iterations`: Maximum node visits to prevent infinite loops

**Returns:** Final execution context with these keys:
- `completed`: True if workflow completed
- `iterations`: Number of iterations executed
- `execution_path`: List of node IDs visited
- `environment`: Environment value
- `workflow_id`: Workflow ID

**Raises:**
- `ValueError`: If workflow has no start node or exceeds max iterations

**Example:**
```python
result = workflow.execute({'input': 'value'})
print(f"Path: {result['execution_path']}")
print(f"Iterations: {result['iterations']}")
```

##### `to_dict() -> Dict[str, Any]`

Export workflow to dictionary format.

**Returns:** Dictionary representation of the workflow

##### `to_json(indent: int = 2) -> str`

Export workflow to JSON string.

**Parameters:**
- `indent`: JSON indentation level

**Returns:** JSON string representation

##### `validate() -> List[str]`

Validate the workflow structure.

**Returns:** List of validation errors (empty if valid)

**Example:**
```python
errors = workflow.validate()
if errors:
    print(f"Validation failed: {errors}")
```

---

### WorkflowBuilder

Builder class for creating workflows with a fluent interface.

#### Constructor

```python
WorkflowBuilder(
    workflow_id: str,
    name: str,
    environment: Environment = Environment.DEVELOPMENT
)
```

#### Methods

##### `with_description(description: str) -> WorkflowBuilder`

Add description to the workflow.

**Returns:** Self for chaining

##### `with_metadata(key: str, value: Any) -> WorkflowBuilder`

Add metadata to the workflow.

**Returns:** Self for chaining

##### `add_start_node(node_id: str, name: str, action: Optional[Callable] = None) -> WorkflowBuilder`

Add a start node to the workflow.

**Returns:** Self for chaining

##### `add_process_node(node_id: str, name: str, action: Optional[Callable] = None, config: Optional[Dict] = None) -> WorkflowBuilder`

Add a process node to the workflow.

**Returns:** Self for chaining

##### `add_decision_node(node_id: str, name: str, action: Optional[Callable] = None) -> WorkflowBuilder`

Add a decision node to the workflow.

**Returns:** Self for chaining

##### `add_end_node(node_id: str, name: str, action: Optional[Callable] = None) -> WorkflowBuilder`

Add an end node to the workflow.

**Returns:** Self for chaining

##### `connect(from_node: str, to_node: str, condition: Optional[EdgeCondition] = None, priority: int = 0) -> WorkflowBuilder`

Connect two nodes with an edge.

**Returns:** Self for chaining

##### `build() -> Workflow`

Build and return the workflow.

**Returns:** The constructed workflow

**Raises:**
- `ValueError`: If workflow validation fails

**Example:**
```python
workflow = (
    WorkflowBuilder('my_workflow', 'My Workflow')
    .with_description('A sample workflow')
    .add_start_node('start', 'Start')
    .add_process_node('process', 'Process')
    .add_end_node('end', 'End')
    .connect('start', 'process')
    .connect('process', 'end')
    .build()
)
```

---

### Node

Represents a node in the workflow.

#### Constructor

```python
Node(
    node_id: str,
    name: str,
    node_type: NodeType,
    action: Optional[Callable[[Dict], Dict]] = None,
    config: Dict[str, Any] = None,
    metadata: NodeMetadata = None
)
```

**Parameters:**
- `node_id`: Unique identifier for the node
- `name`: Human-readable name
- `node_type`: Type of node (START, PROCESS, DECISION, END, etc.)
- `action`: Function to execute when node is visited
- `config`: Configuration parameters
- `metadata`: Additional node metadata

#### Methods

##### `execute(context: Dict[str, Any]) -> Dict[str, Any]`

Execute the node's action with the given context.

**Parameters:**
- `context`: Current workflow execution context

**Returns:** Updated context after node execution

**Example:**
```python
def my_action(context):
    context['processed'] = True
    return context

node = Node(
    node_id='process_1',
    name='Process Data',
    node_type=NodeType.PROCESS,
    action=my_action
)

context = {}
context = node.execute(context)
print(context['processed'])  # True
```

---

### Edge

Represents a directed edge between two nodes.

#### Constructor

```python
Edge(
    edge_id: str,
    from_node: str,
    to_node: str,
    condition: EdgeCondition = EdgeCondition(EdgeConditionType.ALWAYS),
    priority: int = 0,
    metadata: Dict[str, Any] = None
)
```

**Parameters:**
- `edge_id`: Unique identifier for the edge
- `from_node`: Source node ID
- `to_node`: Destination node ID
- `condition`: Condition for edge traversal
- `priority`: Priority for edge selection (higher = more priority)
- `metadata`: Additional edge metadata

#### Methods

##### `can_traverse(context: Dict[str, Any]) -> bool`

Check if this edge can be traversed given the context.

**Parameters:**
- `context`: Current execution context

**Returns:** True if edge can be traversed

**Example:**
```python
edge = Edge(
    edge_id='e1',
    from_node='a',
    to_node='b',
    condition=EdgeCondition(EdgeConditionType.EQUALS, 'status', 'ready')
)

context = {'status': 'ready'}
print(edge.can_traverse(context))  # True
```

---

### EdgeCondition

Represents a condition for edge traversal.

#### Constructor

```python
EdgeCondition(
    condition_type: EdgeConditionType,
    field: Optional[str] = None,
    value: Any = None,
    custom_function: Optional[Callable[[Dict], bool]] = None
)
```

**Parameters:**
- `condition_type`: Type of condition to evaluate
- `field`: Field name to check (for data-based conditions)
- `value`: Expected value for comparison
- `custom_function`: Custom function for complex conditions

#### Methods

##### `evaluate(context: Dict[str, Any]) -> bool`

Evaluate the condition against the provided context.

**Parameters:**
- `context`: Dictionary containing workflow execution context

**Returns:** True if condition is met, False otherwise

**Examples:**

**Always condition:**
```python
condition = EdgeCondition(EdgeConditionType.ALWAYS)
print(condition.evaluate({}))  # True
```

**Equals condition:**
```python
condition = EdgeCondition(EdgeConditionType.EQUALS, 'status', 'success')
print(condition.evaluate({'status': 'success'}))  # True
print(condition.evaluate({'status': 'failure'}))  # False
```

**Greater than condition:**
```python
condition = EdgeCondition(EdgeConditionType.GREATER_THAN, 'score', 80)
print(condition.evaluate({'score': 90}))  # True
print(condition.evaluate({'score': 70}))  # False
```

**Custom condition:**
```python
def custom_check(context):
    return context.get('score', 0) > 80 and context.get('approved', False)

condition = EdgeCondition(
    EdgeConditionType.CUSTOM,
    custom_function=custom_check
)
print(condition.evaluate({'score': 90, 'approved': True}))  # True
```

---

## Manager Classes

### WorkflowManager

High-level workflow management interface.

#### Constructor

```python
WorkflowManager()
```

#### Methods

##### `register_workflow(workflow: Workflow) -> None`

Register a workflow with the manager.

**Example:**
```python
manager = WorkflowManager()
manager.register_workflow(workflow)
```

##### `execute_workflow(workflow_id: str, initial_context: Optional[Dict[str, Any]] = None, override_environment: Optional[Environment] = None) -> Dict[str, Any]`

Execute a workflow with environment-specific configurations.

**Parameters:**
- `workflow_id`: ID of workflow to execute
- `initial_context`: Initial execution context
- `override_environment`: Optional environment override

**Returns:** Final execution context

**Example:**
```python
result = manager.execute_workflow(
    'my_workflow',
    {'input': 'value'},
    override_environment=Environment.STAGING
)
```

##### `get_workflow(workflow_id: str) -> Optional[Workflow]`

Get a workflow by ID.

##### `list_workflows(environment: Optional[Environment] = None) -> List[Workflow]`

List all workflows, optionally filtered by environment.

**Example:**
```python
# All workflows
all_workflows = manager.list_workflows()

# Production workflows only
prod_workflows = manager.list_workflows(Environment.PRODUCTION)
```

##### `get_execution_history(workflow_id: Optional[str] = None) -> List[Dict[str, Any]]`

Get execution history.

**Parameters:**
- `workflow_id`: Optional workflow ID to filter by

**Returns:** List of execution records with these keys:
- `workflow_id`: Workflow ID
- `started_at`: Start timestamp (ISO format)
- `completed_at`: Completion timestamp (ISO format)
- `duration_seconds`: Execution duration
- `status`: 'success' or 'failed'
- `environment`: Environment value

##### `configure_environment(environment: Environment, config: Dict[str, Any]) -> None`

Configure settings for a specific environment.

**Example:**
```python
manager.configure_environment(
    Environment.PRODUCTION,
    {
        'max_iterations': 2000,
        'timeout_seconds': 900,
        'auto_rollback': False
    }
)
```

##### `get_environment_config(environment: Environment) -> Dict[str, Any]`

Get configuration for an environment.

##### `export_to_file(filepath: Path) -> None`

Export all workflows to a file.

##### `get_statistics() -> Dict[str, Any]`

Get statistics about workflows and executions.

**Returns:** Dictionary with these keys:
- `total_workflows`: Total number of workflows
- `workflows_by_environment`: Count by environment
- `total_executions`: Total execution count
- `successful_executions`: Successful execution count
- `failed_executions`: Failed execution count
- `executions_by_environment`: Execution count by environment

**Example:**
```python
stats = manager.get_statistics()
print(f"Total workflows: {stats['total_workflows']}")
print(f"Success rate: {stats['successful_executions'] / stats['total_executions']}")
```

---

### WorkflowRegistry

Registry for managing multiple workflows.

#### Constructor

```python
WorkflowRegistry()
```

#### Methods

##### `register(workflow: Workflow) -> None`

Register a workflow in the registry.

**Raises:**
- `ValueError`: If workflow already registered or validation fails

##### `unregister(workflow_id: str) -> None`

Unregister a workflow from the registry.

##### `get(workflow_id: str) -> Optional[Workflow]`

Retrieve a workflow by ID.

##### `list(environment: Optional[Environment] = None) -> List[Workflow]`

List all registered workflows, optionally filtered by environment.

##### `execute(workflow_id: str, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`

Execute a registered workflow.

##### `get_execution_history(workflow_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]`

Get execution history for workflows.

##### `export_workflows(filepath: Path) -> None`

Export all workflows to a JSON file.

##### `clear() -> None`

Clear all workflows from the registry.

---

## Enums

### NodeType

Defines the types of nodes in the workflow.

**Values:**
- `START`: Entry point of the workflow
- `PROCESS`: Performs an action or computation
- `DECISION`: Makes decisions without executing logic
- `END`: Terminal node marking completion
- `PARALLEL`: Splits execution into parallel paths
- `MERGE`: Merges parallel paths back together

**Example:**
```python
from core.workflow import NodeType

node = Node(
    node_id='my_node',
    name='My Node',
    node_type=NodeType.PROCESS
)
```

---

### Environment

Defines the deployment environments.

**Values:**
- `SANDBOX`: Experimentation environment
- `STAGING`: Pre-production testing environment
- `PRODUCTION`: Live production environment
- `DEVELOPMENT`: Local development environment

**Example:**
```python
from core.workflow import Environment

workflow = WorkflowBuilder(
    'my_workflow',
    'My Workflow',
    Environment.PRODUCTION
).build()
```

---

### EdgeConditionType

Defines types of conditions for edge routing.

**Values:**
- `ALWAYS`: Always traverse (default)
- `EQUALS`: Field equals value
- `NOT_EQUALS`: Field doesn't equal value
- `GREATER_THAN`: Field greater than value
- `LESS_THAN`: Field less than value
- `CONTAINS`: Value contained in field
- `CUSTOM`: Custom function for complex conditions

**Example:**
```python
from core.workflow import EdgeConditionType, EdgeCondition

# Equals condition
condition = EdgeCondition(EdgeConditionType.EQUALS, 'status', 'ready')

# Greater than condition
condition = EdgeCondition(EdgeConditionType.GREATER_THAN, 'score', 80)

# Custom condition
def my_condition(context):
    return context.get('approved', False) and context.get('score', 0) > 90

condition = EdgeCondition(
    EdgeConditionType.CUSTOM,
    custom_function=my_condition
)
```

---

## Data Classes

### NodeMetadata

Metadata for workflow nodes.

#### Constructor

```python
NodeMetadata(
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
    tags: List[str] = [],
    description: str = "",
    owner: str = ""
)
```

**Attributes:**
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `tags`: List of tags for categorization
- `description`: Detailed description
- `owner`: Owner or team responsible

**Example:**
```python
from core.workflow import NodeMetadata

metadata = NodeMetadata(
    tags=['critical', 'deployment'],
    description='Deploys to production',
    owner='DevOps Team'
)

node = Node(
    node_id='deploy',
    name='Deploy',
    node_type=NodeType.PROCESS,
    metadata=metadata
)
```

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
