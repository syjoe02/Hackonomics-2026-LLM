#!/bin/sh

echo "Checking llama model..."

if ! ollama list | grep -q llama3; then
  echo "Downloading llama3..."
  ollama pull llama3
else
  echo "Model already installed"
fi

echo "Starting Ollama..."
ollama serve