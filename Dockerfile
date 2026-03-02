# Base image with PyTorch and CUDA support
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# System dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our serverless code
COPY . .

# Set placeholder for the API Key security
ENV API_AUTH_TOKEN="YOUR_SECRET_TOKEN_HERE"

# Run the RunPod serverless handler
CMD ["python", "-u", "runpod_handler.py"]
