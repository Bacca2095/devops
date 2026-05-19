FROM python:3.14-slim AS dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-group dev --no-install-project


FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY --from=dependencies /app/.venv .venv
COPY . .
RUN uv sync --frozen --no-group dev

FROM python:3.14-slim AS production
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY --from=builder /app/app ./app
COPY --from=builder /app/main.py .
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/alembic.ini .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && fastapi run main.py --host 0.0.0.0 --port 8000"]
