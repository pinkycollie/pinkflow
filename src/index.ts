/* PinkFlow SDK - deterministic, audit-first, Deaf-first (visual-first) */

import { z } from "zod";
import crypto from "node:crypto";

/** ---------- Types (authoritative) ---------- */

export type ISO8601 = string;

export type PinkFlowEnv = "development" | "staging" | "production";

export type ConsentCategory = "Essential" | "Functional" | "Analytics" | "AI" | "Marketing";

export type DataClass = "pii" | "metadata" | "logs" | "embeddings" | "none";

export type PinkFlowEventType =
  | "pinkflow.workflow.validate"
  | "pinkflow.workflow.run.requested"
  | "pinkflow.workflow.run.started"
  | "pinkflow.workflow.run.succeeded"
  | "pinkflow.workflow.run.failed"
  | "pinkflow.audit.recorded";

export interface PinkFlowContext {
  tenant_id: string;
  env: PinkFlowEnv;
  correlation_id: string;
  request_id: string;
  idempotency_key?: string;
  vde_id?: string; // Verified Deployment Event ID (optional)
  x402_id?: string; // critical ops governance id (optional)
}

export interface PinkFlowEnvelope<TPayload> {
  spec_version: "1.0";
  event_type: PinkFlowEventType;
  occurred_at: ISO8601;

  context: PinkFlowContext;

  consent: {
    category: ConsentCategory;
    version: string; // e.g. "2026-01"
  };

  data_class: DataClass;

  payload: TPayload;
}

/** ---------- Validation (non-negotiable) ---------- */

const envSchema = z.enum(["development", "staging", "production"]);

const contextSchema = z.object({
  tenant_id: z.string().min(1),
  env: envSchema,
  correlation_id: z.string().min(8),
  request_id: z.string().min(8),
  idempotency_key: z.string().min(8).optional(),
  vde_id: z.string().min(8).optional(),
  x402_id: z.string().min(8).optional(),
});

const envelopeSchema = z.object({
  spec_version: z.literal("1.0"),
  event_type: z.string().min(1),
  occurred_at: z.string().min(10),
  context: contextSchema,
  consent: z.object({
    category: z.enum(["Essential", "Functional", "Analytics", "AI", "Marketing"]),
    version: z.string().min(1),
  }),
  data_class: z.enum(["pii", "metadata", "logs", "embeddings", "none"]),
  payload: z.unknown(),
});

/** ---------- Utilities ---------- */

export function isoNow(): ISO8601 {
  return new Date().toISOString();
}

export function id(prefix: string): string {
  return `${prefix}_${crypto.randomUUID()}`;
}

export function sha256(input: string): string {
  return crypto.createHash("sha256").update(input).digest("hex");
}

/** ---------- Logger (structured, no secrets) ---------- */

export type LogLevel = "debug" | "info" | "warn" | "error";

export interface Logger {
  log(level: LogLevel, msg: string, fields?: Record<string, unknown>): void;
}

export const consoleLogger: Logger = {
  log(level, msg, fields = {}) {
    const line = {
      ts: isoNow(),
      level,
      msg,
      ...fields,
    };
    // One-line JSON logs (ship to Fibonrose later)
    process.stdout.write(JSON.stringify(line) + "\n");
  },
};

/** ---------- PinkFlow Client ---------- */

export interface PinkFlowClientOptions {
  baseUrl: string; // e.g. https://api.mbtq.dev/pinkflow/v1
  tenantId: string;
  env: PinkFlowEnv;
  consentVersion: string;
  logger?: Logger;
}

export class PinkFlowClient {
  private readonly baseUrl: string;
  private readonly tenantId: string;
  private readonly env: PinkFlowEnv;
  private readonly consentVersion: string;
  private readonly logger: Logger;

  constructor(opts: PinkFlowClientOptions) {
    this.baseUrl = opts.baseUrl.replace(/\/+$/, "");
    this.tenantId = opts.tenantId;
    this.env = opts.env;
    this.consentVersion = opts.consentVersion;
    this.logger = opts.logger ?? consoleLogger;
  }

  makeContext(partial?: Partial<PinkFlowContext>): PinkFlowContext {
    const ctx: PinkFlowContext = {
      tenant_id: this.tenantId,
      env: this.env,
      correlation_id: partial?.correlation_id ?? id("corr"),
      request_id: partial?.request_id ?? id("req"),
      idempotency_key: partial?.idempotency_key,
      vde_id: partial?.vde_id,
      x402_id: partial?.x402_id,
    };
    return contextSchema.parse(ctx);
  }

  envelope<TPayload>(input: Omit<PinkFlowEnvelope<TPayload>, "spec_version" | "occurred_at">): PinkFlowEnvelope<TPayload> {
    const envlp: PinkFlowEnvelope<TPayload> = {
      spec_version: "1.0",
      occurred_at: isoNow(),
      ...input,
    };
    // Validate whole envelope shape
    envelopeSchema.parse(envlp);
    return envlp;
  }

  async validateWorkflow(args: { name: string; source: string; context?: Partial<PinkFlowContext> }) {
    const ctx = this.makeContext(args.context);
    const event = this.envelope({
      event_type: "pinkflow.workflow.validate",
      context: ctx,
      consent: { category: "Essential", version: this.consentVersion },
      data_class: "metadata",
      payload: {
        workflow_name: args.name,
        source_sha256: sha256(args.source),
      },
    });

    this.logger.log("info", "Workflow validate requested", { event_type: event.event_type, correlation_id: ctx.correlation_id });

    // Placeholder for a real API call
    return { ok: true as const, event };
  }

  async runWorkflow(args: {
    name: string;
    input: unknown;
    context?: Partial<PinkFlowContext>;
    idempotencyKey?: string;
  }) {
    const ctx = this.makeContext({
      ...args.context,
      idempotency_key: args.idempotencyKey ?? id("idem"),
    });

    const event = this.envelope({
      event_type: "pinkflow.workflow.run.requested",
      context: ctx,
      consent: { category: "Essential", version: this.consentVersion },
      data_class: "metadata",
      payload: {
        workflow_name: args.name,
        input_preview: safePreview(args.input),
      },
    });

    this.logger.log("info", "Workflow run requested", {
      workflow_name: args.name,
      correlation_id: ctx.correlation_id,
      request_id: ctx.request_id,
      idempotency_key: ctx.idempotency_key,
    });

    // Placeholder for a real API call
    return { accepted: true as const, event };
  }
}

/** ---------- Visual-first safe preview (no secrets) ---------- */
export function safePreview(value: unknown): unknown {
  // Ensure logs stay readable and do not leak sensitive data.
  // Replace large blobs with summaries.
  try {
    const json = JSON.stringify(value);
    if (json.length <= 600) return value;
    return { _preview: "truncated", length: json.length };
  } catch {
    return { _preview: "unserializable" };
  }
}
```
