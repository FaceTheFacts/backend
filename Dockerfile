FROM python:3.9-slim as downloader
RUN apt-get update && apt-get install -y \
    # packages to install
    curl \
    # clear the cache
    && rm -rf /var/lib/apt/lists/*

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - --preview
ENV PATH=$PATH:/root/.local/bin

# generate requirements.txt
COPY pyproject.toml poetry.lock ./
RUN poetry export > requirements.txt


FROM python:3.9-slim
WORKDIR /src

# install dependencies
COPY --from=downloader /requirements.txt ./
RUN pip install -r requirements.txt

# add files
COPY main.py ./
COPY backend/ backend/

# run server
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
