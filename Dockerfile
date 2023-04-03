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
RUN poetry export > /home/user/requirements.txt
USER user


# Final image
FROM python:3.9
WORKDIR /src

# Install dependencies
COPY --from=downloader /home/user/requirements.txt ./
RUN pip install -r requirements.txt

# Add files
COPY src/ src/

# Run server
EXPOSE 8000
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port 8000"]
