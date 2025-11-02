#!/usr/bin/env python3
"""
Verification script to check if the ANPR system is properly set up.
Run this before attempting to use main.py, add_missing_data.py, or visualize.py
"""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor}.{version.micro} is too old. Need 3.8+")
        return False

def check_dependencies():
    """Check if all required Python packages are installed"""
    required_packages = [
        ('cv2', 'opencv-python'),
        ('easyocr', 'easyocr'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
        ('ultralytics', 'ultralytics'),
        ('filterpy', 'filterpy'),
    ]
    
    missing = []
    for package, pip_name in required_packages:
        try:
            __import__(package)
            print(f"✓ {pip_name}")
        except ImportError:
            print(f"✗ {pip_name} (missing)")
            missing.append(pip_name)
    
    return len(missing) == 0, missing

def check_sort_tracker():
    """Check if SORT tracker is available"""
    if not os.path.isdir('./sort'):
        print("✗ SORT tracker directory not found")
        print("  Run: git clone https://github.com/abewley/sort.git")
        return False
    
    if not os.path.isfile('./sort/sort.py'):
        print("✗ SORT tracker sort.py not found")
        return False
    
    # Try to import SORT
    sys.path.insert(0, './sort')
    try:
        from sort import Sort
        print("✓ SORT tracker")
        return True
    except ImportError as e:
        print(f"✗ SORT tracker (import error: {e})")
        return False

def check_files():
    """Check if all required files are present"""
    required_files = [
        'main.py',
        'util.py',
        'visualize.py',
        'add_missing_data.py',
    ]
    
    missing = []
    for filename in required_files:
        if os.path.isfile(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} (missing)")
            missing.append(filename)
    
    return len(missing) == 0, missing

def check_models():
    """Check if required models are available"""
    issues = []
    
    # Check license plate detector
    if not os.path.isfile('./models/license_plate_detector.pt'):
        print("✗ License plate detector model not found")
        print("  Expected at: ./models/license_plate_detector.pt")
        print("  See README.md for how to obtain this model")
        issues.append('license_plate_detector.pt')
    else:
        print("✓ License plate detector model")
    
    # YOLOv8n will be auto-downloaded, so we just inform the user
    if not os.path.isfile('./yolov8n.pt'):
        print("ℹ YOLOv8n model not found (will be auto-downloaded on first run)")
    else:
        print("✓ YOLOv8n model")
    
    return len(issues) == 0, issues

def check_input_video():
    """Check if input video is available"""
    if not os.path.isfile('./sample.mp4'):
        print("✗ Input video not found")
        print("  Expected at: ./sample.mp4")
        print("  Download a sample from: https://www.pexels.com/video/traffic-flow-in-the-highway-2103099/")
        return False
    else:
        print("✓ Input video (sample.mp4)")
        return True

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("ANPR System Setup Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check Python version
    print("\n1. Checking Python version...")
    if not check_python_version():
        all_checks_passed = False
    
    # Check dependencies
    print("\n2. Checking Python dependencies...")
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        all_checks_passed = False
        print(f"\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing_deps)}")
    
    # Check SORT tracker
    print("\n3. Checking SORT tracker...")
    if not check_sort_tracker():
        all_checks_passed = False
    
    # Check required files
    print("\n4. Checking required files...")
    files_ok, missing_files = check_files()
    if not files_ok:
        all_checks_passed = False
    
    # Check models
    print("\n5. Checking models...")
    models_ok, missing_models = check_models()
    if not models_ok:
        all_checks_passed = False
    
    # Check input video
    print("\n6. Checking input video...")
    if not check_input_video():
        all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. python main.py")
        print("  2. python add_missing_data.py")
        print("  3. python visualize.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nRefer to README.md and QUICKSTART.md for setup instructions.")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
