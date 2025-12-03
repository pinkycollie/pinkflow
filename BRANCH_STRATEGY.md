# Branch Strategy Quick Reference

A visual guide to PinkFlow's branching strategy and workflow.

---

## 🌲 Branch Structure

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                        MAIN BRANCH                          │
│                   (Production Ready)                        │
│                                                             │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │             │             │             │             │ │
│  │  release/   │  feature/   │  bugfix/    │  hotfix/    │ │
│  │  v0.2.0     │  new-feat   │  fix-issue  │  urgent     │ │
│  │             │             │             │             │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Branch Types at a Glance

| Prefix | Purpose | Base | Lifetime | Example |
|--------|---------|------|----------|---------|
| `feature/` | New features | main | Until merged | `feature/oauth-login` |
| `bugfix/` | Bug fixes | main | Until merged | `bugfix/validation-error` |
| `hotfix/` | Critical fixes | main | Immediate | `hotfix/security-patch` |
| `release/` | Prepare release | main | Until deployed | `release/v0.2.0` |
| `docs/` | Documentation | main | Until merged | `docs/api-guide` |
| `refactor/` | Code cleanup | main | Until merged | `refactor/auth-module` |
| `test/` | Add tests | main | Until merged | `test/unit-tests` |
| `chore/` | Maintenance | main | Until merged | `chore/dependencies` |
| `experiment/` | Experiments | any | Temporary | `experiment/new-tech` |

---

## 🔄 Typical Workflow

```
Step 1: Start from Main
┌─────────────────┐
│      main       │
└────────┬────────┘
         │
         │ git checkout main
         │ git pull origin main
         │
         ▼

Step 2: Create Feature Branch
┌─────────────────┐
│  feature/login  │
└────────┬────────┘
         │
         │ git checkout -b feature/login
         │
         ▼

Step 3: Make Changes
┌─────────────────┐
│   Develop       │
│   Commit        │
│   Test          │
└────────┬────────┘
         │
         │ git add .
         │ git commit -m "feat: add login"
         │
         ▼

Step 4: Push & PR
┌─────────────────┐
│   Create PR     │
└────────┬────────┘
         │
         │ git push origin feature/login
         │ Open PR on GitHub
         │
         ▼

Step 5: Review & Merge
┌─────────────────┐
│   Review        │
│   Approve       │
│   Merge         │
└────────┬────────┘
         │
         ▼

Step 6: Cleanup
┌─────────────────┐
│  Delete Branch  │
└─────────────────┘
```

---

## 📊 PinkFlow Ecosystem Branches

### Component-Specific Branches

```
DeafAuth Component
├── feature/deafauth-oauth
├── bugfix/deafauth-session
└── test/deafauth-auth-flow

FibonRose Component
├── feature/fibonrose-scoring
├── bugfix/fibonrose-validation
└── refactor/fibonrose-engine

PinkSync Component
├── feature/pinksync-websocket
├── bugfix/pinksync-reconnect
└── test/pinksync-realtime

360Magicians Component
├── feature/magicians-ai-proxy
├── bugfix/magicians-api
└── experiment/magicians-gemini

Workflow System
├── feature/workflow-nodes
├── bugfix/workflow-execution
└── refactor/workflow-builder
```

---

## 🎨 Visual Branch Timeline

```
main ──────●──────●──────●──────●──────●──────●────────▶
           │      │      │      │      │      │
           │      │      │      │      │      └─ Merge PR #3
           │      │      │      │      │
           │      │      │      │      └─ Merge PR #2
           │      │      │      │
           │      │      │      └─ Release v0.2.0
           │      │      │
           │      │      └─ Merge PR #1
           │      │
           │      └─ Create release branch
           │
           └─ Start development

feature/new-feature ──●──●──●──●──PR──▶ merged
                      │  │  │  │
                      └──┴──┴──┴─ commits

bugfix/fix-issue ──●──●──PR──▶ merged
                   │  │
                   └──┴─ quick fix

hotfix/urgent ──●──PR──▶ merged immediately
                │
                └─ critical fix
```

---

## 🔍 Branch Naming Patterns

### Good Examples ✅

```bash
# Features
feature/oauth-integration
feature/360-video-feedback
feature/deafauth-sso

# Bug Fixes
bugfix/login-timeout
bugfix/42-api-error
bugfix/validation-crash

# Documentation
docs/update-readme
docs/api-reference
docs/onboarding-guide

# Refactoring
refactor/auth-module
refactor/workflow-engine
refactor/database-queries

# Tests
test/unit-tests-auth
test/integration-workflow
test/e2e-login-flow

# Chores
chore/update-dependencies
chore/ci-pipeline
chore/github-actions

# Hotfixes
hotfix/security-xss
hotfix/data-loss-bug
hotfix/critical-crash
```

### Bad Examples ❌

```bash
# Too vague
new-feature        # What feature?
fix               # Fix what?
update            # Update what?

# Wrong format
Feature/NewStuff  # Use lowercase
my_branch         # Use hyphens, not underscores
john-work         # Describe work, not person

# Too long
feature/add-the-new-oauth-integration-with-google-and-facebook-login

# No prefix
oauth-integration  # Missing type prefix
```

---

## 💡 Quick Decision Tree

```
What are you working on?
│
├─ New Feature?
│  └─ Use: feature/your-feature-name
│
├─ Fixing a Bug?
│  ├─ Critical/Production?
│  │  └─ Use: hotfix/fix-description
│  └─ Not Critical?
│     └─ Use: bugfix/fix-description
│
├─ Updating Docs?
│  └─ Use: docs/doc-description
│
├─ Refactoring Code?
│  └─ Use: refactor/refactor-description
│
├─ Adding Tests?
│  └─ Use: test/test-description
│
├─ Maintenance Work?
│  └─ Use: chore/task-description
│
└─ Experimenting?
   └─ Use: experiment/experiment-name
```

---

## 🚦 Branch Protection Status

```
MAIN BRANCH (Highly Protected)
┌────────────────────────────────┐
│ ✓ Require PR reviews (2+)      │
│ ✓ Require status checks        │
│ ✓ Require up-to-date branch    │
│ ✓ Require conversation resolved│
│ ✗ No direct commits             │
│ ✗ No force push                 │
│ ✗ No deletions                  │
└────────────────────────────────┘

RELEASE BRANCHES (Protected)
┌────────────────────────────────┐
│ ✓ Require PR reviews (1+)      │
│ ✓ Require status checks        │
│ ✗ No force push                 │
└────────────────────────────────┘

FEATURE BRANCHES (Standard)
┌────────────────────────────────┐
│ ✓ Can be rebased                │
│ ✓ Can be force pushed           │
│ ✓ Deleted after merge           │
└────────────────────────────────┘
```

---

## 📈 Branch Lifecycle Stages

```
┌──────────┐
│ Created  │ ◄── git checkout -b feature/name
└────┬─────┘
     │
     ▼
┌──────────┐
│  Active  │ ◄── Making commits, pushing changes
└────┬─────┘
     │
     ▼
┌──────────┐
│ PR Open  │ ◄── Pull request created
└────┬─────┘
     │
     ▼
┌──────────┐
│ Review   │ ◄── Under code review
└────┬─────┘
     │
     ▼
┌──────────┐
│ Approved │ ◄── Reviews approved
└────┬─────┘
     │
     ▼
┌──────────┐
│  Merged  │ ◄── Merged to main
└────┬─────┘
     │
     ▼
┌──────────┐
│ Deleted  │ ◄── Branch cleaned up
└──────────┘
```

---

## 🎯 Component Prefix Examples

When working on specific PinkFlow components:

```
DeafAuth:
├─ feature/deafauth-jwt-refresh
├─ bugfix/deafauth-token-expiry
└─ test/deafauth-oauth-flow

FibonRose:
├─ feature/fibonrose-trust-score
├─ bugfix/fibonrose-governance
└─ refactor/fibonrose-validation

PinkSync:
├─ feature/pinksync-websocket-v2
├─ bugfix/pinksync-connection
└─ test/pinksync-realtime-sync

360Magicians:
├─ feature/magicians-gemini-api
├─ bugfix/magicians-workflow
└─ experiment/magicians-auto-code

Workflow:
├─ feature/workflow-conditional
├─ bugfix/workflow-execution
└─ refactor/workflow-builder
```

---

## 🔧 Common Commands

```bash
# Create new branch
git checkout -b feature/your-feature

# Switch branches
git checkout branch-name

# List all branches
git branch -a

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Sync with main
git checkout main
git pull origin main
git checkout your-branch
git merge main

# Rebase on main
git rebase main

# Push new branch
git push -u origin branch-name

# Force push (use carefully!)
git push --force-with-lease
```

---

## 📱 Mobile-Friendly Cheat Sheet

```
CREATE: git checkout -b TYPE/name
TYPES:
  feature/  - new stuff
  bugfix/   - fix bug
  hotfix/   - urgent fix
  docs/     - documentation
  refactor/ - cleanup
  test/     - tests
  chore/    - maintenance

NAMING:
  ✓ lowercase
  ✓ use-hyphens
  ✓ descriptive
  ✗ no_underscores
  ✗ NoCapitals

WORKFLOW:
  1. Create branch
  2. Make changes
  3. Commit often
  4. Push to fork
  5. Create PR
  6. Get reviewed
  7. Merge!
```

---

## 📚 Related Documentation

- 📘 [Full Branch Naming Guide](BRANCH_NAMING.md)
- 🏷️ [Labels Guide](LABELS.md)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)
- 🚀 [Onboarding Guide](ONBOARDING.md)

---

**Last Updated**: 2025-12-03  
**Part of the PinkFlow Deaf-First Innovation Ecosystem**
