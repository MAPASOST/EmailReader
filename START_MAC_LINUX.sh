#!/bin/bash

echo "================================================"
echo "Email Reader - Starting Application"
echo "================================================"
echo ""
echo "The app will automatically install any missing"
echo "dependencies. This may take a moment on first run."
echo ""

# Activate virtual environment and run the GUI
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

python3 email_app.py
