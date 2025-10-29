#!/usr/bin/env python3
"""
Quick start script for Smart Contract AI Analyzer.
Simple approach that just starts the dashboard (works in mock mode).
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def main():
    """Quick start - just dashboard."""
    print("🚀 Smart Contract AI Analyzer - Quick Start")
    print("=" * 50)
    
    # Check if dashboard exists
    if not Path("dashboard/dashboard.py").exists():
        print("❌ dashboard/dashboard.py not found!")
        return False
    
    print("🌐 Starting Dashboard (Mock Mode)...")
    print("📱 Dashboard will be available at: http://localhost:8501")
    print("⚠️ API Backend not started - using mock analysis")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Start dashboard
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard/dashboard.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)