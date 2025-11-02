"""
Real-Time Multi-Agent AI System for Vehicle Access Control
Main Application File - Agents 1 & 2

This module implements:
- Agent 1: Vision & OCR Agent (License plate detection and recognition)
- Agent 2: Access Control (Gatekeeper) Agent (Authorization and logging)
"""

import cv2
import easyocr
import csv
import os
from datetime import datetime
import re
import numpy as np
from pathlib import Path


class VisionOCRAgent:
    """
    Agent 1: Vision & OCR Agent
    
    Responsibilities:
    - Capture video frames from camera or video file
    - Detect license plates using basic image processing
    - Extract text from plates using OCR (EasyOCR)
    - Clean and format the extracted text
    """
    
    def __init__(self):
        """Initialize the Vision & OCR Agent with EasyOCR reader."""
        print("Initializing Vision & OCR Agent...")
        # Initialize EasyOCR reader for English
        # Using GPU if available, otherwise CPU
        self.reader = easyocr.Reader(['en'], gpu=True if cv2.cuda.getCudaEnabledDeviceCount() > 0 else False)
        print("Vision & OCR Agent ready!")
    
    def preprocess_frame(self, frame):
        """
        Preprocess frame for better plate detection.
        
        Args:
            frame: Input BGR frame from video
            
        Returns:
            Preprocessed grayscale frame
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to reduce noise while preserving edges
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        
        return gray
    
    def detect_plate_region(self, frame):
        """
        Detect potential license plate region using edge detection and contours.
        
        This is a simplified approach. For production use, YOLOv8 with a 
        specialized license plate model would be more accurate.
        
        Args:
            frame: Input BGR frame
            
        Returns:
            Cropped plate region or None if no plate detected
        """
        gray = self.preprocess_frame(frame)
        
        # Edge detection
        edged = cv2.Canny(gray, 30, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        plate_contour = None
        
        # Look for rectangular contours (potential plate)
        for contour in contours:
            # Approximate the contour
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.018 * perimeter, True)
            
            # License plates are typically rectangular (4 corners)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                
                # Check aspect ratio (typical plate ratio is between 2:1 and 5:1)
                aspect_ratio = w / float(h)
                
                # Check if contour area is reasonable
                area = cv2.contourArea(approx)
                
                if 2.0 <= aspect_ratio <= 5.0 and area > 500:
                    plate_contour = approx
                    break
        
        if plate_contour is not None:
            # Extract the plate region
            x, y, w, h = cv2.boundingRect(plate_contour)
            plate_region = frame[y:y+h, x:x+w]
            
            # Draw rectangle on original frame for visualization
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            return plate_region
        
        return None
    
    def clean_plate_text(self, text):
        """
        Clean and format OCR-extracted text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned and formatted plate number
        """
        if not text:
            return ""
        
        # Remove spaces
        text = text.replace(" ", "").replace("-", "").replace(".", "")
        
        # Convert to uppercase
        text = text.upper()
        
        # Remove non-alphanumeric characters
        text = re.sub(r'[^A-Z0-9]', '', text)
        
        # Common OCR corrections
        text = text.replace("O", "0").replace("I", "1").replace("S", "5")
        
        return text
    
    def extract_text_from_plate(self, plate_region):
        """
        Extract text from plate region using EasyOCR.
        
        Args:
            plate_region: Cropped plate image
            
        Returns:
            Extracted and cleaned plate number
        """
        if plate_region is None or plate_region.size == 0:
            return None
        
        # Use EasyOCR to read text
        results = self.reader.readtext(plate_region)
        
        if results:
            # Get the text with highest confidence
            plate_text = max(results, key=lambda x: x[2])[1]
            
            # Clean and format the text
            cleaned_text = self.clean_plate_text(plate_text)
            
            return cleaned_text if cleaned_text else None
        
        return None
    
    def process_frame(self, frame):
        """
        Process a single frame to detect and read license plate.
        
        Args:
            frame: Input BGR frame
            
        Returns:
            Dictionary with plate_number and frame, or None if no plate detected
        """
        # Detect plate region
        plate_region = self.detect_plate_region(frame)
        
        if plate_region is not None:
            # Extract text from plate
            plate_number = self.extract_text_from_plate(plate_region)
            
            if plate_number:
                return {
                    "plate_number": plate_number,
                    "frame": frame
                }
        
        return None


class AccessControlAgent:
    """
    Agent 2: Access Control (Gatekeeper) Agent
    
    Responsibilities:
    - Maintain whitelist of authorized plates
    - Make access decisions (ALLOW/DENY)
    - Trigger appropriate actions (gate open/alarm)
    - Log all access attempts
    """
    
    def __init__(self, whitelist_file="authorized_plates.csv", log_file="access_log.csv"):
        """
        Initialize the Access Control Agent.
        
        Args:
            whitelist_file: Path to CSV file containing authorized plates
            log_file: Path to access log CSV file
        """
        print("Initializing Access Control Agent...")
        self.whitelist_file = whitelist_file
        self.log_file = log_file
        
        # Load authorized plates
        self.authorized_plates = self.load_whitelist()
        
        # Initialize log file if it doesn't exist
        self.initialize_log()
        
        print(f"Access Control Agent ready! Loaded {len(self.authorized_plates)} authorized plates.")
    
    def load_whitelist(self):
        """
        Load authorized plate numbers from CSV file.
        
        Returns:
            Set of authorized plate numbers
        """
        authorized = set()
        
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    plate = row['plate_number'].strip().upper()
                    authorized.add(plate)
        else:
            print(f"Warning: Whitelist file {self.whitelist_file} not found!")
        
        return authorized
    
    def initialize_log(self):
        """Initialize the access log file with headers if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'plate_number', 'status'])
    
    def check_authorization(self, plate_number):
        """
        Check if a plate number is authorized.
        
        Args:
            plate_number: License plate number to check
            
        Returns:
            True if authorized, False otherwise
        """
        return plate_number in self.authorized_plates
    
    def trigger_gate_open(self):
        """Simulate opening the gate/barrier."""
        print("=" * 50)
        print("✓ GATE OPENING...")
        print("=" * 50)
    
    def trigger_alarm(self):
        """Simulate triggering an alarm for unauthorized access."""
        print("=" * 50)
        print("✗ ACCESS DENIED - ALARM TRIGGERED!")
        print("=" * 50)
    
    def log_access_attempt(self, plate_number, status):
        """
        Log an access attempt to the CSV file.
        
        Args:
            plate_number: License plate number
            status: "ALLOW" or "DENY"
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, plate_number, status])
    
    def process_plate(self, plate_number):
        """
        Process a detected plate number and make access decision.
        
        Args:
            plate_number: Detected license plate number
            
        Returns:
            Dictionary with decision status
        """
        # Check authorization
        is_authorized = self.check_authorization(plate_number)
        
        # Make decision
        status = "ALLOW" if is_authorized else "DENY"
        
        # Trigger appropriate action
        if is_authorized:
            self.trigger_gate_open()
        else:
            self.trigger_alarm()
        
        # Log the attempt
        self.log_access_attempt(plate_number, status)
        
        return {"decision": status, "plate_number": plate_number}


def main():
    """
    Main application loop.
    
    Coordinates Agent 1 (Vision/OCR) and Agent 2 (Access Control) to:
    1. Capture video frames
    2. Detect and read license plates
    3. Make access control decisions
    4. Log all attempts
    """
    print("=" * 70)
    print("VEHICLE ACCESS CONTROL SYSTEM - MULTI-AGENT AI")
    print("=" * 70)
    print()
    
    # Initialize agents
    vision_agent = VisionOCRAgent()
    access_agent = AccessControlAgent()
    
    print()
    print("Select video source:")
    print("1. Webcam (default)")
    print("2. Video file")
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        video_path = input("Enter video file path: ").strip()
        cap = cv2.VideoCapture(video_path)
    else:
        # Use webcam (0 is usually the default webcam)
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video source!")
        return
    
    print()
    print("System is running... Press 'q' to quit.")
    print()
    
    # Track processed plates to avoid duplicate processing
    processed_plates = {}
    frame_count = 0
    
    while True:
        # Read frame from video source
        ret, frame = cap.read()
        
        if not ret:
            print("End of video or error reading frame.")
            break
        
        frame_count += 1
        
        # Process every Nth frame to reduce load (adjust as needed)
        if frame_count % 10 != 0:
            # Display frame
            cv2.imshow('Vehicle Access Control System', frame)
            
            # Check for quit command
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            continue
        
        # Agent 1: Process frame to detect and read plate
        result = vision_agent.process_frame(frame.copy())
        
        if result:
            plate_number = result['plate_number']
            annotated_frame = result['frame']
            
            # Check if we've recently processed this plate (avoid duplicates)
            current_time = datetime.now()
            
            if plate_number not in processed_plates or \
               (current_time - processed_plates[plate_number]).seconds > 10:
                
                print(f"\n🚗 License Plate Detected: {plate_number}")
                
                # Agent 2: Process the plate for access control
                decision = access_agent.process_plate(plate_number)
                
                print(f"Decision: {decision['decision']}")
                
                # Update processed plates
                processed_plates[plate_number] = current_time
                
                # Display annotated frame
                cv2.putText(annotated_frame, f"Plate: {plate_number}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Status: {decision['decision']}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, 
                           (0, 255, 0) if decision['decision'] == "ALLOW" else (0, 0, 255), 2)
                
                cv2.imshow('Vehicle Access Control System', annotated_frame)
                cv2.waitKey(2000)  # Show result for 2 seconds
            else:
                # Display frame without reprocessing
                cv2.imshow('Vehicle Access Control System', annotated_frame)
        else:
            # Display frame
            cv2.imshow('Vehicle Access Control System', frame)
        
        # Check for quit command
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print()
    print("=" * 70)
    print("System shutdown complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
