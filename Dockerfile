FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy all necessary files for building the package
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY prompts ./prompts

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy data files
COPY data ./data

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs').read()"

CMD ["uv", "run", "uvicorn", "concierge.app:app", "--host", "0.0.0.0", "--port", "8000"]
