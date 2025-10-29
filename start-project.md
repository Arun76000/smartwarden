# Smart Contract AI Analyzer - Project Startup Guide

## 🚀 Quick Start Guide

This guide will help you set up and run the Smart Contract AI Analyzer project from scratch. Follow these steps to get the system up and running.

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 5GB available space
- **Internet**: Required for downloading dependencies and models

### Required Software
1. **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
2. **Git** - [Download from git-scm.com](https://git-scm.com/downloads)
3. **Node.js 14+** (optional, for some tools) - [Download from nodejs.org](https://nodejs.org/)

---

## 🛠️ Installation Steps

### Step 1: Clone or Navigate to Project Directory
```bash
# If you haven't cloned the project yet:
git clone <repository-url>
cd smart-contract-ai-analyzer

# Or if you're already in the project directory:
cd /path/to/smart-contract-ai-analyzer
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter issues, try upgrading pip first:
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run Environment Setup Script
```bash
# Run the automated setup script
python scripts/setup_environment.py
```

This script will:
- Create necessary directories
- Download sample vulnerable contracts
- Set up configuration files
- Check for external tools
- Initialize Git repository (if needed)

### Step 5: Install External Security Tools (Optional but Recommended)
```bash
# Install Slither (static analysis tool)
pip install slither-analyzer

# Install Mythril (symbolic execution tool)
pip install mythril

# Install Solidity compiler
npm install -g solc
# OR
pip install py-solc-x
```

---

## 🏃‍♂️ Running the Project

### Option 1: Web Dashboard (Recommended for Beginners)
```bash
# Start the Streamlit dashboard
streamlit run dashboard/dashboard.py

# The dashboard will open in your browser at:
# http://localhost:8501
```

**Features Available:**
- Upload and analyze smart contracts
- Interactive vulnerability visualization
- Tool comparison results
- Performance metrics
- PDF report generation

### Option 2: REST API Server
```bash
# Start the Flask API server
python -m src.api.app

# API will be available at:
# http://localhost:5000/api
```

**API Endpoints:**
- `POST /api/analyze` - Analyze a smart contract
- `GET /api/health` - Check API health
- `GET /api/docs` - API documentation

### Option 3: Command Line Interface
```bash
# Analyze a single contract
python -m src.cli analyze contract.sol

# Analyze with all tools
python -m src.cli analyze contract.sol --slither --mythril --compare

# Batch analysis
python -m src.cli batch-analyze contracts/ results/

# Generate reports
python -m src.cli report results.json --format summary

# Check system status
python -m src.cli status
```

### Option 4: Using the Convenience Script
```bash
# Make the script executable (Linux/macOS)
chmod +x sca-cli.py

# Run analysis
python sca-cli.py analyze contract.sol
```

---

## 📁 Project Structure Overview

```
smart-contract-ai-analyzer/
├── src/                          # Core application code
│   ├── api/                      # REST API implementation
│   ├── data/                     # Data processing modules
│   ├── features/                 # Feature extraction
│   ├── models/                   # AI/ML models
│   ├── integration/              # External tool integration
│   ├── utils/                    # Utility functions
│   ├── visualization/            # Chart and plot generation
│   ├── reporting/                # PDF report generation
│   └── cli.py                    # Command-line interface
├── dashboard/                    # Streamlit web interface
│   ├── pages/                    # Dashboard pages
│   ├── components/               # Reusable UI components
│   └── utils/                    # Dashboard utilities
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── system/                   # Integration tests
│   └── fixtures/                 # Test data
├── configs/                      # Configuration files
├── docs/                         # Documentation
├── scripts/                      # Setup and utility scripts
├── data/                         # Data storage (created by setup)
├── models/                       # Trained models (created by setup)
├── results/                      # Analysis results (created by setup)
└── requirements.txt              # Python dependencies
```

---

## 🧪 Testing the Installation

### 1. Run Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/unit/ -v
pytest tests/system/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 2. Test CLI Functionality
```bash
# Check system status
python -m src.cli status

# Test with sample contract
python -m src.cli analyze data/raw/safe_contract.sol

# Test API health
curl http://localhost:5000/api/health
```

### 3. Test Dashboard
1. Start the dashboard: `streamlit run dashboard/dashboard.py`
2. Open browser to `http://localhost:8501`
3. Upload a sample contract from `data/raw/`
4. Verify analysis results display correctly

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
# API Configuration
FLASK_ENV=development
API_HOST=127.0.0.1
API_PORT=5000
LOG_LEVEL=INFO

# Dashboard Configuration
DASHBOARD_TITLE="Smart Contract AI Analyzer"
DASHBOARD_THEME=light

# External Tools
SLITHER_PATH=/usr/local/bin/slither
MYTHRIL_PATH=/usr/local/bin/myth

# Model Paths
BINARY_MODEL_PATH=models/binary_classifier.joblib
MULTICLASS_MODEL_PATH=models/multiclass_classifier.joblib

# Analysis Settings
DEFAULT_TIMEOUT=300
MAX_FILE_SIZE=1048576
```

### Configuration Files
- `configs/api_config.yaml` - API server settings
- `configs/dashboard_config.yaml` - Dashboard settings

---

## 📊 Sample Usage Examples

### Example 1: Analyze a Vulnerable Contract
```bash
# Create a test contract
cat > test_contract.sol << EOF
pragma solidity ^0.8.0;
contract VulnerableContract {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        msg.sender.call{value: amount}("");  // Vulnerable!
        balances[msg.sender] -= amount;
    }
}
EOF

# Analyze it
python -m src.cli analyze test_contract.sol --slither --compare
```

### Example 2: Batch Analysis
```bash
# Create a directory with multiple contracts
mkdir test_contracts
cp data/raw/*.sol test_contracts/

# Analyze all contracts
python -m src.cli batch-analyze test_contracts/ results/ --slither --mythril
```

### Example 3: API Usage
```bash
# Start API server
python -m src.api.app &

# Analyze via API
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.8.0; contract Safe {}",
    "analysis_options": {
      "include_ai_analysis": true,
      "include_slither": true
    }
  }'
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the project root and virtual environment is activated
cd /path/to/smart-contract-ai-analyzer
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

#### 2. Permission Errors
```bash
# Error: Permission denied
# Solution: Fix file permissions
chmod +x sca-cli.py
chmod +x scripts/setup_environment.py
```

#### 3. Port Already in Use
```bash
# Error: Port 5000 already in use
# Solution: Kill the process or use different port
# Find process: lsof -i :5000
# Kill process: kill -9 <PID>
# Or use different port: API_PORT=5001 python -m src.api.app
```

#### 4. External Tools Not Found
```bash
# Error: slither/mythril command not found
# Solution: Install external tools
pip install slither-analyzer mythril
# Or check PATH: echo $PATH
```

#### 5. Memory Issues
```bash
# Error: Out of memory
# Solution: Increase timeout and reduce batch size
python -m src.cli analyze contract.sol --timeout 600
```

#### 6. Model Files Missing
```bash
# Error: Model file not found
# Solution: Run setup script or create dummy models
python scripts/setup_environment.py
```

---

## 📈 Performance Optimization

### For Better Performance:
1. **Use SSD storage** for faster file I/O
2. **Increase RAM** for larger contract analysis
3. **Use parallel processing** for batch analysis:
   ```bash
   python -m src.cli batch-analyze contracts/ results/ --parallel 4
   ```
4. **Enable caching** in configuration files
5. **Use specific analysis tools** only when needed

---

## 🔄 Development Workflow

### For Developers:
1. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Run code quality checks**:
   ```bash
   black src/ tests/ dashboard/
   flake8 src/ tests/ dashboard/
   mypy src/
   ```

4. **Run tests before committing**:
   ```bash
   pytest tests/ -v --cov=src
   ```

---

## 📞 Getting Help

### Resources:
- **Documentation**: Check `docs/` directory
- **API Documentation**: `docs/api_documentation.md`
- **CLI Usage**: `docs/cli_usage.md`
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions

### Debug Mode:
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python -m src.cli analyze contract.sol --verbose

# Check system status
python -m src.cli status --verbose
```

---

## 🎯 Next Steps

After successful setup:

1. **Explore the Dashboard**: Upload sample contracts and explore features
2. **Try Different Analysis Tools**: Compare AI vs Slither vs Mythril results
3. **Generate Reports**: Create PDF reports for your analyses
4. **Integrate with CI/CD**: Use CLI for automated security testing
5. **Customize Models**: Train your own models with custom datasets
6. **Extend Functionality**: Add new vulnerability detection patterns

---

## 📝 Quick Reference Commands

```bash
# Setup
python scripts/setup_environment.py

# Start Dashboard
streamlit run dashboard/dashboard.py

# Start API
python -m src.api.app

# CLI Analysis
python -m src.cli analyze contract.sol
python -m src.cli batch-analyze contracts/ results/
python -m src.cli report results.json --format summary
python -m src.cli status

# Testing
pytest tests/ -v
python -m src.cli analyze data/raw/safe_contract.sol

# Development
black src/ && flake8 src/ && mypy src/
```

---

**🎉 Congratulations! Your Smart Contract AI Analyzer is now ready to use!**

For detailed usage instructions, refer to the specific documentation files in the `docs/` directory.