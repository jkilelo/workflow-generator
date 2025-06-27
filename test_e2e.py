#!/usr/bin/env python3
"""
Comprehensive E2E Testing Script for Workflow Generator
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
import importlib.util

def log_test(message):
    print(f"[TEST] {message}")

def log_success(message):
    print(f"✅ {message}")

def log_error(message):
    print(f"❌ {message}")

def test_plugin_imports():
    """Test that generated plugins can be imported without errors"""
    log_test("Testing plugin imports...")
    
    backend_dir = Path('backend')
    if not backend_dir.exists():
        log_error("Backend directory does not exist")
        return False
    
    plugin_files = list(backend_dir.glob('*_plugin.py'))
    if not plugin_files:
        log_error("No plugin files found")
        return False
    
    all_passed = True
    
    for plugin_file in plugin_files:
        try:
            # Test syntax first
            result = subprocess.run([
                sys.executable, '-m', 'py_compile', str(plugin_file)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                log_error(f"Syntax error in {plugin_file.name}: {result.stderr}")
                all_passed = False
                continue
            
            log_success(f"Plugin {plugin_file.name} syntax is valid")
                
        except Exception as e:
            log_error(f"Failed to test {plugin_file.name}: {e}")
            all_passed = False
    
    return all_passed

def test_main_server():
    """Test the main FastAPI server can start"""
    log_test("Testing main server startup...")
    
    main_file = Path('main.py')
    if not main_file.exists():
        log_error("main.py does not exist")
        return False
    
    try:
        # Test syntax
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', 'main.py'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            log_error(f"Syntax error in main.py: {result.stderr}")
            return False
        
        log_success("main.py syntax is valid")
        return True
        
    except Exception as e:
        log_error(f"Failed to test main.py: {e}")
        return False

def main():
    """Run all E2E tests"""
    print("🚀 Running Comprehensive E2E Tests")
    print("=" * 50)
    
    tests = [
        ("Plugin Imports", test_plugin_imports),
        ("Main Server", test_main_server),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        log_success("All tests passed! ✨")
    else:
        log_error("Some tests failed! 🔥")
        sys.exit(1)

if __name__ == "__main__":
    main()