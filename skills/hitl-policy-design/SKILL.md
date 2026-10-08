---
name: hitl-policy-design
description: Design human-in-the-loop approval policies for agents — which tools to gate, how to write approval requests humans can decide in seconds, and how to avoid approval fatigue. Use when wiring an agent for real (unattended or semi-attended) use.
---

# HITL policy design

The goal is not "a human approves everything". The goal is: humans spend their
attention only on decisions that actually need judgment, and every decision is
auditable afterward.

## When to use

- Setting approval policy for a new agent or tool
- Users are rubber-stamping everything (fatigue) or ignoring the agent (over-gating)
- An agent did damage and you're deciding what to gate next

## The risk-tier model

Classify every tool by its worst-case side effect, not its usual one:

| Tier | Meaning | Examples | Default |
|---|---|---|---|
| `read` | no side effects | read_file, list_dir, search | never gate |
| `write` | reversible local mutation | write_file, edit_file | gate |
| `execute` | code execution, network, irreversible/remote | run_shell, deploy, http POST | gate |

Then override by name, not by vibes: `never_require` for tools you've audited
in *this* deployment, `always_require` for anything touching money, prod, or
external identity.

## Writing approval requests a human can decide in 3 seconds

The approval prompt is a UI. Include:

1. **Verb + object**: "write 42 chars to `SUMMARY.md`" — not "write_file(...)"
2. **The diff, not the payload**: show what changes, truncated
3. **Why now**: which step of the plan triggered it

Offer four answers, not two: **yes / no / edit / always-this-tool**.
`edit` (approve with human-corrected arguments) resolves most denials without
another model round-trip. `no` must capture *why* — the rationale goes back to
the model and into the audit trail; a bare "denied" teaches nothing.

## Anti-patterns

- **Approval fatigue**: gating reads, or gating a write every 20 seconds.
  Humans start typing `y` blindly, which is worse than no gate. Measure:
  approvals per minute should be < 1 in steady state.
- **Gating without recording**: a decision nobody can audit afterward is
  compliance theater. Decisions must be trace events with rationale.
- **Retry loops after denial**: the model re-asks the same call. Feed the
  rationale back with explicit "do not retry the same call".
- **One global policy**: unattended eval runs and prod runs need different
  policies (permissive vs default). The policy is config, not code.

## Failure notes

- **EDIT paths are undertested in most stacks** — test that the agent proceeds
  with the *edited* args, not its original ones.
- **'Always this tool' is a session-scope privilege** — it must not persist
  across runs, or it becomes a silent policy hole.
- **Async gates (Slack/webhook) change agent behavior**: long waits make some
  models abandon the plan. Keep the pending state in the trace so you can see it.
