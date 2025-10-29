#!/usr/bin/env python3
"""
Smart Contract AI Analyzer - Convenience CLI Script

This script provides a convenient way to run the Smart Contract AI Analyzer
without having to use the full module path.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main CLI
from src.cli import main

if __name__ == '__main__':
    main()