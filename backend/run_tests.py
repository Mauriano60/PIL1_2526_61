#!/usr/bin/env python
"""
Test runner script for the MentorLink backend.
Run all tests, specific test suites, or with coverage report.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --coverage   # Run with coverage report
    python run_tests.py --validators # Run only validator tests
    python run_tests.py --auth       # Run only auth tests
    python run_tests.py -x           # Stop on first failure
"""

import os
import sys
import subprocess
from pathlib import Path

# Inserer le commentaire requis pour le script
# Par CHABI AYEDOUN Yoéla

def run_all_tests():
    """Run all tests."""
    print("🧪 Running all tests...")
    
    # On récupère l'environnement actuel et on y injecte le dossier parent (backend) dans le PYTHONPATH
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)

    return subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=Path(__file__).parent,
        env=current_env  # On passe le nouvel environnement ici
    )
def run_with_coverage():
    """Run tests with coverage report."""
    print("📊 Running tests with coverage report...")
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v",
            "--cov=.",
            "--cov-report=html",
            "--cov-report=term-missing"
        ],
        cwd=Path(__file__).parent,
        env=current_env
    )


def run_validators_tests():
    """Run only validator tests."""
    print("✓ Running validator tests...")
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_validators.py", "-v"],
        cwd=Path(__file__).parent,
        env=current_env
    )


def run_auth_tests():
    """Run only authentication tests."""
    print("🔐 Running authentication tests...")
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_auth_routes.py", "-v"],
        cwd=Path(__file__).parent,
        env=current_env
    )


def run_responses_tests():
    """Run only response utility tests."""
    print("📨 Running response utility tests...")
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_responses.py", "-v"],
        cwd=Path(__file__).parent,
        env=current_env
    )


def run_specific_test(test_name):
    """Run a specific test."""
    print(f"Running specific test: {test_name}...")
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = str(Path(__file__).parent)
    return subprocess.run(
        [sys.executable, "-m", "pytest", f"tests/{test_name}", "-v"],
        cwd=Path(__file__).parent,
        env=current_env
    )


def show_help():
    """Show help message."""
    print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        result = run_all_tests()
    else:
        arg = sys.argv[1]
        if arg == "--coverage":
            result = run_with_coverage()
        elif arg == "--validators":
            result = run_validators_tests()
        elif arg == "--auth":
            result = run_auth_tests()
        elif arg == "--responses":
            result = run_responses_tests()
        elif arg == "-h" or arg == "--help":
            show_help()
            sys.exit(0)
        elif arg.startswith("test_"):
            result = run_specific_test(arg)
        else:
            print(f"Unknown argument: {arg}")
            show_help()
            sys.exit(1)
    
    sys.exit(result.returncode)
