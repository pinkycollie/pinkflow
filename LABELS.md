# GitHub Labels Guide

This document explains the label system used in the PinkFlow repository to organize and categorize issues and pull requests.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Label Categories](#label-categories)
- [How to Use Labels](#how-to-use-labels)
- [Label Reference](#label-reference)
- [Examples](#examples)

---

## 🌟 Overview

Labels help us:
- **Organize** work by type, priority, and status
- **Filter** issues and PRs efficiently
- **Track** progress across components
- **Communicate** issue state and requirements
- **Welcome** new contributors with appropriate tasks

---

## 🏷️ Label Categories

### Priority Labels
Indicate how urgent an issue is

| Label | Color | When to Use |
|-------|-------|-------------|
| `priority: critical` | 🔴 Red | Production down, security vulnerabilities, data loss |
| `priority: high` | 🟠 Orange | Major features, important bugs affecting users |
| `priority: medium` | 🟡 Yellow | Standard work, planned features |
| `priority: low` | 🟢 Green | Nice-to-haves, minor improvements |

### Type Labels
Categorize the nature of work

| Label | Color | Description |
|-------|-------|-------------|
| `type: bug` | 🔴 Red | Something isn't working |
| `type: feature` | 🟢 Green | New feature or enhancement |
| `type: documentation` | 🔵 Blue | Documentation changes |
| `type: refactor` | 🟡 Yellow | Code improvements without changing functionality |
| `type: test` | 🔵 Blue | Test additions or improvements |
| `type: security` | 🔴 Red | Security-related issues |
| `type: performance` | 🟣 Purple | Performance improvements |
| `type: dependencies` | 🔵 Blue | Dependency updates |
| `type: ci/cd` | 🟤 Brown | CI/CD pipeline work |

### Status Labels
Track where an issue is in its lifecycle

| Label | Color | Description |
|-------|-------|-------------|
| `status: needs triage` | ⚪ Gray | New issues needing review |
| `status: in progress` | 🟢 Green | Actively being worked on |
| `status: blocked` | 🔴 Red | Waiting on something else |
| `status: needs review` | 🟡 Yellow | Ready for code review |
| `status: on hold` | 🔵 Blue | Paused temporarily |

### Component Labels
Identify which part of PinkFlow is affected

| Label | Description |
|-------|-------------|
| `component: frontend` | React/TypeScript UI |
| `component: backend` | FastAPI services |
| `component: deafauth` | DeafAuth authentication service |
| `component: fibonrose` | FibonRose trust engine |
| `component: pinksync` | PinkSync real-time service |
| `component: 360magicians` | AI workflow agents |
| `component: workflow` | Workflow orchestration system |
| `component: infrastructure` | Deployment and infrastructure |

### Accessibility Labels
Focus on Deaf-First and accessibility features

| Label | Description |
|-------|-------------|
| `accessibility: deaf-first` | Deaf-First design principles |
| `accessibility: wcag` | WCAG compliance |
| `accessibility: screen reader` | Screen reader compatibility |

### Size/Effort Labels
Estimate time required

| Label | Time Estimate |
|-------|---------------|
| `size: xs` | < 1 hour |
| `size: s` | 1-3 hours |
| `size: m` | 1 day |
| `size: l` | 2-3 days |
| `size: xl` | 1+ week |

### Experience Level Labels
Help contributors find appropriate tasks

| Label | Description |
|-------|-------------|
| `good first issue` | Perfect for new contributors |
| `help wanted` | Community help needed |
| `mentor available` | Guidance available for this issue |

### Special Labels
Handle edge cases and special situations

| Label | Description |
|-------|-------------|
| `breaking change` | Introduces breaking changes |
| `needs discussion` | Requires community input |
| `wontfix` | Will not be addressed |
| `duplicate` | Already exists elsewhere |
| `invalid` | Not a valid issue |
| `question` | Question needing answer |

### Milestone Labels
Track release milestones

| Label | Version |
|-------|---------|
| `milestone: foundation` | v0.1.0 |
| `milestone: backend` | v0.2.0 |
| `milestone: realtime` | v0.3.0 |
| `milestone: ai` | v0.4.0 |
| `milestone: v1.0` | v1.0.0 |

### Environment Labels
Specify deployment environment

| Label | Environment |
|-------|-------------|
| `env: sandbox` | Testing environment |
| `env: staging` | Pre-production |
| `env: production` | Live production |

---

## 🎯 How to Use Labels

### For Issues

**When Creating an Issue:**
1. **Type Label** (required): What kind of issue?
2. **Priority Label** (optional): How urgent?
3. **Component Label** (recommended): Which part affected?
4. **Size Label** (optional): Estimated effort

**Example:**
```
Title: Login fails with invalid credentials
Labels: type: bug, priority: high, component: deafauth, size: s
```

### For Pull Requests

**When Creating a PR:**
1. **Type Label**: Matches the work type
2. **Component Label**: What you changed
3. **Status Label**: Current state
4. **Special Labels**: If applicable

**Example:**
```
Title: feat: add OAuth integration to DeafAuth
Labels: type: feature, component: deafauth, status: needs review, size: l
```

### Adding Labels

**As a Contributor:**
- Add labels when creating issues
- Suggest labels in PR description
- Maintainers will adjust as needed

**As a Maintainer:**
- Apply labels during triage
- Update status as work progresses
- Add component/priority labels
- Use milestone labels for release planning

---

## 📚 Label Reference

### Full Label List

#### Priority
- `priority: critical` - Urgent, immediate attention
- `priority: high` - Important, address soon
- `priority: medium` - Normal priority
- `priority: low` - When time permits

#### Type
- `type: bug` - Fix broken functionality
- `type: feature` - Add new functionality
- `type: documentation` - Improve docs
- `type: refactor` - Improve code quality
- `type: test` - Add/improve tests
- `type: security` - Security improvements
- `type: performance` - Speed/efficiency
- `type: dependencies` - Update packages
- `type: ci/cd` - Build/deploy changes

#### Status
- `status: needs triage` - Awaiting review
- `status: in progress` - Being worked on
- `status: blocked` - Waiting on dependency
- `status: needs review` - Ready for review
- `status: on hold` - Temporarily paused

#### Component
- `component: frontend` - UI/React work
- `component: backend` - API/server work
- `component: deafauth` - Auth service
- `component: fibonrose` - Trust system
- `component: pinksync` - Real-time sync
- `component: 360magicians` - AI agents
- `component: workflow` - Workflow engine
- `component: infrastructure` - DevOps/infra

#### Accessibility
- `accessibility: deaf-first` - Deaf-First design
- `accessibility: wcag` - WCAG compliance
- `accessibility: screen reader` - SR support

#### Size
- `size: xs` - Quick fix (< 1 hour)
- `size: s` - Small task (1-3 hours)
- `size: m` - Medium task (1 day)
- `size: l` - Large task (2-3 days)
- `size: xl` - Very large (1+ week)

#### Experience
- `good first issue` - Beginner-friendly
- `help wanted` - Need help
- `mentor available` - Mentorship offered

#### Special
- `breaking change` - API/behavior change
- `needs discussion` - Needs input
- `wontfix` - Won't address
- `duplicate` - Duplicate issue
- `invalid` - Not valid
- `question` - Needs answer

#### Milestone
- `milestone: foundation` - v0.1.0
- `milestone: backend` - v0.2.0
- `milestone: realtime` - v0.3.0
- `milestone: ai` - v0.4.0
- `milestone: v1.0` - v1.0.0

#### Environment
- `env: sandbox` - Sandbox testing
- `env: staging` - Staging testing
- `env: production` - Production issue

---

## 📖 Examples

### Example 1: Bug Report

**Issue:** Login page crashes on mobile devices

**Appropriate Labels:**
```
type: bug
priority: high
component: frontend
component: deafauth
size: m
```

**Reasoning:**
- It's a bug (something broken)
- High priority (affects users)
- Frontend and auth affected
- Medium effort to fix

### Example 2: Feature Request

**Issue:** Add video feedback upload for sign language

**Appropriate Labels:**
```
type: feature
priority: medium
component: frontend
component: backend
accessibility: deaf-first
size: xl
milestone: realtime
```

**Reasoning:**
- New feature request
- Medium priority (planned feature)
- Requires frontend and backend
- Deaf-First accessibility feature
- Large effort (multiple days)
- Planned for v0.3.0 milestone

### Example 3: Documentation Update

**Issue:** Update API documentation with new endpoints

**Appropriate Labels:**
```
type: documentation
priority: medium
component: backend
size: s
good first issue
```

**Reasoning:**
- Documentation work
- Normal priority
- Backend API docs
- Small effort
- Good for new contributors

### Example 4: Security Fix

**Issue:** XSS vulnerability in form validation

**Appropriate Labels:**
```
type: security
type: bug
priority: critical
component: frontend
size: s
```

**Reasoning:**
- Security issue and bug
- Critical priority
- Frontend vulnerability
- Quick fix needed

### Example 5: Pull Request

**PR:** feat: implement OAuth 2.0 for DeafAuth

**Appropriate Labels:**
```
type: feature
component: deafauth
component: backend
status: needs review
breaking change
size: l
milestone: backend
```

**Reasoning:**
- Feature implementation
- DeafAuth and backend changes
- Ready for review
- Breaking API change
- Large effort
- Part of v0.2.0 milestone

---

## 🔍 Finding Issues by Labels

### Common Queries

**Good for beginners:**
```
is:issue is:open label:"good first issue"
```

**Help wanted:**
```
is:issue is:open label:"help wanted"
```

**Frontend bugs:**
```
is:issue is:open label:"type: bug" label:"component: frontend"
```

**High priority items:**
```
is:issue is:open label:"priority: high"
```

**Documentation tasks:**
```
is:issue is:open label:"type: documentation"
```

**Current milestone:**
```
is:issue is:open label:"milestone: backend"
```

**Quick wins (small tasks):**
```
is:issue is:open label:"size: xs" OR label:"size: s"
```

---

## 🛠️ Maintaining Labels

### For Maintainers

**Regular Maintenance:**
1. Review `status: needs triage` weekly
2. Update status labels as work progresses
3. Add priority labels to new issues
4. Remove outdated labels
5. Ensure consistent labeling

**Label Hygiene:**
- Remove duplicate labels
- Update stale status labels
- Archive completed milestone labels
- Keep descriptions up to date

**Creating New Labels:**
- Discuss with team first
- Follow naming conventions
- Choose appropriate colors
- Write clear descriptions
- Document in this guide

---

## 📞 Questions?

If you have questions about labels:
- Comment on the issue
- Ask in GitHub Discussions (when enabled)
- Refer to [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Last Updated**: 2025-12-03  
**Part of the PinkFlow Deaf-First Innovation Ecosystem**
