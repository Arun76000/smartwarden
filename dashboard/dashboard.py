"""
Main Streamlit dashboard for Smart Contract AI Analyzer.
"""

import streamlit as st
import sys
from pathlib import Path
import importlib.util
import os
import logging

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Load pages dynamically to avoid import issues
pages_dir = Path(__file__).parent / "pages"
loaded_pages = {}

for page_file in ["analyze.py", "results.py", "comparison.py", "metrics.py", "about.py"]:
    page_path = pages_dir / page_file
    if page_path.exists():
        spec = importlib.util.spec_from_file_location(page_file[:-3], page_path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            loaded_pages[page_file[:-3]] = module
            logger.info(f"✅ Successfully loaded page: {page_file[:-3]}")
        except Exception as e:
            logger.warning(f"❌ Failed to load page {page_file}: {e}")
            # Create a dummy module with show_page function
            class DummyModule:
                def show_page(self):
                    st.error(f"Page {page_file[:-3]} is not available: {e}")
                    st.write(f"Error details: {str(e)}")
            loaded_pages[page_file[:-3]] = DummyModule()
    else:
        logger.warning(f"❌ Page file not found: {page_file}")

# Page configuration
st.set_page_config(
    page_title="Smart Contract AI Analyzer",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e8b57;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .vulnerability-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .vulnerability-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .vulnerability-medium {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .vulnerability-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .safe-contract {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .code-snippet {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.25rem;
        padding: 0.75rem;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    if 'contract_code' not in st.session_state:
        st.session_state.contract_code = ""
    
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🔍 Analyze Contract"
    
    if 'tool_comparison_results' not in st.session_state:
        st.session_state.tool_comparison_results = None

def navigate_to_page(page_name):
    """Helper function to navigate to a specific page."""
    page_mapping = {
        "analyze": "🔍 Analyze Contract",
        "results": "📊 Results", 
        "comparison": "⚖️ Tool Comparison",
        "metrics": "📈 Performance Metrics",
        "about": "ℹ️ About"
    }
    
    if page_name in page_mapping:
        st.session_state.current_page = page_mapping[page_name]
    elif page_name in page_mapping.values():
        st.session_state.current_page = page_name

def create_sidebar():
    """Create the sidebar navigation."""
    st.sidebar.markdown('<div class="sidebar-header">🔒 Smart Contract AI Analyzer</div>', unsafe_allow_html=True)
    
    # Navigation mapping
    page_mapping = {
        "🔍 Analyze Contract": "analyze",
        "📊 Results": "results", 
        "⚖️ Tool Comparison": "comparison",
        "📈 Performance Metrics": "metrics",
        "ℹ️ About": "about"
    }
    
    # Get current page index
    page_names = list(page_mapping.keys())
    try:
        current_index = page_names.index(st.session_state.current_page)
    except ValueError:
        current_index = 0
        st.session_state.current_page = page_names[0]
    
    selected_page_display = st.sidebar.selectbox(
        "Navigate to:",
        page_names,
        index=current_index
    )
    
    # Update session state and get page key
    st.session_state.current_page = selected_page_display
    selected_page = page_mapping[selected_page_display]
    
    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ System Status")
    
    # Mock system status - in real implementation, this would check actual system health
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("AI Models", "✅ Loaded")
    with col2:
        st.metric("External Tools", "⚠️ Partial")
    
    # Analysis statistics
    if st.session_state.analysis_history:
        st.sidebar.markdown("### 📊 Analysis Stats")
        total_analyses = len(st.session_state.analysis_history)
        vulnerable_count = sum(1 for result in st.session_state.analysis_history if result.get('is_vulnerable', False))
        
        st.sidebar.metric("Total Analyses", total_analyses)
        st.sidebar.metric("Vulnerabilities Found", vulnerable_count)
        
        if total_analyses > 0:
            vulnerability_rate = (vulnerable_count / total_analyses) * 100
            st.sidebar.metric("Vulnerability Rate", f"{vulnerability_rate:.1f}%")
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("🗑️ Clear Analysis History"):
        st.session_state.analysis_history = []
        st.session_state.analysis_results = None
        st.success("Analysis history cleared!")
    
    if st.sidebar.button("📥 Load Sample Contract"):
        sample_contract = '''pragma solidity ^0.8.0;

contract VulnerableExample {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Vulnerable to reentrancy
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // Bad randomness
    function randomNumber() public view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp))) % 100;
    }
}'''
        st.session_state.contract_code = sample_contract
        st.success("Sample contract loaded!")
    
    return selected_page

def display_header():
    """Display the main header."""
    st.markdown('<div class="main-header">🔒 Smart Contract AI Analyzer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        Advanced AI-powered security analysis for Ethereum smart contracts
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Display header
    display_header()
    
    # Route to appropriate page
    try:
        if selected_page == "analyze" and "analyze" in loaded_pages:
            loaded_pages["analyze"].show_page()
        elif selected_page == "results" and "results" in loaded_pages:
            loaded_pages["results"].show_page()
        elif selected_page == "comparison" and "comparison" in loaded_pages:
            loaded_pages["comparison"].show_page()
        elif selected_page == "metrics" and "metrics" in loaded_pages:
            loaded_pages["metrics"].show_page()
        elif selected_page == "about" and "about" in loaded_pages:
            loaded_pages["about"].show_page()
        else:
            st.error(f"❌ Page '{selected_page}' is not available")
            st.info("Available pages: " + ", ".join(loaded_pages.keys()))
    
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        logger.error(f"Page loading error: {e}")
        
        # Show error details in expander for debugging
        with st.expander("Error Details"):
            st.code(str(e))

if __name__ == "__main__":
    main()