FROM python:3.9-slim AS downloader
RUN apt-get update && apt-get install -y \
    # packages to install
    curl \
    # clear the cache
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r user && useradd -r -g user user
USER user

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - --preview
ENV PATH=$PATH:/root/.local/bin

# generate requirements.txt
COPY pyproject.toml poetry.lock ./
RUN poetry update
RUN poetry export > requirements.txt

FROM python:3.8-slim
WORKDIR /src

# install dependencies
COPY --from=downloader /requirements.txt ./
RUN pip install -r requirements.txt

# install redis
RUN apt-get update && apt-get install -y \
    # packages to install
    redis-server \
    # clear the cache
    && rm -rf /var/lib/apt/lists/*

# add files
COPY src/ src/

# run server
EXPOSE 80
CMD ["sh", "-c", "redis-server --bind 127.0.0.1 --port 6379 & uvicorn src.api.main:app --host 0.0.0.0 --port 80"]
