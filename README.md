# shopify-cowork

A demo Claude Code plugin for Shopify development workflows.

## Installation

Add this marketplace and install:

```bash
/plugin marketplace add mehul-portfolio/shopify-cowork
/plugin install shopify-cowork@mehul-portfolio/shopify-cowork
```

Or test locally:

```bash
claude --plugin-dir ./shopify-cowork
```

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| hello | `/shopify-cowork:hello` | Verify plugin is installed |
| store-check | `/shopify-cowork:store-check` | Demo Shopify store health check |

## Available Agents

| Agent | Description |
|-------|-------------|
| demo-reviewer | Demo Shopify theme code reviewer |

## Plugin Structure

```
shopify-cowork/
├── .claude-plugin/
│   └── plugin.json         # Plugin manifest
├── skills/
│   ├── hello/SKILL.md      # Greeting / install verification
│   └── store-check/SKILL.md # Demo store health check
├── agents/
│   └── demo-reviewer.md    # Demo code review agent
├── hooks/
│   └── hooks.json          # Event hooks (empty for demo)
├── settings.json           # Default settings
└── README.md
```

## License

MIT
