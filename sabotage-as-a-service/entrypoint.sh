#!/bin/sh
# Run initialization script
python initializer.py
# Then launch the main server
exec python main.py
