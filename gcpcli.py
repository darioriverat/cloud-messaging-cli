#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Get the directory of the current script
    script_dir = Path(__file__).parent
    gcptoolkit_dir = script_dir / "gcptoolkit"

    # Get script name and arguments
    if len(sys.argv) < 2:
        print("Error: No script name provided")
        print("Usage: python gcpcli.py <script_name> [args...]")
        print("Available scripts:")
        list_available_scripts(gcptoolkit_dir)
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    # Check if the Python file exists in the gcptoolkit directory
    script_path = gcptoolkit_dir / f"{script_name}.py"

    if not script_path.exists():
        print(f"Error: Python script not found: {script_name}.py in {gcptoolkit_dir}")
        print("Available scripts:")
        list_available_scripts(gcptoolkit_dir)
        sys.exit(1)

    # Run the script with uv run
    try:
        cmd = ["uv", "run", str(script_path)] + script_args
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'uv' command not found. Please install uv: https://docs.astral.sh/uv/")
        sys.exit(1)

def list_available_scripts(gcptoolkit_dir):
    """List all available Python scripts in the gcptoolkit directory."""
    if not gcptoolkit_dir.exists():
        print(f"  No gcptoolkit directory found at {gcptoolkit_dir}")
        return

    python_files = list(gcptoolkit_dir.glob("*.py"))
    if python_files:
        for py_file in sorted(python_files):
            script_name = py_file.stem
            print(f"  {script_name}")
    else:
        print("  No Python scripts found")

if __name__ == "__main__":
    main()