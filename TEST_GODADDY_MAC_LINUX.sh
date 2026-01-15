#!/bin/bash

echo "================================================"
echo "GoDaddy Email Connection Test"
echo "================================================"
echo ""

# Activate virtual environment if it exists
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found."
fi

echo ""
echo "Starting test..."
echo ""

python3 test_godaddy.py

echo ""
read -p "Press Enter to exit..."
