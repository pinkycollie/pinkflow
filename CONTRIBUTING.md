# Contributing to PinkFlow

Thank you for your interest in contributing to PinkFlow! This document provides guidelines and instructions for contributing to the project.

## 🌟 About PinkFlow

PinkFlow is part of the MBTQ.dev Deaf-First innovation ecosystem. It serves as a process-orchestration layer for partners and collaborators, helping to transform external inputs into standardized, Deaf-First compliant processes.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Submission Guidelines](#submission-guidelines)
- [Coding Standards](#coding-standards)
- [Community and Support](#community-and-support)

---

## 🚀 Quick Start

**New to PinkFlow?** Check out our comprehensive guides:

- 📘 **[Onboarding Guide](ONBOARDING.md)** - Step-by-step guide for new contributors
- 🌿 **[Branch Naming Conventions](BRANCH_NAMING.md)** - How to name your branches
- 🏷️ **[Labels Guide](LABELS.md)** - Understanding our label system

These guides will help you get started quickly and follow our best practices.

---

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Detailed steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots if applicable
- Environment details (OS, browser, versions, etc.)

Use the bug report template when creating issues.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Examples of how it would work

Use the feature request template when creating issues.

### Contributing Code

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Commit your changes** using clear, descriptive commit messages
5. **Push to your fork** and submit a pull request

### Documentation Improvements

Documentation is crucial for the project. Contributions to improve:
- README files
- Code comments
- API documentation
- User guides
- Examples

are always welcome!

## 🛠️ Development Setup

### Prerequisites

The PinkFlow ecosystem includes multiple components. Depending on what you're working on, you may need:

- **Frontend (React + TypeScript)**:
  - Node.js (v16 or higher)
  - npm or yarn
  
- **Backend (FastAPI)**:
  - Python 3.8+
  - pip
  
- **Real-time Services (Node.js)**:
  - Node.js (v16 or higher)
  - WebSocket support

### Getting Started

1. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/PinkFlow.git
   cd PinkFlow
   ```

2. **Set up your development environment**:
   - For frontend development, navigate to the relevant directory and install dependencies
   - For backend development, set up a virtual environment and install requirements
   - See component-specific README files for detailed setup instructions

3. **Create a branch** for your work (see [Branch Naming Conventions](BRANCH_NAMING.md)):
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** and test thoroughly

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

## 📝 Submission Guidelines

### Pull Request Process

1. **Update documentation** to reflect any changes
2. **Follow the PR template** and fill out all sections
3. **Ensure CI checks pass** (automated tests, linting, etc.)
4. **Request review** from maintainers
5. **Address feedback** promptly and respectfully

### PR Title Format

Use conventional commit format (see [Branch Naming Conventions](BRANCH_NAMING.md) for details):
- `feat: add new feature`
- `fix: resolve bug in component`
- `docs: update README`
- `style: format code`
- `refactor: restructure module`
- `test: add test coverage`
- `chore: update dependencies`

For more details on branching and naming, see [BRANCH_NAMING.md](BRANCH_NAMING.md).

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs in the body when relevant

## 💻 Coding Standards

### General Principles

- Write clear, readable code
- Follow the existing code style in the repository
- Comment complex logic
- Keep functions focused and concise
- Write meaningful variable and function names

### Language-Specific Standards

**TypeScript/JavaScript**:
- Use TypeScript for type safety
- Follow ESLint configuration
- Use functional components with hooks (React)
- Prefer `const` over `let`, avoid `var`

**Python**:
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions under 50 lines when possible

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Run all tests before submitting PR
- Include both unit and integration tests when applicable

## 🌍 Community and Support

### Getting Help

- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Report bugs and request features
- **Pull Requests**: Propose changes and improvements

### Governance

PinkFlow uses a governance model aligned with the MBTQ.dev ecosystem:
- Trust-based contribution validation (FibonRose)
- Community voting on major decisions
- Transparent decision-making process

### Recognition

Contributors are recognized through:
- Credit in release notes
- Contributor listing in README
- FibonRose trust profile integration (for ecosystem participants)

## 🎯 Priority Areas

Current focus areas where contributions are especially welcome:

1. **Backend API Implementation**: Building out FastAPI services
2. **Real-time Collaboration**: PinkSync WebSocket integration
3. **Authentication**: DeafAuth implementation
4. **Documentation**: API docs, user guides, examples
5. **Testing**: Increasing test coverage
6. **Accessibility**: Ensuring Deaf-First design principles

## 📄 License

By contributing to PinkFlow, you agree that your contributions will be licensed under the same license as the project (TBD - to be defined by maintainers).

## 🙏 Thank You!

Your contributions help make PinkFlow and the MBTQ.dev ecosystem more accessible, secure, and useful for everyone. We appreciate your time and effort!

---

**Questions?** Open a discussion or reach out to the maintainers.
