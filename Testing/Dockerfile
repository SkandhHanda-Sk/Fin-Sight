# Dockerfile (Improved Version)
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libmagic1 && rm -rf /var/lib/apt/lists/*

# --- Add these lines to create a non-root user ---
# Create a non-privileged user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements and install as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# The path needs to be relative to the build context (the 'Testing' directory)
COPY ./backend /app

# --- Add these lines to change ownership and switch user ---
# Change ownership of the app directory to the new user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser
# --- End of new lines ---

EXPOSE 5001

# The command to run when the container starts
CMD ["python", "app.py"]