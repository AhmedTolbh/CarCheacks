"""
Create a demo video with simulated license plates for testing
"""

import cv2
import numpy as np

def create_demo_video(output_path='demo_video.mp4', duration_seconds=10, fps=30):
    """
    Create a simple demo video with license plate-like text
    
    Args:
        output_path: Path to save the video
        duration_seconds: Duration of the video in seconds
        fps: Frames per second
    """
    # Video properties
    width, height = 640, 480
    total_frames = duration_seconds * fps
    
    # Sample license plate numbers
    plates = ['ABC123', 'XYZ789', 'DEF456', 'GHI101', 'JKL202']
    
    print(f"Creating demo video: {output_path}")
    print(f"Duration: {duration_seconds}s, FPS: {fps}, Total frames: {total_frames}")
    
    # Create video writer with proper resource management
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    try:
        for frame_num in range(total_frames):
            # Create a frame with a gradient background
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add gradient
            for i in range(height):
                color_val = int(50 + (i / height) * 100)
                frame[i, :] = [color_val, color_val, color_val + 20]
            
            # Select plate based on frame number
            plate_idx = (frame_num // (fps * 2)) % len(plates)
            plate_text = plates[plate_idx]
            
            # Draw a white rectangle (simulated license plate)
            plate_x = 200
            plate_y = 200
            plate_width = 240
            plate_height = 80
            
            cv2.rectangle(frame, (plate_x, plate_y), 
                         (plate_x + plate_width, plate_y + plate_height),
                         (255, 255, 255), -1)
            
            # Add border
            cv2.rectangle(frame, (plate_x, plate_y), 
                         (plate_x + plate_width, plate_y + plate_height),
                         (0, 0, 0), 2)
            
            # Add plate text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            font_thickness = 3
            text_size = cv2.getTextSize(plate_text, font, font_scale, font_thickness)[0]
            
            # Center the text
            text_x = plate_x + (plate_width - text_size[0]) // 2
            text_y = plate_y + (plate_height + text_size[1]) // 2
            
            cv2.putText(frame, plate_text, (text_x, text_y),
                       font, font_scale, (0, 0, 0), font_thickness)
            
            # Add frame number
            cv2.putText(frame, f"Frame: {frame_num + 1}/{total_frames}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Write frame
            out.write(frame)
    finally:
        # Release resources
        out.release()
    
    print(f"✅ Demo video created successfully: {output_path}")
    print(f"License plates in video: {', '.join(plates)}")


if __name__ == "__main__":
    import sys
    
    # Get duration from command line or use default
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    create_demo_video(duration_seconds=duration)
