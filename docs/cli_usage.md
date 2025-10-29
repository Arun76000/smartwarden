# Smart Contract AI Analyzer - CLI Usage Guide

The Smart Contract AI Analyzer provides a comprehensive command-line interface for analyzing smart contracts using AI models and external security tools.

## Installation

1. **Install the package**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install external tools** (optional):
   ```bash
   pip install slither-analyzer mythril
   ```

3. **Set up the environment**:
   ```bash
   python scripts/setup_environment.py
   ```

## Quick Start

### Basic Analysis
```bash
# Analyze a single contract with AI
python -m src.cli analyze contract.sol

# Or use the convenience script
python sca-cli.py analyze contract.sol
```

### Advanced Analysis
```bash
# Analyze with all tools and comparison
python -m src.cli analyze contract.sol --slither --mythril --compare

# Save results to file
python -m src.cli analyze contract.sol --output results.json
```

## Commands

### 1. analyze
Analyze a single smart contract file.

**Usage:**
```bash
python -m src.cli analyze <contract_file> [options]
```

**Options:**
- `--output, -o`: Output file for results (JSON format)
- `--no-ai`: Disable AI analysis
- `--slither`: Enable Slither static analysis
- `--mythril`: Enable Mythril symbolic execution
- `--compare`: Compare results from different tools
- `--timeout`: Analysis timeout in seconds (default: 300)

**Examples:**
```bash
# Basic AI analysis
python -m src.cli analyze examples/vulnerable.sol

# Full analysis with all tools
python -m src.cli analyze examples/vulnerable.sol --slither --mythril --compare

# AI-only analysis with custom output
python -m src.cli analyze contract.sol --output my_results.json

# External tools only (no AI)
python -m src.cli analyze contract.sol --no-ai --slither --mythril
```

### 2. batch-analyze
Analyze multiple smart contracts in a directory.

**Usage:**
```bash
python -m src.cli batch-analyze <input_directory> <output_directory> [options]
```

**Options:**
- `--no-ai`: Disable AI analysis
- `--slither`: Enable Slither analysis for all contracts
- `--mythril`: Enable Mythril analysis for all contracts
- `--compare`: Compare tool results for each contract
- `--parallel`: Number of parallel processes (default: 1)

**Examples:**
```bash
# Batch analyze with AI only
python -m src.cli batch-analyze contracts/ results/

# Batch analyze with all tools
python -m src.cli batch-analyze contracts/ results/ --slither --mythril --compare

# Parallel processing
python -m src.cli batch-analyze contracts/ results/ --parallel 4
```

### 3. report
Generate analysis reports from results files.

**Usage:**
```bash
python -m src.cli report <results_file> [options]
```

**Options:**
- `--format`: Output format (json, summary, csv)
- `--output, -o`: Output file (default: stdout)

**Examples:**
```bash
# Generate summary report
python -m src.cli report results.json --format summary

# Generate CSV report
python -m src.cli report batch_results.json --format csv --output report.csv

# Pretty-print JSON
python -m src.cli report results.json --format json
```

### 4. status
Check the availability of external tools and system status.

**Usage:**
```bash
python -m src.cli status
```

**Output:**
```
External Tools Status:
----------------------------------------
  ✓ Slither: Available
  ✗ Mythril: Not available
```

### 5. models
List available AI models and their information.

**Usage:**
```bash
python -m src.cli models
```

**Output:**
```
Available Models:
----------------------------------------
  binary_classifier.joblib
    Size: 2.3 MB
    Modified: 2024-01-15 10:30:45

  multiclass_classifier.joblib
    Size: 3.1 MB
    Modified: 2024-01-15 10:32:12
```

## Global Options

- `--version`: Show version information
- `--verbose, -v`: Enable verbose logging
- `--config`: Path to configuration file

## Output Formats

### JSON Output
The default output format provides structured data:

```json
{
  "contract_path": "contract.sol",
  "timestamp": "2024-01-15T10:30:45.123456",
  "analysis_options": {
    "ai_analysis": true,
    "slither_analysis": true,
    "mythril_analysis": false,
    "compare_tools": true
  },
  "results": {
    "ai_analysis": {
      "binary_classification": {
        "prediction": "vulnerable",
        "confidence": 0.87,
        "vulnerability_probability": 0.87
      },
      "multiclass_classification": {
        "predicted_type": "reentrancy",
        "probabilities": {
          "safe": 0.13,
          "reentrancy": 0.72,
          "access_control": 0.08,
          "arithmetic": 0.04,
          "unchecked_calls": 0.02,
          "dos": 0.01,
          "bad_randomness": 0.00
        }
      },
      "execution_time": 0.45
    },
    "slither_analysis": {
      "vulnerabilities": [
        {
          "type": "reentrancy-eth",
          "severity": "High",
          "confidence": "High",
          "description": "Reentrancy vulnerability detected",
          "line": 25
        }
      ],
      "execution_time": 2.1
    },
    "tool_comparison": {
      "consensus": "vulnerable",
      "agreement_score": 0.95,
      "conflicting_results": false
    }
  }
}
```

### Summary Report
Human-readable summary format:

```
============================================================
SMART CONTRACT ANALYSIS REPORT
============================================================

Contract: vulnerable_contract.sol
Timestamp: 2024-01-15T10:30:45.123456

AI Analysis:
  Prediction: VULNERABLE
  Confidence: 87.00%
  Vulnerability Probability: 87.00%
  Predicted Type: reentrancy
  Top Probabilities:
    reentrancy: 72.00%
    access_control: 8.00%
    arithmetic: 4.00%

Slither Analysis:
  Vulnerabilities Found: 3
    - reentrancy-eth: High
    - unused-return: Medium
    - pragma: Informational
  Execution Time: 2.10s
============================================================
```

### CSV Report
Tabular format suitable for spreadsheet analysis:

```csv
contract_path,ai_prediction,ai_confidence,predicted_type,slither_vulnerabilities,mythril_vulnerabilities,analysis_time
contract1.sol,vulnerable,0.87,reentrancy,3,1,2.5
contract2.sol,safe,0.92,safe,0,0,1.8
```

## Configuration

### Environment Variables
```bash
# Logging level
export LOG_LEVEL=DEBUG

# Model paths
export BINARY_MODEL_PATH=models/custom_binary.joblib
export MULTICLASS_MODEL_PATH=models/custom_multiclass.joblib

# Tool paths
export SLITHER_PATH=/usr/local/bin/slither
export MYTHRIL_PATH=/usr/local/bin/myth
```

### Configuration File
Create a YAML configuration file:

```yaml
# config.yaml
models:
  binary_classifier: "models/binary_classifier.joblib"
  multiclass_classifier: "models/multiclass_classifier.joblib"

tools:
  slither:
    enabled: true
    path: "/usr/local/bin/slither"
    timeout: 300
  mythril:
    enabled: true
    path: "/usr/local/bin/myth"
    timeout: 600

analysis:
  default_timeout: 300
  max_file_size: 1048576  # 1MB
  
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

Use with:
```bash
python -m src.cli analyze contract.sol --config config.yaml
```

## Integration Examples

### CI/CD Pipeline
```bash
#!/bin/bash
# analyze_contracts.sh

# Analyze all contracts in the project
python -m src.cli batch-analyze contracts/ analysis_results/ --slither --compare

# Generate summary report
python -m src.cli report analysis_results/batch_analysis_summary.json --format summary

# Check if any vulnerabilities were found
if grep -q '"prediction": "vulnerable"' analysis_results/*.json; then
    echo "⚠️  Vulnerabilities detected!"
    exit 1
else
    echo "✅ All contracts appear safe"
    exit 0
fi
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Analyze staged .sol files
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.sol$'); do
    echo "Analyzing $file..."
    python -m src.cli analyze "$file" --slither --compare
    
    if [ $? -ne 0 ]; then
        echo "❌ Analysis failed for $file"
        exit 1
    fi
done

echo "✅ All contracts analyzed successfully"
```

### Automated Monitoring
```python
#!/usr/bin/env python3
# monitor_contracts.py

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ContractHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.sol'):
            print(f"Contract modified: {event.src_path}")
            subprocess.run([
                'python', '-m', 'src.cli', 'analyze', 
                event.src_path, '--slither', '--compare'
            ])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ContractHandler(), 'contracts/', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

## Advanced Usage

### Custom Analysis Workflows

**1. Security Audit Workflow**
```bash
#!/bin/bash
# security_audit.sh

CONTRACT_DIR="$1"
REPORT_DIR="audit_$(date +%Y%m%d_%H%M%S)"

if [ -z "$CONTRACT_DIR" ]; then
    echo "Usage: $0 <contract_directory>"
    exit 1
fi

echo "🔍 Starting security audit for $CONTRACT_DIR"
mkdir -p "$REPORT_DIR"

# Step 1: Comprehensive analysis
echo "Step 1: Running comprehensive analysis..."
python -m src.cli batch-analyze "$CONTRACT_DIR" "$REPORT_DIR/analysis" \
    --slither --mythril --compare --parallel 4

# Step 2: Generate reports
echo "Step 2: Generating reports..."
python -m src.cli report "$REPORT_DIR/analysis/batch_analysis_summary.json" \
    --format summary --output "$REPORT_DIR/summary_report.txt"

python -m src.cli report "$REPORT_DIR/analysis/batch_analysis_summary.json" \
    --format csv --output "$REPORT_DIR/vulnerability_matrix.csv"

# Step 3: Extract high-severity findings
echo "Step 3: Extracting critical findings..."
python3 << EOF
import json
import sys

with open('$REPORT_DIR/analysis/batch_analysis_summary.json', 'r') as f:
    data = json.load(f)

critical_findings = []
for result in data.get('results', []):
    contract_path = result.get('contract_path', 'Unknown')
    
    # Check AI predictions
    if 'results' in result and 'ai_analysis' in result['results']:
        ai_result = result['results']['ai_analysis']
        if 'binary_classification' in ai_result:
            if ai_result['binary_classification']['prediction'] == 'vulnerable':
                confidence = ai_result['binary_classification']['confidence']
                if confidence > 0.8:
                    critical_findings.append({
                        'contract': contract_path,
                        'type': 'AI High Confidence Vulnerability',
                        'confidence': confidence,
                        'details': ai_result.get('multiclass_classification', {}).get('predicted_type', 'Unknown')
                    })
    
    # Check Slither findings
    if 'results' in result and 'slither_analysis' in result['results']:
        slither_result = result['results']['slither_analysis']
        for vuln in slither_result.get('vulnerabilities', []):
            if vuln.get('severity', '').lower() in ['high', 'critical']:
                critical_findings.append({
                    'contract': contract_path,
                    'type': f"Slither {vuln.get('severity', 'Unknown')}",
                    'vulnerability': vuln.get('type', 'Unknown'),
                    'description': vuln.get('description', 'No description')
                })

# Save critical findings
with open('$REPORT_DIR/critical_findings.json', 'w') as f:
    json.dump(critical_findings, f, indent=2)

print(f"Found {len(critical_findings)} critical findings")
EOF

echo "✅ Security audit completed. Results in $REPORT_DIR/"
```

**2. Continuous Integration Script**
```bash
#!/bin/bash
# ci_security_check.sh

set -e

echo "🔒 Running security checks..."

# Create temporary results directory
RESULTS_DIR=$(mktemp -d)
trap "rm -rf $RESULTS_DIR" EXIT

# Analyze all contracts
python -m src.cli batch-analyze contracts/ "$RESULTS_DIR" --slither --compare

# Check for vulnerabilities
VULNERABLE_COUNT=$(python3 << EOF
import json
import sys

try:
    with open('$RESULTS_DIR/batch_analysis_summary.json', 'r') as f:
        data = json.load(f)
    
    vulnerable_count = 0
    for result in data.get('results', []):
        if 'results' in result and 'ai_analysis' in result['results']:
            ai_result = result['results']['ai_analysis']
            if 'binary_classification' in ai_result:
                if ai_result['binary_classification']['prediction'] == 'vulnerable':
                    if ai_result['binary_classification']['confidence'] > 0.7:
                        vulnerable_count += 1
    
    print(vulnerable_count)
except Exception as e:
    print(0)
EOF
)

if [ "$VULNERABLE_COUNT" -gt 0 ]; then
    echo "❌ Found $VULNERABLE_COUNT high-confidence vulnerabilities"
    python -m src.cli report "$RESULTS_DIR/batch_analysis_summary.json" --format summary
    exit 1
else
    echo "✅ No high-confidence vulnerabilities detected"
    exit 0
fi
```

### Custom Output Processing

**1. Vulnerability Dashboard Data**
```python
#!/usr/bin/env python3
# generate_dashboard_data.py

import json
import sys
from collections import defaultdict
from datetime import datetime

def process_analysis_results(results_file):
    """Process analysis results for dashboard display"""
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    dashboard_data = {
        'summary': {
            'total_contracts': 0,
            'vulnerable_contracts': 0,
            'safe_contracts': 0,
            'analysis_timestamp': datetime.now().isoformat()
        },
        'vulnerability_breakdown': defaultdict(int),
        'tool_performance': defaultdict(lambda: {'total': 0, 'vulnerabilities': 0}),
        'contracts': []
    }
    
    results = data.get('results', [data] if 'contract_path' in data else [])
    
    for result in results:
        contract_info = {
            'path': result.get('contract_path', 'Unknown'),
            'status': 'unknown',
            'vulnerabilities': [],
            'tools_used': []
        }
        
        dashboard_data['summary']['total_contracts'] += 1
        
        if 'results' in result:
            analysis_results = result['results']
            
            # Process AI analysis
            if 'ai_analysis' in analysis_results:
                ai_result = analysis_results['ai_analysis']
                contract_info['tools_used'].append('AI')
                
                if 'binary_classification' in ai_result:
                    binary = ai_result['binary_classification']
                    prediction = binary['prediction']
                    confidence = binary['confidence']
                    
                    if prediction == 'vulnerable' and confidence > 0.7:
                        contract_info['status'] = 'vulnerable'
                        dashboard_data['summary']['vulnerable_contracts'] += 1
                        
                        if 'multiclass_classification' in ai_result:
                            vuln_type = ai_result['multiclass_classification']['predicted_type']
                            dashboard_data['vulnerability_breakdown'][vuln_type] += 1
                            contract_info['vulnerabilities'].append({
                                'type': vuln_type,
                                'source': 'AI',
                                'confidence': confidence
                            })
                    else:
                        if contract_info['status'] == 'unknown':
                            contract_info['status'] = 'safe'
                            dashboard_data['summary']['safe_contracts'] += 1
            
            # Process Slither analysis
            if 'slither_analysis' in analysis_results:
                slither_result = analysis_results['slither_analysis']
                contract_info['tools_used'].append('Slither')
                dashboard_data['tool_performance']['slither']['total'] += 1
                
                vulnerabilities = slither_result.get('vulnerabilities', [])
                if vulnerabilities:
                    dashboard_data['tool_performance']['slither']['vulnerabilities'] += 1
                    
                    for vuln in vulnerabilities:
                        if vuln.get('severity', '').lower() in ['high', 'medium']:
                            contract_info['vulnerabilities'].append({
                                'type': vuln.get('type', 'Unknown'),
                                'source': 'Slither',
                                'severity': vuln.get('severity', 'Unknown'),
                                'description': vuln.get('description', '')
                            })
            
            # Process Mythril analysis
            if 'mythril_analysis' in analysis_results:
                mythril_result = analysis_results['mythril_analysis']
                contract_info['tools_used'].append('Mythril')
                dashboard_data['tool_performance']['mythril']['total'] += 1
                
                vulnerabilities = mythril_result.get('vulnerabilities', [])
                if vulnerabilities:
                    dashboard_data['tool_performance']['mythril']['vulnerabilities'] += 1
                    
                    for vuln in vulnerabilities:
                        contract_info['vulnerabilities'].append({
                            'type': vuln.get('type', 'Unknown'),
                            'source': 'Mythril',
                            'severity': vuln.get('severity', 'Unknown'),
                            'description': vuln.get('description', '')
                        })
        
        dashboard_data['contracts'].append(contract_info)
    
    return dashboard_data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_dashboard_data.py <results_file.json>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    dashboard_data = process_analysis_results(results_file)
    
    print(json.dumps(dashboard_data, indent=2))
```

**2. Risk Assessment Report**
```python
#!/usr/bin/env python3
# risk_assessment.py

import json
import sys
from typing import Dict, List, Any

class RiskAssessment:
    def __init__(self):
        self.risk_weights = {
            'reentrancy': 0.9,
            'access_control': 0.8,
            'arithmetic': 0.7,
            'unchecked_calls': 0.6,
            'dos': 0.5,
            'bad_randomness': 0.4
        }
        
        self.severity_weights = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.5,
            'low': 0.2,
            'informational': 0.1
        }
    
    def calculate_risk_score(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate overall risk score for a contract"""
        risk_score = 0.0
        max_score = 0.0
        
        if 'results' not in analysis_result:
            return 0.0
        
        results = analysis_result['results']
        
        # AI analysis contribution
        if 'ai_analysis' in results:
            ai_result = results['ai_analysis']
            
            if 'binary_classification' in ai_result:
                binary = ai_result['binary_classification']
                if binary['prediction'] == 'vulnerable':
                    confidence = binary['confidence']
                    risk_score += confidence * 0.4  # 40% weight for AI binary
                    max_score += 0.4
            
            if 'multiclass_classification' in ai_result:
                multiclass = ai_result['multiclass_classification']
                predicted_type = multiclass['predicted_type']
                probability = multiclass['probabilities'].get(predicted_type, 0)
                
                if predicted_type in self.risk_weights:
                    type_weight = self.risk_weights[predicted_type]
                    risk_score += probability * type_weight * 0.3  # 30% weight for AI multiclass
                    max_score += 0.3
        
        # Slither analysis contribution
        if 'slither_analysis' in results:
            slither_result = results['slither_analysis']
            vulnerabilities = slither_result.get('vulnerabilities', [])
            
            slither_score = 0.0
            for vuln in vulnerabilities:
                severity = vuln.get('severity', 'low').lower()
                if severity in self.severity_weights:
                    slither_score += self.severity_weights[severity]
            
            # Normalize and add to risk score
            if vulnerabilities:
                normalized_slither = min(slither_score / len(vulnerabilities), 1.0)
                risk_score += normalized_slither * 0.2  # 20% weight for Slither
                max_score += 0.2
        
        # Mythril analysis contribution
        if 'mythril_analysis' in results:
            mythril_result = results['mythril_analysis']
            vulnerabilities = mythril_result.get('vulnerabilities', [])
            
            mythril_score = 0.0
            for vuln in vulnerabilities:
                severity = vuln.get('severity', 'low').lower()
                if severity in self.severity_weights:
                    mythril_score += self.severity_weights[severity]
            
            # Normalize and add to risk score
            if vulnerabilities:
                normalized_mythril = min(mythril_score / len(vulnerabilities), 1.0)
                risk_score += normalized_mythril * 0.1  # 10% weight for Mythril
                max_score += 0.1
        
        # Normalize final score
        if max_score > 0:
            return min(risk_score / max_score, 1.0)
        else:
            return 0.0
    
    def get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        elif risk_score >= 0.2:
            return "LOW"
        else:
            return "MINIMAL"
    
    def generate_report(self, results_file: str) -> Dict[str, Any]:
        """Generate comprehensive risk assessment report"""
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        results = data.get('results', [data] if 'contract_path' in data else [])
        
        report = {
            'assessment_summary': {
                'total_contracts': len(results),
                'risk_distribution': {
                    'CRITICAL': 0,
                    'HIGH': 0,
                    'MEDIUM': 0,
                    'LOW': 0,
                    'MINIMAL': 0
                },
                'average_risk_score': 0.0
            },
            'contract_assessments': []
        }
        
        total_risk_score = 0.0
        
        for result in results:
            risk_score = self.calculate_risk_score(result)
            risk_level = self.get_risk_level(risk_score)
            
            contract_assessment = {
                'contract_path': result.get('contract_path', 'Unknown'),
                'risk_score': round(risk_score, 3),
                'risk_level': risk_level,
                'recommendations': self.get_recommendations(result, risk_score)
            }
            
            report['contract_assessments'].append(contract_assessment)
            report['assessment_summary']['risk_distribution'][risk_level] += 1
            total_risk_score += risk_score
        
        if results:
            report['assessment_summary']['average_risk_score'] = round(
                total_risk_score / len(results), 3
            )
        
        return report
    
    def get_recommendations(self, analysis_result: Dict[str, Any], risk_score: float) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        if risk_score >= 0.8:
            recommendations.append("🚨 URGENT: This contract requires immediate security review")
            recommendations.append("Consider halting deployment until vulnerabilities are addressed")
        elif risk_score >= 0.6:
            recommendations.append("⚠️ HIGH PRIORITY: Schedule comprehensive security audit")
            recommendations.append("Implement additional testing before production deployment")
        elif risk_score >= 0.4:
            recommendations.append("📋 MEDIUM PRIORITY: Review identified issues and implement fixes")
            recommendations.append("Consider additional static analysis tools")
        elif risk_score >= 0.2:
            recommendations.append("✅ LOW RISK: Monitor for best practices compliance")
            recommendations.append("Regular security reviews recommended")
        else:
            recommendations.append("✅ MINIMAL RISK: Contract appears secure")
            recommendations.append("Maintain current security practices")
        
        # Specific recommendations based on findings
        if 'results' in analysis_result:
            results = analysis_result['results']
            
            if 'ai_analysis' in results:
                ai_result = results['ai_analysis']
                if 'multiclass_classification' in ai_result:
                    predicted_type = ai_result['multiclass_classification']['predicted_type']
                    
                    if predicted_type == 'reentrancy':
                        recommendations.append("🔄 Implement reentrancy guards (ReentrancyGuard)")
                        recommendations.append("Follow checks-effects-interactions pattern")
                    elif predicted_type == 'access_control':
                        recommendations.append("🔐 Review and strengthen access control mechanisms")
                        recommendations.append("Implement role-based access control")
                    elif predicted_type == 'arithmetic':
                        recommendations.append("🔢 Use SafeMath library or Solidity 0.8+ built-in checks")
                        recommendations.append("Add explicit overflow/underflow protection")
        
        return recommendations

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python risk_assessment.py <results_file.json>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    assessor = RiskAssessment()
    report = assessor.generate_report(results_file)
    
    print(json.dumps(report, indent=2))
```

## API Integration

### REST API Client
```python
#!/usr/bin/env python3
# api_client.py

import requests
import json
import sys
from typing import Dict, Any, Optional

class SmartContractAnalyzerAPI:
    def __init__(self, base_url: str = "http://localhost:5000/api"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def analyze_contract(self, contract_code: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze contract via API"""
        if options is None:
            options = {"include_ai_analysis": True}
        
        payload = {
            "contract_code": contract_code,
            "analysis_options": options
        }
        
        response = self.session.post(
            f"{self.base_url}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        return response.json()
    
    def analyze_file(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze contract file via API"""
        with open(file_path, 'r', encoding='utf-8') as f:
            contract_code = f.read()
        
        return self.analyze_contract(contract_code, options)
    
    def get_health(self) -> Dict[str, Any]:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# CLI wrapper for API client
def main():
    if len(sys.argv) < 2:
        print("Usage: python api_client.py <contract_file> [api_url]")
        sys.exit(1)
    
    contract_file = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:5000/api"
    
    client = SmartContractAnalyzerAPI(api_url)
    
    try:
        # Check API health
        health = client.get_health()
        print(f"API Status: {health.get('status', 'unknown')}")
        
        # Analyze contract
        result = client.analyze_file(contract_file)
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()$'); do
    echo "Analyzing $file..."
    python -m src.cli analyze "$file" --slither --compare
    
    if [ $? -ne 0 ]; then
        echo "❌ Analysis failed for $file"
        exit 1
    fi
done

echo "✅ All contracts analyzed successfully"
```

### Automated Monitoring
```python
#!/usr/bin/env python3
# monitor_contracts.py

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ContractHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.sol'):
            print(f"Contract modified: {event.src_path}")
            subprocess.run([
                'python', '-m', 'src.cli', 'analyze', 
                event.src_path, '--slither', '--compare'
            ])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ContractHandler(), 'contracts/', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Ensure you're in the project root directory
cd /path/to/smart-contract-ai-analyzer

# Install dependencies
pip install -r requirements.txt

# Run from project root
python -m src.cli analyze contract.sol
```

**2. External tools not found**
```bash
# Check tool availability
python -m src.cli status

# Install missing tools
pip install slither-analyzer mythril
```

**3. Model files not found**
```bash
# Check available models
python -m src.cli models

# Run setup script to download/create models
python scripts/setup_environment.py
```

**4. Permission errors**
```bash
# Make CLI script executable
chmod +x sca-cli.py

# Or run with python
python sca-cli.py analyze contract.sol
```

**5. Memory issues with large contracts**
```bash
# Increase timeout
python -m src.cli analyze large_contract.sol --timeout 600

# Disable memory-intensive tools
python -m src.cli analyze large_contract.sol --no-ai --slither
```

### Debug Mode
```bash
# Enable verbose logging
python -m src.cli analyze contract.sol --verbose

# Check system status
python -m src.cli status --verbose
```

## Performance Tips

1. **Parallel Processing**: Use `--parallel` for batch analysis
2. **Selective Analysis**: Use `--no-ai` or specific tool flags to reduce analysis time
3. **Timeout Management**: Adjust `--timeout` based on contract complexity
4. **Result Caching**: Results are automatically cached to avoid re-analysis

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the main documentation in `docs/`
- Open an issue on the project repository
- Use `--verbose` flag for detailed error information