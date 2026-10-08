---
name: mcp-server-authoring
description: Design and ship MCP servers that agents actually use well — tool naming, descriptions-as-prompts, output budgets, error strings, packaging, registry submission. Use when creating a new MCP server or reviewing one before release.
---

# MCP server authoring

Your users are models, not humans. Every surface of the server — names,
descriptions, outputs, errors — is a prompt. Write them like prompts.

## When to use

- Starting a new MCP server
- A server works for humans but agents misuse it
- Preparing a registry submission

## Design rules that matter

1. **Descriptions are when-to-use, not what-it-is.**
   Bad: "Queries traces." Good: "Top-k slowest spans. Use for 'why was this
   run slow?'." The model routes on your description; write the trigger
   phrases it will hear.
2. **Return less.** A tool that dumps 50KB trains the model to avoid it.
   Summarize by default; offer a `limit` parameter; keep trees the only
   nested shape.
3. **Errors are instructions.** "error: no trace matching 'abc'; known
   prefixes: f920, 3b7c" gets the next call right. "Not found" doesn't.
4. **Accept fuzzy ids.** Prefix matching for any long identifier — models
   truncate and typo them constantly.
5. **Side effects declare themselves.** Read-only tools should be obviously
   read-only (name + description), so hosts can auto-approve them. Unknown
   tools get gated as execute-risk by careful hosts (agent-harness does).

## Ship checklist

- [ ] `uvx your-server` / `npx your-server` installs and starts in one command
- [ ] README has a copy-paste client config (Claude Desktop + one more)
- [ ] A demo: real output in the README, from a real run, not hand-written
- [ ] Each tool tested through the protocol (not just the underlying functions)
- [ ] Tagged release with changelog
- [ ] Submitted to the MCP registry (`modelcontextprotocol/registry`) and one awesome-list
- [ ] License file (MIT/Apache-2.0) — no license means corporate users can't touch it

## Testing

- Unit-test the core as pure functions (no MCP imports)
- Integration-test the server over real stdio JSON-RPC with a tiny client
- Keep a golden fixture of real input data in the repo (mcp-trace ships a real
  harness trace) — hand-written fixtures drift from reality

## Failure notes

- **Tool-count bloat is real**: past ~15 tools, routing quality degrades.
  Merge near-duplicates (one `query` tool with a `kind` param beats five
  near-identical tools) or split the server.
- **Long-running tools need progress or timeouts** — a 60s silent tool call
  gets killed by clients with shorter timeouts, and the model sees a generic
  failure.
- **Don't log secrets to stderr carelessly** — some clients surface server
  stderr into chat context.
