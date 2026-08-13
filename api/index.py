import os
import sys

# Add project root directory to python path for Vercel serverless function entrypoint
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Vercel WSGI entry point
app = app
