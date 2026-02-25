# shopify-cowork

A Claude Code plugin marketplace for Shopify development workflows.

## Installation

```bash
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@prajapatimehul/shopify-cowork
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/shopify-cowork:hello` | Verify plugin is installed |

## Available Skills

| Skill | Description |
|-------|-------------|
| `hello` | Greeting / install verification |
| `store-check` | Demo Shopify store health check |

## Available Agents

| Agent | Description |
|-------|-------------|
| `demo-reviewer` | Demo Shopify theme code reviewer |

## Repo Structure

```
.claude-plugin/
└── marketplace.json            # Marketplace manifest
shopify-cowork/                 # Plugin directory
├── .claude-plugin/
│   └── plugin.json             # Plugin manifest
├── commands/
│   └── hello.md                # /hello command
├── skills/
│   ├── hello/SKILL.md          # Greeting skill
│   └── store-check/SKILL.md   # Store health check skill
└── agents/
    └── demo-reviewer.md        # Code review agent
```

## License

MIT
