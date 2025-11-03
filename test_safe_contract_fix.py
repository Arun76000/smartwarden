#!/usr/bin/env python3
"""
Test the improved safe contract detection.
"""

import requests
import json

def test_safe_contract():
    """Test the safe contract detection fix."""
    
    safe_contract = """
pragma solidity ^0.8.0;

contract SafeContract {
    mapping(address => uint256) public balances;
    address public owner;
    bool private locked;
    
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    modifier noReentrant() {
        require(!locked);
        locked = true;
        _;
        locked = false;
    }
    
    function withdraw(uint256 amount) public noReentrant {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
    }
}"""
    
    print("🧪 Testing Safe Contract Detection Fix")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json={'contract_code': safe_contract},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"📊 Analysis Results:")
            print(f"   Vulnerable: {result.get('is_vulnerable')}")
            print(f"   Risk Score: {result.get('risk_score')}")
            print(f"   Vulnerabilities: {len(result.get('vulnerabilities', []))}")
            print(f"   Method: {result.get('analysis_method')}")
            print(f"   Confidence: {result.get('confidence')}")
            
            vulnerabilities = result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"\n🚨 Detected Issues:")
                for vuln in vulnerabilities:
                    print(f"   - {vuln.get('type')}: {vuln.get('severity')} ({vuln.get('source')})")
                    print(f"     {vuln.get('description')}")
            else:
                print(f"\n✅ No vulnerabilities detected")
            
            # Check if detection is correct
            is_vulnerable = result.get('is_vulnerable', True)
            if not is_vulnerable:
                print(f"\n🎉 SUCCESS: Safe contract correctly identified as SAFE!")
                return True
            else:
                print(f"\n⚠️ ISSUE: Safe contract still flagged as vulnerable")
                return False
                
        else:
            print(f"❌ Analysis failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_vulnerable_contract():
    """Test that vulnerable contracts are still detected."""
    
    vulnerable_contract = """
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        
        // Vulnerable: external call before state change
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        
        balances[msg.sender] -= amount;
    }
}"""
    
    print("\n🧪 Testing Vulnerable Contract Detection")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json={'contract_code': vulnerable_contract},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"📊 Analysis Results:")
            print(f"   Vulnerable: {result.get('is_vulnerable')}")
            print(f"   Risk Score: {result.get('risk_score')}")
            print(f"   Vulnerabilities: {len(result.get('vulnerabilities', []))}")
            
            is_vulnerable = result.get('is_vulnerable', False)
            if is_vulnerable:
                print(f"\n✅ SUCCESS: Vulnerable contract correctly identified as VULNERABLE!")
                return True
            else:
                print(f"\n⚠️ ISSUE: Vulnerable contract not detected")
                return False
                
        else:
            print(f"❌ Analysis failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🔧 Testing Safe Contract Detection Fix")
    print("=" * 60)
    
    safe_test = test_safe_contract()
    vulnerable_test = test_vulnerable_contract()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    if safe_test and vulnerable_test:
        print("🎉 SUCCESS: Both safe and vulnerable contract detection working!")
        print("✅ Safe contracts: Correctly identified as safe")
        print("✅ Vulnerable contracts: Correctly identified as vulnerable")
        return True
    else:
        if not safe_test:
            print("❌ Safe contract detection still needs work")
        if not vulnerable_test:
            print("❌ Vulnerable contract detection broken")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Safe Contract Detection: FIXED!")
    else:
        print("\n⚠️ Still needs adjustment")