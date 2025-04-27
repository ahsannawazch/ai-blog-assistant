# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV PIP_NO_CACHE_DIR=True

# Set work directory
WORKDIR /src

# Install system dependencies if needed (Chainlit needs libmagic for uploads, sometimes others)
RUN apt-get update && apt-get install -y \
    libmagic-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your source code
COPY src/ .

# Expose the default Chainlit port
EXPOSE 8000

# Command to run your app
CMD ["chainlit", "run", "app.py", "-h", "0.0.0.0", "-p", "8000"]
