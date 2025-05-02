# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables (optional fallback)
ENV PORT=9090

# Expose the port
EXPOSE 9090

# Run the Flask app
CMD ["python", "first.py"]