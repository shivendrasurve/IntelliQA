#!/bin/bash

echo "Starting Mock FinTech API..."
cd /app/mock-api && node server.js &

echo "Waiting for API to be ready..."
sleep 3

echo "Verifying API is running..."
curl -f http://localhost:3000/accounts/acc_001
echo ""

echo "Running IntelliQA Test Suite..."
cd /app
pytest test-suite/api-tests/ -v --tb=short

