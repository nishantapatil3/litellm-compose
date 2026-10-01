# LiteLLM Docker Compose

A Docker Compose setup for running [LiteLLM](https://github.com/BerriAI/litellm) proxy server with PostgreSQL and Redis.

> **Opinionated deployment.** This is not a generic LiteLLM template — it's an opinionated setup focused on pairing **LiteLLM + OpenRouter + Claude Code** (and Claude Desktop). The model list, guardrail, and env layout are all shaped around that specific pairing.

## Why this exists

Running Claude Code and the Claude Desktop app against Anthropic's paid API adds up quickly. This stack pairs both clients with OpenRouter's free-tier Nemotron models via LiteLLM, so a small OpenRouter wallet deposit (~$10 unlocks roughly 1,000 requests/day on free-tier models) covers day-to-day usage.

- **Cost-shaped model routing.** `config.yaml` exposes three model aliases — `claude-haiku-4-5-20251001`, `claude-sonnet-4-6`, and `claude-opus-4-8` — that transparently route to Nemotron Nano (30B), Super (120B), and Ultra (550B) on OpenRouter. Claude Code / Desktop keep pointing at their familiar model names; LiteLLM does the swap.
- **Nemotron ≈ Claude tier.** The Nemotron family is used as a capability-equivalent stand-in for the Haiku / Sonnet / Opus hierarchy.
- **File-upload guardrail.** A custom LiteLLM pre-call guardrail (`guardrails/no_file_input_guardrail.py`) blocks document / PDF / file uploads before they ever hit the model, since processing them would burn tokens against the OpenRouter budget. **Images are allowed** and routed to the Haiku tier (Nemotron Nano supports vision), so vision use stays cheap.
- **Drop-in for Claude Code + Claude Desktop.** Point either client at `http://localhost:4000/` with `sk-1234` (or whatever you set `LITELLM_MASTER_KEY` to) and they behave as if talking to Anthropic — with the guardrail and model routing in the middle. For Claude Desktop pairing, see the LiteLLM tutorial: [Pairing Claude Desktop with LiteLLM (Cowork)](https://docs.litellm.ai/docs/tutorials/claude_desktop_cowork).

## Services

- **LiteLLM Proxy**: AI gateway/proxy server running on port 4000
- **PostgreSQL**: Database for storing models and configurations on port 5432
- **Redis**: Response cache backend for LiteLLM

## Prerequisites

- Docker and Docker Compose installed
- [Task](https://taskfile.dev/) (optional, for using Taskfile commands)
- `.env` file with your configuration (see `.env.example`)

## Quick Start

### Using Task (recommended)

```bash
# Copy the example env file and configure it
cp .env.example .env

# Edit .env with your API keys and settings
nano .env

# Start services
task up

# Stop services
task down

# Stop services and remove volumes
task down-volumes
```

### Using Docker Compose directly

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop services and remove volumes
docker-compose down -v
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Required variables are documented in `.env.example`.

### LiteLLM Config (Optional)

To use a custom LiteLLM configuration file:

1. Create a `config.yaml` file (see `config.yaml` example)
2. Uncomment the volumes and command sections in `docker-compose.yml`
3. Restart the services

## Accessing Services

- **LiteLLM API**: http://localhost:4000
- **LiteLLM UI**: http://localhost:4000/ui
- **PostgreSQL**: localhost:5432

### Metrics and Cache

Redis is configured as LiteLLM's response cache using the internal Docker hostname `redis`. Cached entries use the `litellm-cache` namespace with a 10 minute TTL.

## Health Checks

The services include health checks to ensure they're running properly:

- LiteLLM: checks `/health/liveliness` endpoint
- PostgreSQL: checks database connectivity

## Data Persistence

- PostgreSQL data is persisted in the `litellm_postgres_data` volume
- Redis cache data is persisted in the `litellm_redis_data` volume

## Task Commands

- `task up` - Start all services in detached mode
- `task down` - Stop all services
- `task down-volumes` - Stop services and remove all volumes (clean slate)

## Claude Code CLI Setup

To use this LiteLLM proxy with Claude Code CLI, add the following to your Claude Code settings:

```json
{
  "model": "litellm-text",
  "modelOverrides": {
    "claude-sonnet-4-6": "litellm-text",
    "claude-haiku-4-5": "litellm-text",
    "claude-opus-4-6": "litellm-text"
  },
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4000",
    "ANTHROPIC_API_KEY": "sk-1234",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY": "1"
  }
}
```

**Notes:**
- `ANTHROPIC_BASE_URL` points to the LiteLLM proxy running locally on port 4000
- `ANTHROPIC_API_KEY` should match the API key configured in your LiteLLM setup
- `litellm-text` uses OpenRouter Owl Alpha as primary, then Gemma 31B, then Gemma 26B, then popular last-resort fallbacks
- The remaining popular last-resort fallbacks may not preserve Claude Code's live streaming token counter

## Development Guidelines
- Use Taskfile commands instead of direct docker-compose commands
- Keep sensitive data in `.env` (gitignored)
- Follow existing commit message style (imperative mood, clear descriptions)

## Documentation

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)

## License

This configuration is provided as-is for use with LiteLLM.
