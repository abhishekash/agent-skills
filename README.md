# agent-skills

A collection of Agent Skills (`SKILL.md`) for building and operating agentic systems — authored against the pattern that made [obra/superpowers](https://github.com/obra/superpowers) and [anthropics/skills](https://github.com/anthropics/skills) effective: **concrete workflows, opinionated tables, and honest "works / fails when" notes.**

A skill is a prompt-shaped artifact: the model sees the `name` + `description` in its context (progressive disclosure) and loads the body only when relevant. Descriptions are therefore written as routing triggers ("Use when…"), not marketing copy.

## Skills

| Skill | Use when |
|---|---|
| [agent-trace-debugging](skills/agent-trace-debugging/SKILL.md) | A run was slow/expensive/loopy; "why did the agent do that?" — diagnose from OTel traces (via [mcp-trace](https://github.com/abhishekash/mcp-trace)) instead of re-running |
| [hitl-policy-design](skills/hitl-policy-design/SKILL.md) | Wiring approval gates: risk tiers, approval-request UX, avoiding approval fatigue |
| [mcp-server-authoring](skills/mcp-server-authoring/SKILL.md) | Building/reviewing an MCP server: descriptions-as-prompts, output budgets, ship checklist |
| [eval-driven-agent-dev](skills/eval-driven-agent-dev/SKILL.md) | Changing prompts/tools/models: tasks + scorers before edits, deterministic-first |

## Using them

Any harness that speaks the `SKILL.md` format can load these — point your skills directory here:

```bash
harness run "…" --skills ./agent-skills/skills     # agent-harness
```

Format: flat YAML-subset frontmatter (`name`, `description`), then the body. Validated in CI by [`scripts/validate_skills.py`](scripts/validate_skills.py) (zero-dep, checks frontmatter, name↔dir match, description length/routing phrasing).

## Authoring principles (applied to every skill here)

1. **When-to-use is the API.** If the description doesn't name trigger situations, the skill won't fire when it should.
2. **Workflows over advice.** Numbered steps an agent can follow beat principles it can only admire.
3. **Failure notes are mandatory.** Every skill here lists where it breaks or misleads — that's what separates a useful skill from a lucky one.
4. **Tables for pattern-matching.** Symptom→cause and scorer→catches tables are the highest-value content per token.

## License

MIT
