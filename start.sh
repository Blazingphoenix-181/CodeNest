#!/bin/bash
# CodeNest - Offline AI Coding Assistant
# Run this script to start the app

set -e

echo ""
echo "  ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗███████╗████████╗"
echo "  ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔════╝╚══██╔══╝"
echo "  ██║     ██║   ██║██║  ██║█████╗  ██╔██╗ ██║█████╗  ███████╗   ██║   "
echo "  ██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║   ██║   "
echo "  ╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚████║███████╗███████║   ██║   "
echo "   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝   ╚═╝   "
echo ""
echo "  Offline AI Coding Assistant — 100% Private, No Internet Required"
echo ""

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "  [ERROR] Ollama not found."
    echo "  Install it from: https://ollama.ai"
    echo "  Then run: ollama pull phi3"
    exit 1
fi

# Start Ollama in background if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Check if model exists, pull if not
MODEL=${CODENEST_MODEL:-phi3}
echo "  Checking model: $MODEL"
if ! ollama list | grep -q "$MODEL"; then
    echo "  Pulling $MODEL (first time only, may take a few minutes)..."
    ollama pull $MODEL
fi

# Install Python deps
if [ ! -d "venv" ]; then
    echo "  Setting up Python environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "  ✓ Ollama running"
echo "  ✓ Model: $MODEL"
echo "  ✓ Starting CodeNest..."
echo ""
echo "  Open your browser at: http://localhost:8000"
echo "  Press Ctrl+C to stop"
echo ""

uvicorn app:app --host 0.0.0.0 --port 8000 --reload
