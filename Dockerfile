# Dockerfile (Backend - No Changes Needed)
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libmagic1 && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user and group for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements and install as root to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# The path is relative to the build context (the 'Testing' directory)
COPY ./backend /app

# Change ownership of the app directory to the new user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

EXPOSE 5001

# The command to run when the container starts
CMD ["python", "app.py"]