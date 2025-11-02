# Vehicle Access Control System - Multi-Agent AI

A real-time, multi-agent AI system for smart vehicle access control using computer vision, OCR, and data analytics.

## 🎯 Overview

This system uses three specialized AI agents working together to provide intelligent vehicle access control:

1. **Agent 1: Vision & OCR Agent** - Detects vehicles and reads license plates using computer vision and OCR
2. **Agent 2: Access Control Agent** - Makes authorization decisions and logs all access attempts
3. **Agent 3: Data Analytics Agent** - Provides real-time analytics and visualizations through a dashboard

## 🏗️ System Architecture

```
┌─────────────────────┐
│   Video Source      │
│ (Camera/Video File) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Agent 1: Vision & OCR Agent        │
│  - Frame capture                    │
│  - Plate detection (edge detection) │
│  - OCR (EasyOCR)                    │
│  - Text cleaning                    │
└──────────┬──────────────────────────┘
           │ plate_number
           ▼
┌─────────────────────────────────────┐
│  Agent 2: Access Control Agent      │
│  - Whitelist check                  │
│  - Allow/Deny decision              │
│  - Gate/alarm trigger               │
│  - Access logging                   │
└──────────┬──────────────────────────┘
           │ access_log.csv
           ▼
┌─────────────────────────────────────┐
│  Agent 3: Data Analytics Agent      │
│  - Real-time data ingestion         │
│  - KPI calculation                  │
│  - Interactive dashboard            │
│  - Visualizations                   │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam or video file for testing
- (Optional) CUDA-compatible GPU for faster OCR processing

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AhmedTolbh/CarCheacks.git
   cd CarCheacks
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import cv2, easyocr, streamlit, pandas; print('All dependencies installed successfully!')"
   ```

## 🎮 Usage

The system requires two terminal windows to run both the main application and the dashboard.

### Terminal 1: Start the Main Application (Agents 1 & 2)

```bash
python main.py
```

When prompted, choose your video source:
- Choose option **1** for live stream from security camera (IP camera/RTSP)
  - Enter RTSP URL (e.g., `rtsp://username:password@192.168.1.100:554/stream`)
  - Or enter IP camera HTTP stream (e.g., `http://192.168.1.100:8080/video`)
- Choose option **2** for video file upload (then enter the file path)
- Choose option **3** for webcam

The application will:
- Capture video frames from your chosen source
- Detect and read license plates using YOLOv8 (if available) or edge detection
- Make access control decisions
- Log all attempts to `access_log.csv`

**Controls:**
- Press `q` to quit the application

### Terminal 2: Start the Analytics Dashboard (Agent 3)

```bash
streamlit run dashboard.py
```

This will open a web browser with the analytics dashboard at `http://localhost:8501`

The dashboard displays:
- **KPIs**: Total entries, allowed, denied, and allow rate
- **Pie Chart**: ALLOW vs DENY distribution
- **Bar Chart**: Top 10 vehicles by entry attempts
- **Hourly Chart**: Traffic distribution by hour
- **Live Log**: Searchable and filterable access log table

### Testing Without a Camera

To test the dashboard without running the camera system, generate demo data:

```bash
python generate_demo_data.py 50
```

This creates `access_log.csv` with 50 sample entries. You can then run the dashboard to see the analytics.

## 📁 Project Structure

```
CarCheacks/
├── main.py                    # Main application (Agents 1 & 2)
├── dashboard.py               # Streamlit dashboard (Agent 3)
├── authorized_plates.csv      # Whitelist of authorized plates
├── requirements.txt           # Python dependencies
├── generate_demo_data.py      # Demo data generator for testing
├── validate_system.py         # System validation script
├── access_log.csv            # Access log (generated at runtime)
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🔧 Configuration

### Adding Authorized Plates

Edit `authorized_plates.csv` to add or remove authorized license plates:

```csv
plate_number
ABC123
XYZ789
DEF456
```

### Adjusting Detection Parameters

In `main.py`, you can adjust:

- **Frame processing rate**: Change `frame_count % 10` (line ~412) to process more/fewer frames
- **Duplicate prevention**: Change the 10-second window (line ~420)
- **Edge detection sensitivity**: Adjust Canny parameters (line ~91)
- **Contour size threshold**: Modify area check (line ~118)

### Dashboard Refresh Rate

In the dashboard sidebar:
- Toggle **Auto-refresh** on/off
- Adjust refresh interval (1-30 seconds)

## 🔍 How It Works

### Agent 1: Vision & OCR Agent

1. **Frame Preprocessing**: Converts frames to grayscale and applies bilateral filtering
2. **Plate Detection**: 
   - **Primary Method**: Uses YOLOv8 pre-trained models for accurate license plate detection on car dashboards
   - **Fallback Method**: Uses Canny edge detection and contour analysis if YOLOv8 is unavailable
3. **OCR Extraction**: Uses EasyOCR to read text from detected plate regions
4. **Text Cleaning**: Removes spaces, corrects common OCR errors (O→0, I→1, S→5)
5. **Video Source Support**: 
   - IP cameras and RTSP streams (security cameras)
   - Video file upload
   - Local webcam

### Agent 2: Access Control Agent

1. **Whitelist Loading**: Reads authorized plates from CSV into a set for fast lookup
2. **Authorization Check**: Compares detected plate against whitelist
3. **Decision Making**: Returns ALLOW or DENY based on authorization
4. **Action Triggering**: Simulates gate opening or alarm
5. **Logging**: Appends timestamp, plate number, and status to CSV

### Agent 3: Data Analytics Agent

1. **Data Ingestion**: Reads `access_log.csv` with pandas
2. **KPI Calculation**: Computes totals and percentages
3. **Visualization**: Creates interactive charts with Plotly
4. **Live Updates**: Auto-refreshes at configurable intervals

## 🛠️ Troubleshooting

### IP Camera / RTSP Stream Issues
- Verify the stream URL is correct and accessible
- Check network connectivity to the camera
- Ensure username/password are correct if required
- Some cameras require specific URL formats (check camera documentation)

### Camera not detected
- Try different camera indices: `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)`
- Check camera permissions
- Ensure camera is not in use by another application

### Low OCR accuracy
- YOLOv8 model provides better plate detection than edge detection
- Improve lighting conditions
- Use higher resolution camera or video stream
- Adjust preprocessing parameters
- Use a specialized license plate detection model (replace `yolov8n.pt` with a license plate specific model)

### Dashboard not updating
- Ensure `access_log.csv` is being created by main.py
- Check auto-refresh is enabled
- Verify file permissions

### GPU not being used
- Install CUDA toolkit and PyTorch with CUDA support
- Verify GPU availability: `python -c "import torch; print(torch.cuda.is_available())"`

### YOLOv8 Model Download
- On first run, YOLOv8 will automatically download the model (may take a few minutes)
- Ensure you have internet connection for initial setup
- Models are cached locally after first download

## 📊 Sample Output

### Console Output (main.py)
```
Initializing Vision & OCR Agent...
Loading YOLOv8 license plate detection model...
YOLOv8 model loaded successfully!
Vision & OCR Agent ready! (GPU: True, YOLOv8: True)

Select video source:
1. Live stream from security camera (IP camera/RTSP)
2. Upload/Load video file
3. Webcam
Enter choice (1, 2, or 3): 1

Stream URL: rtsp://192.168.1.100:554/stream

🚗 License Plate Detected: ABC123
==================================================
✓ GATE OPENING...
==================================================
Decision: ALLOW

🚗 License Plate Detected: XYZ999
==================================================
✗ ACCESS DENIED - ALARM TRIGGERED!
==================================================
Decision: DENY
```

### Dashboard Display
- Clean, interactive web interface
- Real-time charts and metrics
- Searchable data table
- Export capabilities

## 🔐 Security Considerations

- Access logs contain sensitive vehicle data - protect appropriately
- Whitelist file should have restricted permissions
- Consider encrypting stored data for production use
- Implement proper authentication for dashboard access
- Secure RTSP/IP camera streams with strong passwords
- Use VPN or secure network for remote camera access

## 🚧 Future Enhancements

- Fine-tune YOLOv8 on custom license plate dataset
- Multi-camera support with camera management interface
- Email/SMS notifications for denied access
- Advanced analytics (peak hours, suspicious patterns)
- Integration with physical gate controllers
- Cloud deployment with database backend
- Mobile application for monitoring

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This system now uses YOLOv8 for improved license plate detection. The model will be automatically downloaded on first run. For even better accuracy, you can replace the default `yolov8n.pt` model with a specialized license plate detection model trained on car dashboard and vehicle datasets. A fallback to basic edge detection is available if YOLOv8 is unavailable.