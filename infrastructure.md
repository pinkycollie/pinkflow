# 🌸 PINKFLOW Infrastructure

**Deaf‑First • Visual‑First • Governance‑Ready**

This repository contains the Infrastructure‑as‑Code (IaC) for the PinkSync / MBTQ ecosystem.

PINKFLOW is not a collection of cloud scripts. It is a **constitutionally governed infrastructure system** designed to be legible, auditable, and accessible to Deaf and Hard‑of‑Hearing developers, partners, and autonomous agents.

If you are here to "just deploy something," pause. Read this once. Everything else will make sense faster.

---

## 1. Canonical System Map

```
🔵 DeafAuth → 🌸 PinkSync → 🟣 MBTQ Agents → 🟦 VR4Deaf → 🟡 Agora → ☁️ Clouds
```

Identity flows first. Infrastructure executes second.

Clouds are execution substrates — never sources of authority.

---

## 2. Repository Structure (Non‑Negotiable)

```
infra/
 ├── environments/
 │    ├── dev/
 │    ├── staging/
 │    └── prod/
 └── modules/
```

### Rules

* `environments/` **instantiate modules only**
* `modules/` contain reusable logic
* No environment‑specific resources inside modules
* No direct resources inside environments

Violations will be rejected in review.

---

## 3. Environments

### dev

* Sandbox only
* `terraform plan` allowed
* No production credentials

### staging

* Mirrors production topology
* Used for validation and review

### prod

* No direct `terraform apply`
* Pipeline‑only deployments
* Drift detection enabled

Production is protected by design, not trust.

---

## 4. Security Doctrine

Security is enforced structurally.

**Always required:**

* Encryption at rest
* TLS / HTTPS in transit
* Secrets via Secret Manager only
* IAM scoped per service
* Cloudflare SSL at the edge

If security is optional, the module is invalid.

---

## 5. Naming & Tagging Standards

### Resource Naming

```
pinkflow-{env}-{component}-{purpose}
```

### Mandatory Tags

* `system = pinkflow`
* `layer = orchestration | identity | immersive | governance | agent | infra`
* `data_sensitivity = public | internal | private`

Resources without tags are considered unmanaged.

---

## 6. Module Contract Requirements

Every module **must** include:

* Minimal, explicit inputs
* Clear outputs (URLs, IDs, secret refs)
* `README.md`
* A **diagram** explaining the module
* Example usage

Modules without diagrams fail review automatically.

---

## 7. Multi‑Cloud Responsibility Model

### Cloudflare

* DNS
* SSL / TLS
* Global routing

### Google Cloud

* Cloud Run (PinkSync, MBTQ agents)
* GCS buckets
* Domain mappings

### AWS

* S3 (ASL datasets)
* Lambda (video pipelines)
* Media processing

### Azure

* Functions
* Storage
* Enterprise connectors

PinkSync determines execution based on latency, cost, compliance, and identity context.

---

## 8. Deaf‑First Development Norms

Infrastructure work must be **visually legible**:

* Diagrams in every PR
* Screenshots > prose
* Short sentences
* Captions on all videos
* No voice‑only explanations

Accessibility is not delegated. It is enforced.

---

## 9. Governance & Audit Readiness

This repository is audit‑ready by default:

* Changes are reviewable
* Decisions are traceable
* Logs are inspectable
* Accessibility claims are verifiable

Governance is a feature, not overhead.

---

## 10. Source of Authority

This repository implements the rules defined in:

**PINKFLOW Infrastructure Constitution (v1)**

If this README and the Constitution ever conflict, **the Constitution wins**.

---

## 11. What This Repo Is Not

* Not a cloud tutorial
* Not a certification
* Not optional guidance

This repository defines **how infrastructure is allowed to exist** inside the PinkSync ecosystem.

---

Welcome to PINKFLOW.

If you can see it, you can govern it.
