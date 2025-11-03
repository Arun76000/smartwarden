# 🚀 Smart Warden - Complete Deployment Guide

## 📋 Table of Contents
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [API Backend Setup](#api-backend-setup)
- [Swagger Documentation](#swagger-documentation)
- [Running the System](#running-the-system)
- [Testing & Validation](#testing--validation)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## 🖥️ System Requirements

### **Minimum Requirements:**
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher (3.12 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for package installation

### **Optional Requirements:**
- **Docker Desktop**: For external tool integration (optional - native tools work without Docker)
- **Git**: For version control and updates
- **Visual Studio Code**: Recommended IDE

---

## 📦 Installation Guide

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd smart-contract-ai-analyzer
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, flask, pandas, numpy, scikit_learn; print('All dependencies installed successfully!')"
```

### **Step 4: Verify System Setup**
```bash
# Run system validation
python validate_system.py

# Check AI integration status
python check_ai_status.py
```

---

## 🔧 API Backend Setup

### **API Architecture Overview**
Smart Warden provides a comprehensive REST API built with Flask that includes:
- **Contract Analysis Endpoints**
- **Model Management**
- **Tool Integration**
- **Health Monitoring**
- **Swagger Documentation**

### **API Configuration**

#### **1. Environment Variables (Optional)**
Create a `.env` file in the project root:
```env
# API Configuration
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=5000

# Model Configuration
MODELS_DIR=models
FEATURES_COUNT=67

# External Tools
ENABLE_DOCKER_TOOLS=True
ENABLE_NATIVE_TOOLS=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/api.log
```

#### **2. API Server Files**
The API backend consists of:
- `simple_api.py` - Main API server
- `src/api/` - API modules (if using modular structure)
- `src/models/model_loader.py` - Model management
- `src/integration/` - External tool integration

### **Starting the API Backend**

#### **Option 1: Simple API Server (Recommended)**
```bash
# Start the API server
python simple_api.py

# API will be available at:
# - Health Check: http://localhost:5000/health
# - Analysis: http://localhost:5000/api/analyze
# - Swagger UI: http://localhost:5000/swagger
```

#### **Option 2: Production WSGI Server**
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn (Linux/macOS)
gunicorn -w 4 -b 0.0.0.0:5000 simple_api:app

# Run with Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 simple_api:app
```

### **API Endpoints Overview**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/api/analyze` | POST | Analyze smart contract |
| `/api/models/info` | GET | Model information |
| `/api/tools/status` | GET | External tools status |
| `/swagger` | GET | Swagger UI documentation |
| `/api/swagger.json` | GET | OpenAPI specification |

---

## 📚 Swagger Documentation

### **Accessing Swagger UI**
1. **Start the API server**: `python simple_api.py`
2. **Open browser**: Navigate to `http://localhost:5000/swagger`
3. **Explore endpoints**: Interactive API documentation with "Try it out" functionality

### **Creating Swagger Documentation**

#### **1. Install Swagger Dependencies**
```bash
pip install flask-restx flask-swagger-ui
```

#### **2. Add Swagger to API**
Create `src/api/swagger_config.py`:
```python
from flask_restx import Api, Resource, fields
from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_bp,
    version='1.0.0',
    title='Smart Warden API',
    description='AI-powered Smart Contract Security Analyzer API',
    doc='/swagger/',
    contact='support@smartwarden.ai',
    license='MIT'
)

# Define models for Swagger
analysis_request = api.model('AnalysisRequest', {
    'contract_code': fields.String(required=True, description='Solidity contract source code'),
    'filename': fields.String(description='Contract filename'),
    'options': fields.Raw(description='Analysis options')
})

vulnerability = api.model('Vulnerability', {
    'type': fields.String(description='Vulnerability type'),
    'severity': fields.String(description='Severity level'),
    'confidence': fields.Float(description='Confidence score'),
    'line_number': fields.Integer(description='Line number'),
    'description': fields.String(description='Vulnerability description'),
    'recommendation': fields.String(description='Fix recommendation')
})

analysis_result = api.model('AnalysisResult', {
    'analysis_id': fields.String(description='Unique analysis ID'),
    'success': fields.Boolean(description='Analysis success status'),
    'is_vulnerable': fields.Boolean(description='Contract vulnerability status'),
    'risk_score': fields.Integer(description='Risk score (0-100)'),
    'confidence': fields.Float(description='Overall confidence'),
    'vulnerabilities': fields.List(fields.Nested(vulnerability)),
    'analysis_time': fields.Float(description='Analysis duration in seconds'),
    'tools_used': fields.List(fields.String, description='Analysis tools used')
})
```

#### **3. Complete OpenAPI Specification**
Create `docs/api/openapi.yaml`:
```yaml
openapi: 3.0.3
info:
  title: Smart Warden - AI Smart Contract Security Analyzer API
  description: |
    Comprehensive API for AI-powered smart contract vulnerability detection.
    
    ## Features
    - AI-powered binary and multi-class vulnerability detection
    - External tool integration (Slither, Mythril)
    - Tool comparison and consensus analysis
    - Real-time analysis with progress tracking
    - Professional vulnerability reporting
    
    ## Authentication
    Currently no authentication required for development.
    Production deployment should implement API key authentication.
    
  version: 1.0.0
  contact:
    name: Smart Warden Team
    email: support@smartwarden.ai
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:5000
    description: Development server
  - url: https://api.smartwarden.ai
    description: Production server

paths:
  /health:
    get:
      summary: Health Check
      description: Check API server health and status
      tags: [System]
      responses:
        '200':
          description: Server is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
                  timestamp:
                    type: string
                    format: date-time
                  version:
                    type: string
                    example: "1.0.0"

  /api/analyze:
    post:
      summary: Analyze Smart Contract
      description: Submit a Solidity contract for comprehensive security analysis
      tags: [Analysis]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnalysisRequest'
            examples:
              simple_contract:
                summary: Simple Contract
                value:
                  contract_code: |
                    pragma solidity ^0.8.0;
                    contract SimpleStorage {
                        uint256 public value;
                        function setValue(uint256 _value) public {
                            value = _value;
                        }
                    }
                  options:
                    include_slither: false
                    include_mythril: false
              vulnerable_contract:
                summary: Vulnerable Contract
                value:
                  contract_code: |
                    pragma solidity ^0.7.0;
                    contract Vulnerable {
                        mapping(address => uint) balances;
                        function withdraw() public {
                            uint amount = balances[msg.sender];
                            msg.sender.call{value: amount}("");
                            balances[msg.sender] = 0;
                        }
                    }
                  options:
                    include_slither: true
                    include_mythril: true
                    compare_tools: true
      responses:
        '200':
          description: Analysis completed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AnalysisResult'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /api/models/info:
    get:
      summary: Get Model Information
      description: Retrieve information about loaded AI models
      tags: [Models]
      responses:
        '200':
          description: Model information retrieved
          content:
            application/json:
              schema:
                type: object
                properties:
                  models_loaded:
                    type: integer
                    description: Number of models loaded
                  binary_model:
                    type: object
                    properties:
                      accuracy:
                        type: number
                        description: Model accuracy
                      training_date:
                        type: string
                        format: date-time
                  multiclass_model:
                    type: object
                    properties:
                      accuracy:
                        type: number
                      classes:
                        type: array
                        items:
                          type: string

  /api/tools/status:
    get:
      summary: External Tools Status
      description: Check availability of external security tools
      tags: [Tools]
      responses:
        '200':
          description: Tools status retrieved
          content:
            application/json:
              schema:
                type: object
                properties:
                  slither:
                    type: object
                    properties:
                      available:
                        type: boolean
                      implementation:
                        type: string
                        enum: [docker, native, fallback]
                  mythril:
                    type: object
                    properties:
                      available:
                        type: boolean
                      implementation:
                        type: string
                        enum: [docker, native, fallback]

components:
  schemas:
    AnalysisRequest:
      type: object
      required:
        - contract_code
      properties:
        contract_code:
          type: string
          description: Solidity contract source code
          example: |
            pragma solidity ^0.8.0;
            contract Example {
                uint256 public value;
                function setValue(uint256 _value) public {
                    value = _value;
                }
            }
        filename:
          type: string
          description: Optional filename for the contract
          example: "MyContract.sol"
        options:
          type: object
          description: Analysis configuration options
          properties:
            include_slither:
              type: boolean
              default: false
              description: Include Slither static analysis
            include_mythril:
              type: boolean
              default: false
              description: Include Mythril symbolic execution
            compare_tools:
              type: boolean
              default: false
              description: Enable tool comparison analysis
            generate_pdf_report:
              type: boolean
              default: false
              description: Generate PDF report

    Vulnerability:
      type: object
      properties:
        type:
          type: string
          description: Vulnerability type
          enum: [reentrancy, access_control, arithmetic, unchecked_calls, dos, bad_randomness]
          example: "reentrancy"
        severity:
          type: string
          description: Severity level
          enum: [critical, high, medium, low]
          example: "high"
        confidence:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: Confidence score
          example: 0.85
        line_number:
          type: integer
          description: Line number where vulnerability was found
          example: 15
        description:
          type: string
          description: Detailed vulnerability description
          example: "Potential reentrancy vulnerability detected"
        recommendation:
          type: string
          description: Recommended fix
          example: "Use checks-effects-interactions pattern"
        source:
          type: string
          description: Analysis tool that detected this vulnerability
          enum: [AI, Slither, Mythril]
          example: "AI"

    AnalysisResult:
      type: object
      properties:
        analysis_id:
          type: string
          description: Unique analysis identifier
          example: "comprehensive_1698765432"
        success:
          type: boolean
          description: Analysis completion status
          example: true
        is_vulnerable:
          type: boolean
          description: Overall vulnerability assessment
          example: true
        risk_score:
          type: integer
          minimum: 0
          maximum: 100
          description: Overall risk score
          example: 75
        confidence:
          type: number
          minimum: 0.0
          maximum: 1.0
          description: Overall confidence level
          example: 0.87
        vulnerabilities:
          type: array
          items:
            $ref: '#/components/schemas/Vulnerability'
          description: List of detected vulnerabilities
        analysis_time:
          type: number
          description: Analysis duration in seconds
          example: 12.34
        timestamp:
          type: string
          format: date-time
          description: Analysis timestamp
        tools_used:
          type: array
          items:
            type: string
          description: List of analysis tools used
          example: ["AI", "Slither", "Mythril"]
        tool_comparison:
          type: object
          description: Tool comparison results (if enabled)
          properties:
            consensus:
              type: object
              properties:
                is_vulnerable:
                  type: boolean
                confidence:
                  type: number
                agreement_level:
                  type: string
                  enum: [unanimous, majority, split]
            tool_agreement:
              type: number
              minimum: 0.0
              maximum: 1.0
              description: Agreement percentage between tools

    Error:
      type: object
      properties:
        error:
          type: string
          description: Error message
          example: "Invalid contract code provided"
        code:
          type: string
          description: Error code
          example: "INVALID_INPUT"
        details:
          type: string
          description: Additional error details
        timestamp:
          type: string
          format: date-time

  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for authentication (production only)

tags:
  - name: System
    description: System health and status endpoints
  - name: Analysis
    description: Smart contract analysis endpoints
  - name: Models
    description: AI model management endpoints
  - name: Tools
    description: External tools management endpoints
```

---

## 🏃‍♂️ Running the System

### **Quick Start Options**

#### **Option 1: Dashboard Only (Fastest)**
```bash
# Start dashboard with mock analysis
python quick_start.py

# Access at: http://localhost:8501
```

#### **Option 2: API Backend Only**
```bash
# Start API server
python simple_api.py

# Test API health
curl http://localhost:5000/health

# Access Swagger UI: http://localhost:5000/swagger
```

#### **Option 3: Full System (API + Dashboard)**
```bash
# Clean any existing processes
python cleanup_ports.py

# Start complete system
python start_system.py

# Access points:
# - API: http://localhost:5000
# - Dashboard: http://localhost:8501
# - Swagger: http://localhost:5000/swagger
```

### **Manual Startup Process**

#### **1. Start API Backend**
```bash
# Terminal 1: Start API
python simple_api.py

# Verify API is running
curl -X GET http://localhost:5000/health
```

#### **2. Start Dashboard (Optional)**
```bash
# Terminal 2: Start Dashboard
streamlit run dashboard/dashboard.py

# Access at: http://localhost:8501
```

#### **3. Test Integration**
```bash
# Test API analysis endpoint
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.8.0; contract Test { uint256 public value; }",
    "options": {
      "include_slither": true,
      "include_mythril": true,
      "compare_tools": true
    }
  }'
```

---

## 🧪 Testing & Validation

### **System Validation**
```bash
# Run complete system validation
python validate_system.py

# Check AI integration status
python check_ai_status.py

# Run comprehensive tests
python -m pytest tests/test_comprehensive.py -v
```

### **API Testing**

#### **1. Health Check**
```bash
curl -X GET http://localhost:5000/health
```

#### **2. Model Information**
```bash
curl -X GET http://localhost:5000/api/models/info
```

#### **3. Tools Status**
```bash
curl -X GET http://localhost:5000/api/tools/status
```

#### **4. Contract Analysis**
```bash
# Simple analysis
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.8.0; contract Safe { uint256 public value; function setValue(uint256 _value) public { value = _value; } }"
  }'

# Full analysis with all tools
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_code": "pragma solidity ^0.7.0; contract Vulnerable { mapping(address => uint) balances; function withdraw() public { uint amount = balances[msg.sender]; msg.sender.call{value: amount}(\"\"); balances[msg.sender] = 0; } }",
    "options": {
      "include_slither": true,
      "include_mythril": true,
      "compare_tools": true
    }
  }'
```

### **Performance Testing**
```bash
# Install testing tools
pip install locust

# Create performance test
cat > locustfile.py << EOF
from locust import HttpUser, task, between

class SmartWardenUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def analyze_contract(self):
        self.client.post("/api/analyze", json={
            "contract_code": "pragma solidity ^0.8.0; contract Test { uint256 public value; }"
        })
EOF

# Run performance test
locust -f locustfile.py --host=http://localhost:5000
```

---

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **1. Port Already in Use**
```bash
# Clean up ports
python cleanup_ports.py

# Or manually kill processes
# Windows:
taskkill /f /im python.exe
# Linux/macOS:
pkill -f python
```

#### **2. Module Import Errors**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### **3. AI Models Not Loading**
```bash
# Check model files exist
ls -la models/

# Retrain models if needed
python train_models.py
python train_multiclass_model.py

# Verify model loading
python -c "from src.models.model_loader import ModelLoader; loader = ModelLoader(); print(loader.load_all_models())"
```

#### **4. External Tools Not Working**
```bash
# Check tools status
python -c "from src.integration.docker_tools import check_tools_availability; print(check_tools_availability())"

# Native tools should always work
python -c "from src.integration.native_tools import check_native_tools_availability; print(check_native_tools_availability())"
```

#### **5. Dashboard Not Loading**
```bash
# Check Streamlit installation
pip install streamlit --upgrade

# Run dashboard directly
streamlit run dashboard/dashboard.py --server.port 8501
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG     # Windows

# Run with verbose output
python simple_api.py --debug
```

### **Log Files**
- **API Logs**: `logs/api.log`
- **Analysis Logs**: `logs/analyzer.log`
- **System Logs**: `logs/system.log`

---

## 🚀 Production Deployment

### **Environment Setup**

#### **1. Production Environment Variables**
```env
# Production Configuration
FLASK_ENV=production
FLASK_DEBUG=False
API_HOST=0.0.0.0
API_PORT=5000

# Security
SECRET_KEY=your-secret-key-here
API_KEY_REQUIRED=True
CORS_ORIGINS=https://yourdomain.com

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/smartwarden

# External Services
REDIS_URL=redis://localhost:6379
SENTRY_DSN=your-sentry-dsn

# Monitoring
ENABLE_METRICS=True
METRICS_PORT=9090
```

#### **2. Production Dependencies**
```bash
# Install production server
pip install gunicorn redis celery

# Install monitoring
pip install prometheus-client sentry-sdk
```

### **Docker Deployment**

#### **1. Create Dockerfile**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 smartwarden && chown -R smartwarden:smartwarden /app
USER smartwarden

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "simple_api:app"]
```

#### **2. Docker Compose**
```yaml
version: '3.8'

services:
  smartwarden-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    restart: unless-stopped

  smartwarden-dashboard:
    build: .
    command: streamlit run dashboard/dashboard.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    depends_on:
      - smartwarden-api
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - smartwarden-api
      - smartwarden-dashboard
    restart: unless-stopped

volumes:
  redis_data:
```

### **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartwarden-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smartwarden-api
  template:
    metadata:
      labels:
        app: smartwarden-api
    spec:
      containers:
      - name: smartwarden-api
        image: smartwarden:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: smartwarden-api-service
spec:
  selector:
    app: smartwarden-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

### **Monitoring & Logging**

#### **1. Application Monitoring**
```python
# Add to simple_api.py
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter('smartwarden_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('smartwarden_request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    REQUEST_DURATION.observe(time.time() - request.start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

#### **2. Centralized Logging**
```python
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Sentry integration
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

# File logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/smartwarden.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

---

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │   REST API      │    │   AI Models     │
│   (Streamlit)   │◄──►│   (Flask)       │◄──►│   (Scikit-learn)│
│   Port: 8501    │    │   Port: 5000    │    │   Binary/Multi  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Interface│    │   Tool Integration│   │   Feature       │
│   - File Upload │    │   - Native Slither│   │   Extraction    │
│   - Real-time   │    │   - Native Mythril│   │   (67 features) │
│   - Visualizations│   │   - Tool Comparison│  │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🎯 Quick Reference

### **Essential Commands**
```bash
# System validation
python validate_system.py

# Start dashboard only
python quick_start.py

# Start API only
python simple_api.py

# Start full system
python start_system.py

# Check system status
python check_ai_status.py

# Clean up processes
python cleanup_ports.py

# Run tests
python -m pytest tests/ -v
```

### **Key URLs**
- **Dashboard**: http://localhost:8501
- **API Health**: http://localhost:5000/health
- **Swagger UI**: http://localhost:5000/swagger
- **API Analysis**: http://localhost:5000/api/analyze

### **Support & Documentation**
- **System Guide**: `SYSTEM_GUIDE.md`
- **Quick Start**: `QUICK_START.md`
- **API Documentation**: Available at `/swagger` endpoint
- **Troubleshooting**: Check log files in `logs/` directory

---

**🎉 Smart Warden is now ready for production deployment with full API backend, Swagger documentation, and comprehensive monitoring capabilities!**