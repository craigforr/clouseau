# Clouseau Configuration

## Configuration Files

Clouseau uses two main configuration files:

- `config.yaml` - Application and provider configuration
- `settings.yaml` - User preferences and UI settings

## config.yaml

### LLM Providers

```yaml
providers:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-3-sonnet-20240229

  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: gpt-4
```

### Database

```yaml
database:
  path: ~/.clouseau/clouseau.db
  echo: false
```

### Server

```yaml
server:
  host: 127.0.0.1
  port: 8000
```

## settings.yaml

### UI Preferences

```yaml
ui:
  theme: dark
  font_size: 14
  show_token_count: true
```

### Defaults

```yaml
defaults:
  provider: anthropic
  model: claude-3-sonnet-20240229
  temperature: 0.7
```

## Environment Variables

Configuration supports environment variable substitution:

```yaml
api_key: ${API_KEY}           # Required
api_key: ${API_KEY:-default}  # With default value
```
