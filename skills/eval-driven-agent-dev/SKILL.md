---
name: eval-driven-agent-dev
description: Write tasks and scorers before touching prompts or tools — the agent equivalent of TDD. Use when changing a prompt, adding a tool, switching models, or when "it feels worse since the change" but nobody can prove it.
---

# Eval-driven agent development

Prompt edits feel productive and regress silently. Evals turn "feels better"
into a table. Write the task suite *before* the change you're about to make.

## When to use

- Changing a system prompt, tool description, or model
- Adding a tool (did old behaviors survive?)
- Reviewing someone else's agent PR (where are the evals?)

## Minimal loop

1. **Write 5–10 tasks as data** (yaml/json): prompt + expectations. Include
   at least one *safety* task (the agent should refuse or get denied) and one
   *budget* task (finish under N steps / M tokens).
2. **Score outcomes, not vibes**: `answer_contains`, `tool_called(X, args~)`,
   `no_denied_side_effects`, `max_steps`, `max_cost`. Each scorer is one
   honest function returning pass/fail + reason.
3. **Run deterministically first**: a scripted/replay provider makes the loop
   itself testable offline. Then run the same suite against the real model
   (`--live`) for signal.
4. **Record everything**: the run's trace is the debugging artifact when a
   scorer fails. An eval without a trace is a shrug.

## Scorer patterns

| Scorer | Catches |
|---|---|
| `answer_contains` / regex | task comprehension regressions |
| `tool_called` (name + arg match) | routing regressions after description edits |
| `denied_write_attempted` | safety regressions (agent *tried* the dangerous call) |
| `max_steps` / `max_tokens` | loop blowups, context bloat |
| `trace_assert` (span exists, e.g. `hitl.decision` present) | mechanism regressions (gate got bypassed) |

## Anti-patterns

- **LLM-as-judge as the first scorer** — start with deterministic asserts;
  add judges only for genuinely fuzzy quality, and pin their model+prompt.
- **Evaluating only the happy path** — the denial/budget/adversarial tasks are
  where agents actually break.
- **One-off runs without baselines** — store results per commit; a table that
  says "this PR: 7/10 → 9/10" is a code review superpower.

## Failure notes

- **Scripted providers can't judge answer quality** — they verify the loop,
  tools, and gates, not model smarts. Be explicit about which mode a results
  table came from.
- **Live runs are nondeterministic**: run k≥3 and report pass rates, or fix
  temperature=0 and say so.
- **Small suites overfit fast** — 10 tasks will be gamed by any prompt tweak
  that mentions them. Rotate in fresh tasks monthly.
