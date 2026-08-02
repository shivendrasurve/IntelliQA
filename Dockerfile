FROM python:3.11-slim

# Install Node.js and curl
RUN apt-get update && apt-get install -y nodejs npm curl && apt-get clean

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Install Mock API dependencies
RUN cd mock-api && npm install

# Make startup script executable
RUN chmod +x start.sh

# Start API then run tests
CMD ["bash", "start.sh"]
