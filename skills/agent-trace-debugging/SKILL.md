---
name: agent-trace-debugging
description: Diagnose slow, expensive, or misbehaving agent runs from their OpenTelemetry traces. Use when a run was slow, cost too much, looped, or did something unexpected — and whenever someone asks "why did the agent do that?".
---

# Agent trace debugging

Diagnose agent runs from traces instead of re-running and guessing. Traces are
the flight recorder; use them before touching prompts or code.

## When to use

- A run was slow, expensive, or hit `max_steps`
- The agent called an unexpected tool, or called one tool 15 times
- A human denied something and you want to know what and why
- Regression triage: "this worked last week"

## Prerequisites

- Traces as JSONL span files (agent-harness format: one OTel span per line)
- `mcp-trace` mounted, or `harness trace render <file>` as fallback

## Workflow

1. **Orient with `list_runs`** — find the run by task text, duration, or cost.
   Full 32-char trace ids are error-prone; every mcp-trace tool accepts prefixes.
2. **`run_summary` before `span_tree`** — the summary tells you the *shape*
   (llm calls, tool calls, denials, stopped_reason). Only open the tree if the
   shape looks wrong.
3. **Latency question → `slowest_spans`**, not the tree. One slow tool call
   (often `run_shell` or a network MCP tool) usually dominates.
4. **Behavior question → `approval_log` + the tool span attributes.** Denials
   carry the human's rationale — read it before "fixing" the agent; the denial
   is often the correct outcome.
5. **Cost question → `token_usage`.** If input tokens grow superlinearly per
   step, the loop is re-feeding large tool outputs; fix the tool's truncation,
   not the model.

## Common findings and their real causes

| Symptom in trace | Usually means | First fix |
|---|---|---|
| `llm.complete` input tokens ↑ every step | unbounded context growth | truncate/summarize tool outputs |
| same `tool.call` repeated with identical args | tool returned an error the model can't parse | improve the error string, add "do not retry" guidance |
| `tool.call` slow, `run_shell` | subprocess or grep over huge tree | narrow the command, add include/exclude |
| denial, rationale "too broad" | agent asked for a bigger action than needed | teach it to stage: read → small write |
| `max_steps` reached, all steps look sane | task needs decomposition | split the task; don't just raise max_steps |

## Failure notes (honest)

- **Fails when traces lack token/cost attributes** — older harness versions
  didn't emit `llm.usage.*`; check with `search_spans("llm.usage")` first.
- **Misleading when the clock is wrong** — durations come from span timestamps;
  if the host clock jumped, trust ordering, not milliseconds.
- **Can't see *why the model chose* a call** — traces show what happened, not
  model reasoning. If the provider logs reasoning blocks, correlate by step.
- **Denials without rationale** mean the human typed nothing; ask them, don't
  invent a reason.
