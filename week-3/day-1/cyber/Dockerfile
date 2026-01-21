# --- Stage 1: Frontend Build ---
FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
# Next.js export çıktısını 'out' klasörüne alır
RUN npm run build

# --- Stage 2: Production Image ---
FROM python:3.12-slim
WORKDIR /app

# Sistem gereksinimleri (Supervisor dahil)
RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# UV Paket yöneticisi
RUN pip install uv

# Python bağımlılıkları
COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --frozen

# Backend kodlarını kopyala (server.py ve ollama_proxy.py)
COPY backend/ ./

# Frontend çıktılarını kopyala (Terminal 3'ün işini server.py yapacak)
# DİKKAT: server.py içindeki yol ile burası aynı olmalı (/app/frontend)

COPY --from=frontend-build /app/out ./frontend

# Supervisor ayar dosyasını kopyala (1. Adımda oluşturduğun dosya)
COPY backend/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV OPENAI_API_KEY="sk-1234"
ENV OPENAI_BASE_URL="http://localhost:4000"

# Health check (Hem proxy hem backend ayakta mı?)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:4000/v1/models && curl -f http://localhost:8000/health || exit 1

# Portları aç
EXPOSE 4000 8000

# Supervisor'ı başlat (Orkestra şefi)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]