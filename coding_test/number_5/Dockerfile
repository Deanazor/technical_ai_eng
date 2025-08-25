FROM python:3.10-slim

ENV PYTHON_VERSION=3.10 \
    OLLAMA_HOST=0.0.0.0:11434

RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://ollama.com/install.sh | sh

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
RUN uv python install ${PYTHON_VERSION}

COPY ./pyproject.toml pyproject.toml
COPY ./uv.lock uv.lock
RUN uv sync

RUN uv run python -c "import easyocr; reader = easyocr.Reader(['en'])"

COPY ./run_application.sh ./
RUN chmod u+x run_application.sh

COPY ./app /app
COPY ./frontend /frontend

ENTRYPOINT ["./run_application.sh"]