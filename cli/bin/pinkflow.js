#!/usr/bin/env node
/**
 * PinkFlow CLI (Node ESM)
 * Deterministic output, structured logs, strong UX.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const ANSI = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  cyan: "\x1b[36m",
};

function usage() {
  return `
${ANSI.bold}pinkflow${ANSI.reset} — CLI

Commands:
  validate <workflowFile>
  run <workflowFile> --input <jsonFile>

Flags:
  --json        Machine-readable output
  --tenant      Tenant ID (required)
  --env         development|staging|production (default: development)
  --baseUrl     API base URL
  --consent     Consent version (default: 2026-01)

Examples:
  pinkflow validate workflow.json --tenant acme --env staging
  pinkflow run workflow.json --input input.json --tenant acme --json
`.trim();
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const tok = argv[i];
    if (tok.startsWith("--")) {
      const key = tok.slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      args[key] = val;
    } else {
      args._.push(tok);
    }
  }
  return args;
}

function out(obj, jsonMode) {
  if (jsonMode) {
    process.stdout.write(JSON.stringify(obj) + "\n");
    return;
  }
  // Visual-first output
  if (obj.ok) {
    process.stdout.write(`${ANSI.green}OK${ANSI.reset} ${obj.message}\n`);
  } else {
    process.stdout.write(`${ANSI.red}ERROR${ANSI.reset} ${obj.message}\n`);
  }
  if (obj.details) {
    process.stdout.write(`${ANSI.dim}${JSON.stringify(obj.details, null, 2)}${ANSI.reset}\n`);
  }
}

async function readJson(filePath) {
  const raw = await fs.readFile(filePath, "utf8");
  return JSON.parse(raw);
}

async function main() {
  const args = parseArgs(process.argv);
  const [cmd, file] = args._;

  if (!cmd || cmd === "help" || args.help) {
    process.stdout.write(usage() + "\n");
    process.exit(0);
  }

  const tenant = args.tenant;
  const env = args.env ?? "development";
  const baseUrl = args.baseUrl ?? "https://api.pinkflow.mbtq.dev";
  const consent = args.consent ?? "2026-01";
  const jsonMode = Boolean(args.json);

  if (!tenant) {
    out({ ok: false, message: "Missing --tenant" }, jsonMode);
    process.exit(2);
  }

  if (!file) {
    out({ ok: false, message: "Missing workflow file path" }, jsonMode);
    process.exit(2);
  }

  const workflowPath = path.resolve(process.cwd(), file);

  // Minimal deterministic checks (no vibes)
  let workflow;
  try {
    workflow = await readJson(workflowPath);
  } catch (e) {
    out({ ok: false, message: "Workflow file is not valid JSON", details: String(e) }, jsonMode);
    process.exit(2);
  }

  if (cmd === "validate") {
    // Basic schema-like checks (replace with real SDK call)
    const ok = typeof workflow?.name === "string" && workflow.name.length > 0;
    if (!ok) {
      out({ ok: false, message: "Invalid workflow: missing 'name' string" }, jsonMode);
      process.exit(2);
    }
    out(
      {
        ok: true,
        message: `Validated workflow '${workflow.name}'`,
        details: { tenant, env, baseUrl, consent, file: workflowPath },
      },
      jsonMode
    );
    return;
  }

  if (cmd === "run") {
    const inputFile = args.input;
    if (!inputFile) {
      out({ ok: false, message: "Missing --input <jsonFile>" }, jsonMode);
      process.exit(2);
    }

    let input;
    try {
      input = await readJson(path.resolve(process.cwd(), inputFile));
    } catch (e) {
      out({ ok: false, message: "Input file is not valid JSON", details: String(e) }, jsonMode);
      process.exit(2);
    }

    out(
      {
        ok: true,
        message: `Run accepted for '${workflow.name ?? "unknown"}'`,
        details: {
          tenant,
          env,
          baseUrl,
          consent,
          workflow: workflow.name ?? null,
          input_keys: input && typeof input === "object" ? Object.keys(input) : [],
        },
      },
      jsonMode
    );
    return;
  }

  out({ ok: false, message: `Unknown command: ${cmd}` }, jsonMode);
  process.exit(2);
}

main().catch((err) => {
  process.stderr.write(`${ANSI.red}FATAL${ANSI.reset} ${String(err)}\n`);
  process.exit(1);
});
