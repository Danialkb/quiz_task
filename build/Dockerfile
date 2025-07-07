FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

# Install curl and other required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

# Install dependencies
COPY pyproject.toml .
RUN uv sync

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./src /src
