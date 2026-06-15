PinkFlow Agents & AI System

This document describes the agent and AI system architecture within the Magicians ecosystem.

---

## 🤖 Overview

PinkFlow integrates AI-driven agents through the **Magiciancore** layer, providing intelligent automation and assistance across the business lifecycle: **Idea → Build → Grow → Managed**.

---

## 📋 Table of Contents

- [Agent Architecture](#agent-architecture)
- [MagicianCore](#360magicians-suite)
- [Agent Types](#agent-types)
- [Integration Points](#integration-points)
- [Workflow Automation](#workflow-automation)
- [Project Context Management](#project-context-management)
- [Development Guide](#development-guide)
- [Configuration](#configuration)

---

## 🏗️ Agent Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    MAGICIAN Ecosystem                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Frontend  │  │  Backend   │  │  Workflow  │           │
│  │   (HMTX)  │  │  (Flask) │  │   System   │           │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘           │
│        │               │               │                    │
│        └───────────────┴───────────────┘                    │
│                        │                                     │
│                        ▼                                     │
│              ┌──────────────────┐                          │
│              │   AI Proxy       │                          │
│              │  (MAGICIAN API)    │                          │
│              └────────┬─────────┘                          │
│                       │                                     │
│                       ▼                                     │
│         ┌─────────────────────────────┐                   │
│         │     MagicianCore      │                   │
│         ├─────────────────────────────┤                   │
│         │  • Business Agents          │                   │
│         │  • Workflow Agents          │                   │
│         │  • Code Review Agents       │                   │
│         │  • Documentation Agents     │                   │
│         │  • Analysis Agents          │                   │
│         └─────────────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **MagicianCore** - Core orchestration engine
2. **360Magicians** - Specialized AI agents
3. **AI Proxy** - Secure backend API gateway
4. **Workflow System** - Agent task coordination

---

## 🎯 360Magicians Suite

### Agent Categories

#### 1. Business Lifecycle Agents

**Idea Phase Agents:**
- Concept validation
- Market research
- Feasibility analysis
- Requirement gathering

**Build Phase Agents:**
- Architecture planning
- Code generation assistance
- Testing automation
- Documentation generation

**Grow Phase Agents:**
- Performance optimization
- Scaling recommendations
- Feature prioritization
- User feedback analysis

**Managed Phase Agents:**
- Monitoring assistance
- Issue triage
- Maintenance planning
- Technical debt analysis

#### 2. Workflow Automation Agents

- **Task Orchestration**: Coordinate multi-step workflows
- **Conditional Routing**: Smart decision-making in workflows
- **Error Handling**: Automatic recovery and retry logic
- **Notification Management**: Intelligent alert routing

#### 3. Code & Development Agents

- **Code Review**: Automated code quality analysis
- **Security Scanning**: Vulnerability detection
- **Refactoring Suggestions**: Code improvement recommendations
- **Test Generation**: Automated test creation

#### 4. Documentation Agents

- **Documentation Generation**: Auto-generate docs from code
- **README Enhancement**: Improve project documentation
- **API Documentation**: Generate API reference docs
- **Tutorial Creation**: Create learning materials

#### 5. Community & Support Agents

- **Issue Triage**: Categorize and prioritize issues
- **Question Answering**: Provide technical support
- **Contribution Review**: Assess pull requests
- **Onboarding Assistance**: Guide new contributors

---

## 🔧 Agent Types

### 1. Synchronous Agents

Execute immediately and return results:

```python
# Example: Code review agent
async def review_code(code: str, context: dict) -> ReviewResult:
    """Synchronous agent that reviews code immediately."""
    result = await ai_proxy.analyze(code, context)
    return ReviewResult(
        suggestions=result.suggestions,
        issues=result.issues,
        score=result.quality_score
    )
```

**Use Cases:**
- Real-time code review
- Instant feedback on submissions
- Quick analysis tasks

### 2. Asynchronous Agents

Process tasks in background:

```python
# Example: Documentation generation agent
async def generate_docs(repo_path: str) -> Task:
    """Asynchronous agent that generates documentation."""
    task = await task_queue.enqueue(
        agent="doc_generator",
        params={"repo_path": repo_path}
    )
    return task
```

**Use Cases:**
- Large-scale analysis
- Documentation generation
- Performance profiling
- Batch processing

### 3. Workflow Agents

Integrate with workflow system:

```python
# Example: Multi-stage deployment agent
workflow = (
    WorkflowBuilder('deploy_agent', 'Deployment Agent', Environment.PRODUCTION)
    .add_start_node('start', 'Start')
    .add_process_node('validate', 'Validate', validate_code)
    .add_process_node('test', 'Run Tests', run_tests)
    .add_process_node('deploy', 'Deploy', deploy_to_prod)
    .add_end_node('end', 'End')
    .connect('start', 'validate')
    .connect('validate', 'test')
    .connect('test', 'deploy')
    .connect('deploy', 'end')
    .build()
)
```

**Use Cases:**
- CI/CD pipelines
- Multi-step automation
- Complex business processes

---

## 🔌 Integration Points

### Frontend Integration

```typescript
// React component using AI agent
import { useAgent } from '@pinkflow/hooks';

function CodeReviewer() {
  const { invoke, loading, result } = useAgent('code-review');
  
  const handleReview = async (code: string) => {
    const review = await invoke({ code, language: 'typescript' });
    // Handle review results
  };
  
  return (
    <div>
      {loading ? <Spinner /> : <ReviewResults data={result} />}
    </div>
  );
}
```

### Backend Integration

```python
# FastAPI endpoint using agent
from pinkflow.agents import AgentRegistry

@app.post("/api/review/code")
async def review_code(request: CodeReviewRequest):
    agent = AgentRegistry.get("code-review")
    result = await agent.execute(
        code=request.code,
        context=request.context
    )
    return ReviewResponse(
        suggestions=result.suggestions,
        issues=result.issues
    )
```

### Workflow Integration

```python
# Workflow node using agent
from workflow_system.core import WorkflowBuilder

def create_ai_workflow():
    return (
        WorkflowBuilder('ai_workflow', 'AI Workflow', Environment.PRODUCTION)
        .add_process_node(
            'ai_analysis',
            'AI Analysis',
            lambda ctx: ai_agent.analyze(ctx['data'])
        )
        .build()
    )
```

---

## ⚙️ Workflow Automation

### Agent-Powered Workflows

#### Code Review Workflow

```
PR Created → Code Review Agent → Security Scan Agent → Test Agent → Deploy Agent
```

#### Documentation Workflow

```
Code Change → Doc Agent Detects → Generate Docs → Review Agent → Update Repo
```

#### Issue Triage Workflow

```
Issue Created → Classification Agent → Priority Agent → Assignment Agent → Notify
```

### Conditional Routing with Agents

```python
from workflow_system.core import EdgeCondition, EdgeConditionType

# Route based on AI agent decision
workflow.connect(
    'ai_check', 'auto_approve',
    EdgeCondition(
        EdgeConditionType.CUSTOM,
        custom_function=lambda ctx: ai_agent.should_approve(ctx)
    )
)
```

---

## 🔄 Project Context Management

### Managing BUILD or PLAN Context for Incoming Projects

When external projects are cloned or forked into the PinkFlow ecosystem, agents need context to determine whether to BUILD (implement/develop) or PLAN (design/architect) for that project. This section describes how agents handle incoming projects.

#### Context Detection

```python
# Agent context detection for incoming projects
from pinkflow.agents import ProjectContextDetector

async def detect_project_context(repo_url: str, repo_path: str) -> dict:
    """Detect project context from cloned/forked repository."""
    detector = ProjectContextDetector()
    
    context = await detector.analyze(
        repo_url=repo_url,
        repo_path=repo_path,
        checks=[
            'existing_structure',
            'documentation_completeness',
            'build_configuration',
            'test_coverage',
            'dependencies'
        ]
    )
    
    return {
        'mode': context.recommended_mode,  # 'BUILD' or 'PLAN'
        'readiness': context.readiness_score,  # 0-100
        'gaps': context.identified_gaps,
        'suggestions': context.agent_suggestions
    }
```

#### Mode Determination Logic

**PLAN Mode** - When agents should focus on planning and design:
- New or skeleton projects with minimal implementation
- Projects missing critical documentation
- Projects without clear architecture
- Fork intended for major redesign
- Readiness score < 40%

**BUILD Mode** - When agents should focus on implementation:
- Projects with clear architecture and documentation
- Existing codebases needing feature additions
- Well-structured projects with defined patterns
- Fork intended for incremental improvements
- Readiness score ≥ 40%

#### Agent Workflow for Cloned Projects

```
Incoming Project (Clone/Fork)
        ↓
   Detect Context
        ↓
    ┌───┴───┐
    │       │
 PLAN     BUILD
  Mode     Mode
    │       │
    ├───────┤
    │       │
    ▼       ▼
Generate   Generate
Planning   Implementation
Agents     Agents
    │       │
    └───┬───┘
        ↓
   Execute Workflow
        ↓
    Deliverables
```

### Configuration by Project Source

#### GitHub Clone Configuration

```yaml
# config/project_context.yml
github_clone:
  default_mode: "auto-detect"  # or "BUILD" or "PLAN"
  
  detection_rules:
    # Trigger PLAN mode if:
    plan_triggers:
      - missing_readme: true
      - no_build_config: true
      - empty_src_directory: true
      - no_package_manager: true
      - readiness_threshold: 40
    
    # Trigger BUILD mode if:
    build_triggers:
      - has_tests: true
      - has_ci_config: true
      - dependency_manifest_exists: true
      - readiness_threshold: 40
  
  agent_preferences:
    plan_mode_agents:
      - "architecture-planner"
      - "doc-generator"
      - "requirement-analyzer"
      - "tech-stack-advisor"
    
    build_mode_agents:
      - "code-generator"
      - "test-generator"
      - "code-reviewer"
      - "refactor-assistant"
```

#### Fork-Specific Handling

```python
# Handle forked projects
from pinkflow.agents import ForkAnalyzer

async def analyze_fork(original_repo: str, fork_repo: str) -> dict:
    """Analyze fork to determine agent strategy."""
    analyzer = ForkAnalyzer()
    
    # Compare fork with original
    diff = await analyzer.compare(original_repo, fork_repo)
    
    # Determine intent
    intent = analyzer.classify_intent(diff, patterns=[
        'feature_addition',
        'bug_fix',
        'complete_rewrite',
        'architecture_change',
        'documentation_improvement'
    ])
    
    # Recommend agent mode
    if intent in ['complete_rewrite', 'architecture_change']:
        mode = 'PLAN'
        focus = 'design_and_architecture'
    else:
        mode = 'BUILD'
        focus = 'implementation_and_testing'
    
    return {
        'mode': mode,
        'focus': focus,
        'divergence': diff.divergence_score,
        'recommended_agents': analyzer.get_agents_for_intent(intent)
    }
```

### Project Onboarding Workflow

#### Automatic Context Setup

```python
# Automatic project onboarding
from pinkflow.agents import ProjectOnboarder

async def onboard_project(repo_url: str, source: str) -> dict:
    """Onboard incoming project and set up agent context."""
    onboarder = ProjectOnboarder()
    
    # Clone/Fork the project
    project = await onboarder.import_project(
        repo_url=repo_url,
        source=source  # 'clone' or 'fork'
    )
    
    # Detect context
    context = await onboarder.detect_context(project)
    
    # Initialize appropriate agents
    agents = await onboarder.initialize_agents(
        mode=context['mode'],
        project=project,
        focus_areas=context['gaps']
    )
    
    # Create workflow
    workflow = await onboarder.create_workflow(
        agents=agents,
        context=context,
        deliverables=context['suggestions']
    )
    
    return {
        'project_id': project.id,
        'mode': context['mode'],
        'agents': [a.name for a in agents],
        'workflow_id': workflow.id,
        'status': 'ready'
    }
```

#### Manual Context Override

```python
# Allow manual override of detected context
from pinkflow.agents import AgentRegistry

# Force PLAN mode regardless of detection
project_context = {
    'mode': 'PLAN',  # Override auto-detection
    'reason': 'Restructuring for Deaf-First architecture',
    'custom_agents': [
        'accessibility-analyzer',
        'architect-ai',
        'deafauth-integration'
    ]
}

# Initialize with custom context
workflow = await create_custom_workflow(
    project=project,
    context=project_context
)
```

### Context Persistence

#### Storing Project Context

```python
# Store context for reuse across agent invocations
from pinkflow.storage import ContextStore

async def save_project_context(project_id: str, context: dict):
    """Persist project context for future agent use."""
    store = ContextStore()
    
    await store.save(
        key=f"project:{project_id}:context",
        data={
            'mode': context['mode'],
            'detected_at': datetime.utcnow(),
            'readiness_score': context['readiness'],
            'active_agents': context['agents'],
            'workflow_state': context['workflow'],
            'metadata': {
                'repo_url': context['repo_url'],
                'source': context['source'],
                'last_analysis': context['analysis']
            }
        },
        ttl=86400 * 30  # 30 days
    )

async def load_project_context(project_id: str) -> dict:
    """Load saved project context."""
    store = ContextStore()
    return await store.get(f"project:{project_id}:context")
```

### Best Practices

#### 1. Always Detect Context First

```python
# Good: Detect context before agent initialization
context = await detect_project_context(repo_url, repo_path)
agents = await initialize_agents_for_mode(context['mode'])

# Bad: Assuming mode without detection
agents = await initialize_agents_for_mode('BUILD')  # Don't assume!
```

#### 2. Respect Project Boundaries

```python
# Respect existing project structure
if context['mode'] == 'BUILD':
    # Work within existing architecture
    agent.respect_patterns(project.detected_patterns)
    agent.follow_conventions(project.coding_style)
else:  # PLAN mode
    # Suggest improvements but preserve core intent
    agent.propose_architecture(project.requirements)
    agent.maintain_compatibility(project.constraints)
```

#### 3. Handle Ambiguous Cases

```python
# Handle cases where mode is unclear
if context['readiness'] >= 35 and context['readiness'] <= 45:
    # Borderline case - get user input
    mode = await prompt_user_for_mode(
        project=project,
        context=context,
        suggestion=context['mode']
    )
else:
    # Clear case - proceed with detected mode
    mode = context['mode']
```

### Integration with PinkFlow Workflow

#### Workflow-Based Context Management

```python
from workflow_system.core import WorkflowBuilder, Environment

def create_project_intake_workflow():
    """Workflow for incoming project analysis and setup."""
    return (
        WorkflowBuilder('project_intake', 'Project Intake', Environment.PRODUCTION)
        .add_start_node('start', 'Start')
        .add_process_node('clone', 'Clone/Fork Project', clone_project)
        .add_process_node('analyze', 'Analyze Context', detect_project_context)
        .add_decision_node('mode_check', 'Check Mode')
        .add_process_node('plan_setup', 'Setup PLAN Agents', setup_plan_agents)
        .add_process_node('build_setup', 'Setup BUILD Agents', setup_build_agents)
        .add_process_node('execute', 'Execute Agents', run_agents)
        .add_end_node('end', 'Complete')
        
        .connect('start', 'clone')
        .connect('clone', 'analyze')
        .connect('analyze', 'mode_check')
        .connect(
            'mode_check', 'plan_setup',
            EdgeCondition(EdgeConditionType.EQUALS, 'mode', 'PLAN')
        )
        .connect(
            'mode_check', 'build_setup',
            EdgeCondition(EdgeConditionType.EQUALS, 'mode', 'BUILD')
        )
        .connect('plan_setup', 'execute')
        .connect('build_setup', 'execute')
        .connect('execute', 'end')
        .build()
    )
```

### Examples

#### Example 1: Clone New Project (PLAN Mode)

```python
# New project with minimal code
result = await onboard_project(
    repo_url="https://github.com/mbtq-dev/new-project",
    source="clone"
)

# Result:
# {
#   'mode': 'PLAN',
#   'reason': 'Empty src directory, no documentation',
#   'agents': ['architecture-planner', 'doc-generator', 'tech-stack-advisor'],
#   'deliverables': ['architecture.md', 'setup-guide.md', 'api-design.md']
# }
```

#### Example 2: Fork Existing Project (BUILD Mode)

```python
# Well-established project needing features
result = await onboard_project(
    repo_url="https://github.com/mbtq-dev/established-project",
    source="fork"
)

# Result:
# {
#   'mode': 'BUILD',
#   'reason': 'Readiness score: 85%, complete documentation',
#   'agents': ['code-generator', 'test-generator', 'code-reviewer'],
#   'deliverables': ['feature-code', 'unit-tests', 'integration-tests']
# }
```

#### Example 3: Mixed Mode (PLAN then BUILD)

```python
# Project needs architecture refinement before building
result = await onboard_project(
    repo_url="https://github.com/mbtq-dev/refactor-project",
    source="fork"
)

# Result:
# {
#   'mode': 'PLAN',
#   'reason': 'Architecture gaps detected',
#   'next_mode': 'BUILD',
#   'agents': ['architecture-planner', 'refactor-planner'],
#   'workflow': 'sequential',  # PLAN first, then BUILD
#   'deliverables': ['refactor-plan.md', 'new-architecture.md']
# }
```

---

## 🛠️ Development Guide

### Creating a New Agent

```python
from pinkflow.agents import BaseAgent, AgentConfig

class CustomAgent(BaseAgent):
    """Custom AI agent implementation."""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.model = config.model
        self.temperature = config.temperature
    
    async def execute(self, **kwargs) -> dict:
        """Execute agent logic."""
        # Implement agent functionality
        result = await self.ai_proxy.call(
            prompt=self.build_prompt(kwargs),
            model=self.model,
            temperature=self.temperature
        )
        return self.parse_response(result)
    
    def build_prompt(self, params: dict) -> str:
        """Build AI prompt from parameters."""
        # Construct prompt
        pass
    
    def parse_response(self, response: str) -> dict:
        """Parse AI response."""
        # Extract structured data
        pass
```

### Registering an Agent

```python
from pinkflow.agents import AgentRegistry

# Register agent
AgentRegistry.register(
    name="custom-agent",
    agent_class=CustomAgent,
    config=AgentConfig(
        model="gemini-pro",
        temperature=0.7,
        max_tokens=2000
    )
)
```

### Testing Agents

```python
import pytest
from pinkflow.agents import AgentRegistry

@pytest.mark.asyncio
async def test_custom_agent():
    """Test custom agent functionality."""
    agent = AgentRegistry.get("custom-agent")
    result = await agent.execute(input="test data")
    
    assert result is not None
    assert "output" in result
    assert result["status"] == "success"
```

---

## 🔐 Security & Privacy

### Best Practices

1. **API Key Management**
   - Store keys in Server side
   - Use secure backend proxy
   - Never expose keys in frontend

2. **Data Privacy**
   - Sanitize inputs before sending to AI
   - Don't send sensitive data to external APIs
   - Log requests for audit trails

3. **Rate Limiting**
   - Implement request quotas
   - Queue requests during high load
   - Cache common responses

4. **Error Handling**
   - Graceful degradation when AI unavailable
   - Fallback to rule-based systems
   - Log errors without exposing details

### Secure Configuration

```python
# config/agents.py
import os

AGENT_CONFIG = {
    "magician_api_key": os.getenv("magician_API_KEY"),
    "max_retries": 3,
    "timeout": 30,
    "rate_limit": 100,  # requests per minute
    "enable_caching": True,
    "cache_ttl": 3600,  # seconds
}
```

---

## 📊 Agent Monitoring

### Metrics to Track

- **Execution Time**: How long agents take
- **Success Rate**: Percentage of successful executions
- **Error Rate**: Failed agent invocations
- **API Usage**: Token consumption and costs
- **Cache Hit Rate**: Efficiency of caching

### Monitoring Dashboard

```python
from pinkflow.monitoring import AgentMetrics

# Track agent performance
@track_metrics
async def execute_agent(agent_name: str, params: dict):
    start_time = time.time()
    try:
        result = await agent.execute(**params)
        AgentMetrics.record_success(agent_name, time.time() - start_time)
        return result
    except Exception as e:
        AgentMetrics.record_failure(agent_name, str(e))
        raise
```

---

## 🚀 Deployment

### Environment Variables

```bash
# .env
Magician_API_KEY=your_api_key_here
AGENT_BACKEND_URL=https://api.360magicians.com
AGENT_TIMEOUT=30
AGENT_MAX_RETRIES=3
ENABLE_AGENT_CACHING=true
AGENT_LOG_LEVEL=INFO
```

### Docker Configuration

```dockerfile
# Dockerfile for agent service
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV AGENT_ENV=production

CMD ["uvicorn", "agents.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Kubernetes Deployment

```yaml
# k8s/agents-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pinkflow-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pinkflow-agents
  template:
    metadata:
      labels:
        app: pinkflow-agents
    spec:
      containers:
      - name: agents
        image: pinkflow/agents:latest
        env:
        - name: MAGiCIAN_API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: magician-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

## 📚 Agent Library

### Available Agents

| Agent Name | Type | Purpose | Status |
|------------|------|---------|--------|
| `code-review` | Sync | Code quality analysis | ✅ Active |
| `doc-generator` | Async | Documentation creation | ✅ Active |
| `security-scanner` | Sync | Vulnerability detection | ✅ Active |
| `test-generator` | Async | Test case creation | 🔄 Beta |
| `issue-triage` | Sync | Issue categorization | ✅ Active |
| `pr-reviewer` | Sync | Pull request review | ✅ Active |
| `performance-analyzer` | Async | Performance analysis | 📋 Planned |
| `deployment-orchestrator` | Workflow | CI/CD automation | 📋 Planned |

---

## 🔗 Related Documentation

- [Workflow System](../workflow-system/README.md) - Workflow orchestration
- [API Documentation](../API.md) - API endpoints
- [Backend Documentation](../backend.md) - Backend architecture
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute

---

## 📞 Support

For agent-related questions:
- Check [Documentation](../DOCS_INDEX.md)
- Open an issue with `component: 360magicians` label
- Review [API Documentation](../API.md)

---

## 🎯 Future Enhancements

### Planned Features

1. **Multi-Model Support**
   - Support for GPT-4, Claude, and other LLMs
   - Model selection based on task type
   - Cost optimization strategies

2. **Agent Marketplace**
   - Community-contributed agents
   - Agent versioning and updates
   - Rating and review system

3. **Advanced Workflows**
   - Agent chaining and composition
   - Dynamic agent selection
   - Self-improving agents

4. **Enhanced Monitoring**
   - Real-time dashboards
   - Cost tracking and optimization
   - Performance profiling

5. **Deaf-First AI Features**
   - Sign language video analysis
   - Visual-first AI interactions
   - Accessibility-focused agents

---

**Last Updated**: 2025-12-05  
**Version**: 1.0.0  
**Part of the PinkFlow Deaf-First Innovation Ecosystem**
