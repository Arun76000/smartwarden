"""
Contract analysis page for the Streamlit dashboard.
"""

import streamlit as st
import sys
from pathlib import Path
import time
import json
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:5000"

# Mock classes for development
class AnalysisRequest:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class VulnerabilityFinding:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class AnalysisResult:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def call_api_analysis(contract_code, options=None):
    """Call the API backend for analysis."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json={
                "contract_code": contract_code,
                "options": options or {}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None

def check_api_health():
    """Check if API backend is available."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def show_page():
    """Display the contract analysis page."""
    st.header("🔍 Smart Contract Analysis")
    
    # API Status indicator
    col1, col2 = st.columns([3, 1])
    with col2:
        if check_api_health():
            st.success("🟢 API Connected")
        else:
            st.warning("🟡 API Offline (Mock Mode)")
    
    # Analysis options in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Analysis Options")
        
        include_ai = st.checkbox("AI Analysis", value=True, help="Use AI models for vulnerability detection")
        include_slither = st.checkbox("Slither Analysis", value=True, help="Run Slither static analysis")
        include_mythril = st.checkbox("Mythril Analysis", value=False, help="Run Mythril symbolic execution (slower)")
        include_comparison = st.checkbox("Tool Comparison", value=True, help="Compare results across tools")
        generate_pdf = st.checkbox("Generate PDF Report", value=False, help="Generate downloadable PDF report")
        
        st.markdown("---")
        
        # Analysis timeout
        timeout = st.slider("Analysis Timeout (seconds)", min_value=30, max_value=300, value=120)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Contract Code")
        
        # Contract input methods
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Code", "Use Session Code"],
            horizontal=True
        )
        
        contract_code = ""
        filename = "contract.sol"
        
        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Choose a Solidity file",
                type=['sol'],
                help="Upload a .sol file containing your smart contract"
            )
            
            if uploaded_file is not None:
                try:
                    contract_code = uploaded_file.read().decode('utf-8')
                    filename = uploaded_file.name
                    st.success(f"File '{filename}' uploaded successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        elif input_method == "Paste Code":
            contract_code = st.text_area(
                "Paste your Solidity contract code:",
                height=400,
                placeholder="pragma solidity ^0.8.0;\n\ncontract MyContract {\n    // Your contract code here\n}",
                help="Paste the complete Solidity source code"
            )
            
            filename = st.text_input("Contract filename:", value="contract.sol")
        
        elif input_method == "Use Session Code":
            if st.session_state.contract_code:
                contract_code = st.session_state.contract_code
                st.code(contract_code, language='solidity')
                st.info("Using contract code from session")
            else:
                st.warning("No contract code in session. Please use another input method.")
        
        # Update session state
        if contract_code:
            st.session_state.contract_code = contract_code
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        if contract_code:
            # Basic contract statistics
            lines = len(contract_code.split('\n'))
            chars = len(contract_code)
            functions = contract_code.count('function ')
            
            st.metric("Lines of Code", lines)
            st.metric("Characters", chars)
            st.metric("Functions", functions)
            
            # Basic validation
            has_pragma = 'pragma solidity' in contract_code.lower()
            has_contract = 'contract ' in contract_code.lower()
            
            if has_pragma:
                st.success("✅ Pragma statement found")
            else:
                st.warning("⚠️ No pragma statement")
            
            if has_contract:
                st.success("✅ Contract definition found")
            else:
                st.warning("⚠️ No contract definition")
        else:
            st.info("Upload or paste contract code to see statistics")
    
    # Analysis section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button(
            "🚀 Analyze Contract",
            type="primary",
            disabled=not contract_code,
            help="Start comprehensive security analysis"
        )
    
    with col2:
        if st.button("🧹 Clear Code"):
            st.session_state.contract_code = ""
            st.rerun()
    
    with col3:
        if st.button("💾 Save to Session"):
            if contract_code:
                st.session_state.contract_code = contract_code
                st.success("Code saved to session!")
    
    # Run analysis
    if analyze_button and contract_code:
        run_analysis(
            contract_code=contract_code,
            filename=filename,
            include_ai=include_ai,
            include_slither=include_slither,
            include_mythril=include_mythril,
            include_comparison=include_comparison,
            generate_pdf=generate_pdf,
            timeout=timeout
        )

def run_analysis(contract_code: str, filename: str, include_ai: bool, include_slither: bool, 
                include_mythril: bool, include_comparison: bool, generate_pdf: bool, timeout: int):
    """
    Run the contract analysis.
    
    Args:
        contract_code: Solidity source code
        filename: Contract filename
        include_ai: Whether to include AI analysis
        include_slither: Whether to include Slither
        include_mythril: Whether to include Mythril
        include_comparison: Whether to include tool comparison
        generate_pdf: Whether to generate PDF report
        timeout: Analysis timeout in seconds
    """
    # Create analysis request
    analysis_options = {
        'include_ai_analysis': include_ai,
        'include_slither': include_slither,
        'include_mythril': include_mythril,
        'include_feature_importance': include_ai,
        'detailed_report': True
    }
    
    request = AnalysisRequest(
        contract_code=contract_code,
        filename=filename,
        analysis_options=analysis_options,
        include_tool_comparison=include_comparison,
        generate_pdf_report=generate_pdf
    )
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize analysis
        status_text.text("Initializing analysis...")
        progress_bar.progress(10)
        
        # Run analysis
        status_text.text("Extracting features...")
        progress_bar.progress(30)
        
        # Simulate progress updates (in real implementation, this would be actual progress)
        time.sleep(1)
        
        status_text.text("Running AI models...")
        progress_bar.progress(50)
        time.sleep(1)
        
        if include_slither or include_mythril:
            status_text.text("Running external tools...")
            progress_bar.progress(70)
            time.sleep(1)
        
        status_text.text("Aggregating results...")
        progress_bar.progress(90)
        
        # Try API first, fallback to mock
        api_result = call_api_analysis(contract_code, analysis_options)
        
        if api_result and api_result.get('success'):
            result = convert_api_result_to_analysis_result(api_result, filename)
            st.info("✅ Analysis completed using API backend")
        else:
            result = create_mock_analysis_result(contract_code, filename)
            st.warning("⚠️ API unavailable, using mock analysis")
        
        progress_bar.progress(100)
        status_text.text("Analysis complete!")
        
        # Store results in session state
        st.session_state.analysis_results = result
        
        # Add to history
        st.session_state.analysis_history.append({
            'timestamp': result.timestamp,
            'filename': filename,
            'is_vulnerable': result.is_vulnerable,
            'risk_score': result.overall_risk_score,
            'vulnerabilities_count': len(result.vulnerabilities)
        })
        
        # Show success message
        st.success("✅ Analysis completed successfully!")
        
        # Display quick results
        display_quick_results(result)
        
        # Navigation to results
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("💡 Analysis complete! View detailed results below.")
        with col2:
            if st.button("📊 View Results", type="secondary"):
                st.session_state.current_page = "📊 Results"
                st.rerun()
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        logger.error(f"Analysis error: {e}")
        
    finally:
        # Clean up progress indicators
        progress_bar.empty()
        status_text.empty()

def convert_api_result_to_analysis_result(api_result, filename):
    """Convert API response to AnalysisResult object."""
    vulnerabilities = []
    
    for vuln_data in api_result.get('vulnerabilities', []):
        vulnerabilities.append(VulnerabilityFinding(
            vulnerability_type=vuln_data.get('type', 'unknown'),
            severity=vuln_data.get('severity', 'Medium'),
            confidence=vuln_data.get('confidence', 0.5),
            line_number=vuln_data.get('line', 1),
            description=vuln_data.get('description', ''),
            recommendation=vuln_data.get('recommendation', ''),
            code_snippet=vuln_data.get('code_snippet', ''),
            tool_source="API Backend"
        ))
    
    return AnalysisResult(
        analysis_id=api_result.get('analysis_id', f'api_{int(time.time())}'),
        contract_hash=f"hash_{hash(filename) % 1000000}",
        overall_risk_score=api_result.get('risk_score', 0),
        is_vulnerable=api_result.get('is_vulnerable', False),
        confidence_level=api_result.get('confidence', 0.5),
        vulnerabilities=vulnerabilities,
        feature_importance=api_result.get('feature_importance', {}),
        tool_comparison={},
        analysis_time=api_result.get('analysis_time', 1.0),
        timestamp=datetime.now(),
        success=True,
        error_message=None
    )

def create_mock_analysis_result(contract_code: str, filename: str):
    """
    Create a mock analysis result for demonstration.
    In real implementation, this would be replaced by actual analysis.
    """
    from datetime import datetime
    
    # Define classes locally if not imported
    class VulnerabilityFinding:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class AnalysisResult:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    # Detect some basic patterns for demo
    vulnerabilities = []
    
    # Check for reentrancy pattern
    if '.call{value:' in contract_code or '.call(' in contract_code:
        vulnerabilities.append(VulnerabilityFinding(
            vulnerability_type="reentrancy",
            severity="Critical",
            confidence=0.85,
            line_number=contract_code.find('.call') // len(contract_code.split('\n')[0]) + 1,
            description="Potential reentrancy vulnerability detected in external call",
            recommendation="Use the checks-effects-interactions pattern and consider reentrancy guards",
            code_snippet=".call{value: amount}(\"\")",
            tool_source="AI Classifier"
        ))
    
    # Check for timestamp usage
    if 'block.timestamp' in contract_code or 'now' in contract_code:
        vulnerabilities.append(VulnerabilityFinding(
            vulnerability_type="bad_randomness",
            severity="Medium",
            confidence=0.75,
            line_number=contract_code.find('block.timestamp') // len(contract_code.split('\n')[0]) + 1 if 'block.timestamp' in contract_code else 1,
            description="Use of block.timestamp for randomness detected",
            recommendation="Avoid using block.timestamp for randomness. Use secure random number generators",
            code_snippet="block.timestamp",
            tool_source="Pattern Matcher"
        ))
    
    # Calculate risk score
    if vulnerabilities:
        severity_weights = {'Critical': 100, 'High': 80, 'Medium': 60, 'Low': 40}
        risk_score = min(100, sum(severity_weights.get(v.severity, 50) for v in vulnerabilities) // len(vulnerabilities))
        is_vulnerable = True
        confidence = sum(v.confidence for v in vulnerabilities) / len(vulnerabilities)
    else:
        risk_score = 10  # Low risk even for safe contracts
        is_vulnerable = False
        confidence = 0.9
    
    return AnalysisResult(
        analysis_id=f"analysis_{int(time.time())}",
        contract_hash=f"hash_{hash(contract_code) % 1000000}",
        overall_risk_score=risk_score,
        is_vulnerable=is_vulnerable,
        confidence_level=confidence,
        vulnerabilities=vulnerabilities,
        feature_importance={
            'external_call_count': 0.25,
            'state_change_after_call': 0.20,
            'uses_block_timestamp': 0.15,
            'public_function_count': 0.10,
            'payable_function_count': 0.08
        },
        tool_comparison={
            'consensus_findings': [v.vulnerability_type for v in vulnerabilities],
            'agreement_score': 0.8
        },
        analysis_time=2.5,
        timestamp=datetime.now(),
        success=True,
        error_message=None
    )

def display_quick_results(result):
    """Display quick analysis results."""
    st.markdown("### 🎯 Quick Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_color = "red" if result.overall_risk_score > 70 else "orange" if result.overall_risk_score > 40 else "green"
        st.metric("Risk Score", f"{result.overall_risk_score}/100", delta=None)
    
    with col2:
        status = "Vulnerable" if result.is_vulnerable else "Safe"
        st.metric("Status", status)
    
    with col3:
        st.metric("Vulnerabilities", len(result.vulnerabilities))
    
    with col4:
        st.metric("Confidence", f"{result.confidence_level:.1%}")
    
    # Show vulnerabilities summary
    if result.vulnerabilities:
        st.markdown("#### 🚨 Detected Vulnerabilities")
        for vuln in result.vulnerabilities[:3]:  # Show top 3
            severity_class = f"vulnerability-{vuln.severity.lower()}"
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>{vuln.vulnerability_type.replace('_', ' ').title()}</strong> - {vuln.severity}<br>
                <small>{vuln.description}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if len(result.vulnerabilities) > 3:
            st.info(f"... and {len(result.vulnerabilities) - 3} more vulnerabilities. See Results page for details.")
    else:
        st.markdown("""
        <div class="safe-contract">
            <h4>✅ No Critical Vulnerabilities Detected</h4>
            <p>The contract appears to be safe based on the analysis.</p>
        </div>
        """, unsafe_allow_html=True)