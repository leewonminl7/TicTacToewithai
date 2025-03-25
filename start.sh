#!/bin/bash

echo "Installing dependencies..."
pip install flask flask-cors

echo "Starting the Tic-Tac-Toe server..."
python server.py &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 3

echo "Opening Tic-Tac-Toe in your browser..."
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    open http://127.0.0.1:5006
elif [ "$(uname)" == "Linux" ]; then
    # Linux
    xdg-open http://127.0.0.1:5006 || sensible-browser http://127.0.0.1:5006 || firefox http://127.0.0.1:5006
else
    # Windows
    start http://127.0.0.1:5006 || explorer "http://127.0.0.1:5006"
fi

echo "Tic-Tac-Toe is now running!"

wait $SERVER_PID
