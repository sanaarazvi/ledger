# Use official Python runtime
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all files to /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (Render requires this)
EXPOSE 8000

# Environment variable for Flask
ENV PORT=8000

# Run Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
