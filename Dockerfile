# Stage 1: Build environment
FROM python:3.12-slim AS builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment and install Python dependencies
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir \
    librosa \
    paho-mqtt \
    pyyaml \
    numpy

# Copy add-on code
COPY . .

# Stage 2: Final image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy necessary files from builder stage
COPY --from=builder /app /app

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set entrypoint
CMD ["python", "get_mfcc.py"]

