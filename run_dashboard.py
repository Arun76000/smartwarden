#!/usr/bin/env python3
"""
Simple script to run the Smart Contract AI Analyzer dashboard.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit dashboard."""
    print("🚀 Starting Smart Contract AI Analyzer Dashboard...")
    print("=" * 60)
    
    # Check if we're in the right directory
    dashboard_path = Path("dashboard/dashboard.py")
    if not dashboard_path.exists():
        print("❌ Error: dashboard/dashboard.py not found!")
        print("Please run this script from the project root directory.")
        return False
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Error: Streamlit is not installed!")
        print("Please install it with: pip install streamlit")
        return False
    
    # Run the dashboard
    try:
        print("🌐 Starting dashboard server...")
        print("📱 Dashboard will be available at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Run streamlit
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
        print(f"❌ Error running dashboard: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)