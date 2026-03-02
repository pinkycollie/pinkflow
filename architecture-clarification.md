mbtq.dev focus and the PinkFlow ecosystem components 
(DeafAUTH, PinkSync, FibonRose (optional), accessibility services, and partner testing network),
a multi-service, accessibility-first CI/CD + orchestration pipeline that:

Builds and tests each service independently (microservice model)
Ensures Deaf-accessible features are validated automatically (sign-language video, captions, accessible UI flows)
Supports partner onboarding into the PinkSync network for collaborative testing
Deploys to staging and production with branch-aware automation


1. Architecture Overview
mbtq.dev
│
├── services/
│   ├── deafauth/           # Authentication with Deaf accessibility features
│   ├── pinksync/           # Real-time sync & partner network
│   ├── fibonrose/          # Optional metrics & voting system
│   ├── accessibility-nodes/ # Video, captions, sign-language nodes
│
├── frontend/               # Accessible web UI
├── backend/                # API gateway / orchestration
└── workflow-system/        # PinkFlow orchestration engine


2. Local Development — Multi-Service Compose
docker-compose.local.yml
Yamlversion: "3.9"

services:
  deafauth:
    build: ./services/deafauth
    ports:
      - "5001:5000"
    env_file:
      - ./services/deafauth/.env.local
    depends_on:
      - db

  pinksync:
    build: ./services/pinksync
    ports:
      - "5002:5000"
    env_file:
      - ./services/pinksync/.env.local
    depends_on:
      - db
      - redis

  fibonrose:
    build: ./services/fibonrose
    ports:
      - "5003:5000"
    env_file:
      - ./services/fibonrose/.env.local
    depends_on:
      - db

  accessibility-nodes:
    build: ./services/accessibility-nodes
    ports:
      - "5004:5000"

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env.local
    depends_on:
      - deafauth
      - pinksync
      - fibonrose

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: mbtq
      POSTGRES_PASSWORD: mbtqpass
      POSTGRES_DB: mbtqdb
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"


3. GitHub Actions — Multi-Service CI/CD
.github/workflows/mbtq-ci.yml
Yamlname: MBTQ Multi-Service CI/CD

on:
  push:
    branches:
      - main
      - develop
      - 'feature/*'
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [deafauth, pinksync, fibonrose, accessibility-nodes, backend, frontend]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: cd services/${{ matrix.service }} && npm ci || pip install -r requirements.txt
      - run: cd services/${{ matrix.service }} && npm test || pytest

  build-and-push:
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [deafauth, pinksync, fibonrose, accessibility-nodes, backend, frontend]
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v5
        with:
          context: ./services/${{ matrix.service }}
          push: true
          tags: your-docker-user/${{ matrix.service }}:${{ github.ref_name }}


4. Accessibility Testing Integration
We can add automated accessibility tests for Deaf-friendly features:

Video accessibility: Ensure captions and sign-language overlays exist
UI accessibility: Use axe-core or pa11y in CI
Partner network simulation: Mock PinkSync partner nodes for integration tests

Example CI step:
Yaml  accessibility-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g pa11y
      - run: pa11y http://localhost:3000 --reporter cli


5. Kubernetes Deployment
We’ll use Kustomize overlays for staging and production, deploying each service independently.
Example staging overlay:
Yamlimages:
  - name: your-docker-user/deafauth
    newTag: develop
  - name: your-docker-user/pinksync
    newTag: develop
  - name: your-docker-user/fibonrose
    newTag: develop


6. Partner Testing Network

PinkSync can expose a partner registration API for testers
CI can run integration tests against partner nodes in staging
Partners can be onboarded via GitHub PRs adding their node configs


✅ Outcome:
This setup ensures mbtq.dev can:

Build and test all services in isolation and together
Validate Deaf accessibility automatically
Deploy branch-aware to staging and production
Support partner testing in the PinkSync network


