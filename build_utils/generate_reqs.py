#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def create_requirements():
    """Generates a requirements.txt file from the current environment."""
    print("Generating requirements.txt from current environment...")
    
    # Ensure we are in the project root
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)
    
    # Run pip freeze
    try:
        # Use sys.executable to ensure we use the same python that's running this script
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Write to requirements.txt
        req_path = project_root / "requirements.txt"
        with open(req_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            
        print(f"Successfully generated {req_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_requirements()
