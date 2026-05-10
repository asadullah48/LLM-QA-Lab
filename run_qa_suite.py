#!/usr/bin/env python3
"""Master QA Test Runner"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.tests.test_accuracy import AccuracyTester

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

console = Console()

class QATestSuite:
    """Orchestrate all QA tests"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {}
        
    def run_accuracy_tests(self) -> Dict[str, Any]:
        """Run accuracy test suite"""
        console.print("[bold cyan][ACCURACY] Running Accuracy Tests...[/bold cyan]")
        
        # Load test cases
        test_cases = [
            {"question": "What is machine learning?", 
             "expected": "Machine learning enables systems to learn from data."},
            {"question": "What is RAG?", 
             "expected": "RAG is Retrieval-Augmented Generation for enhanced LLM responses."},
            {"question": "What is Python?",
             "expected": "Python is a high-level programming language."}
        ]
        
        tester = AccuracyTester()
        results = tester.run_suite(test_cases)
        return results
    
    def run_all(self, tests: list = None) -> Dict[str, Any]:
        """Run all or selected test suites"""
        
        available_tests = {
            "accuracy": self.run_accuracy_tests,
        }
        
        # Filter tests
        if tests:
            to_run = {k: v for k, v in available_tests.items() if k in tests}
        else:
            to_run = available_tests
        
        self.start_time = datetime.now()
        
        for test_name, test_func in to_run.items():
            console.print(f"\n[bold]Running {test_name} tests...[/bold]")
            self.results[test_name] = test_func()
        
        self.end_time = datetime.now()
        return self.results
    
    def generate_report(self, format: str = "json"):
        """Generate test report"""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        total_tests = sum(r.get("total_tests", 0) for r in self.results.values())
        total_passed = sum(r.get("passed", 0) for r in self.results.values())
        
        if format == "json":
            report = {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": duration,
                "summary": {
                    "total_tests": total_tests,
                    "passed": total_passed,
                    "failed": total_tests - total_passed,
                    "pass_rate": total_passed / total_tests if total_tests > 0 else 0
                },
                "detailed_results": self.results
            }
            
            # Save to file
            output_dir = Path("data/results")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            console.print(f"\n[green]✓ Report saved to {output_file}[/green]")
            return report
            
        elif format == "table":
            table = Table(title="QA Test Suite Results")
            table.add_column("Test Suite", style="cyan")
            table.add_column("Pass Rate", style="green")
            table.add_column("Avg Score", style="yellow")
            
            for test_name, results in self.results.items():
                table.add_row(
                    test_name.capitalize(),
                    f"{results.get('pass_rate', 0):.1%}",
                    f"{results.get('average_score', 0):.2f}"
                )
            
            console.print(table)
            return None

@click.command()
@click.option('--tests', '-t', multiple=True, 
              help='Specific tests to run (accuracy)')
@click.option('--format', '-f', default='table', 
              help='Output format (table, json)')
def main(tests, format):
    """Run LLM QA Test Suite"""
    
    console.print(Panel.fit(
        "[bold blue]LLM QA Lab[/bold blue]\n"
        "[dim]Professional AI Quality Assurance Suite[/dim]",
        border_style="blue"
    ))
    
    suite = QATestSuite()
    
    try:
        console.print("\n[yellow]Starting test execution...[/yellow]\n")
        results = suite.run_all(list(tests) if tests else None)
        
        console.print("\n[bold green]Test Execution Complete![/bold green]")
        suite.generate_report(format=format)
        
        # Print summary
        total_tests = sum(r.get("total_tests", 0) for r in results.values())
        total_passed = sum(r.get("passed", 0) for r in results.values())
        
        if total_tests > 0:
            if total_passed == total_tests:
                console.print("\n[bold green][SUCCESS] All tests passed![/bold green]")
            else:
                console.print(f"\n[bold yellow][WARNING] {total_tests - total_passed}/{total_tests} tests failed[/bold yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[red]Test execution interrupted by user[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]ERROR: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
