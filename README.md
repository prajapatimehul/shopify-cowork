# Shopify Store Analyzer

Agent skill for auditing Shopify stores across SEO, GEO (AI visibility), and AEO (answer engine readiness). Works with Claude Code, Claude Agent SDK, claude.ai, and Codex.

Built on the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) open standard.

## What It Does

Comprehensive public-data audit for any Shopify store. No authentication required.

- **SEO**: Crawlability, structured data, content depth, titles, canonicals, technical health
- **GEO**: AI bot access, entity clarity, citation-worthiness, content extractability
- **AEO**: FAQ content quality, featured snippet readiness, voice search, answer formatting

Three modes: full audit, focused audit (single dimension), audit review (verify existing audit).

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

# Project (shared via git)
cp -r skills/store-analyzer .claude/skills/store-analyzer
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

1. Zip the skill directory: `cd skills && zip -r store-analyzer.zip store-analyzer/`
2. Go to **Settings > Features** in claude.ai
3. Upload the zip file
4. Claude uses it automatically when relevant

### Codex / Other Agents

The `SKILL.md` file contains complete instructions that work with any agent system. Copy the skill directory and point your agent to `SKILL.md` as the system prompt or instruction file.

## Repo Structure

```
skills/
└── store-analyzer/
    ├── SKILL.md              # Main skill instructions
    ├── references/
    │   ├── seo-checks.md     # SEO audit checklist
    │   ├── geo-checks.md     # AI visibility checks
    │   ├── aeo-checks.md     # Answer engine checks
    │   ├── catalog-checks.md # Product/collection data quality
    │   ├── troubleshooting.md # Edge cases and partial data
    │   └── testing.md        # Trigger tests and acceptance checks
    ├── assets/
    │   └── report-template.md # Output format templates
    ├── evals/
    │   └── evals.json        # Evaluation prompts
    └── scripts/
        └── check_report.py   # Report structure linter
```

## License

MIT
