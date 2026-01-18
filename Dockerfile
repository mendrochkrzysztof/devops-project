# ============ ETAP 1: builder ============
FROM python:3.14-slim as builder

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY app/requirements.txt .

# Install Python dependencies in user space
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# ============ ETAP 2: test ============
FROM builder as test

# Install test dependencies
RUN pip install --user --no-cache-dir pytest pytest-cov

# Run tests
RUN python -m pytest tests/ -v --cov=app.src --cov-report=term-missing --cov-report=xml:coverage.xml

# ============ ETAP 3: final ============
FROM python:3.14-slim as final

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY --from=builder /app /app

# Add user packages to PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Set environment variables
ENV FLASK_APP=app.src
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')"

# Run application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]