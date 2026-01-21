# Docker Build & Run Instructions

## Monolithic Deployment (Backend + Proxy + Frontend)

This single container includes all three services managed by Supervisor.

### Prerequisites
- Docker installed
- Your Ollama server URL (Cloudflare tunnel or local Ollama instance)
- Semgrep API token from [semgrep.dev](https://semgrep.dev/orgs/-/settings/tokens)

> **Note:** The `.env` file is **NOT** copied into the Docker image. Environment variables must be passed at runtime using `-e` flags.

### Build the Image

```bash
# Build from project root (week-3/day-1/cyber)
docker build -t cyber-analyzer:latest .
```

### Run the Container

```bash
# Run with environment variables (REQUIRED)
docker run -d \
  --name cyber-analyzer \
  -e OLLAMA_API_URL=https://your-cloudflare-tunnel-url.trycloudflare.com \
  -e SEMGREP_APP_TOKEN=your-semgrep-token-here \
  -p 8000:8000 \
  -p 4000:4000 \
  cyber-analyzer:latest
```

**Environment Variables (Pre-configured in Dockerfile):**
- `OPENAI_API_KEY="sk-1234"` - Dummy key for proxy (already set)
- `OPENAI_BASE_URL="http://localhost:4000"` - Points to internal proxy (already set)

**Environment Variables (MUST provide at runtime):**
- `OLLAMA_API_URL` - Your Ollama server endpoint
- `SEMGREP_APP_TOKEN` - Your Semgrep API token

**Working Example:**
```bash
docker run -d \
  --name cyber-analyzer \
  -e OLLAMA_API_URL=https://combines-benz-challenged-block.trycloudflare.com \
  -e SEMGREP_APP_TOKEN=21731836ddfc8dafcb1d3b7c99bba92b1d40723eacfaa005cea9eb56b72dacdb \
  -p 8000:8000 \
  -p 4000:4000 \
  cyber-analyzer:latest
```

### View Logs and Check Health

```bash
# View logs (all services)
docker logs cyber-analyzer --tail 50 -f

# Check health endpoints
curl http://localhost:8000/health
curl http://localhost:4000/v1/models
```

### Access the Application

- **Frontend**: http://localhost:8000 (served by backend via static files)
- **Backend API**: http://localhost:8000/api/*
- **Proxy**: http://localhost:4000 (internal, for debugging)

### System Architecture in Container

```
┌─────────────────────────── Container ───────────────────────────┐
│                                                                   │
│  ┌─────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │  Supervisor │─────▶│ Proxy:4000   │◀────▶│ Backend:8000 │  │
│  └─────────────┘      └──────────────┘      └──────────────┘  │
│         │                     │                      │          │
│         │                     ▼                      │          │
│         │             External Ollama         Frontend Static  │
│         └──────────── (both auto-restart) ────────────┘        │
└───────────────────────────────────────────────────────────────┘
```

### Cloud Deployment

#### AWS App Runner
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag cyber-analyzer:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/cyber-analyzer:latest

docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/cyber-analyzer:latest

# Deploy to App Runner (configure env vars in console)
```

#### Azure Container Instances
```bash
# Push to Azure Container Registry
az acr login --name YOUR_REGISTRY

docker tag cyber-analyzer:latest YOUR_REGISTRY.azurecr.io/cyber-analyzer:latest

docker push YOUR_REGISTRY.azurecr.io/cyber-analyzer:latest

# Create container instance
az container create \
  --resource-group YOUR_RG \
  --name cyber-analyzer \
  --image YOUR_REGISTRY.azurecr.io/cyber-analyzer:latest \
  --dns-name-label cyber-analyzer \
  --ports 8000 \
  --environment-variables \
    OLLAMA_API_URL="your-url" \
    SEMGREP_APP_TOKEN="your-token"
```

### Troubleshooting

**Container won't start:**
```bash
# Check logs
docker logs cyber-analyzer

# Interactive shell
docker exec -it cyber-analyzer /bin/bash

# Check supervisor status
docker exec cyber-analyzer supervisorctl status
```

**Services not responding:**
```bash
# Restart individual service
docker exec cyber-analyzer supervisorctl restart proxy
docker exec cyber-analyzer supervisorctl restart backend
```

**Environment variables not loading:**
```bash
# Verify env vars
docker exec cyber-analyzer env | grep OLLAMA
```

### Stopping the Container

```bash
# Stop gracefully
docker stop cyber-analyzer

# Remove container
docker rm cyber-analyzer

# Remove image
docker rmi cyber-analyzer:latest
```
