# Shopify Cowork Skills

Packaged agent skills for auditing and improving Shopify stores, plus research briefs for additional commerce-agent roles. Works with Claude Code, Claude Agent SDK, claude.ai, and Codex.

Built on the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) open standard.

## What It Includes

Two packaged skills live in `skills/`:

- **store-analyzer**: comprehensive public-data audit for Shopify SEO, GEO (AI visibility), and AEO (answer engine readiness). No authentication required.
- **store-fixer**: authenticated implementation skill for Shopify data and theme changes, with explicit approval and rollback requirements.

Research briefs for future role-specific skills live in `research/skills/`. These are design docs, not packaged skills yet.

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Review this SEO audit and tell me what's real
```

## Installation

### Claude Code

Copy into your personal or project skills directory:

```bash
# Personal (available across all projects)
cp -r skills/store-analyzer ~/.claude/skills/store-analyzer
cp -r skills/store-fixer ~/.claude/skills/store-fixer

# Project (shared via git)
cp -r skills/store-analyzer .claude/skills/store-analyzer
cp -r skills/store-fixer .claude/skills/store-fixer
```

Claude discovers it automatically. Type `/store-analyzer` or let Claude invoke it when relevant.

### Claude Agent SDK

Place the skill in `.claude/skills/` within your project directory and configure the SDK:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",  # Must contain .claude/skills/
    setting_sources=["user", "project"],
    allowed_tools=["Skill", "Read", "Write", "Bash", "WebFetch"],
)

async for message in query(prompt="Audit this Shopify store: example.com", options=options):
    print(message)
```

### claude.ai

1. Zip the skill directory you want to install, for example: `cd skills && zip -r store-analyzer.zip store-analyzer/`
2. Go to **Settings > Features** in claude.ai
3. Upload the zip file
4. Claude uses it automatically when relevant

### Codex / Other Agents

Each packaged skill contains a `SKILL.md` file with complete instructions that work with any agent system. Copy the skill directory and point your agent to `SKILL.md` as the system prompt or instruction file.

## Packaged vs Research

- `skills/` contains installable, runnable skill packages. Each package includes a `SKILL.md` entrypoint and supporting references, assets, evals, or scripts.
- `research/skills/` contains research briefs for future commerce-agent roles. These folders are usually `README.md` only and are not ready-to-install skills yet.

## Repo Structure

```text
skills/
├── store-analyzer/
│   ├── SKILL.md
│   ├── references/
│   ├── assets/
│   ├── evals/
│   └── scripts/
└── store-fixer/
    ├── SKILL.md
    ├── references/
    ├── assets/
    └── scripts/

research/
├── README.md
└── skills/
    ├── catalog-manager/
    ├── catalog-writer/
    ├── crm-automation/
    ├── customer-service/
    ├── finance-ops/
    ├── order-ops/
    ├── procurement-ops/
    └── reconciliation/
```

## License

MIT
