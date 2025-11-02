"""
Demo Data Generator for Vehicle Access Control System

This script generates sample access log data to test the dashboard
without needing to run the full camera system.
"""

import csv
import random
from datetime import datetime, timedelta

# Sample plate numbers (mix of authorized and unauthorized)
AUTHORIZED_PLATES = ['ABC123', 'XYZ789', 'DEF456', 'GHI789', 'JKL012', 'MNO345', 'PQR678', 'STU901', 'VWX234']
UNAUTHORIZED_PLATES = ['INVALID1', 'FAKE999', 'NOTREAL', 'BOGUS88', 'WRONG77', 'BAD666', 'NOPE123']

ALL_PLATES = AUTHORIZED_PLATES + UNAUTHORIZED_PLATES

def generate_demo_data(num_entries=50, output_file='access_log.csv'):
    """
    Generate demo access log data.
    
    Args:
        num_entries: Number of log entries to generate
        output_file: Output CSV file path
    """
    print(f"Generating {num_entries} demo access log entries...")
    
    # Initialize CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'plate_number', 'status'])
    
    # Generate entries
    base_time = datetime.now() - timedelta(hours=24)
    
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        
        for i in range(num_entries):
            # Generate timestamp (spread over last 24 hours)
            timestamp = base_time + timedelta(minutes=random.randint(0, 24*60))
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            # Select plate (70% chance of authorized plate)
            if random.random() < 0.7:
                plate = random.choice(AUTHORIZED_PLATES)
                status = "ALLOW"
            else:
                plate = random.choice(UNAUTHORIZED_PLATES)
                status = "DENY"
            
            # Write entry
            writer.writerow([timestamp_str, plate, status])
            
            if (i + 1) % 10 == 0:
                print(f"  Generated {i + 1}/{num_entries} entries...")
    
    print(f"✓ Demo data saved to {output_file}")
    print(f"\nYou can now run: streamlit run dashboard.py")


if __name__ == "__main__":
    import sys
    
    # Get number of entries from command line or use default
    num_entries = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    
    generate_demo_data(num_entries)
