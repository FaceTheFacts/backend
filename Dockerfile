FROM python:3.9-slim as downloader
RUN apt-get update && apt-get install -y \
    # packages to install
    curl \
    # clear the cache
    && rm -rf /var/lib/apt/lists/*

# install pipenv
RUN apt-get install pipenv

# generate requirements.txt
COPY Pipfile Pipfile.lock ./
RUN pipenv lock -r > requirements.txt

FROM python:3.8-slim
WORKDIR /src

# install dependencies
COPY --from=downloader /requirements.txt ./
RUN pip install -r requirements.txt

# add files
COPY src/ src/

# run server
EXPOSE 80
CMD [ "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "80" ]
