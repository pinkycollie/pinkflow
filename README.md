# 🟣 Pinkflow CLI

**Deaf-first DevOps automation for the MBTQ Universe**

Pinkflow is a comprehensive CLI tool that orchestrates the entire MBTQ Universe ecosystem, providing automated code generation, deployment, documentation management, and accessibility verification.

## 🌟 Features

### 🚀 Core Automation
- **AI-Powered Code Generation** - Claude AI integration for automated project scaffolding
- **Multi-Platform Deployment** - Vercel, GitHub Actions, and custom deployment pipelines
- **Real-time Sync** - Cross-platform synchronization with GitHub, Notion, and Vercel
- **Accessibility First** - PinkSync compliance verification for Deaf-first development

### 📚 Documentation Automation
- **Mermaid Diagram Export** - Auto-export diagrams to SVG/PNG on every push
- **Documentation Validation** - Automated checks for completeness and quality
- **Notion Integration** - Real-time sync of documentation to Notion databases
- **Live Architecture Diagrams** - Interactive web-based architecture visualization

### 🛠️ Development Tools
- **Project Scaffolding** - Generate services, components, and APIs with templates
- **Validation Engine** - Comprehensive project structure and configuration validation
- **CLI Extensions** - Extensible command system for custom automation

## 🏗️ Architecture

```
MBTQ Universe Ecosystem Flow:

mbtq.dev (Frontend) 
    ↓ (Push builds)
Pinkflow CLI (Orchestration)
    ↓ (Deploy to production)
Production Domains (Vercel/Cloud)
    ↓ (Accessibility layer)
PinkSync API (Real-time communication)
    ↓ (Authentication)
DeafAuth (API auth microservice)
    ↓ (Builders & Integration)
360 Magicians Group (Development team)
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/360magicians/pinkflow.git
cd pinkflow

# Install dependencies
npm install

# Build the CLI
npm run build

# Link globally (optional)
npm link
```

### Configuration

1. Copy the environment template:
```bash
cp env.example .env
```

2. Configure your environment variables:
```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY=your_private_key

# Vercel Configuration
VERCEL_TOKEN=your_vercel_token
VERCEL_TEAM_ID=your_team_id

# Claude AI Configuration
CLAUDE_API_KEY=your_claude_api_key

# Notion Configuration
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id

# PinkSync Configuration
PINKFLOW_API_URL=https://api.pinksync.dev
PINKFLOW_API_KEY=your_pinksync_api_key
```

## 📖 CLI Commands

### Core Commands

```bash
# Sync data across all platforms
pinkflow sync [--all] [--notion] [--github] [--vercel]

# Deploy project to Vercel
pinkflow deploy <project> [--staging] [--prod] [--tag <tag>]

# Build new project with Claude AI
pinkflow build <name> [--framework <framework>] [--database <database>] [--auth <auth>] [--realtime <realtime>] [--ui <ui>] [--features <features>]

# View sync and deployment logs
pinkflow log [--today] [--module <module>] [--action <action>]

# Show system status
pinkflow status

# Verify PinkSync accessibility compliance
pinkflow pinksync <url> [--tag <tag>]
```

### Documentation Commands

```bash
# Scaffold new service or component
pinkflow scaffold <type> <name> [--framework <framework>] [--template <template>] [--output <path>]

# Validate project structure and documentation
pinkflow validate [--docs] [--structure] [--config] [--all]
```

### Available Scaffold Types

- **service** - Generate a new service with TypeScript, tests, and documentation
- **component** - Create React/Vue components with props and tests
- **api** - Scaffold REST API endpoints with controllers and services
- **auth** - Generate authentication modules and middleware

### Examples

```bash
# Generate a new user service
pinkflow scaffold service user-service --framework nextjs --output ./services

# Create a React component
pinkflow scaffold component UserProfile --framework react

# Build a full-stack app
pinkflow build my-app --framework nextjs --database neon --auth deafauth --realtime socketio --ui shadcn

# Deploy to production
pinkflow deploy my-app --prod --tag v1.0.0

# Validate everything
pinkflow validate --all
```

## 🔄 Automation Workflows

### GitHub Actions

The project includes several automated workflows:

1. **Mermaid Export** (`.github/workflows/docs-mermaid-export.yml`)
   - Automatically exports Mermaid diagrams to SVG/PNG
   - Triggers on markdown file changes
   - Commits exported diagrams back to repository

2. **Documentation Validation** (`.github/workflows/docs-validate.yml`)
   - Validates documentation completeness
   - Checks for required files and structure
   - Fails PRs with missing documentation

3. **Notion Sync** (`.github/workflows/notion-sync.yml`)
   - Syncs key documentation to Notion
   - Updates existing pages or creates new ones
   - Maintains documentation versioning

### Scripts

```bash
# Export Mermaid diagrams
npm run docs:export

# Validate documentation
npm run docs:validate

# Sync to Notion
npm run docs:sync
```

## 🏗️ Project Structure

```
pinkflow/
├── src/
│   ├── cli.ts                 # Main CLI entry point
│   ├── config/
│   │   └── index.ts          # Configuration management
│   ├── services/
│   │   ├── build.ts          # AI-powered project building
│   │   ├── claude.ts         # Claude AI integration
│   │   ├── github.ts         # GitHub API integration
│   │   ├── notion.ts         # Notion API integration
│   │   ├── pinksync.ts       # PinkSync accessibility
│   │   ├── scaffold.ts       # Project scaffolding
│   │   ├── sync.ts           # Cross-platform sync
│   │   ├── validation.ts     # Project validation
│   │   └── vercel.ts         # Vercel deployment
│   └── types/
│       └── index.ts          # TypeScript type definitions
├── docs/
│   ├── architecture-diagram.html  # Live architecture diagram
│   └── diagrams/                  # Exported Mermaid diagrams
├── scripts/
│   ├── export-mermaid.js     # Mermaid export script
│   ├── validate-docs.js      # Documentation validation
│   └── sync-notion.js        # Notion sync script
├── .github/workflows/        # GitHub Actions workflows
└── package.json
```

## 🎨 Live Architecture Diagram

Access the interactive architecture diagram at:
```
docs/architecture-diagram.html
```

Features:
- **Multiple Views** - Ecosystem, Deployment, Services, Data Flow
- **Interactive Controls** - Theme switching, animation toggles
- **Export Options** - Download diagrams as SVG/PNG
- **Real-time Updates** - Auto-refresh for live data

## 🔧 Development

### Building

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Adding New Commands

1. Create a new service in `src/services/`
2. Add the command to `src/cli.ts`
3. Update types in `src/types/index.ts`
4. Add tests and documentation

### Extending Templates

1. Add new template types to `ScaffoldService`
2. Create template files with placeholders
3. Update the CLI help documentation

## 🌐 Ecosystem Integration

### MBTQ Universe Components

- **mbtq.dev** - Main frontend application (Nuxt 3/Next.js)
- **DeafAuth** - Authentication microservice
- **PinkSync** - Real-time communication and accessibility layer
- **360 Magicians Group** - Development and integration team

### External Services

- **Vercel** - Deployment and hosting
- **GitHub** - Version control and CI/CD
- **Notion** - Documentation and project management
- **Claude AI** - Code generation and documentation
- **Neon.tech** - Database hosting
- **Socket.io** - Real-time communication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Development Guidelines

- Follow TypeScript best practices
- Add JSDoc comments for all functions
- Include Mermaid diagrams for complex flows
- Ensure PinkSync accessibility compliance
- Test all CLI commands before submitting

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: [GitHub Issues](https://github.com/360magicians/pinkflow/issues)
- **Discussions**: [GitHub Discussions](https://github.com/360magicians/pinkflow/discussions)

## 🎯 Roadmap

- [ ] **Advanced AI Features** - Multi-model code generation
- [ ] **Plugin System** - Extensible CLI with custom plugins
- [ ] **Visual Builder** - GUI for non-technical users
- [ ] **Multi-language Support** - Internationalization
- [ ] **Advanced Analytics** - Deployment and usage metrics
- [ ] **Team Collaboration** - Multi-user workflows and permissions

---

**Built with ❤️ by the 360 Magicians Group for the Deaf community** 