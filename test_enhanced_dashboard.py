"""
Test script for the enhanced dashboard
Validates that all components can be imported and initialized
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit")
    except ImportError as e:
        print(f"✗ Streamlit: {e}")
        return False
    
    try:
        import cv2
        print("✓ OpenCV")
    except ImportError as e:
        print(f"✗ OpenCV: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas")
    except ImportError as e:
        print(f"✗ Pandas: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✓ Plotly")
    except ImportError as e:
        print(f"✗ Plotly: {e}")
        return False
    
    try:
        from main_old import VisionOCRAgent, AccessControlAgent
        print("✓ Agents from main_old.py")
    except ImportError as e:
        print(f"✗ Agents: {e}")
        return False
    
    return True


def test_dashboard_module():
    """Test that dashboard_enhanced.py can be imported"""
    print("\nTesting dashboard module...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import dashboard_enhanced
        print("✓ dashboard_enhanced.py can be imported")
        
        # Check for main classes/functions
        if hasattr(dashboard_enhanced, 'EnhancedDashboard'):
            print("✓ EnhancedDashboard class found")
        else:
            print("✗ EnhancedDashboard class not found")
            return False
        
        if hasattr(dashboard_enhanced, 'main'):
            print("✓ main() function found")
        else:
            print("✗ main() function not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error importing dashboard_enhanced: {e}")
        return False


def test_demo_video_creation():
    """Test demo video creation"""
    print("\nTesting demo video creation...")
    
    try:
        from create_demo_video import create_demo_video
        print("✓ create_demo_video module imported")
        
        # Test creating a very short demo video
        test_file = "test_demo_short.mp4"
        create_demo_video(output_path=test_file, duration_seconds=1, fps=10)
        
        if os.path.exists(test_file):
            print(f"✓ Demo video created: {test_file}")
            
            # Verify it can be opened
            import cv2
            cap = cv2.VideoCapture(test_file)
            if cap.isOpened():
                print("✓ Demo video can be opened")
                cap.release()
                
                # Cleanup
                os.remove(test_file)
                print("✓ Test file cleaned up")
                return True
            else:
                print("✗ Demo video cannot be opened")
                return False
        else:
            print(f"✗ Demo video not created")
            return False
            
    except Exception as e:
        print(f"✗ Error testing demo video: {e}")
        return False


def test_file_structure():
    """Verify required files exist"""
    print("\nChecking file structure...")
    
    required_files = [
        'main.py',
        'main_old.py',
        'dashboard.py',
        'dashboard_enhanced.py',
        'create_demo_video.py',
        'requirements.txt',
        'authorized_plates.csv',
        'ENHANCED_DASHBOARD_GUIDE.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("=" * 60)
    print("Enhanced Dashboard Validation Tests")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test file structure
    results.append(("File Structure", test_file_structure()))
    
    # Test dashboard module
    results.append(("Dashboard Module", test_dashboard_module()))
    
    # Test demo video creation
    results.append(("Demo Video Creation", test_demo_video_creation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
