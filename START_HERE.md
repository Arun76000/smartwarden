# 🚀 Smart Contract AI Analyzer - Start Here

## 🎯 **Quick Start Options**

### **Option 1: Dashboard Only (Recommended for First Try)**

```bash
python quick_start.py
```

- Starts just the dashboard at http://localhost:8501
- Uses mock analysis (no API needed)
- Perfect for exploring the UI

### **Option 2: Full System (Dashboard + API)**

```bash
# If ports are busy, clean them first:
python cleanup_ports.py

# Then start the full system:
python start_system.py
```

- Starts both API backend and dashboard
- Real API integration
- Full functionality

### **Option 3: Manual Start**

```bash
# Terminal 1: Start API
python simple_api.py

# Terminal 2: Start Dashboard
streamlit run dashboard/dashboard.py
```

---

## 🔧 **Troubleshooting**

### **If "Port already in use" error:**

```bash
# Clean up ports first
python cleanup_ports.py

# Then try again
python start_system.py
```

### **If API won't start:**

```bash
# Just use dashboard in mock mode
python quick_start.py
```

### **If nothing works:**

```bash
# Manual cleanup (Windows)
taskkill /f /im python.exe

# Then try quick start
python quick_start.py
```

---

## 🌐 **Access Points**

- **Dashboard**: http://localhost:8501
- **API Health**: http://localhost:5000/health (if API running)

---

## ✅ **What Works**

### **Dashboard Features (Always Work)**

- 🔍 **Analyze Contract**: Upload/paste Solidity code
- 📊 **Results**: View analysis results with charts
- ⚖️ **Tool Comparison**: Compare different analysis methods
- 📈 **Performance Metrics**: System statistics
- ℹ️ **About**: Project information

### **Analysis Features**

- **Mock Mode**: Pattern-based vulnerability detection
- **API Mode**: Enhanced analysis via backend (when API running)
- **Real-time Progress**: Live analysis updates
- **Export Options**: JSON/CSV downloads

---

## 🎮 **How to Use**

1. **Start the system** using one of the options above
2. **Open browser** to http://localhost:8501
3. **Upload a contract** or paste Solidity code
4. **Run analysis** and view results
5. **Explore other tabs** for detailed information

---

## 📝 **Sample Contract for Testing**

```solidity
pragma solidity ^0.8.0;

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
}
```

This contract has intentional vulnerabilities that the analyzer will detect!

---

## 🆘 **Need Help?**

1. **Try Quick Start first**: `python quick_start.py`
2. **Check the logs** in the terminal for error messages
3. **Use cleanup script** if ports are busy: `python cleanup_ports.py`
4. **Restart your terminal** if things get stuck

**The system is designed to work even if some components fail - the dashboard will always work in mock mode!** 🎉
