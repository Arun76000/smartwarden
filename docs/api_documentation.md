# API Documentation

## Smart Contract Security Analyzer REST API

This document provides comprehensive documentation for the Smart Contract Security Analyzer REST API.

### Base URL
```
http://localhost:5000/api
```

### Authentication
Currently, the API does not require authentication. This may change in future versions.

### Content Type
All requests should use `Content-Type: application/json` unless otherwise specified.

### Rate Limiting
- **Rate Limit**: 100 requests per minute per IP
- **Burst Limit**: 10 requests per second
- **Headers**: Rate limit information is returned in response headers:
  - `X-RateLimit-Limit`: Request limit per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

---

## Endpoints

### 1. Health Check

#### `GET /health`

Check the health status of the API service.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600,
  "services": {
    "database": "healthy",
    "ml_models": "healthy",
    "external_tools": {
      "slither": "available",
      "mythril": "available"
    }
  }
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

---

### 2. Contract Analysis

#### `POST /analyze`

Analyze a smart contract for security vulnerabilities.

**Request Body:**
```json
{
  "contract_code": "pragma solidity ^0.8.0;\\n\\ncontract Example { ... }",
  "filename": "Example.sol",
  "analysis_options": {
    "include_ai_analysis": true,
    "include_slither": true,
    "include_mythril": true,
    "include_feature_importance": true,
    "detailed_report": true
  },
  "include_tool_comparison": true,
  "generate_pdf_report": false
}
```

**Parameters:**
- `contract_code` (string, required): Solidity source code
- `filename` (string, optional): Contract filename (default: "contract.sol")
- `analysis_options` (object, optional): Analysis configuration
  - `include_ai_analysis` (boolean): Use AI models (default: true)
  - `include_slither` (boolean): Run Slither analysis (default: true)
  - `include_mythril` (boolean): Run Mythril analysis (default: false)
  - `include_feature_importance` (boolean): Include feature importance (default: true)
  - `detailed_report` (boolean): Generate detailed report (default: true)
- `include_tool_comparison` (boolean): Compare tools (default: true)
- `generate_pdf_report` (boolean): Generate PDF report (default: false)

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis_1642248600",
    "contract_hash": "abc123def456",
    "overall_risk_score": 75,
    "is_vulnerable": true,
    "confidence_level": 0.87,
    "vulnerabilities": [
      {
        "vulnerability_type": "reentrancy",
        "severity": "Critical",
        "confidence": 0.92,
        "line_number": 15,
        "description": "Potential reentrancy vulnerability detected",
        "recommendation": "Use checks-effects-interactions pattern",
        "code_snippet": "msg.sender.call{value: amount}(\"\")",
        "tool_source": "AI Classifier"
      }
    ],
    "feature_importance": {
      "external_call_count": 0.25,
      "state_change_after_call": 0.20,
      "uses_block_timestamp": 0.15
    },
    "tool_comparison": {
      "consensus_findings": ["reentrancy"],
      "agreement_score": 0.85,
      "tool_performances": {
        "ai_binary": {
          "prediction": "vulnerable",
          "confidence": 0.87,
          "execution_time": 0.5,
          "success": true
        },
        "slither": {
          "findings_count": 2,
          "execution_time": 1.2,
          "success": true
        }
      }
    },
    "analysis_time": 2.5,
    "timestamp": "2024-01-15T10:30:00Z",
    "success": true
  },
  "message": "Contract analysis completed successfully"
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid contract code or parameters
- `413 Payload Too Large`: Contract code exceeds size limit
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Analysis failed

---

#### `POST /analyze/file`

Analyze a smart contract from file upload.

**Request:** Multipart form data
- `file`: Solidity contract file (.sol)
- `options`: JSON string with analysis options (optional)

**Response:** Same as `/analyze` endpoint

**Status Codes:** Same as `/analyze` endpoint

---

#### `GET /analysis/{analysis_id}`

Retrieve analysis results by ID.

**Parameters:**
- `analysis_id` (string): Analysis identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis_1642248600",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z",
    // ... full analysis results
  }
}
```

**Status Codes:**
- `200 OK`: Results retrieved successfully
- `404 Not Found`: Analysis ID not found
- `500 Internal Server Error`: Retrieval failed

---

### 3. Model Information

#### `GET /models/info`

Get information about available ML models.

**Response:**
```json
{
  "success": true,
  "data": {
    "binary_classifier": {
      "available": true,
      "model_type": "RandomForestClassifier",
      "accuracy": 0.87,
      "last_trained": "2024-01-15T10:30:00Z"
    },
    "multiclass_classifier": {
      "available": true,
      "model_type": "RandomForestClassifier",
      "accuracy": 0.83,
      "classes": ["safe", "reentrancy", "access_control", "arithmetic"],
      "last_trained": "2024-01-15T10:30:00Z"
    },
    "feature_extractor": {
      "available": true,
      "feature_count": 35,
      "version": "1.0.0"
    }
  }
}
```

**Status Codes:**
- `200 OK`: Information retrieved successfully
- `500 Internal Server Error`: Failed to get model information

---

#### `GET /models/performance`

Get model performance metrics.

**Response:**
```json
{
  "success": true,
  "data": {
    "binary_classifier": {
      "accuracy": 0.87,
      "precision": 0.85,
      "recall": 0.89,
      "f1_score": 0.87,
      "roc_auc": 0.92,
      "test_samples": 150
    },
    "multiclass_classifier": {
      "accuracy": 0.83,
      "macro_f1": 0.81,
      "micro_f1": 0.83,
      "per_class_metrics": {
        "safe": {"precision": 0.90, "recall": 0.88, "f1": 0.89},
        "reentrancy": {"precision": 0.82, "recall": 0.85, "f1": 0.83}
      },
      "test_samples": 150
    }
  }
}
```

**Status Codes:**
- `200 OK`: Performance metrics retrieved successfully
- `500 Internal Server Error`: Failed to get performance metrics

---

### 4. System Status

#### `GET /status`

Get detailed system status.

**Response:**
```json
{
  "success": true,
  "data": {
    "api_version": "1.0.0",
    "status": "operational",
    "services": {
      "ai_models": "available",
      "slither": "available",
      "mythril": "available",
      "feature_extractor": "available"
    },
    "uptime": "2 hours 15 minutes",
    "total_analyses": 42,
    "cache_status": "enabled",
    "last_updated": "2024-01-15T10:30:00Z"
  }
}
```

**Status Codes:**
- `200 OK`: Status retrieved successfully
- `500 Internal Server Error`: Failed to get system status

---

#### `GET /tools/status`

Get status of external analysis tools.

**Response:**
```json
{
  "success": true,
  "data": {
    "slither": {
      "available": true,
      "version": "0.9.6",
      "last_check": "2024-01-15T10:30:00Z"
    },
    "mythril": {
      "available": true,
      "version": "0.23.25",
      "last_check": "2024-01-15T10:30:00Z"
    }
  }
}
```

**Status Codes:**
- `200 OK`: Tool status retrieved successfully
- `500 Internal Server Error`: Failed to get tool status

---

### 5. Tool Comparison

#### `POST /compare`

Compare multiple analysis tools on a contract.

**Request Body:**
```json
{
  "contract_code": "pragma solidity ^0.8.0; contract Example { ... }",
  "tools": ["ai_binary", "ai_multiclass", "slither", "mythril"],
  "ground_truth": ["reentrancy"]
}
```

**Parameters:**
- `contract_code` (string, required): Solidity source code
- `tools` (array, required): List of tools to compare
- `ground_truth` (array, optional): Known vulnerabilities for evaluation

**Available Tools:**
- `ai_binary`: Binary AI classifier
- `ai_multiclass`: Multi-class AI classifier
- `slither`: Slither static analysis
- `mythril`: Mythril symbolic execution

**Response:**
```json
{
  "success": true,
  "data": {
    "comparison_id": "comparison_1642248600",
    "contract_hash": "abc123def456",
    "tools_compared": ["ai_binary", "slither"],
    "ground_truth": ["reentrancy"],
    "results": {
      "ai_binary": {
        "prediction": "vulnerable",
        "confidence": 0.87,
        "execution_time": 0.5,
        "success": true
      },
      "slither": {
        "vulnerabilities_found": ["reentrancy"],
        "findings_count": 1,
        "execution_time": 1.2,
        "success": true
      }
    },
    "consensus_findings": ["reentrancy"],
    "agreement_score": 0.85,
    "execution_time": 2.1
  },
  "message": "Tool comparison completed successfully"
}
```

**Status Codes:**
- `200 OK`: Comparison completed successfully
- `400 Bad Request`: Invalid tools or contract code
- `500 Internal Server Error`: Comparison failed

---

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details (optional)"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- `BAD_REQUEST`: Invalid request data
- `NOT_FOUND`: Resource not found
- `METHOD_NOT_ALLOWED`: HTTP method not allowed
- `FILE_TOO_LARGE`: File size exceeds limit
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded
- `INVALID_CONTRACT_CODE`: Contract code validation failed
- `ANALYSIS_ERROR`: Analysis execution failed
- `INTERNAL_SERVER_ERROR`: Unexpected server error

### Validation Errors

For validation errors, the response includes detailed field-level errors:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "validation_errors": [
      {
        "field": "contract_code",
        "message": "Contract code cannot be empty",
        "invalid_value": ""
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Per-IP Limits**: 100 requests per minute
- **Burst Limits**: 10 requests per second
- **Analysis Limits**: 5 concurrent analyses per IP

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Request limit per window
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset time (Unix timestamp)

When rate limits are exceeded, the API returns a `429 Too Many Requests` status.

---

## Request/Response Examples

### Example 1: Basic Contract Analysis

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.8.0;\n\ncontract SimpleStorage {\n    uint256 public value;\n    \n    function setValue(uint256 _value) public {\n        value = _value;\n    }\n}",
    "filename": "SimpleStorage.sol"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis_1642248600",
    "contract_hash": "abc123def456",
    "overall_risk_score": 10,
    "is_vulnerable": false,
    "confidence_level": 0.95,
    "vulnerabilities": [],
    "analysis_time": 1.2,
    "timestamp": "2024-01-15T10:30:00Z",
    "success": true
  },
  "message": "Contract analysis completed successfully"
}
```

### Example 2: File Upload Analysis

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/file \
  -F "file=@contract.sol" \
  -F 'options={"include_mythril": true}'
```

### Example 3: Tool Comparison

**Request:**
```bash
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.8.0;\n\ncontract Vulnerable {\n    mapping(address => uint) balances;\n    \n    function withdraw() public {\n        uint amount = balances[msg.sender];\n        msg.sender.call{value: amount}(\"\");\n        balances[msg.sender] = 0;\n    }\n}",
    "tools": ["ai_binary", "slither"]
  }'
```

---

## SDK and Client Libraries

### Python Client Example

```python
import requests

class SmartContractAnalyzer:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
    
    def analyze_contract(self, contract_code, **options):
        response = requests.post(
            f"{self.base_url}/analyze",
            json={
                "contract_code": contract_code,
                **options
            }
        )
        return response.json()
    
    def get_analysis(self, analysis_id):
        response = requests.get(f"{self.base_url}/analysis/{analysis_id}")
        return response.json()

# Usage
analyzer = SmartContractAnalyzer()
result = analyzer.analyze_contract(contract_code)
```

### JavaScript Client Example

```javascript
class SmartContractAnalyzer {
    constructor(baseUrl = 'http://localhost:5000/api') {
        this.baseUrl = baseUrl;
    }
    
    async analyzeContract(contractCode, options = {}) {
        const response = await fetch(`${this.baseUrl}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contract_code: contractCode,
                ...options
            })
        });
        return response.json();
    }
    
    async getAnalysis(analysisId) {
        const response = await fetch(`${this.baseUrl}/analysis/${analysisId}`);
        return response.json();
    }
}

// Usage
const analyzer = new SmartContractAnalyzer();
const result = await analyzer.analyzeContract(contractCode);
```

---

## Deployment and Configuration

### Environment Variables

- `FLASK_ENV`: Environment (development, production, testing)
- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 5000)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `CORS_ORIGINS`: Allowed CORS origins
- `RATE_LIMIT_PER_MINUTE`: Rate limit per minute (default: 100)
- `MAX_CONTENT_LENGTH`: Maximum request size (default: 1MB)

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "-m", "src.api.app"]
```

### Production Considerations

1. **Security**: Implement authentication and authorization
2. **Monitoring**: Add application performance monitoring
3. **Logging**: Configure structured logging
4. **Caching**: Implement Redis for result caching
5. **Load Balancing**: Use nginx or similar for load balancing
6. **Database**: Add persistent storage for analysis results

---

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial API release
- Contract analysis endpoints
- Model information endpoints
- Tool comparison functionality
- Basic rate limiting
- Comprehensive error handling

---

## Support

For API support and questions:
- **Documentation**: This document
- **Issues**: GitHub Issues
- **Email**: support@smartcontractanalyzer.com

---

*Last updated: January 15, 2024*