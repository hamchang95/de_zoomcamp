FROM python:3.13.11-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

# create virtual env inside project
ENV VIRTUAL_ENV=/code/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install deps first (better caching)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

# copy script last
COPY ingestion.py .


ENTRYPOINT ["uv", "run", "ingestion.py"]
