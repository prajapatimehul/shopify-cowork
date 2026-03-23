# Shopify Cowork Skills

Packaged agent skills for auditing and improving Shopify stores. Works as a **Claude Code plugin**, standalone **Agent Skills** (Codex, Cursor, Gemini CLI), or via **Claude Agent SDK**.

Built on the [Agent Skills Open Standard](https://agentskills.io/specification).

## Skills

- **store-analyzer**: Public-data audit for Shopify SEO, GEO (AI visibility), and AEO (answer engine readiness). No authentication required.
- **store-fixer**: Authenticated implementation skill for Shopify data and theme changes, with explicit approval and rollback.

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Review this SEO audit and tell me what's real
```

## Installation

### Claude Code (plugin — recommended)

```bash
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@shopify-cowork
```

Skills appear as `/shopify-cowork:store-analyzer` and `/shopify-cowork:store-fixer`.

### Claude Code (manual)

```bash
# Personal (available across all projects)
cp -r skills/store-analyzer ~/.claude/skills/store-analyzer
cp -r skills/store-fixer ~/.claude/skills/store-fixer

# Project (shared via git)
cp -r skills/store-analyzer .claude/skills/store-analyzer
cp -r skills/store-fixer .claude/skills/store-fixer
```

### Codex

**Option A — Skill installer (recommended):**

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo prajapatimehul/shopify-cowork \
  --path skills/store-analyzer skills/store-fixer
```

Installs to `~/.codex/skills/store-analyzer` and `~/.codex/skills/store-fixer`. Restart Codex after installing.

**Option B — Manual copy:**

```bash
# Clone the repo
git clone https://github.com/prajapatimehul/shopify-cowork.git
cd shopify-cowork

# Copy to Codex skills directory
cp -r skills/store-analyzer ~/.codex/skills/store-analyzer
cp -r skills/store-fixer ~/.codex/skills/store-fixer
```

**Option C — Project-level (per-repo):**

```bash
cp -r skills/store-analyzer .agents/skills/store-analyzer
```

Or clone the repo — `.agents/skills/` symlinks are included.

**After installing, use naturally:**

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Plan fixes for SEO issues in my Shopify store
```

> **Note:** `store-analyzer` uses public data only. `store-fixer` makes authenticated Shopify changes and requires explicit approval before every write.

### Cursor

```bash
cp -r skills/store-analyzer .cursor/skills/store-analyzer
```

### Gemini CLI

```bash
cp -r skills/store-analyzer .gemini/skills/store-analyzer
```

### Claude Agent SDK

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

1. Zip the skill: `cd skills && zip -r store-analyzer.zip store-analyzer/`
2. Go to **Settings > Features** in claude.ai
3. Upload the zip file

## Repo Structure

```text
.claude-plugin/          # Claude Code plugin manifest
  plugin.json
  marketplace.json
.agents/skills/          # Cross-platform skill discovery (Codex, Cursor, etc.)
  store-analyzer -> ../../skills/store-analyzer
  store-fixer -> ../../skills/store-fixer
skills/                  # Canonical skill packages
  store-analyzer/
    SKILL.md
    references/
    assets/
    evals/
    scripts/
  store-fixer/
    SKILL.md
    references/
    assets/
    scripts/
research/                # Design docs for future skills (not installable)
  skills/
```

## License

MIT
