# Dashboard Video Upload Guide

## Overview

The enhanced dashboard (`dashboard_enhanced.py`) provides a complete integrated solution for vehicle access control with video upload and processing capabilities. This guide explains how to use all the features available on the dashboard.

## What This Dashboard Does

The dashboard integrates all three agents into a single web interface:

1. **Agent 1 (Vision & OCR)**: Detects license plates and reads text from video frames
2. **Agent 2 (Access Control)**: Checks authorization and makes access decisions  
3. **Agent 3 (Analytics)**: Processes logs, generates insights, and visualizes data

All of these processes are available through the dashboard with video upload functionality.

## Quick Start

### Prerequisites

Install all required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Dashboard

Start the enhanced dashboard:

```bash
streamlit run dashboard_enhanced.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Features

### Tab 1: Video Upload & Analysis 📹

This tab allows you to upload videos and process them in real-time:

**Features:**
- Upload video files (MP4, AVI, MOV, MKV)
- Real-time video processing with live frame display
- License plate detection and recognition
- Access control decisions displayed on each frame
- Progress tracking during processing
- Agent activity log showing real-time communication between agents

**How to Use:**
1. Click "Choose a video file" to upload a video
2. Review the video information (frames, FPS, duration)
3. Click "🚀 Start Processing" to begin analysis
4. Watch as the system:
   - Detects license plates in each frame
   - Reads the plate numbers using OCR
   - Makes authorization decisions
   - Logs all access attempts
5. View the Agent Activity Log on the right to see how agents communicate

**What Happens During Processing:**
- Every 10th frame is analyzed to optimize performance
- When a license plate is detected:
  - Agent 1 extracts the plate number
  - Agent 2 checks if it's authorized
  - Agent 3 logs the access attempt
  - Results are displayed on the frame
  - Activity is logged in real-time

### Tab 2: Analytics Dashboard 📊

This tab displays comprehensive analytics from all processed videos:

**Features:**
- **Key Performance Indicators (KPIs)**:
  - Total Entries: Number of access attempts
  - Total Allowed: Number of authorized entries
  - Total Denied: Number of denied entries
  - Allow Rate: Percentage of allowed entries

- **Visualizations**:
  - Pie chart showing ALLOW vs DENY distribution
  - Bar chart of top 10 vehicles by entry attempts
  - Live access log table with search and filter

**How to Use:**
1. After processing videos, switch to this tab
2. Review the KPIs at the top
3. Examine the visualizations
4. Search for specific plates in the log table
5. Filter by status (ALLOW/DENY)
6. Download filtered data as CSV

### Tab 3: Agent Workflow 🔄

This tab visualizes how the multi-agent system works:

**Features:**
- Interactive workflow diagram showing agent communication
- Detailed description of each agent's capabilities
- Real-time activity timeline
- System architecture explanation

**What You'll See:**
- **Visual Workflow**: Shows how data flows from video input through all three agents
- **Agent Details**: Explains what each agent does and what technologies it uses
- **Activity Timeline**: Lists recent agent communications and actions

## System Architecture

### Agent Communication Flow

```
Video Input
    ↓
Agent 1: Vision & OCR
    - Captures frames from uploaded video
    - Detects license plates using edge detection or YOLOv8
    - Extracts text using EasyOCR
    ↓
Agent 2: Access Control
    - Receives plate number from Agent 1
    - Checks against authorized plates whitelist
    - Makes ALLOW/DENY decision
    - Logs access attempt
    ↓
Agent 3: Analytics
    - Reads access logs
    - Calculates KPIs
    - Generates visualizations
    - Provides real-time dashboard updates
```

### Data Flow

1. **Video Upload**: User uploads video through dashboard
2. **Frame Processing**: Agent 1 processes frames every 10th frame
3. **Plate Detection**: Agent 1 detects and reads license plates
4. **Authorization Check**: Agent 2 checks plate against whitelist
5. **Decision Making**: Agent 2 makes ALLOW/DENY decision
6. **Logging**: Agent 2 logs the access attempt to CSV
7. **Analytics**: Agent 3 reads logs and updates dashboard
8. **Visualization**: Dashboard displays results in real-time

## Configuration

### Authorized Plates

The system reads authorized plates from `authorized_plates.csv`:

```csv
plate_number,owner_name,vehicle_type
ABC123,John Doe,Car
XYZ789,Jane Smith,Truck
```

To add authorized plates:
1. Edit `authorized_plates.csv`
2. Add new lines with plate_number, owner_name, vehicle_type
3. Save the file
4. The system will automatically load the new plates

### Processing Options

You can configure processing in `dashboard_enhanced.py`:

- **Frame Skip**: Currently processes every 10th frame (line 197)
  - Change `if frame_count % 10 != 0:` to process more/fewer frames
  
- **Plate Detection Cooldown**: 5 seconds between detecting the same plate (line 212)
  - Change `(current_time - processed_plates[plate_number]).seconds > 5` to adjust

- **Display Update Rate**: Updates display every 30 frames (line 244)
  - Change `if frame_count % 30 == 0:` to update more/less frequently

## Technical Details

### Agent Implementation

The agents are implemented in `main_old.py`:

- **VisionOCRAgent**: 
  - Uses EasyOCR for text extraction
  - Supports both edge detection and YOLOv8 for plate detection
  - Cleans and formats OCR output

- **AccessControlAgent**:
  - Loads whitelist from CSV file
  - Makes authorization decisions
  - Logs all access attempts with timestamps

### Technologies Used

- **Streamlit**: Web dashboard framework
- **OpenCV**: Video processing and computer vision
- **EasyOCR**: License plate text recognition
- **Pandas**: Data processing and analytics
- **Plotly**: Interactive visualizations
- **YOLOv8** (optional): Advanced license plate detection

## Troubleshooting

### Video Processing is Slow

**Issue**: Video takes a long time to process

**Solutions**:
- The system processes every 10th frame by default to optimize performance
- For faster processing, increase the skip rate (e.g., every 15th or 20th frame)
- For better accuracy, decrease the skip rate (e.g., every 5th frame)

### No Plates Detected

**Issue**: System doesn't detect any license plates

**Solutions**:
- Ensure video has clear, visible license plates
- Check video quality and lighting
- Try a different video with front/rear views of vehicles
- Use the demo video generator: `python create_demo_video.py 10`

### Dashboard Doesn't Load

**Issue**: Error when starting dashboard

**Solutions**:
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that `main_old.py` exists (contains agent classes)
- Ensure `authorized_plates.csv` exists
- Check Python version (requires Python 3.8+)

### Agent Import Error

**Issue**: "Could not import agents from main_old.py"

**Solutions**:
- Verify `main_old.py` exists in the same directory
- Install required packages: `pip install opencv-python easyocr`
- Check for any syntax errors in `main_old.py`

## Best Practices

### For Demonstrations

1. **Prepare Demo Videos**:
   - Use videos with clear, front-facing license plates
   - Ensure good lighting conditions
   - Keep videos short (10-30 seconds) for quick demos

2. **Set Up Authorized Plates**:
   - Add some test plates to `authorized_plates.csv`
   - Include both authorized and unauthorized plates in your demo video

3. **Show All Tabs**:
   - Start with video upload to show processing
   - Switch to analytics to show KPIs and visualizations
   - End with workflow tab to explain the architecture

### For Development

1. **Testing Changes**:
   - Use short demo videos for quick iteration
   - Check agent activity log for debugging
   - Monitor console output for errors

2. **Performance Optimization**:
   - Adjust frame skip rate based on video length
   - Use YOLOv8 for better plate detection (if model available)
   - Process videos offline for large batches

3. **Data Management**:
   - Regularly back up `access_log.csv`
   - Clean old logs using the dashboard's "Clear Logs" button
   - Export important data using the CSV download feature

## Example Workflow

Here's a complete example of using the dashboard:

1. **Start Dashboard**:
   ```bash
   streamlit run dashboard_enhanced.py
   ```

2. **Prepare Authorized Plates**:
   - Edit `authorized_plates.csv`
   - Add: `ABC123,Test User,Car`

3. **Create Demo Video**:
   ```bash
   python create_demo_video.py 10
   ```

4. **Upload and Process**:
   - Go to "Video Upload & Analysis" tab
   - Upload `demo_video.mp4`
   - Click "Start Processing"
   - Watch real-time detection

5. **View Analytics**:
   - Switch to "Analytics Dashboard" tab
   - Review KPIs and visualizations
   - Search for plate "ABC123"

6. **Understand System**:
   - Switch to "Agent Workflow" tab
   - Review system architecture
   - Check activity timeline

## Next Steps

- **Add More Features**: Extend the dashboard with additional analytics
- **Improve Detection**: Train custom YOLOv8 model for better accuracy
- **Real-Time Camera**: Add support for live camera feed
- **Export Reports**: Generate PDF reports of analytics
- **User Management**: Add authentication and user roles

## Support

For issues or questions:
- Check the troubleshooting section above
- Review error messages in the console
- Ensure all dependencies are correctly installed
- Check that all required files exist (main_old.py, authorized_plates.csv, etc.)
