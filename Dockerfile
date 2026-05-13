##############################################################################
# Dockerfile
# WHY THIS FILE EXISTS:
#   Packages the Flask application into a portable Docker image.
#   This image is pushed to Amazon ECR and pulled by EKS worker
#   nodes to run the application inside Kubernetes pods.
##############################################################################

# Base image — pinned version, slim variant for minimal attack surface
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first — optimizes Docker layer caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/app.py .

# Document the port the container listens on
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]