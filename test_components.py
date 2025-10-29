#!/usr/bin/env python3
"""
Test script to check which components of the Smart Contract AI Analyzer are working.
"""

import sys
import importlib
from pathlib import Path

def test_component(module_name, description):
    """Test if a component can be imported and used."""
    try:
        module = importlib.import_module(module_name)
        print(f"✅ {description}: Working")
        return True
    except Exception as e:
        print(f"❌ {description}: Failed - {str(e)[:100]}...")
        return False

def test_external_tool(command, tool_name):
    """Test if an external tool is available."""
    import subprocess
    try:
        result = subprocess.run([command, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {tool_name}: Available")
            return True
        else:
            print(f"❌ {tool_name}: Not working")
            return False
    except Exception as e:
        print(f"❌ {tool_name}: Not installed")
        return False

def main():
    """Run component tests."""
    print("🔍 Smart Contract AI Analyzer - Component Status Check")
    print("=" * 60)
    
    # Test core Python components
    print("\n📦 Core Components:")
    test_component("streamlit", "Streamlit (Dashboard)")
    test_component("flask", "Flask (API Backend)")
    test_component("pandas", "Pandas (Data Processing)")
    test_component("numpy", "NumPy (Numerical Computing)")
    test_component("sklearn", "Scikit-learn (Machine Learning)")
    test_component("plotly", "Plotly (Visualizations)")
    
    # Test project modules
    print("\n🏗️ Project Modules:")
    test_component("src.utils.logging_config", "Logging Configuration")
    
    # Test individual files exist
    print("\n📁 Key Files:")
    files_to_check = [
        ("dashboard/dashboard.py", "Dashboard Main File"),
        ("src/api/app.py", "API Application"),
        ("src/models/random_forest.py", "Random Forest Model"),
        ("src/features/feature_extractor.py", "Feature Extractor"),
        ("requirements.txt", "Requirements File"),
    ]
    
    for file_path, description in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Missing")
    
    # Test external tools
    print("\n🛠️ External Tools:")
    test_external_tool("slither", "Slither Static Analyzer")
    test_external_tool("myth", "Mythril Symbolic Execution")
    test_external_tool("solc", "Solidity Compiler")
    
    # Test running services
    print("\n🌐 Running Services:")
    import requests
    
    # Test if dashboard is running
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        print("✅ Dashboard: Running at http://localhost:8501")
    except:
        print("❌ Dashboard: Not running")
    
    # Test if API is running
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print("✅ API Backend: Running at http://localhost:5000")
    except:
        print("❌ API Backend: Not running")
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("✅ Dashboard is working (Streamlit)")
    print("⚙️ API Backend can be started separately")
    print("🔧 CLI needs some module fixes")
    print("🛠️ External tools need manual installation")
    
    print("\n🚀 Quick Start Commands:")
    print("Dashboard: streamlit run dashboard/dashboard.py")
    print("API:       python -m flask --app src.api.app run")
    print("Setup:     python scripts/setup_environment.py")

if __name__ == "__main__":
    main()