#!/bin/bash

run_app() {
    # Windows
    if [[ "$OSTYPE" == "win32" || "$OSTYPE" == "msys"] || "$OSTYPE" == "cygwin" ]]; then
        echo "Running on Windows..."
        start cmd /k "py app.py"
    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        echo "Running on Linux..."
        gnome-terminal -- bash -c "python3 app.py; exec bash"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Running on macOS"
        osascript -e 'tell application "Terminal" to do script "python3 app.py"'
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

run_app