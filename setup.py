#!/usr/bin/env python3
"""
Setup script for Basketball Shot Tracker
Installs required dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    packages = ['requests', 'bs4', 'pandas', 'matplotlib', 'numpy']
    
    print("\nTesting package imports...")
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            return False
    return True

def main():
    """Main setup function"""
    print("🏀 Basketball Shot Tracker Setup")
    print("=" * 40)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    # Install packages
    if not install_requirements():
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed - some packages could not be imported")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nYou can now run the scraper with:")
    print("python webScraper.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
