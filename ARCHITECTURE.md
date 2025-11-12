# MBTQ Universe: Deaf-First DevOps Architecture

## 🏗️ Overview

This document provides a clear, actionable blueprint for the MBTQ Universe ecosystem, including Pinkflow, DeafAuth, PinkSync, 360 Magicians, and mbtq.dev. Use this as your onboarding, partner, and internal reference.

---

## 🟣 Pinkflow (dev.mbtquniverse.com)

- **Role:** DevOps control tower for all automation, CI/CD, sync, deploy, and logs
- **Location:** `dev.mbtquniverse.com`
- **Key Integrations:** GitHub, Vercel, Notion, Claude AI, PinkSync
- **Best Practice:** Keep modular, stateless, and internal (not customer-facing)

### Folder Structure
```
pinkflow/
├── src/
│   ├── cli.ts              # Main CLI entry point
│   ├── config/             # Configuration management
│   ├── services/           # Service implementations
│   └── types/              # TypeScript type definitions
├── .github/workflows/      # GitHub Actions
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── README.md
```

---

## 🔐 DeafAuth (Microservice)

- **Role:** Deaf-first authentication & identity API
- **Location:** Deploy as a container, serverless function, or cloud run (no public domain needed)
- **Key Integrations:** Any app needing auth (Pinkflow, PinkSync, 360 Magicians, partners)
- **Best Practice:** Stateless, API-first, easy to embed

### Folder Structure
```
deafauth/
├── src/
│   ├── api/                # Auth endpoints (OAuth, MFA, etc.)
│   ├── models/             # User, session, token models
│   ├── services/           # Business logic (auth, MFA, etc.)
│   └── utils/              # Helpers, encryption, etc.
├── Dockerfile
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🧬 PinkSync (Middleware/SDK)

- **Role:** Accessibility, real-time sync, and service routing layer
- **Location:** Embedded in client apps, or as a middleware service
- **Key Integrations:** All MBTQ/partner apps, Pinkflow, 360 Magicians
- **Best Practice:** Universal interface, plug-and-play, stateless

### Folder Structure
```
pinksync/
├── src/
│   ├── middleware/         # Express/Koa/Nest/Next middlewares
│   ├── sdk/                # Client SDKs (JS/TS, React, Vue, etc.)
│   ├── services/           # Accessibility, comms, sync logic
│   └── utils/              # Helpers, validators
├── package.json
├── tsconfig.json
└── README.md
```

---

## 💻 mbtq.dev (Dev Studio)

- **Role:** Code generation, repo management, CI/CD playground
- **Location:** `mbtq.dev`
- **Key Integrations:** Pinkflow, GitHub, Claude, Notion
- **Best Practice:** Source of truth for builds, tests, and codegen

### Folder Structure
```
mbtq.dev/
├── src/
│   ├── codegen/            # AI/Claude code generation logic
│   ├── templates/          # Project/app templates
│   ├── pipelines/          # CI/CD scripts and workflows
│   └── utils/              # Helpers, scaffolding
├── .github/workflows/
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🚦 Deploy Flow (End-to-End)

1. **Dev/Codegen:**
   - Code is generated or updated in `mbtq.dev` (AI, templates, manual dev)
   - Pushed to GitHub (private or public repo)

2. **Orchestration:**
   - Pinkflow (dev.mbtquniverse.com) detects push or is triggered manually
   - Runs CI/CD, syncs with Notion, triggers Vercel deploy, runs PinkSync checks

3. **Accessibility/Sync:**
   - PinkSync middleware/SDK is embedded in all apps for real-time accessibility and comms
   - Pinkflow verifies PinkSync compliance before production deploy

4. **Production:**
   - Deploys to production domains (360magicians.com, vr4deaf.org, etc.)
   - PinkSync continues to monitor and report accessibility/comms

5. **Auth:**
   - DeafAuth microservice provides authentication for all apps/services

---

## 📝 Onboarding Checklist

- [ ] Setup Pinkflow at `dev.mbtquniverse.com` with all API keys/secrets
- [ ] Deploy DeafAuth as a microservice (container/serverless)
- [ ] Integrate PinkSync SDK/middleware in all apps
- [ ] Use mbtq.dev for all codegen, repo, and CI/CD
- [ ] Document all endpoints, flows, and partner integration points

---

**For questions, updates, or to contribute, contact 360 Magicians Group.** 