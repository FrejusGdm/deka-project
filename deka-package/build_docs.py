#!/usr/bin/env python3
"""
Build documentation for Deka.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Build documentation."""
    print("📚 Building Deka Documentation")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("mkdocs.yml"):
        print("❌ mkdocs.yml not found. Please run from the deka-package directory.")
        sys.exit(1)
    
    # Install documentation dependencies
    if not run_command("pip install mkdocs mkdocs-material mkdocstrings[python]", "Installing documentation dependencies"):
        sys.exit(1)
    
    # Build documentation
    if not run_command("mkdocs build", "Building documentation"):
        sys.exit(1)
    
    print("\n🎉 Documentation built successfully!")
    print("📁 Documentation files are in the 'site/' directory")
    print("🌐 To serve locally, run: mkdocs serve")
    print("🚀 To deploy to GitHub Pages, run: mkdocs gh-deploy")

if __name__ == "__main__":
    main()
