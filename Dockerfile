# Use Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies with specific versions to avoid conflicts



# Copy project files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "first.py"]
