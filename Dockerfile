# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and switch to a new directory
WORKDIR /app
RUN apt update
RUN apt upgrade
RUN apt install git -y
# Copy the requirements file into the image
COPY requirements.txt /app/requirements.txt

COPY gitleaks /usr/local/bin/gitleaks
COPY trufflehog /usr/local/bin/trufflehog

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the FastAPI app files into the image
COPY . /app

# Set up the command to run the app
CMD ["uvicorn", "main:app", "--workers", "6", "--host", "0.0.0.0", "--port", "8000"]
