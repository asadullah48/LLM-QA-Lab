#!/usr/bin/env python3
"""Master QA Test Runner with Features"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from src.utils.logger import logger
from src.utils.config_loader import config
from src.tests.test_accuracy import AccuracyTester

console = Console()

class QATestSuite:
    """Orchestrate all QA tests"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {}
        self.config = config
        
    def run_accuracy_tests(self) -> Dict[str, Any]:
        """Run accuracy test suite"""
        console.print("[bold cyan]📊 Running Accuracy Tests...[/bold cyan]")
        
        # Load test cases from config or data file
        test_cases = [
            {"question": "What is machine learning?", 
             "expected": "Machine learning enables systems to learn from data."},
            {"question": "What is RAG?", 
             "expected": "RAG is Retrieval-Augmented Generation for enhanced LLM responses."}
        ]
        
        tester = AccuracyTester()
        results = tester.run_suite(test_cases)
        return results
    
    def run_all(self, tests: list = None) -> Dict[str, Any]:
        """Run all or selected test suites"""
        
        available_tests = {
            "accuracy": self.run_accuracy_tests,
            "robustness": None,  # To be implemented
            "bias": None,        # To be implemented
            "rag": None,         # To be implemented
            "consistency": None  # To be implemented
        }
        
        # Filter tests
        if tests:
            to_run = {k: v for k, v in available_tests.items() if k in tests and v}
        else:
            to_run = {k: v for k, v in available_tests.items() if v}
        
        self.start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            for test_name, test_func in to_run.items():
                task = progress.add_task(f"Running {test_name} tests...", total=None)
                self.results[test_name] = test_func()
                progress.update(task, completed=True)
        
        self.end_time = time.time()
        return self.results
    
    def generate_report(self, format: str = "json") -> str:
        """Generate test report"""
        duration = self.end_time - self.start_time
        
        # Calculate overall metrics
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
            output_file = f"data/results/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            Path("data/results").mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            console.print(f"\n[green]✓ Report saved to {output_file}[/green]")
            
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
            
        return report

@click.command()
@click.option('--tests', '-t', multiple=True, 
              help='Specific tests to run (accuracy, robustness, bias, rag, consistency)')
@click.option('--format', '-f', default='table', 
              help='Output format (table, json)')
@click.option('--config', '-c', help='Custom config file path')
def main(tests, format, config):
    """Run LLM QA Test Suite"""
    
    console.print(Panel.fit(
        "[bold blue]🤖 LLM QA Lab[/bold blue]\n"
        "[dim]Professional AI Quality Assurance Suite[/dim]",
        border_style="blue"
    ))
    
    if config:
        console.print(f"Using config: {config}")
    
    suite = QATestSuite()
    
    try:
        console.print("\n[yellow]Starting test execution...[/yellow]\n")
        results = suite.run_all(tests if tests else None)
        
        console.print("\n[bold green]✅ Test Execution Complete![/bold green]")
        suite.generate_report(format=format)
        
        # Print summary
        total_tests = sum(r.get("total_tests", 0) for r in results.values())
        total_passed = sum(r.get("passed", 0) for r in results.values())
        
        if total_passed == total_tests:
            console.print("\n[bold green]🎉 All tests passed! 🎉[/bold green]")
        else:
            console.print(f"\n[bold yellow]⚠️  {total_tests - total_passed} tests failed[/bold yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[red]Test execution interrupted by user[/red]")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        console.print(f"\n[red]❌ Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()

