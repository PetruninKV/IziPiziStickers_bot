FROM python:3.10-buster

ARG POETRY_VERSION=1.3.2
ENV POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /app/
RUN poetry install -n --without=dev

RUN mkdir -p /root/.u2net && \
    wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx \
    -O /root/.u2net/u2net.onnx

COPY bot /app/bot
COPY .env /app

CMD ["python3.10", "bot/bot.py"]
