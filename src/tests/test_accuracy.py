"""accuracy testing module"""

from typing import Dict, List, Any
from dataclasses import dataclass
from tqdm import tqdm
from rich.table import Table
from rich.console import Console
from src.core.llm_client import llm_client
from src.utils.logger import logger
from src.utils.config_loader import config

console = Console()

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    expected: str
    actual: str
    score: float
    passed: bool
    details: Dict[str, Any]

class AccuracyTester:
    """Test LLM accuracy against golden dataset"""
    
    def __init__(self):
        self.threshold = config.get("evaluation.pass_threshold", 0.8)
        self.scoring_method = config.get("evaluation.default_scoring", "hybrid")
        self.results = []
        
    def exact_match_scoring(self, expected: str, actual: str) -> float:
        """Exact match scoring"""
        return 1.0 if expected.strip().lower() == actual.strip().lower() else 0.0
    
    def partial_scoring(self, expected: str, actual: str) -> float:
        """Partial match based on word overlap"""
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())
        
        if not expected_words:
            return 0.0
            
        intersection = expected_words.intersection(actual_words)
        return len(intersection) / len(expected_words)
    
    def run_test(self, question: str, expected_answer: str) -> TestResult:
        """Run single accuracy test"""
        logger.info(f"Testing: {question[:50]}...")
        
        # Get LLM response
        actual_answer = llm_client.generate(question)
        
        # Calculate scores
        exact_score = self.exact_match_scoring(expected_answer, actual_answer)
        partial_score = self.partial_scoring(expected_answer, actual_answer)
        
        # Hybrid scoring
        final_score = (exact_score * 0.7) + (partial_score * 0.3)
        
        passed = final_score >= self.threshold
        
        return TestResult(
            test_name=question[:100],
            expected=expected_answer,
            actual=actual_answer,
            score=final_score,
            passed=passed,
            details={
                "exact_score": exact_score,
                "partial_score": partial_score
            }
        )
    
    def run_suite(self, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """Run full test suite"""
        logger.info(f"Running accuracy test suite with {len(test_cases)} cases")
        
        # Progress bar
        for test in tqdm(test_cases, desc="Testing accuracy"):
            result = self.run_test(test["question"], test["expected"])
            self.results.append(result)
        
        # Calculate statistics
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0
        
        # Display results
        table = Table(title="Accuracy Test Results")
        table.add_column("Test", style="cyan", no_wrap=False)
        table.add_column("Score", style="yellow")
        table.add_column("Status", style="green" if passed/total > 0.8 else "red")
        
        for result in self.results[:5]:  # Show first 5
            status = "✓ PASS" if result.passed else "✗ FAIL"
            table.add_row(
                result.test_name[:50] + "...",
                f"{result.score:.2%}",
                status
            )
        
        console.print(table)
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "average_score": avg_score,
            "results": self.results
        }

# Example usage
if __name__ == "__main__":
    # Sample test cases
    sample_tests = [
        {
            "question": "What is machine learning?",
            "expected": "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
        },
        {
            "question": "What is Python?",
            "expected": "Python is a high-level programming language known for its readability and versatility."
        }
    ]
    
    tester = AccuracyTester()
    results = tester.run_suite(sample_tests)
    console.print(f"\n[bold]Summary:[/bold] Pass rate: {results['pass_rate']:.2%}")
