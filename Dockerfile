FROM python:3.12.0-slim-bookworm

WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN uv sync --locked

COPY . .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]