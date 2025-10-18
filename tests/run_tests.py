#!/usr/bin/env python3
"""
Test runner script for the restaurant seating system
"""
import sys
import subprocess
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

def run_tests(test_type="all", verbose=True):
    """Run tests based on type."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # Add test type specific options
    if test_type == "unit":
        cmd.extend(["-m", "unit", "tests/test_models.py", "tests/test_services.py"])
    elif test_type == "api":
        cmd.extend(["-m", "api", "tests/test_api.py"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "coverage":
        cmd.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    else:  # all
        cmd.append("tests/")
    
    # Add additional options
    cmd.extend([
        "--tb=short",
        "--disable-warnings",
        "--color=yes"
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run the tests
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode

def main():
    """Main function to run tests."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"
    
    print(f"Running {test_type} tests...")
    print("=" * 50)
    
    exit_code = run_tests(test_type)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
