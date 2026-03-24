# LiteLLM Compose Project

## Overview
This project provides a Docker Compose setup for running LiteLLM proxy server with PostgreSQL database backend.

## Project Structure
- `docker-compose.yml` - Main service configuration for LiteLLM and PostgreSQL
- `config.yaml` - LiteLLM proxy configuration (mounted into container)
- `.env` - Environment variables for database and API keys
- `Taskfile.yaml` - Task runner for common operations
- `README.md` - User-facing documentation

## Key Commands
- `task` or `task up` - Start services in detached mode
- `task down` - Stop services
- `task down-volumes` - Stop services and remove volumes

## Services
### LiteLLM Proxy
- Runs on port 4000
- Uses `config.yaml` for model configuration
- Depends on PostgreSQL database
- Health checks configured for monitoring

### PostgreSQL Database
- PostgreSQL 16
- Port 5432
- Data persisted in named volume `litellm_db_data`
- Credentials managed via `.env` file

## Configuration
- LiteLLM config is in `config.yaml` and mounted to `/app/config.yaml`
- Environment variables in `.env` include database credentials and API keys
- Database connection string format: `postgresql://user:password@db:5432/litellm`

## Claude Code CLI Setup

To use this LiteLLM proxy with Claude Code CLI, configure the following environment variables:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:4000/",
    "ANTHROPIC_AUTH_TOKEN": "sk-1234",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "nvidia_nim/moonshotai/kimi-k2-instruct",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "nvidia_nim/moonshotai/kimi-k2-instruct",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```

**Notes:**
- `ANTHROPIC_BASE_URL` points to the LiteLLM proxy running locally on port 4000
- `ANTHROPIC_AUTH_TOKEN` should match the API key configured in your LiteLLM setup
- Model names should correspond to models defined in your `config.yaml`

## Development Guidelines
- Use Taskfile commands instead of direct docker-compose commands
- Keep sensitive data in `.env` (gitignored)
- Follow existing commit message style (imperative mood, clear descriptions)
