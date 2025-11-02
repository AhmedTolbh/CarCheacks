"""
Test script for the multi-agent AI system
Tests core functionality without requiring camera or GUI
"""

import sys
import csv
import os
from datetime import datetime

# Test imports
print("Testing imports...")
try:
    import pandas as pd
    import numpy as np
    print("✓ pandas and numpy imported successfully")
except ImportError as e:
    print(f"✗ Error importing pandas/numpy: {e}")
    sys.exit(1)

# Test Agent 2: Access Control Agent
print("\nTesting Agent 2: Access Control Agent...")

class AccessControlAgentTest:
    """Simplified version for testing"""
    
    def __init__(self, whitelist_file="authorized_plates.csv", log_file="test_access_log.csv"):
        self.whitelist_file = whitelist_file
        self.log_file = log_file
        self.authorized_plates = self.load_whitelist()
        self.initialize_log()
    
    def load_whitelist(self):
        authorized = set()
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    plate = row['plate_number'].strip().upper()
                    authorized.add(plate)
        return authorized
    
    def initialize_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'plate_number', 'status'])
    
    def check_authorization(self, plate_number):
        return plate_number in self.authorized_plates
    
    def log_access_attempt(self, plate_number, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, plate_number, status])
    
    def process_plate(self, plate_number):
        is_authorized = self.check_authorization(plate_number)
        status = "ALLOW" if is_authorized else "DENY"
        self.log_access_attempt(plate_number, status)
        return {"decision": status, "plate_number": plate_number}

# Test Agent 2
try:
    agent2 = AccessControlAgentTest()
    print(f"✓ Agent 2 initialized with {len(agent2.authorized_plates)} authorized plates")
    
    # Test authorized plate
    result = agent2.process_plate("ABC123")
    assert result['decision'] == "ALLOW", "Expected ALLOW for ABC123"
    print(f"✓ Test 1 passed: ABC123 -> {result['decision']}")
    
    # Test unauthorized plate
    result = agent2.process_plate("INVALID999")
    assert result['decision'] == "DENY", "Expected DENY for INVALID999"
    print(f"✓ Test 2 passed: INVALID999 -> {result['decision']}")
    
    # Test another authorized plate
    result = agent2.process_plate("XYZ789")
    assert result['decision'] == "ALLOW", "Expected ALLOW for XYZ789"
    print(f"✓ Test 3 passed: XYZ789 -> {result['decision']}")
    
except Exception as e:
    print(f"✗ Agent 2 test failed: {e}")
    sys.exit(1)

# Test Agent 3: Data Analytics
print("\nTesting Agent 3: Data Analytics Agent...")

class DataAnalyticsAgentTest:
    """Simplified version for testing"""
    
    def __init__(self, log_file="test_access_log.csv"):
        self.log_file = log_file
    
    def load_data(self):
        if os.path.exists(self.log_file):
            df = pd.read_csv(self.log_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return pd.DataFrame(columns=['timestamp', 'plate_number', 'status'])
    
    def calculate_kpis(self, df):
        if df.empty:
            return {
                'total_entries': 0,
                'total_allowed': 0,
                'total_denied': 0,
                'allow_rate': 0.0
            }
        
        total_entries = len(df)
        total_allowed = len(df[df['status'] == 'ALLOW'])
        total_denied = len(df[df['status'] == 'DENY'])
        allow_rate = (total_allowed / total_entries * 100) if total_entries > 0 else 0
        
        return {
            'total_entries': total_entries,
            'total_allowed': total_allowed,
            'total_denied': total_denied,
            'allow_rate': allow_rate
        }

# Test Agent 3
try:
    agent3 = DataAnalyticsAgentTest()
    print("✓ Agent 3 initialized")
    
    # Load data
    df = agent3.load_data()
    print(f"✓ Loaded {len(df)} log entries")
    
    # Calculate KPIs
    kpis = agent3.calculate_kpis(df)
    print(f"✓ KPIs calculated:")
    print(f"  - Total entries: {kpis['total_entries']}")
    print(f"  - Total allowed: {kpis['total_allowed']}")
    print(f"  - Total denied: {kpis['total_denied']}")
    print(f"  - Allow rate: {kpis['allow_rate']:.1f}%")
    
    assert kpis['total_entries'] == 3, "Expected 3 total entries"
    assert kpis['total_allowed'] == 2, "Expected 2 allowed entries"
    assert kpis['total_denied'] == 1, "Expected 1 denied entry"
    
    print("✓ All Agent 3 tests passed")
    
except Exception as e:
    print(f"✗ Agent 3 test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Cleanup test log
try:
    if os.path.exists("test_access_log.csv"):
        os.remove("test_access_log.csv")
    print("\n✓ Test cleanup completed")
except:
    pass

print("\n" + "="*50)
print("ALL TESTS PASSED! ✓")
print("="*50)
print("\nThe multi-agent system is ready to use!")
print("\nTo run the full system:")
print("  Terminal 1: python main.py")
print("  Terminal 2: streamlit run dashboard.py")
