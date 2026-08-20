FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY main.py .
COPY thesitting.py omens.py debt.py defiance.py unclaimed.py sheet.py prompts.py oracle_data.py hand_deck.py .

CMD ["uv", "run", "main.py"]
