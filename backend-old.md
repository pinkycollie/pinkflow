🔌 Backend Integration Playbook

Scope: Connect the feature-complete frontend to a live, production-ready backend.
Status: Frontend ✅ Ready — Backend 🚧 Pending

🖥️ Frontend State (as of now)

Framework: React + TypeScript SPA

Role-Aware UI: Adapts by role (Developer, Researcher, Contributor)

Architecture: Component-driven, reusable, maintainable

AI: Gemini API hooks (currently mocked)

State Mgmt: Hook-based system for auth + UI

Mocks: All backend services mocked (authService, contributionService, mockFileSystem)

✅ Ready for backend endpoints — clear separation of concerns makes integration straightforward.

🛠️ Backend Tasks
1. Authentication API (replaces authService.ts)

POST /api/auth/login → Accepts DeafAuth/FibonRose/GitHub OAuth, returns JWT + User object

POST /api/auth/logout → Invalidates token

GET /api/auth/user → Returns current profile (with fibonRoseProfile)

POST /api/user/profile/sync → Sync/update FibonRoseTrustProfile

2. Workspace API (replaces mockFileSystem)

GET /api/workspace/tree → Returns file tree as FileSystemItem[]

GET /api/workspace/file?path= → Returns raw file content

PUT /api/workspace/file?path= → Updates file content

POST /api/workspace/file → Creates new file at path

POST /api/workspace/commit → Commits staged files (Git integration ideal)

3. Curation & Governance API (replaces contributionService.ts)

GET /api/governance/ballots → List all active proposals

POST /api/governance/ballots/:id/vouch → User vouches; backend validates trust score

GET /api/contributions/approved → List approved contributions

4. Real-time Backbone: PinkSync

Stack: Node.js + Socket.io (or equivalent)

Features:

Multi-user collab in PinkFlow Workspace

Real-time notifications

Live presence/status indicators

5. Gemini API Proxy (critical security step)

All Gemini API calls → proxied via backend

E.g. frontend calls: POST /api/ai/summarize

Backend attaches API key + calls Gemini API

Prevents client-side key exposure before production

⚙️ DevOps & Infra Notes

Deployment: SPA build → Vercel or Cloud Run (verify relevance per repo cleanup plan)

Secrets: Use env vars (API_KEY, JWT_SECRET, etc.) — no secrets in client code

CI/CD: GitHub Actions with staged pipeline (dev → staging → prod)

🌐 Big Picture Alignment

The frontend is the entry point to MBTQ’s Deaf-First ecosystem. Backend integration will unlock:

Trusted federated identity (DeafAuth + FibonRose)

AI-assisted workflows (Gemini proxy)

Collaborative governance (DAO-style ballots + PinkSync real-time)

➡️ Once backend endpoints are live, the platform transitions from a polished demo into a fully functional Deaf-First hub for developers, researchers, and contributors.
