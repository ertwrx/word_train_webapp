# Use Python 3.12 to match your development environment
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=wsgi:app

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Create logs directory for Gunicorn
RUN mkdir -p logs && chmod 755 logs

# Expose the port Flask will run on
EXPOSE 5000

# Run the app using gunicorn with your configuration
CMD ["gunicorn", \
    "-w", "3", \
    "-t", "2", \
    "--worker-class", "sync", \
    "--timeout", "30", \
    "-b", "0.0.0.0:5000", \
    "wsgi:app"]
