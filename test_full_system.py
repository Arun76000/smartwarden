#!/usr/bin/env python3
"""
Complete system test script for Smart Contract AI Analyzer.
Tests both frontend and backend integration.
"""

import requests
import time
import json
from pathlib import Path

def test_api_backend():
    """Test API backend functionality."""
    print("🔧 Testing API Backend...")
    
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASS")
        else:
            print(f"❌ Health check: FAIL ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health check: FAIL ({e})")
        return False
    
    # Test analysis endpoint
    test_contract = '''pragma solidity ^0.8.0;

contract TestContract {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Vulnerable to reentrancy
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }
}'''
    
    try:
        response = requests.post(
            f"{base_url}/api/analyze",
            json={"contract_code": test_contract},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Analysis endpoint: PASS")
                print(f"   - Risk Score: {result.get('risk_score', 'N/A')}")
                print(f"   - Vulnerabilities: {len(result.get('vulnerabilities', []))}")
                return True
            else:
                print("❌ Analysis endpoint: FAIL (unsuccessful)")
                return False
        else:
            print(f"❌ Analysis endpoint: FAIL ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Analysis endpoint: FAIL ({e})")
        return False

def test_dashboard_access():
    """Test dashboard accessibility."""
    print("\n🌐 Testing Dashboard Access...")
    
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard accessible: PASS")
            return True
        else:
            print(f"❌ Dashboard accessible: FAIL ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Dashboard accessible: FAIL ({e})")
        return False

def test_file_structure():
    """Test required file structure."""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        "simple_api.py",
        "dashboard/dashboard.py",
        "dashboard/pages/analyze.py",
        "dashboard/pages/results.py",
        "dashboard/pages/comparison.py",
        "dashboard/pages/metrics.py",
        "dashboard/pages/about.py",
        "requirements.txt"
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}: EXISTS")
        else:
            print(f"❌ {file_path}: MISSING")
            all_good = False
    
    return all_good

def test_integration():
    """Test frontend-backend integration."""
    print("\n🔗 Testing Frontend-Backend Integration...")
    
    # This would typically involve selenium or similar for full integration testing
    # For now, we'll test the API endpoints that the frontend uses
    
    endpoints_to_test = [
        "/health",
        "/api/models/status", 
        "/api/tools/status",
        "/api/history"
    ]
    
    base_url = "http://localhost:5000"
    all_good = True
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}: PASS")
            else:
                print(f"❌ {endpoint}: FAIL ({response.status_code})")
                all_good = False
        except Exception as e:
            print(f"❌ {endpoint}: FAIL ({e})")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("🧪 Smart Contract AI Analyzer - System Test Suite")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("API Backend", test_api_backend),
        ("Dashboard Access", test_dashboard_access),
        ("Integration", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Tests...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)