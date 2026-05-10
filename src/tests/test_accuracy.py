"""accuracy testing module"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from src.core.llm_client import llm_client

@dataclass
class TestResult:
    """Test result data structure (JSON serializable)"""
    test_name: str
    expected: str
    actual: str
    score: float
    passed: bool
    details: Dict[str, Any]
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "test_name": self.test_name,
            "expected": self.expected,
            "actual": self.actual,
            "score": self.score,
            "passed": self.passed,
            "details": self.details
        }

class AccuracyTester:
    """Test LLM accuracy against golden dataset"""
    
    def __init__(self):
        self.threshold = 0.6
        self.results = []
        
    def exact_match_scoring(self, expected: str, actual: str) -> float:
        """Exact match scoring (case-insensitive)"""
        expected_clean = expected.strip().lower()
        actual_clean = actual.strip().lower()
        return 1.0 if expected_clean == actual_clean else 0.0
    
    def partial_scoring(self, expected: str, actual: str) -> float:
        """Partial match based on word overlap"""
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())
        
        if not expected_words:
            return 0.0
            
        intersection = expected_words.intersection(actual_words)
        return len(intersection) / len(expected_words)
    
    def semantic_scoring(self, expected: str, actual: str) -> float:
        """Simple keyword-based semantic scoring"""
        expected_keywords = set(expected.lower().split())
        actual_keywords = set(actual.lower().split())
        
        if not expected_keywords:
            return 0.0
            
        common = expected_keywords.intersection(actual_keywords)
        return len(common) / len(expected_keywords)
    
    def run_test(self, question: str, expected_answer: str) -> TestResult:
        """Run single accuracy test"""
        print(f"[TEST] {question[:50]}...")
        
        # Get LLM response
        actual_answer = llm_client.generate(question)
        
        # Calculate scores
        exact_score = self.exact_match_scoring(expected_answer, actual_answer)
        partial_score = self.partial_scoring(expected_answer, actual_answer)
        semantic_score = self.semantic_scoring(expected_answer, actual_answer)
        
        # Hybrid scoring (weighted)
        final_score = (exact_score * 0.4) + (partial_score * 0.3) + (semantic_score * 0.3)
        
        passed = final_score >= self.threshold
        
        return TestResult(
            test_name=question[:100],
            expected=expected_answer[:100],
            actual=actual_answer[:100],
            score=final_score,
            passed=passed,
            details={
                "exact_score": exact_score,
                "partial_score": partial_score,
                "semantic_score": semantic_score
            }
        )
    
    def run_suite(self, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """Run full test suite"""
        print(f"\n[SUITE] Running accuracy test suite with {len(test_cases)} cases")
        print("=" * 60)
        
        self.results = []
        
        for i, test in enumerate(test_cases, 1):
            result = self.run_test(test["question"], test["expected"])
            self.results.append(result)
            
            # Print individual result
            status = "PASS" if result.passed else "FAIL"
            print(f"{status} | Score: {result.score:.1%} | {result.test_name[:50]}...")
            if not result.passed:
                print(f"      Expected: {result.expected[:60]}...")
                print(f"      Got:      {result.actual[:60]}...")
        
        print("=" * 60)
        
        # Calculate statistics
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0
        
        print(f"\n[SUMMARY] {passed}/{total} passed | Average Score: {avg_score:.1%}")
        
        if passed == total:
            print("[SUCCESS] Excellent! All tests passed!")
        elif avg_score >= 0.7:
            print("[OK] Good results! Minor improvements needed.")
        else:
            print("[WARNING] Some tests need work. Review the responses above.")
        
        # Convert results to dictionaries for JSON serialization
        serializable_results = [r.to_dict() for r in self.results]
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "average_score": avg_score,
            "results": serializable_results
        }
