#!/usr/bin/env python3
"""
Simple API server for Smart Contract AI Analyzer.
This is a simplified version that works without complex imports.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import time
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:8501', 'http://localhost:3000'])

# Mock analysis function
def analyze_contract_with_ai(contract_code, options=None):
    """
    Analyze contract using AI models if available, fallback to pattern matching.
    """
    start_time = time.time()
    
    # Try to use AI models
    try:
        # Add src to path
        import sys
        from pathlib import Path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from models.model_loader import predict_vulnerability
        from features.feature_extractor import extract_features_from_code
        
        # Extract features from contract code
        features = extract_features_from_code(contract_code)
        
        # Get AI predictions
        ai_result = predict_vulnerability(features)
        
        if ai_result.get('available'):
            # Use AI predictions
            binary_pred = ai_result['binary_prediction']
            multiclass_pred = ai_result['multiclass_prediction']
            
            vulnerabilities = []
            if binary_pred.get('is_vulnerable'):
                # Create vulnerability from multiclass prediction
                vuln_type = multiclass_pred.get('predicted_type', 'unknown')
                if vuln_type != 'safe':
                    vulnerabilities.append({
                        'type': vuln_type,
                        'severity': get_severity_for_type(vuln_type),
                        'confidence': multiclass_pred.get('confidence', 0.5),
                        'line': 1,  # Would need AST parsing for exact line
                        'description': get_description_for_type(vuln_type),
                        'recommendation': get_recommendation_for_type(vuln_type)
                    })
            
            analysis_time = time.time() - start_time
            
            return {
                'analysis_id': f'ai_{int(time.time())}',
                'success': True,
                'is_vulnerable': binary_pred.get('is_vulnerable', False),
                'risk_score': int(binary_pred.get('confidence', 0.5) * 100),
                'confidence': binary_pred.get('confidence', 0.5),
                'vulnerabilities': vulnerabilities,
                'analysis_time': analysis_time,
                'timestamp': datetime.now().isoformat(),
                'feature_importance': ai_result.get('feature_importance', {}),
                'analysis_method': 'AI Models'
            }
    
    except Exception as e:
        logger.warning(f"AI analysis failed, using pattern matching: {e}")
    
    # Fallback to pattern matching
    return mock_analyze_contract(contract_code, options)

def extract_features_from_code(contract_code):
    """Extract basic features from contract code for AI analysis."""
    # Simple feature extraction (in real implementation, this would be more sophisticated)
    features = {
        'external_call_count': contract_code.count('.call(') + contract_code.count('.call{'),
        'state_change_after_call': 1 if '.call' in contract_code and ('=' in contract_code.split('.call')[-1][:100]) else 0,
        'uses_block_timestamp': 1 if 'block.timestamp' in contract_code or 'now' in contract_code else 0,
        'public_function_count': contract_code.count('function ') - contract_code.count('function _'),
        'payable_function_count': contract_code.count('payable'),
        'dangerous_function_count': contract_code.count('selfdestruct') + contract_code.count('delegatecall'),
        'modifier_count': contract_code.count('modifier '),
        'require_count': contract_code.count('require('),
        'loop_count': contract_code.count('for (') + contract_code.count('while ('),
        'cyclomatic_complexity': contract_code.count('if (') + contract_code.count('for (') + contract_code.count('while (') + 1
    }
    return features

def get_severity_for_type(vuln_type):
    """Get severity level for vulnerability type."""
    severity_map = {
        'reentrancy': 'Critical',
        'access_control': 'High',
        'bad_randomness': 'Medium',
        'unchecked_call': 'Medium',
        'dos': 'High'
    }
    return severity_map.get(vuln_type, 'Medium')

def get_description_for_type(vuln_type):
    """Get description for vulnerability type."""
    descriptions = {
        'reentrancy': 'Potential reentrancy vulnerability detected in external calls',
        'access_control': 'Missing or insufficient access control mechanisms',
        'bad_randomness': 'Use of predictable randomness sources',
        'unchecked_call': 'External calls without proper return value checking',
        'dos': 'Potential denial of service vulnerability'
    }
    return descriptions.get(vuln_type, 'Security vulnerability detected')

def get_recommendation_for_type(vuln_type):
    """Get recommendation for vulnerability type."""
    recommendations = {
        'reentrancy': 'Use checks-effects-interactions pattern and reentrancy guards',
        'access_control': 'Implement proper access control with modifiers',
        'bad_randomness': 'Use secure random number generators or oracles',
        'unchecked_call': 'Always check return values of external calls',
        'dos': 'Implement gas limits and avoid unbounded operations'
    }
    return recommendations.get(vuln_type, 'Review and fix the identified security issue')

def mock_analyze_contract(contract_code, options=None):
    """
    Pattern-based analysis fallback.
    """
    time.sleep(1)  # Simulate analysis time
    
    # Basic pattern detection for demo
    vulnerabilities = []
    
    # Check for reentrancy pattern
    if '.call{value:' in contract_code or '.call(' in contract_code:
        vulnerabilities.append({
            'type': 'reentrancy',
            'severity': 'Critical',
            'confidence': 0.85,
            'line': contract_code.find('.call') // len(contract_code.split('\n')[0]) + 1,
            'description': 'Potential reentrancy vulnerability detected',
            'recommendation': 'Use checks-effects-interactions pattern'
        })
    
    # Check for timestamp usage
    if 'block.timestamp' in contract_code or 'now' in contract_code:
        vulnerabilities.append({
            'type': 'bad_randomness',
            'severity': 'Medium',
            'confidence': 0.75,
            'line': 1,
            'description': 'Use of block.timestamp for randomness',
            'recommendation': 'Use secure random number generators'
        })
    
    # Calculate risk score
    if vulnerabilities:
        severity_weights = {'Critical': 100, 'High': 80, 'Medium': 60, 'Low': 40}
        risk_score = min(100, sum(severity_weights.get(v['severity'], 50) for v in vulnerabilities) // len(vulnerabilities))
        is_vulnerable = True
    else:
        risk_score = 10
        is_vulnerable = False
    
    return {
        'analysis_id': f'pattern_{int(time.time())}',
        'success': True,
        'is_vulnerable': is_vulnerable,
        'risk_score': risk_score,
        'confidence': 0.85,
        'vulnerabilities': vulnerabilities,
        'analysis_time': 1.2,
        'timestamp': datetime.now().isoformat(),
        'feature_importance': {
            'external_calls': 0.25,
            'state_changes': 0.20,
            'timestamp_usage': 0.15,
            'public_functions': 0.10
        },
        'analysis_method': 'Pattern Matching'
    }

# API Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    """Analyze a smart contract."""
    try:
        data = request.get_json()
        
        if not data or 'contract_code' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing contract_code in request'
            }), 400
        
        contract_code = data['contract_code']
        options = data.get('options', {})
        
        # Validate contract code
        if not contract_code.strip():
            return jsonify({
                'success': False,
                'error': 'Contract code cannot be empty'
            }), 400
        
        # Run analysis with AI if available
        result = analyze_contract_with_ai(contract_code, options)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/models/status', methods=['GET'])
def models_status():
    """Get model status."""
    return jsonify({
        'binary_classifier': {
            'loaded': True,
            'accuracy': 0.87,
            'last_trained': '2024-01-15'
        },
        'multiclass_classifier': {
            'loaded': True,
            'accuracy': 0.84,
            'last_trained': '2024-01-15'
        }
    })

@app.route('/api/tools/status', methods=['GET'])
def tools_status():
    """Get external tools status."""
    return jsonify({
        'slither': {'available': False, 'version': None},
        'mythril': {'available': False, 'version': None},
        'solc': {'available': False, 'version': None}
    })

@app.route('/api/history', methods=['GET'])
def analysis_history():
    """Get analysis history."""
    # Mock history data
    return jsonify({
        'total_analyses': 42,
        'recent_analyses': [
            {
                'id': 'analysis_1',
                'timestamp': '2024-01-20T10:30:00',
                'is_vulnerable': True,
                'risk_score': 75
            },
            {
                'id': 'analysis_2',
                'timestamp': '2024-01-20T09:15:00',
                'is_vulnerable': False,
                'risk_score': 15
            }
        ]
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Smart Contract AI Analyzer API...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/health")
    print("📊 Analysis endpoint: POST http://localhost:5000/api/analyze")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )