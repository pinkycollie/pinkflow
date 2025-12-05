# PinkFlow Agents & AI System

This document describes the agent and AI system architecture within the PinkFlow ecosystem.

---

## 🤖 Overview

PinkFlow integrates AI-driven agents through the **360Magicians** suite, providing intelligent automation and assistance across the business lifecycle: **Idea → Build → Grow → Managed**.

---

## 📋 Table of Contents

- [Agent Architecture](#agent-architecture)
- [360Magicians Suite](#360magicians-suite)
- [Agent Types](#agent-types)
- [Integration Points](#integration-points)
- [Workflow Automation](#workflow-automation)
- [Development Guide](#development-guide)
- [Configuration](#configuration)

---

## 🏗️ Agent Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    PinkFlow Ecosystem                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Frontend  │  │  Backend   │  │  Workflow  │           │
│  │   (React)  │  │  (FastAPI) │  │   System   │           │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘           │
│        │               │               │                    │
│        └───────────────┴───────────────┘                    │
│                        │                                     │
│                        ▼                                     │
│              ┌──────────────────┐                          │
│              │   AI Proxy       │                          │
│              │  (Gemini API)    │                          │
│              └────────┬─────────┘                          │
│                       │                                     │
│                       ▼                                     │
│         ┌─────────────────────────────┐                   │
│         │     360Magicians Suite      │                   │
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
   - Store keys in environment variables
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
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
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
GEMINI_API_KEY=your_api_key_here
AGENT_BACKEND_URL=https://api.pinkflow.dev
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
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: gemini-api-key
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
