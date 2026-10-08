# Contributing to agent-skills

## Validate locally

```bash
python scripts/validate_skills.py skills
```

## Adding a skill

Create `skills/<kebab-case-name>/SKILL.md` with flat frontmatter containing `name` and a routing-oriented `description` that says `Use when ...`.

The body should include a concrete workflow, examples or tables, and an honest failure-notes section. Avoid generic motivational prose. Skills should be compatible with the progressive-disclosure loader used by agent-harness.

Keep pull requests focused on one skill or one precise revision. Explain which trigger situations and failure modes changed.
