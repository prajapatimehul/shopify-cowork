# Shopify Store Skills

Agent skills for auditing and fixing Shopify stores. Works with Claude Code, Claude Agent SDK, claude.ai, and Codex.

Built on the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) open standard.

## Skills

### Store Analyzer

Comprehensive SEO + GEO + AEO audit for any public Shopify store. No authentication required.

- **SEO**: Crawlability, structured data, content depth, titles, canonicals, technical health
- **GEO**: AI bot access, entity clarity, citation-worthiness, content extractability
- **AEO**: FAQ content quality, featured snippet readiness, voice search, answer formatting

Three modes: full audit, focused audit (single dimension), audit review (verify existing audit).

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Review this SEO audit and tell me what's real
```

### Store Fixer

Authenticated Shopify implementation — takes analyzer findings and fixes them via theme code or Admin API.

- **Theme**: robots.txt, JSON-LD, FAQ sections, canonicals, internal linking
- **Admin API**: product titles, descriptions, tags, collection metadata, metafields
- **Safety**: explicit approval gate, rollback required before execution, verification after

```
Take this audit and implement the top 3 fixes
Fix missing FAQ schema on this Shopify store
What access does the client need before we can fix this?
```

## Installation

### Claude Code

Copy the skills you want into your personal or project skills directory:

```bash
# Personal (available across all projects)
cp -r skills/store-analyzer ~/.claude/skills/store-analyzer
cp -r skills/store-fixer ~/.claude/skills/store-fixer

# Project (shared via git)
cp -r skills/store-analyzer .claude/skills/store-analyzer
cp -r skills/store-fixer .claude/skills/store-fixer
```

Claude discovers them automatically. Type `/store-analyzer` or let Claude invoke them when relevant.

### Claude Agent SDK

Place skills in `.claude/skills/` within your project directory and configure the SDK:

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

1. Zip a skill directory: `cd skills && zip -r store-analyzer.zip store-analyzer/`
2. Go to **Settings > Features** in claude.ai
3. Upload the zip file
4. Claude uses it automatically when relevant

### Codex / Other Agents

The `SKILL.md` files contain complete instructions that work with any agent system. Copy the skill directory and point your agent to `SKILL.md` as the system prompt or instruction file.

## Repo Structure

```
skills/
├── store-analyzer/
│   ├── SKILL.md              # Main skill instructions
│   ├── references/
│   │   ├── seo-checks.md     # SEO audit checklist
│   │   ├── geo-checks.md     # AI visibility checks
│   │   ├── aeo-checks.md     # Answer engine checks
│   │   ├── catalog-checks.md # Product/collection data quality
│   │   ├── troubleshooting.md # Edge cases and partial data
│   │   └── testing.md        # Trigger tests and acceptance checks
│   ├── assets/
│   │   └── report-template.md # Output format templates
│   ├── evals/
│   │   └── evals.json        # Evaluation prompts
│   └── scripts/
│       └── check_report.py   # Report structure linter
└── store-fixer/
    ├── SKILL.md              # Main skill instructions
    ├── references/
    │   ├── access-setup.md   # Theme Access / Admin API setup
    │   ├── fix-methods.md    # Decision tree: theme vs API vs manual
    │   ├── safety-and-rollback.md # Rollback and verification checklists
    │   └── testing.md        # Trigger tests and acceptance checks
    ├── assets/
    │   └── fix-summary-template.md # Fix output format
    ├── evals/
    │   └── evals.json        # Evaluation prompts
    └── scripts/
        └── check_fix_summary.py # Summary structure validator
```

## License

MIT
