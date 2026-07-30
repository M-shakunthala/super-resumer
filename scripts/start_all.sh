#!/bin/bash

# AI Job Agent - Startup Script (Manual Mode)
# Use this while Docker installation is being resolved

echo "🚀 Starting AI Job Agent (Manual Mode)"
echo "========================================"

# Check if required files exist
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file with OPENAI_API_KEY"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY not set in environment"
    echo "Please set OPENAI_API_KEY in .env file or export it"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    # Kill background processes
    jobs
    kill %1 %2 2>/dev/null
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start the dashboard in background
echo "📊 Starting Streamlit Dashboard..."
streamlit run ui/dashboard.py --server.port=8501 --server.address=0.0.0.0 > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!

echo "🤖 Starting Job Bot..."
python run.py > logs/bot.log 2>&1 &
BOT_PID=$!

echo ""
echo "✅ Services started!"
echo "Dashboard: http://localhost:8501"
echo "Bot logs: logs/bot.log"
echo "Dashboard logs: logs/dashboard.log"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait