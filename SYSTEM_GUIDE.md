# 🚀 Smart Contract AI Analyzer - Complete System Guide

## 📋 **System Components Overview**

The Smart Contract AI Analyzer consists of multiple components that can run independently or together:

### **1. 🌐 Dashboard (Frontend) - ✅ RUNNING**

- **What it does**: Web interface for contract analysis
- **Status**: Currently running at http://localhost:8501
- **How to run**: `streamlit run dashboard/dashboard.py`

### **2. 🔧 API Backend Server**

- **What it does**: RESTful API for programmatic access
- **Port**: 5000 (default)
- **How to run**: `python -m src.api.app`

### **3. 💻 Command Line Interface (CLI)**

- **What it does**: Terminal-based analysis tool
- **How to run**: `python -m src.cli --help`

### **4. 🤖 Machine Learning Models**

- **What they do**: AI-powered vulnerability detection
- **Components**: Binary classifier, Multi-class classifier
- **Status**: Need to be trained or loaded

### **5. 🛠️ External Tools Integration**

- **Slither**: Static analysis tool
- **Mythril**: Symbolic execution tool
- **Status**: Need to be installed separately

---

## 🏃‍♂️ **How to Run Each Component**

### **Dashboard (Already Running)**

```bash
# Option 1: Direct
streamlit run dashboard/dashboard.py

# Option 2: Using script
python run_dashboard.py

# Option 3: Windows batch
run_dashboard.bat
```

### **API Backend Server**

```bash
# Run Flask API server
python -m src.api.app

# Or with specific configuration
FLASK_ENV=development python -m src.api.app

# API will be available at: http://localhost:5000
```

### **Command Line Interface**

```bash
# Show help
python -m src.cli --help

# Analyze a single contract
python -m src.cli analyze contract.sol

# Batch analysis
python -m src.cli batch-analyze contracts/

# Compare tools
python -m src.cli compare contract.sol --tools slither,mythril,ai
```

### **Setup and Training**

```bash
# Setup environment and train models
python scripts/setup_environment.py

# Train models manually
python -m src.models.random_forest --train
python -m src.models.multiclass_classifier --train
```

---

## 🔧 **Installation Requirements for Full Functionality**

### **Core Python Dependencies (Already Installed)**

- Flask, Streamlit, scikit-learn, pandas, numpy, etc.

### **External Tools (Need Manual Installation)**

#### **1. Slither Installation**

```bash
# Install Slither
pip install slither-analyzer

# Verify installation
slither --version
```

#### **2. Mythril Installation**

```bash
# Install Mythril
pip install mythril

# Verify installation
myth version
```

#### **3. Solidity Compiler**

```bash
# Install solc (Solidity compiler)
# Windows (using chocolatey):
choco install solidity

# Or download from: https://github.com/ethereum/solidity/releases
```

---

## 🎯 **Testing Each Component**

### **1. Test Dashboard**

- ✅ Already working at http://localhost:8501
- Upload a sample contract and run mock analysis

### **2. Test API Backend**

```bash
# Start API server
python -m src.api.app

# Test health endpoint
curl http://localhost:5000/health

# Test analysis endpoint
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"contract_code": "pragma solidity ^0.8.0; contract Test {}"}'
```

### **3. Test CLI**

```bash
# Test CLI help
python -m src.cli --help

# Test with sample contract
python -m src.cli analyze tests/fixtures/safe_contract.sol
```

### **4. Test External Tools**

```bash
# Test Slither
slither tests/fixtures/reentrancy_vulnerable.sol

# Test Mythril
myth analyze tests/fixtures/reentrancy_vulnerable.sol
```

---

## 🔄 **Typical Workflow**

### **For Development/Testing:**

1. **Start Dashboard**: `streamlit run dashboard/dashboard.py`
2. **Start API** (optional): `python -m src.api.app`
3. **Use Dashboard**: Upload contracts via web interface

### **For Production/Automation:**

1. **Setup Environment**: `python scripts/setup_environment.py`
2. **Start API Server**: `python -m src.api.app`
3. **Use CLI for Batch**: `python -m src.cli batch-analyze contracts/`

### **For Integration:**

1. **API Endpoints**: Use REST API for integration
2. **CLI Scripts**: Use CLI for automation
3. **Python Imports**: Import modules directly in code

---

## 📊 **What Works Right Now vs What Needs Setup**

### **✅ Currently Working (No Additional Setup)**

- Dashboard web interface
- Mock analysis with sample results
- All UI components and visualizations
- File upload and code editing
- Results display and export

### **⚙️ Needs Setup for Full Functionality**

- **API Backend**: Run `python -m src.api.app`
- **Real AI Analysis**: Train models with `python scripts/setup_environment.py`
- **Slither Integration**: Install Slither tool
- **Mythril Integration**: Install Mythril tool
- **Tool Comparison**: Requires external tools

### **🎯 Recommended Next Steps**

1. **Try the API**: `python -m src.api.app` (should work with mock data)
2. **Install Slither**: `pip install slither-analyzer`
3. **Test CLI**: `python -m src.cli --help`
4. **Setup Models**: `python scripts/setup_environment.py`

---

## 🚨 **Troubleshooting**

### **If API doesn't start:**

- Check if port 5000 is available
- Install missing dependencies: `pip install flask flask-cors`

### **If CLI doesn't work:**

- Check Python path: `python -m src.cli --version`
- Install missing dependencies from requirements.txt

### **If external tools fail:**

- Install Slither: `pip install slither-analyzer`
- Install Mythril: `pip install mythril`
- Install Solidity compiler

### **If models don't load:**

- Run setup script: `python scripts/setup_environment.py`
- Check if model files exist in expected locations

---

## 📞 **Quick Commands Summary**

```bash
# Dashboard (already running)
streamlit run dashboard/dashboard.py

# API Server
python -m src.api.app

# CLI Help
python -m src.cli --help

# Setup Everything
python scripts/setup_environment.py

# Install External Tools
pip install slither-analyzer mythril

# Test API Health
curl http://localhost:5000/health
```

The system is designed to be modular - you can run just the dashboard for demo purposes, or set up the full system for production use!
