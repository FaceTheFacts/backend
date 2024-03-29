# Use a multi-stage build to separate the downloader and final image
FROM python:3.9-slim AS downloader
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r user && useradd -r -g user user

# Create the home directory and necessary directories for the non-root user
RUN mkdir -p /home/user && chown -R user:user /home/user
RUN mkdir -p /home/user/.local/share && mkdir -p /home/user/.local/bin && chown -R user:user /home/user/.local
USER user

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$PATH:/home/user/.local/bin

# Generate requirements.txt
COPY --chown=user:user pyproject.toml poetry.lock ./
USER root
RUN poetry update
RUN poetry export -f requirements.txt --output /home/user/requirements.txt --without-hashes
RUN chmod go-w pyproject.toml poetry.lock
USER user

# Final image
FROM python:3.9
WORKDIR /src

# Create a non-root user and switch to it
RUN groupadd -r user && useradd -r -g user user
RUN mkdir -p /home/user && chown -R user:user /home/user
USER user

# Copy dependencies and requirements.txt file
COPY --from=downloader --chown=user:user /home/user/.local ./.local
COPY --from=downloader --chown=user:user /home/user/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

# Add files
COPY --chown=user:user src/ src/
COPY --chown=user:user .well-known .well-known
COPY --chown=user:user static static
RUN chmod go-w src/ .well-known static

# Run server
EXPOSE 8000
CMD ["sh", "-c", "poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 8000"]

