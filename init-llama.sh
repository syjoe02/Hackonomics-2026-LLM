#!/bin/sh

echo "Starting Ollama server..."

ollama serve &

sleep 5

echo "Checking llama model..."

if ! ollama list | grep -q "llama3:8b"; then
  echo "Downloading llama3:8b..."
  ollama pull llama3:8b
else
  echo "Model already installed"
fi

wait