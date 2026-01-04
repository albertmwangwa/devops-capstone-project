# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY service/ ./service/

# Create non-root user
RUN adduser -D theia && chown -R theia:theia /app
USER theia
# Expose port
EXPOSE 8080

# Run gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:create_app()"]