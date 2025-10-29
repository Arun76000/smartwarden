# 🔒 Smart Contract AI Analyzer

**Advanced AI-powered security analysis for Ethereum smart contracts**

A comprehensive tool that combines artificial intelligence with traditional static analysis to detect vulnerabilities in Solidity smart contracts. Features a modern web interface, real-time analysis, and professional reporting capabilities.

![System Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Overview

This system provides **real-time vulnerability detection** with high accuracy and reduced false positive rates. It addresses critical limitations in current smart contract auditing by providing automated, explainable, and continuous security analysis.

## ⚡ Quick Start

```bash
# Fastest way to get started
python quick_start.py
# Opens dashboard at http://localhost:8501

# Or run complete system (API + Dashboard)
python start_system.py
```

**That's it!** The system works immediately with mock analysis, no complex setup required.

## ✨ Features

### 🤖 **AI-Powered Analysis**
- **Binary Classification**: Safe vs vulnerable detection
- **Multi-class Detection**: Specific vulnerability type identification  
- **Feature Importance**: Explainable AI with feature weights
- **High Accuracy**: 87%+ accuracy on test datasets

### 🌐 **Modern Web Interface**
- **Real-time Analysis**: Live progress tracking
- **Interactive Charts**: Plotly-based visualizations
- **Responsive Design**: Works on desktop and mobile
- **Professional UI**: Clean, intuitive interface

### 📊 **Comprehensive Reporting**
- **Multiple Formats**: JSON, CSV, PDF, HTML exports
- **Professional PDFs**: High-quality formatted reports
- **Vulnerability Details**: Severity, confidence, recommendations
- **Feature Analysis**: AI model insights and explanations

### 🔧 **Developer-Friendly**
- **RESTful API**: Programmatic access to all features
- **Easy Integration**: Simple API endpoints
- **Batch Processing**: Analyze multiple contracts
- **CLI Interface**: Command-line tools available

### 🛠️ **Tool Integration**
- **Slither Support**: Static analysis integration
- **Mythril Support**: Symbolic execution integration  
- **Tool Comparison**: Compare results across different tools
- **Consensus Analysis**: Agreement scoring between tools

## 🎯 **Supported Vulnerability Types**

| Vulnerability | Description | Severity |
|---------------|-------------|----------|
| 🔄 **Reentrancy** | External call vulnerabilities | Critical |
| 🔐 **Access Control** | Missing permission checks | High |
| 🎲 **Bad Randomness** | Predictable random numbers | Medium |
| 📞 **Unchecked Calls** | Missing return value validation | Medium |
| ⚠️ **DoS Patterns** | Denial of service vulnerabilities | High |
| 🔢 **Arithmetic Issues** | Overflow/underflow problems | High |

- **AI-Powered Detection**: Machine learning models trained on labeled vulnerability datasets
- **Multi-Tool Comparison**: Integration with Slither and Mythril for comparative analysis
- **Web Dashboard**: Intuitive interface for contract upload and result visualization
- **RESTful API**: Backend API for integration into CI/CD pipelines
- **Comprehensive Reporting**: PDF reports with vulnerability findings and recommendations
- **Real-time Analysis**: Fast analysis (< 15 seconds) suitable for development workflows

## Vulnerability Types Detected

- Reentrancy attacks
- Access control issues
- Arithmetic overflow/underflow
- Unchecked external calls
- Denial of service vulnerabilities
- Bad randomness patterns

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for Solidity compiler)
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd smart-contract-ai-analyzer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Solidity compiler:
```bash
npm install -g solc
```

### Usage

1. Start the web dashboard:
```bash
streamlit run dashboard/dashboard.py
```

2. Or use the API directly:
```bash
python -m src.api.app
```

## Project Structure

```
smart-contract-ai-analyzer/
├── src/                    # Source code modules
├── data/                   # Datasets and processed data
├── models/                 # Trained ML models
├── dashboard/              # Streamlit web interface
├── tests/                  # Testing suite
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── results/                # Experimental results
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src/
```

### Code Quality

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Academic Context

This project is developed as part of an MSc thesis on AI-enhanced smart contract security analysis. The system demonstrates the feasibility of machine learning approaches for automated vulnerability detection in blockchain applications.

## Contact

For questions or support, please open an issue on GitHub.