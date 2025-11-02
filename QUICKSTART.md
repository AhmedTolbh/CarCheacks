# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: This may take 5-10 minutes due to large packages (PyTorch, OpenCV, etc.)

### Step 2: Test the System (Without Camera)

Generate sample data:
```bash
python generate_demo_data.py 50
```

Start the dashboard:
```bash
streamlit run dashboard.py
```

Open your browser to `http://localhost:8501` to see the analytics!

### Step 3: Run the Full System

**Terminal 1** - Start the main application:
```bash
python main.py
```

Choose your video source:
- **Option 1**: Live stream from security camera (IP/RTSP)
  - Enter your camera's stream URL
  - Example: `rtsp://admin:password@192.168.1.100:554/stream`
- **Option 2**: Upload/load a video file
  - Enter the path to your video file
- **Option 3**: Use your webcam

**Terminal 2** - Start the dashboard:
```bash
streamlit run dashboard.py
```

## 📋 What You'll See

### Main Application (Terminal 1)
- Live video feed with detected license plates highlighted
- Real-time ALLOW/DENY decisions
- Console output showing access control actions

### Analytics Dashboard (Terminal 2)
- **KPI Cards**: Total entries, allowed, denied, allow rate
- **Pie Chart**: Visual breakdown of ALLOW vs DENY
- **Bar Chart**: Top 10 vehicles by entry frequency
- **Line Chart**: Hourly traffic patterns
- **Live Table**: Searchable, filterable access log

## 🎯 Test Cases

1. **Authorized Plate**: ABC123, XYZ789, DEF456
   - Expected: Gate opens, logged as ALLOW

2. **Unauthorized Plate**: INVALID999
   - Expected: Alarm triggered, logged as DENY

## ⚙️ Configuration

Edit `authorized_plates.csv` to add/remove authorized vehicles:
```csv
plate_number
ABC123
XYZ789
YOUR_PLATE_HERE
```

## 🐛 Troubleshooting

**Camera not found?**
- Try different indices: 0, 1, or 2 in the code
- Check camera permissions

**Dashboard shows no data?**
- Ensure `access_log.csv` exists
- Run `python generate_demo_data.py` to create sample data

**Import errors?**
- Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Learn More

See `README.md` for complete documentation.
See `IMPLEMENTATION_SUMMARY.md` for technical details.
