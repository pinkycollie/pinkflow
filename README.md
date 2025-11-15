# PinkFlow – Deaf-First Innovation Ecosystem

[![CI/CD Pipeline](https://github.com/pinkycollie/PinkFlow/actions/workflows/basic.yml/badge.svg)](https://github.com/pinkycollie/PinkFlow/actions/workflows/basic.yml)
[![CodeQL](https://github.com/pinkycollie/PinkFlow/actions/workflows/codeql.yml/badge.svg)](https://github.com/pinkycollie/PinkFlow/actions/workflows/codeql.yml)
[![License](https://img.shields.io/badge/license-TBD-blue.svg)](LICENSE)

### 🚀 Status: Auto-Deploy System Complete ✅

PinkFlow (part of MBTQ.dev) is a **Deaf-First ecosystem** built to empower entrepreneurs, researchers, and creators with AI-driven, accessible business tools. It is designed around the **Idea → Build → Grow → Managed** lifecycle and powered by **MagicianCore** and the **360Magicians** suite.

**New**: PinkFlow now includes a complete **Auto-Deploy System** for provisioning React applications when customers purchase through Stripe. [Learn more →](#auto-deploy-system)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Getting Started](#-getting-started)
- [Use Cases](#-use-cases)
- [Architecture](#-architecture)
- [Development](#-development)
- [Contributing](#-contributing)
- [Security](#-security)
- [Community](#-community)
- [License](#-license)

---

## 🌐 Overview

PinkFlow is a process-orchestration layer for partners and collaborators who don't yet have technical infrastructure. It acts as a "fresh coat" system, onboarding them through streamlined pathways, running them through MBTQ.dev's validation, and giving them clean outputs they can use to integrate back into the ecosystem.

### Key Principles

- **Deaf-First Design**: Built with accessibility at the core, prioritizing visual and asynchronous communication
- **Trust-Based Governance**: Using FibonRose for contributor validation and ethical decision-making
- **Federated Identity**: DeafAuth provides unified authentication across the ecosystem
- **Real-time Collaboration**: PinkSync enables multi-user collaboration with WebSocket support
- **AI-Assisted Workflows**: 360Magicians provide intelligent business automation

---

## ✨ Features

### Current Features

- **Auto-Deploy System**: Complete system for provisioning React apps via Stripe purchases ✅ **NEW**
  - Stripe webhook integration with signature verification
  - Automated GitHub repository creation from templates
  - Vercel project setup and deployment
  - Complete CI/CD pipelines
  - [Learn more →](#auto-deploy-system)
- **Role-Based UI**: Adapts interface based on user role (Developer, Researcher, Contributor)
- **Component-Driven Architecture**: Modular, maintainable React + TypeScript SPA
- **Mocked Services**: Full frontend functionality with mock backend for development
- **AI Integration Hooks**: Ready for Gemini API integration via secure backend proxy
- **Workspace Management**: File tree navigation and editing capabilities
- **Governance System**: Proposal voting and contribution tracking

### Planned Features

- **Live Backend Integration**: FastAPI services for authentication, workspace, and governance
- **Real-time Sync**: PinkSync WebSocket service for multi-user collaboration
- **AI Proxy**: Secure backend proxy for AI API calls
- **Git Integration**: Version control for workspace changes
- **Trust Profiles**: FibonRose integration for contributor trust scoring
- **Notification System**: Real-time updates and alerts

---

## 🚀 Getting Started

### Prerequisites

Depending on which component you're working with:

**Frontend (React + TypeScript)**:
- Node.js v16 or higher
- npm or yarn

**Backend (FastAPI)**:
- Python 3.8+
- pip
- Virtual environment tool (venv or virtualenv)

**Real-time Services (Node.js)**:
- Node.js v16 or higher
- WebSocket support

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pinkycollie/PinkFlow.git
   cd PinkFlow
   ```

2. **Explore the structure**:
   ```bash
   # View repository structure
   ls -la
   
   # Read component documentation
   cat overview
   cat backend.md
   ```

3. **Set up development environment** (component-specific):
   
   See component README files for detailed setup instructions.

### Environment Variables

Create appropriate `.env` files for different components:

```bash
# Example for backend services
GEMINI_API_KEY=your_api_key
JWT_SECRET=your_jwt_secret
DATABASE_URL=your_database_url

# Example for frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:3001
```

**⚠️ Never commit `.env` files to version control!**

---

## 🎯 Use Cases

### For Developers

- **Build Accessible Applications**: Leverage Deaf-First design patterns
- **Integrate with MBTQ Ecosystem**: Use DeafAuth, FibonRose, and PinkSync services
- **Collaborate in Real-time**: Work with distributed teams using PinkSync
- **Automate Workflows**: Utilize 360Magicians AI agents

### For Researchers

- **Study Deaf-First Design**: Access implementation examples and patterns
- **Analyze Trust Systems**: Explore FibonRose governance model
- **Test Accessibility**: Evaluate accessibility features and compliance

### For Contributors

- **Participate in Governance**: Vote on proposals and curate contributions
- **Build Trust Profile**: Earn validation through FibonRose system
- **Share Knowledge**: Contribute documentation, code, and feedback

### For Partners

- **Onboard Smoothly**: Use PinkFlow's transitional wrapper for integration
- **Validate Ideas**: Run concepts through MBTQ.dev's validation process
- **Access Ecosystem**: Connect to the broader Deaf-First innovation hub

---

## 🏗️ Architecture

* **MBTQ.dev Frontend (Pinkflow UI)**

  * React + TypeScript SPA
  * Role-based UI (Developer, Researcher, Contributor)
  * Component-driven architecture
  * Mocked backend services (ready for API swap-in)
  * Gemini API integration (to be proxied securely via backend)

* **MBTQ FastAPI Backend (Scaffolded)**

  * Modular services:

    * **DeafAuth** (Identity & Authentication)
    * **PinkSync** (Real-time sync & notifications)
    * **FibonRose** (Trust & Ethics Engine)
    * **360Magicians** (AI Business Agents)
  * SQLAlchemy models for unified schema
  * API routers & placeholder services
  * JSON schema contract (`build.json`)

* **PinkSync Node.js Service**

  * WebSocket backbone for real-time collaboration
  * Powers PinkFlow multi-user workspace

* **MagicianCore Agents**

  * AI-driven service agents handling lifecycle: Idea → Build → Grow → Managed
  * Connected to `business-magician-api`

### Technology Stack

**Frontend**:
- React 18+
- TypeScript
- Modern hooks-based architecture

**Backend**:
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL/Cloud SQL

**Real-time**:
- Node.js
- Socket.io / WebSockets

**Infrastructure**:
- Google Cloud Platform
- Cloud Run for services
- Vercel for frontend and auto-deployed apps
- GitHub for version control and CI/CD

---

## 🚀 Auto-Deploy System

### Overview

PinkFlow includes a complete auto-deploy system that automatically provisions and deploys React applications when customers make purchases through Stripe.

### How It Works

```
Customer Purchase → Stripe Webhook → GitHub Repo Creation → Vercel Deployment → Live App
```

1. **Customer purchases** a plan through Stripe Checkout
2. **Stripe sends webhook** to PinkFlow with plan details
3. **GitHub repository created** from template, private and configured
4. **Vercel project created** and deployed automatically
5. **Customer receives** repository access and live app URL

### Key Features

- ✅ **Stripe Integration**: Webhook handling with signature verification
- ✅ **GitHub Provisioning**: Automated repository creation from templates
- ✅ **Vercel Deployment**: Automatic project setup and deployment
- ✅ **CI/CD Pipelines**: Complete GitHub Actions workflows
- ✅ **Security First**: All workflows have minimal permissions, 0 vulnerabilities
- ✅ **Comprehensive Documentation**: 2,100+ lines of setup guides and references

### Documentation

- **[AUTODEPLOY.md](AUTODEPLOY.md)** - Complete setup guide and architecture
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Step-by-step integration instructions
- **[SECRETS_REFERENCE.md](SECRETS_REFERENCE.md)** - Environment variables and security
- **[AUTODEPLOY_CHECKLIST.md](AUTODEPLOY_CHECKLIST.md)** - Implementation checklist (100+ items)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual architecture diagrams
- **[IMPLEMENTATION_DETAILS.md](IMPLEMENTATION_DETAILS.md)** - Technical implementation details

### Quick Start

1. **Configure Environment Variables**
   ```bash
   cp .env.example .env.local
   # Fill in Stripe, GitHub, and Vercel credentials
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Test Locally**
   ```bash
   npm run dev
   # Use Stripe CLI to forward webhooks
   ```

4. **Deploy to Production**
   ```bash
   npm run build
   vercel --prod
   ```

### Template Repository

The `template-nextjs-app/` directory contains a complete Next.js application template that is used for provisioning new repositories. It includes:

- Next.js 14 with TypeScript
- GitHub Actions workflows
- Vercel deployment configuration
- Security best practices
- Accessibility features

### Security

✅ **CodeQL Scan**: 0 vulnerabilities  
✅ **All workflows**: Minimal explicit permissions  
✅ **Stripe webhooks**: Signature verification  
✅ **Secrets**: Best practices documented, none in code

---

## 💻 Development

### Project Structure

```
PinkFlow/
├── .github/              # GitHub configuration
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   ├── workflows/        # CI/CD workflows
│   ├── dependabot.yml    # Dependency updates
│   └── PULL_REQUEST_TEMPLATE.md
├── CLI                   # CLI tools (PowerShell + Bash)
├── DeafAUTH             # Authentication service
├── Fibonrose            # Trust & ethics engine
├── IDE                  # IDE integrations
├── data sync            # Data synchronization
├── magicians            # AI agents
├── overview             # Project overview
├── backend.md           # Backend documentation
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
├── CODE_OF_CONDUCT.md   # Community standards
├── SECURITY.md          # Security policy
└── .gitignore           # Git ignore rules
```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the coding standards in [CONTRIBUTING.md](CONTRIBUTING.md)
   - Write tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Run linters
   # Run unit tests
   # Run integration tests
   # Test manually
   ```

4. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: your descriptive commit message"
   git push origin feature/your-feature-name
   ```

5. **Create a pull request**:
   - Use the PR template
   - Link related issues
   - Request review from maintainers

### Coding Standards

- **TypeScript/JavaScript**: Follow ESLint configuration, use TypeScript for type safety
- **Python**: Follow PEP 8, use type hints, write docstrings
- **Comments**: Explain complex logic, avoid obvious comments
- **Testing**: Write tests for new features, maintain coverage
- **Accessibility**: Follow WCAG 2.1 Level AA, test with screen readers

### Running Tests

```bash
# Frontend tests (when implemented)
npm test

# Backend tests (when implemented)
pytest

# E2E tests (when implemented)
npm run test:e2e
```

---

## 🤝 Contributing

We welcome contributions from everyone! Here's how you can help:

### Ways to Contribute

- **Report bugs**: Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Suggest features**: Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- **Improve documentation**: Use the [documentation template](.github/ISSUE_TEMPLATE/documentation.md)
- **Submit code**: Follow the [pull request process](CONTRIBUTING.md#pull-request-process)
- **Review PRs**: Help review and test pull requests
- **Join discussions**: Participate in GitHub Discussions (when enabled)

### Quick Contribution Guide

1. Read the [Code of Conduct](CODE_OF_CONDUCT.md)
2. Read the [Contributing Guidelines](CONTRIBUTING.md)
3. Find an issue to work on or create a new one
4. Fork the repository and create a branch
5. Make your changes following our standards
6. Submit a pull request

### Recognition

Contributors are recognized through:
- Credit in release notes
- Contributor listing
- FibonRose trust profile (for ecosystem participants)

---

## 🔒 Security

Security is a top priority for PinkFlow. We implement:

- **Authentication**: Secure identity management via DeafAuth
- **Authorization**: Role-based access control
- **Data Protection**: Encryption in transit and at rest
- **API Security**: Backend proxy for sensitive operations
- **Code Scanning**: Automated security analysis with CodeQL
- **Dependency Updates**: Automated updates via Dependabot

### Reporting Vulnerabilities

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Review our [Security Policy](SECURITY.md)
3. Report via GitHub Security Advisories
4. Or contact maintainers directly

See [SECURITY.md](SECURITY.md) for detailed security information.

---

## 👥 Community

### Get Involved

- **GitHub Discussions**: Ask questions, share ideas (when enabled)
- **Issues**: Report bugs, request features
- **Pull Requests**: Contribute code and documentation

### Governance

PinkFlow uses a trust-based governance model:
- **FibonRose**: Trust validation for contributors
- **Community Voting**: Major decisions made collectively
- **Transparent Process**: Open discussion and decision-making

---

## 📌 Current Frontend State

✅ Feature-complete for MVP scope
✅ Mocked services allow testing without backend
✅ Role-based components functional
✅ Ready for backend API integration

Next step: Replace mocked data with live API calls.

---

## 📌 Backend API Tasks

1. **Authentication API**

   * `POST /api/auth/login` → JWT + User object
   * `POST /api/auth/logout` → Invalidate session
   * `GET /api/auth/user` → Return current profile
   * `POST /api/user/profile/sync` → Sync FibonRose trust profile

2. **Workspace API**

   * `GET /api/workspace/tree` → File structure
   * `GET /api/workspace/file?path=` → File content
   * `PUT /api/workspace/file?path=` → Update file
   * `POST /api/workspace/file` → Create file
   * `POST /api/workspace/commit` → Commit changes (Git integration planned)

3. **Governance & Curation API**

   * `GET /api/governance/ballots` → Active proposals
   * `POST /api/governance/ballots/:id/vouch` → Vouch with trust validation
   * `GET /api/contributions/approved` → Approved contributions

4. **PinkSync Service**

   * Socket.io or equivalent for multi-user collaboration
   * Frontend hooks already prepared to connect

5. **Gemini API Proxy**

   * Secure backend proxy for Gemini API
   * Prevents exposing API key on client side

---

## 📌 Deployment Notes

* **Frontend**: Deployable on Vercel or Cloud Run (current: Vercel staging, may migrate fully to GCP).
* **Backend**: FastAPI services structured for Cloud Run + Cloud SQL.
* **Real-time (PinkSync)**: Node.js service deployable on Cloud Run with WebSocket support.
* **Environment variables**: Required for Gemini API, Auth secrets, DB URLs.

### Deployment Checklist

- [ ] Configure environment variables
- [ ] Set up database (Cloud SQL)
- [ ] Configure secrets in Google Cloud
- [ ] Set up CI/CD pipeline
- [ ] Enable monitoring and logging
- [ ] Configure domain and SSL
- [ ] Set up backup strategy

---

## 🧑‍🤝‍🧑 Team Instructions

* **Frontend Developers**: Replace mocked services with real API calls once endpoints are live.
* **Backend Engineers**: Implement service logic inside FastAPI scaffolds, connect to DB, and expose APIs.
* **DevOps**: Configure secrets in Google Cloud, ensure CI/CD pipeline for both frontend & backend.
* **Contributors**: Use `pinkflow` workspace as your entry point – governance, contributions, and code review run through MBTQ.dev.

---

## 🌍 Vision

MBTQ.dev is not just another SaaS – it’s a **Deaf-First innovation hub**. With **unified identity (DeafAuth)**, **trusted governance (FibonRose)**, **real-time sync (PinkSync)**, and **business AI agents (360Magicians)**, this ecosystem creates the infrastructure for accessible, compliant, and scalable Deaf-led entrepreneurship globally.

### Mission

To empower Deaf entrepreneurs, researchers, and creators with accessible, AI-driven tools that respect their communication preferences and cultural values.

### Values

- **Accessibility First**: Visual, text-based, asynchronous by default
- **Trust & Ethics**: FibonRose-validated governance
- **Innovation**: AI-assisted workflows for all
- **Inclusion**: Deaf perspectives in every design decision
- **Transparency**: Open processes and clear communication

---

## 📄 License

TBD - License to be defined by maintainers.

---

## 🙏 Acknowledgments

Thank you to all contributors, supporters, and the Deaf community for making this project possible!

---

## 📞 Contact

- **Repository**: [github.com/pinkycollie/PinkFlow](https://github.com/pinkycollie/PinkFlow)
- **Issues**: [Report a bug or request a feature](https://github.com/pinkycollie/PinkFlow/issues)
- **Security**: See [SECURITY.md](SECURITY.md)

---

**Built with ❤️ by the Deaf-First community**
