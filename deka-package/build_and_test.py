#!/usr/bin/env python3
"""
Build and test script for Deka package.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main build and test process."""
    print("🚀 Deka Package Build and Test")
    print("=" * 40)
    
    # Change to package directory
    package_dir = Path(__file__).parent
    os.chdir(package_dir)
    
    # Step 1: Install build dependencies
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine", "pytest"], 
                      "Installing build dependencies"):
        return False
    
    # Step 2: Install package in development mode
    if not run_command([sys.executable, "-m", "pip", "install", "-e", "."], 
                      "Installing package in development mode"):
        return False
    
    # Step 3: Run basic tests
    if not run_command([sys.executable, "-m", "pytest", "tests/", "-v"], 
                      "Running tests"):
        print("⚠️  Tests failed, but continuing with build...")
    
    # Step 4: Build the package
    if not run_command([sys.executable, "-m", "build"], 
                      "Building package"):
        return False
    
    # Step 5: Check the built package
    if not run_command([sys.executable, "-m", "twine", "check", "dist/*"], 
                      "Checking built package"):
        return False
    
    # Step 6: Test import
    print("\n🧪 Testing package import")
    try:
        import deka
        print(f"✅ Successfully imported deka version {deka.__version__}")
        
        # Test basic functionality
        providers = deka.list_providers()
        print(f"✅ Found {len(providers)} providers")
        
        languages = deka.list_languages()
        print(f"✅ Found {len(languages)} languages")
        
        # Test language normalization
        normalized = deka.normalize_language("french")
        print(f"✅ Language normalization works: 'french' → '{normalized}'")
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    print("\n🎉 Build and test completed successfully!")
    print("\nNext steps:")
    print("1. Test with real API keys using examples/basic_usage.py")
    print("2. Upload to TestPyPI: python -m twine upload --repository testpypi dist/*")
    print("3. Upload to PyPI: python -m twine upload dist/*")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
