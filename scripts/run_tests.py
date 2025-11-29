#!/usr/bin/env python3
"""
Local development testing script.
Run all the same checks that CI/CD runs, but locally.
"""

import subprocess
import sys
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(name: str, cmd: list[str], required: bool = True) -> bool:
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"🔍 {name}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=False, text=True)

        if result.returncode == 0:
            print(f"✅ {name} passed!")
            return True
        else:
            print(f"{'❌' if required else '⚠️ '} {name} failed!")
            return not required

    except FileNotFoundError:
        print(f"⚠️  {name} skipped (tool not installed)")
        return not required
    except Exception as e:
        print(f"❌ {name} error: {e}")
        return not required


def main():
    print("\n" + "=" * 60)
    print("🚀 Running Local Development Checks")
    print("=" * 60)

    all_passed = True

    # 1. Run tests with coverage
    all_passed &= run_command(
        "Tests with Coverage",
        [sys.executable, "-m", "pytest", "tests/", "-v", "--cov=.", "--cov-report=term-missing"],
        required=True,
    )

    # 2. Check code formatting
    all_passed &= run_command(
        "Black Code Formatting", [sys.executable, "-m", "black", "--check", "."], required=False
    )

    # 3. Run linter
    all_passed &= run_command(
        "Ruff Linter", [sys.executable, "-m", "ruff", "check", ".", "--fix"], required=True
    )

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Ready to push.")
    else:
        print("❌ Some checks failed. Please fix before pushing.")
    print("=" * 60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
