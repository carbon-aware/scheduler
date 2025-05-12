#!/bin/bash
set -e

echo "Setting up development environment for Carbon Aware Scheduler..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv from https://github.com/astral-sh/uv before running this script."
    exit 1
fi

echo "✅ uv detected"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "scheduler/.venv" ]; then
    echo "Creating virtual environment with uv..."
    cd scheduler
    uv venv .venv
    cd ..
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source scheduler/.venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies using uv
cd scheduler
echo "Syncing project dependencies with uv..."
uv sync
cd ..
echo "✅ Project dependencies installed"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"

echo "Development environment setup complete! 🎉"
echo ""
echo "To activate the environment in the future, run:"
echo "  source scheduler/.venv/bin/activate"
echo ""
echo "To start local development with Tilt:"
echo "  ctlptl create cluster kind --name kind-ca-scheduler"
echo "  tilt up"
