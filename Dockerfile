# Use Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies with specific versions to avoid conflicts
RUN pip install --no-cache-dir protobuf==4.25.3 && \
    pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir pandas==2.0.3 && \
    pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "first.py"]
