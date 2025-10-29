"""
Tool comparison and benchmarking system for smart contract security analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time

from .slither_runner import SlitherAnalyzer, SlitherResult
from .mythril_runner import MythrilAnalyzer, MythrilResult
from ..models.random_forest import RandomForestVulnerabilityDetector
from ..models.multiclass_classifier import MultiClassVulnerabilityClassifier
from ..features.feature_extractor import SolidityFeatureExtractor

logger = logging.getLogger(__name__)


@dataclass
class ToolPerformance:
    """Performance metrics for a single tool."""
    tool_name: str
    execution_time: float
    findings_count: int
    vulnerabilities_found: List[str]
    severity_distribution: Dict[str, int]
    success: bool
    error_message: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ComparisonResult:
    """Result of comparing multiple tools on a contract."""
    contract_name: str
    contract_code: str
    ground_truth: Optional[List[str]]
    tool_performances: Dict[str, ToolPerformance]
    consensus_findings: List[str]
    unique_findings: Dict[str, List[str]]
    agreement_score: float
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'contract_name': self.contract_name,
            'contract_code': self.contract_code,
            'ground_truth': self.ground_truth,
            'tool_performances': {name: perf.to_dict() for name, perf in self.tool_performances.items()},
            'consensus_findings': self.consensus_findings,
            'unique_findings': self.unique_findings,
            'agreement_score': self.agreement_score,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class BenchmarkMetrics:
    """Comprehensive benchmark metrics for tool evaluation."""
    tool_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    false_positive_rate: float
    false_negative_rate: float
    avg_execution_time: float
    success_rate: float
    vulnerability_detection_rates: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ToolComparator:
    """
    Compares and benchmarks different smart contract security analysis tools.
    
    Supported tools:
    - AI-based Random Forest classifier
    - AI-based Multi-class classifier  
    - Slither static analysis
    - Mythril symbolic execution
    """
    
    def __init__(self):
        """Initialize the tool comparator."""
        self.slither = SlitherAnalyzer()
        self.mythril = MythrilAnalyzer()
        self.feature_extractor = SolidityFeatureExtractor()
        
        # Tool availability
        self.available_tools = {
            'slither': self.slither.is_available(),
            'mythril': self.mythril.is_available(),
            'ai_binary': False,  # Will be set when model is loaded
            'ai_multiclass': False  # Will be set when model is loaded
        }
        
        # Loaded models
        self.ai_binary_model = None
        self.ai_multiclass_model = None
        
        # Comparison history
        self.comparison_history = []
        
    def load_ai_models(self, 
                      binary_model_path: Optional[str] = None,
                      multiclass_model_path: Optional[str] = None):
        """
        Load AI models for comparison.
        
        Args:
            binary_model_path: Path to binary classifier model
            multiclass_model_path: Path to multi-class classifier model
        """
        if binary_model_path and Path(binary_model_path).exists():
            try:
                self.ai_binary_model = RandomForestVulnerabilityDetector.load_model(binary_model_path)
                self.available_tools['ai_binary'] = True
                logger.info(f"Loaded binary AI model from {binary_model_path}")
            except Exception as e:
                logger.error(f"Failed to load binary AI model: {e}")
        
        if multiclass_model_path and Path(multiclass_model_path).exists():
            try:
                self.ai_multiclass_model = MultiClassVulnerabilityClassifier.load_model(multiclass_model_path)
                self.available_tools['ai_multiclass'] = True
                logger.info(f"Loaded multi-class AI model from {multiclass_model_path}")
            except Exception as e:
                logger.error(f"Failed to load multi-class AI model: {e}")
    
    def compare_tools(self, 
                     contract_code: str,
                     contract_name: str = "contract",
                     ground_truth: Optional[List[str]] = None,
                     tools: Optional[List[str]] = None) -> ComparisonResult:
        """
        Compare multiple tools on a single contract.
        
        Args:
            contract_code: Solidity source code
            contract_name: Name of the contract
            ground_truth: Known vulnerabilities (for evaluation)
            tools: List of tools to compare (default: all available)
            
        Returns:
            ComparisonResult object
        """
        if tools is None:
            tools = [tool for tool, available in self.available_tools.items() if available]
        
        logger.info(f"Comparing tools {tools} on contract {contract_name}")
        
        tool_performances = {}
        
        # Run each tool
        for tool in tools:
            try:
                performance = self._run_single_tool(tool, contract_code, contract_name)
                tool_performances[tool] = performance
            except Exception as e:
                logger.error(f"Error running {tool}: {e}")
                tool_performances[tool] = ToolPerformance(
                    tool_name=tool,
                    execution_time=0.0,
                    findings_count=0,
                    vulnerabilities_found=[],
                    severity_distribution={},
                    success=False,
                    error_message=str(e)
                )
        
        # Analyze results
        consensus_findings = self._find_consensus(tool_performances)
        unique_findings = self._find_unique_findings(tool_performances)
        agreement_score = self._calculate_agreement_score(tool_performances)
        
        result = ComparisonResult(
            contract_name=contract_name,
            contract_code=contract_code,
            ground_truth=ground_truth,
            tool_performances=tool_performances,
            consensus_findings=consensus_findings,
            unique_findings=unique_findings,
            agreement_score=agreement_score,
            timestamp=datetime.now()
        )
        
        self.comparison_history.append(result)
        return result
    
    def _run_single_tool(self, tool_name: str, contract_code: str, contract_name: str) -> ToolPerformance:
        """
        Run a single tool on the contract.
        
        Args:
            tool_name: Name of the tool to run
            contract_code: Solidity source code
            contract_name: Name of the contract
            
        Returns:
            ToolPerformance object
        """
        start_time = time.time()
        
        if tool_name == 'slither':
            result = self.slither.analyze_contract(contract_code, f"{contract_name}.sol")
            execution_time = result.execution_time
            
            if result.success:
                vulnerabilities = [finding.vulnerability_type for finding in result.findings]
                severity_dist = result._get_severity_distribution()
                
                return ToolPerformance(
                    tool_name='slither',
                    execution_time=execution_time,
                    findings_count=len(result.findings),
                    vulnerabilities_found=vulnerabilities,
                    severity_distribution=severity_dist,
                    success=True,
                    error_message=None
                )
            else:
                return ToolPerformance(
                    tool_name='slither',
                    execution_time=execution_time,
                    findings_count=0,
                    vulnerabilities_found=[],
                    severity_distribution={},
                    success=False,
                    error_message=result.error_message
                )
        
        elif tool_name == 'mythril':
            result = self.mythril.analyze_contract(contract_code, f"{contract_name}.sol")
            execution_time = result.execution_time
            
            if result.success:
                vulnerabilities = [finding.vulnerability_type for finding in result.findings]
                severity_dist = result._get_severity_distribution()
                
                return ToolPerformance(
                    tool_name='mythril',
                    execution_time=execution_time,
                    findings_count=len(result.findings),
                    vulnerabilities_found=vulnerabilities,
                    severity_distribution=severity_dist,
                    success=True,
                    error_message=None
                )
            else:
                return ToolPerformance(
                    tool_name='mythril',
                    execution_time=execution_time,
                    findings_count=0,
                    vulnerabilities_found=[],
                    severity_distribution={},
                    success=False,
                    error_message=result.error_message
                )
        
        elif tool_name == 'ai_binary':
            if not self.ai_binary_model:
                raise ValueError("Binary AI model not loaded")
            
            # Extract features
            features = self.feature_extractor.extract_features(contract_code)
            features_df = pd.DataFrame([features])
            
            # Make prediction
            predictions, probabilities = self.ai_binary_model.predict(features_df)
            execution_time = time.time() - start_time
            
            # Convert prediction to vulnerability list
            vulnerabilities = []
            if predictions[0] == 'vulnerable' or (isinstance(predictions[0], (int, float)) and predictions[0] > 0.5):
                vulnerabilities = ['vulnerable']  # Binary model doesn't specify type
            
            return ToolPerformance(
                tool_name='ai_binary',
                execution_time=execution_time,
                findings_count=len(vulnerabilities),
                vulnerabilities_found=vulnerabilities,
                severity_distribution={'Medium': len(vulnerabilities)} if vulnerabilities else {},
                success=True,
                error_message=None
            )
        
        elif tool_name == 'ai_multiclass':
            if not self.ai_multiclass_model:
                raise ValueError("Multi-class AI model not loaded")
            
            # Extract features
            features = self.feature_extractor.extract_features(contract_code)
            features_df = pd.DataFrame([features])
            
            # Make prediction
            predictions, probabilities = self.ai_multiclass_model.predict(features_df)
            execution_time = time.time() - start_time
            
            # Convert prediction to vulnerability list
            vulnerabilities = []
            if predictions[0] != 'safe':
                vulnerabilities = [predictions[0]]
            
            return ToolPerformance(
                tool_name='ai_multiclass',
                execution_time=execution_time,
                findings_count=len(vulnerabilities),
                vulnerabilities_found=vulnerabilities,
                severity_distribution={'Medium': len(vulnerabilities)} if vulnerabilities else {},
                success=True,
                error_message=None
            )
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def _find_consensus(self, tool_performances: Dict[str, ToolPerformance]) -> List[str]:
        """
        Find vulnerabilities detected by multiple tools.
        
        Args:
            tool_performances: Dictionary of tool performances
            
        Returns:
            List of consensus vulnerabilities
        """
        # Count occurrences of each vulnerability type
        vulnerability_counts = {}
        
        for performance in tool_performances.values():
            if performance.success:
                for vuln in performance.vulnerabilities_found:
                    vulnerability_counts[vuln] = vulnerability_counts.get(vuln, 0) + 1
        
        # Find vulnerabilities detected by at least 2 tools
        consensus_threshold = max(2, len([p for p in tool_performances.values() if p.success]) // 2)
        consensus = [vuln for vuln, count in vulnerability_counts.items() if count >= consensus_threshold]
        
        return consensus
    
    def _find_unique_findings(self, tool_performances: Dict[str, ToolPerformance]) -> Dict[str, List[str]]:
        """
        Find vulnerabilities unique to each tool.
        
        Args:
            tool_performances: Dictionary of tool performances
            
        Returns:
            Dictionary mapping tool names to unique findings
        """
        # Get all vulnerabilities found by each tool
        all_vulnerabilities = set()
        tool_vulnerabilities = {}
        
        for tool_name, performance in tool_performances.items():
            if performance.success:
                tool_vulns = set(performance.vulnerabilities_found)
                tool_vulnerabilities[tool_name] = tool_vulns
                all_vulnerabilities.update(tool_vulns)
        
        # Find unique vulnerabilities for each tool
        unique_findings = {}
        for tool_name, tool_vulns in tool_vulnerabilities.items():
            other_vulns = set()
            for other_tool, other_vulns_set in tool_vulnerabilities.items():
                if other_tool != tool_name:
                    other_vulns.update(other_vulns_set)
            
            unique = tool_vulns - other_vulns
            unique_findings[tool_name] = list(unique)
        
        return unique_findings
    
    def _calculate_agreement_score(self, tool_performances: Dict[str, ToolPerformance]) -> float:
        """
        Calculate agreement score between tools.
        
        Args:
            tool_performances: Dictionary of tool performances
            
        Returns:
            Agreement score between 0 and 1
        """
        successful_tools = [p for p in tool_performances.values() if p.success]
        
        if len(successful_tools) < 2:
            return 0.0
        
        # Get all unique vulnerabilities
        all_vulnerabilities = set()
        for performance in successful_tools:
            all_vulnerabilities.update(performance.vulnerabilities_found)
        
        if not all_vulnerabilities:
            return 1.0  # All tools agree there are no vulnerabilities
        
        # Calculate pairwise agreement
        agreements = []
        for i, tool1 in enumerate(successful_tools):
            for tool2 in successful_tools[i+1:]:
                vulns1 = set(tool1.vulnerabilities_found)
                vulns2 = set(tool2.vulnerabilities_found)
                
                # Jaccard similarity
                intersection = len(vulns1 & vulns2)
                union = len(vulns1 | vulns2)
                
                if union == 0:
                    agreement = 1.0
                else:
                    agreement = intersection / union
                
                agreements.append(agreement)
        
        return np.mean(agreements) if agreements else 0.0
    
    def benchmark_tools(self, 
                       test_contracts: List[Dict[str, Any]],
                       tools: Optional[List[str]] = None) -> Dict[str, BenchmarkMetrics]:
        """
        Benchmark tools on a set of test contracts with ground truth.
        
        Args:
            test_contracts: List of contracts with 'code', 'name', and 'vulnerabilities'
            tools: List of tools to benchmark (default: all available)
            
        Returns:
            Dictionary mapping tool names to benchmark metrics
        """
        if tools is None:
            tools = [tool for tool, available in self.available_tools.items() if available]
        
        logger.info(f"Benchmarking tools {tools} on {len(test_contracts)} contracts")
        
        # Run comparisons on all test contracts
        results = []
        for contract in test_contracts:
            result = self.compare_tools(
                contract_code=contract['code'],
                contract_name=contract['name'],
                ground_truth=contract.get('vulnerabilities', []),
                tools=tools
            )
            results.append(result)
        
        # Calculate metrics for each tool
        benchmark_metrics = {}
        for tool in tools:
            metrics = self._calculate_benchmark_metrics(tool, results)
            benchmark_metrics[tool] = metrics
        
        return benchmark_metrics
    
    def _calculate_benchmark_metrics(self, tool_name: str, results: List[ComparisonResult]) -> BenchmarkMetrics:
        """
        Calculate benchmark metrics for a single tool.
        
        Args:
            tool_name: Name of the tool
            results: List of comparison results
            
        Returns:
            BenchmarkMetrics object
        """
        # Collect predictions and ground truth
        y_true = []
        y_pred = []
        execution_times = []
        success_count = 0
        vulnerability_detections = {}
        
        for result in results:
            if tool_name not in result.tool_performances:
                continue
            
            performance = result.tool_performances[tool_name]
            
            if performance.success:
                success_count += 1
                execution_times.append(performance.execution_time)
                
                # Convert to binary classification (vulnerable vs safe)
                ground_truth = result.ground_truth or []
                has_vulnerabilities = len(ground_truth) > 0
                found_vulnerabilities = len(performance.vulnerabilities_found) > 0
                
                y_true.append(1 if has_vulnerabilities else 0)
                y_pred.append(1 if found_vulnerabilities else 0)
                
                # Track specific vulnerability detection rates
                for vuln_type in ground_truth:
                    if vuln_type not in vulnerability_detections:
                        vulnerability_detections[vuln_type] = {'detected': 0, 'total': 0}
                    
                    vulnerability_detections[vuln_type]['total'] += 1
                    if vuln_type in performance.vulnerabilities_found:
                        vulnerability_detections[vuln_type]['detected'] += 1
        
        # Calculate metrics
        if len(y_true) > 0:
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, zero_division=0)
            recall = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            
            # Calculate false positive and false negative rates
            tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
            fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
            fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
            
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        else:
            accuracy = precision = recall = f1 = fpr = fnr = 0.0
        
        # Calculate vulnerability-specific detection rates
        vuln_detection_rates = {}
        for vuln_type, stats in vulnerability_detections.items():
            if stats['total'] > 0:
                vuln_detection_rates[vuln_type] = stats['detected'] / stats['total']
        
        return BenchmarkMetrics(
            tool_name=tool_name,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            false_positive_rate=fpr,
            false_negative_rate=fnr,
            avg_execution_time=np.mean(execution_times) if execution_times else 0.0,
            success_rate=success_count / len(results) if results else 0.0,
            vulnerability_detection_rates=vuln_detection_rates
        )
    
    def plot_comparison_results(self, result: ComparisonResult, save_path: Optional[str] = None):
        """
        Plot comparison results for a single contract.
        
        Args:
            result: ComparisonResult to plot
            save_path: Path to save the plot
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Execution times
        tools = []
        times = []
        for tool_name, performance in result.tool_performances.items():
            if performance.success:
                tools.append(tool_name)
                times.append(performance.execution_time)
        
        if tools:
            ax1.bar(tools, times, color='skyblue', alpha=0.7)
            ax1.set_title('Execution Time by Tool')
            ax1.set_ylabel('Time (seconds)')
            ax1.tick_params(axis='x', rotation=45)
        
        # 2. Findings count
        findings_counts = []
        for tool in tools:
            findings_counts.append(result.tool_performances[tool].findings_count)
        
        if tools:
            ax2.bar(tools, findings_counts, color='lightcoral', alpha=0.7)
            ax2.set_title('Number of Findings by Tool')
            ax2.set_ylabel('Findings Count')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Vulnerability types found
        all_vulns = set()
        for performance in result.tool_performances.values():
            if performance.success:
                all_vulns.update(performance.vulnerabilities_found)
        
        if all_vulns:
            vuln_matrix = []
            for tool in tools:
                tool_vulns = result.tool_performances[tool].vulnerabilities_found
                row = [1 if vuln in tool_vulns else 0 for vuln in all_vulns]
                vuln_matrix.append(row)
            
            if vuln_matrix:
                sns.heatmap(vuln_matrix, 
                           xticklabels=list(all_vulns),
                           yticklabels=tools,
                           annot=True,
                           cmap='RdYlBu_r',
                           ax=ax3)
                ax3.set_title('Vulnerability Detection Matrix')
                ax3.tick_params(axis='x', rotation=45)
        
        # 4. Agreement score and consensus
        ax4.text(0.1, 0.8, f"Agreement Score: {result.agreement_score:.3f}", fontsize=12, transform=ax4.transAxes)
        ax4.text(0.1, 0.6, f"Consensus Findings: {len(result.consensus_findings)}", fontsize=12, transform=ax4.transAxes)
        ax4.text(0.1, 0.4, f"Contract: {result.contract_name}", fontsize=12, transform=ax4.transAxes)
        
        if result.consensus_findings:
            consensus_text = "\\n".join(result.consensus_findings)
            ax4.text(0.1, 0.2, f"Consensus: {consensus_text}", fontsize=10, transform=ax4.transAxes)
        
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        ax4.set_title('Summary')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_benchmark_results(self, benchmark_metrics: Dict[str, BenchmarkMetrics], save_path: Optional[str] = None):
        """
        Plot benchmark results for multiple tools.
        
        Args:
            benchmark_metrics: Dictionary of benchmark metrics
            save_path: Path to save the plot
        """
        tools = list(benchmark_metrics.keys())
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Overall performance metrics
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        metric_values = {metric: [] for metric in metrics}
        
        for tool in tools:
            for metric in metrics:
                metric_values[metric].append(getattr(benchmark_metrics[tool], metric))
        
        x = np.arange(len(tools))
        width = 0.2
        
        for i, metric in enumerate(metrics):
            ax1.bar(x + i * width, metric_values[metric], width, label=metric.replace('_', ' ').title())
        
        ax1.set_xlabel('Tools')
        ax1.set_ylabel('Score')
        ax1.set_title('Performance Metrics Comparison')
        ax1.set_xticks(x + width * 1.5)
        ax1.set_xticklabels(tools)
        ax1.legend()
        ax1.set_ylim(0, 1)
        
        # 2. Execution time comparison
        exec_times = [benchmark_metrics[tool].avg_execution_time for tool in tools]
        ax2.bar(tools, exec_times, color='orange', alpha=0.7)
        ax2.set_title('Average Execution Time')
        ax2.set_ylabel('Time (seconds)')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. False positive vs False negative rates
        fpr = [benchmark_metrics[tool].false_positive_rate for tool in tools]
        fnr = [benchmark_metrics[tool].false_negative_rate for tool in tools]
        
        x = np.arange(len(tools))
        width = 0.35
        
        ax3.bar(x - width/2, fpr, width, label='False Positive Rate', alpha=0.7)
        ax3.bar(x + width/2, fnr, width, label='False Negative Rate', alpha=0.7)
        ax3.set_xlabel('Tools')
        ax3.set_ylabel('Rate')
        ax3.set_title('Error Rates Comparison')
        ax3.set_xticks(x)
        ax3.set_xticklabels(tools)
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Success rate
        success_rates = [benchmark_metrics[tool].success_rate for tool in tools]
        ax4.bar(tools, success_rates, color='green', alpha=0.7)
        ax4.set_title('Tool Success Rate')
        ax4.set_ylabel('Success Rate')
        ax4.set_ylim(0, 1)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def export_results(self, output_path: str, format: str = 'json'):
        """
        Export comparison history to file.
        
        Args:
            output_path: Path to save the results
            format: Export format ('json' or 'csv')
        """
        if format == 'json':
            results_data = [result.to_dict() for result in self.comparison_history]
            with open(output_path, 'w') as f:
                json.dump(results_data, f, indent=2)
        
        elif format == 'csv':
            # Flatten results for CSV export
            rows = []
            for result in self.comparison_history:
                base_row = {
                    'contract_name': result.contract_name,
                    'agreement_score': result.agreement_score,
                    'consensus_findings_count': len(result.consensus_findings),
                    'timestamp': result.timestamp.isoformat()
                }
                
                for tool_name, performance in result.tool_performances.items():
                    row = base_row.copy()
                    row.update({
                        'tool_name': tool_name,
                        'execution_time': performance.execution_time,
                        'findings_count': performance.findings_count,
                        'success': performance.success,
                        'vulnerabilities_found': ','.join(performance.vulnerabilities_found)
                    })
                    rows.append(row)
            
            df = pd.DataFrame(rows)
            df.to_csv(output_path, index=False)
        
        logger.info(f"Results exported to {output_path}")
    
    def get_available_tools(self) -> Dict[str, bool]:
        """
        Get dictionary of available tools.
        
        Returns:
            Dictionary mapping tool names to availability status
        """
        return self.available_tools.copy()


def main():
    """Example usage of ToolComparator."""
    # Sample vulnerable contract
    vulnerable_contract = """
    pragma solidity ^0.8.0;
    
    contract VulnerableContract {
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
    """
    
    # Initialize comparator
    comparator = ToolComparator()
    
    print("Available tools:")
    for tool, available in comparator.get_available_tools().items():
        print(f"  {tool}: {'✓' if available else '✗'}")
    
    # Compare tools on the sample contract
    print("\\nComparing tools on vulnerable contract...")
    result = comparator.compare_tools(
        contract_code=vulnerable_contract,
        contract_name="VulnerableContract",
        ground_truth=['reentrancy', 'bad_randomness']
    )
    
    print(f"Agreement score: {result.agreement_score:.3f}")
    print(f"Consensus findings: {result.consensus_findings}")
    
    print("\\nTool performances:")
    for tool_name, performance in result.tool_performances.items():
        if performance.success:
            print(f"  {tool_name}:")
            print(f"    Execution time: {performance.execution_time:.2f}s")
            print(f"    Findings: {performance.findings_count}")
            print(f"    Vulnerabilities: {performance.vulnerabilities_found}")
        else:
            print(f"  {tool_name}: Failed - {performance.error_message}")
    
    # Plot results if matplotlib is available
    try:
        comparator.plot_comparison_results(result)
    except ImportError:
        print("Matplotlib not available for plotting")


if __name__ == "__main__":
    main()