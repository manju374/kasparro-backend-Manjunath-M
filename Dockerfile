# STAGE 1: Builder (Compiling dependencies)
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Runtime (The final, secure image)
FROM python:3.9-slim as runner

WORKDIR /app

# Install only runtime libraries (libpq) - no GCC needed here!
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Copy and prepare the startup script
COPY run.sh .
RUN chmod +x run.sh

# Run the script when the container starts
CMD ["./run.sh"]
