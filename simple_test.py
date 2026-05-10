#!/usr/bin/env python3
"""Simple QA Test Runner"""

from src.tests.test_accuracy import AccuracyTester

def main():
    print("🤖 LLM QA Lab")
    print("=" * 50)
    
    # Sample test cases
    test_cases = [
        {
            "question": "What is machine learning?",
            "expected": "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
        },
        {
            "question": "What is RAG?",
            "expected": "RAG is Retrieval-Augmented Generation for enhanced LLM responses."
        },
        {
            "question": "What is Python?",
            "expected": "Python is a high-level programming language."
        }
    ]
    
    tester = AccuracyTester()
    results = tester.run_suite(test_cases)
    
    print("\n" + "=" * 50)
    if results["pass_rate"] >= 0.8:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed. Review results above.")
    
    print(f"\nFinal Score: {results['average_score']:.2%}")

if __name__ == "__main__":
    main()
