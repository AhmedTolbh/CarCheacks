# Enhanced Dashboard - Quick Start Guide

## 🚀 New Feature: Integrated Video Upload Dashboard

The enhanced dashboard (`dashboard_enhanced.py`) provides a complete web-based interface for the Vehicle Access Control System with the following features:

### Features

1. **📹 Video Upload & Real-Time Analysis**
   - Upload videos directly through the web interface
   - Real-time processing with visual feedback
   - Live frame display with license plate detection
   - Processing progress tracking

2. **🔄 Agent Workflow Visualization**
   - Interactive diagram showing agent communication (swarm-like)
   - Real-time activity logs showing agent interactions
   - Timeline view of agent communications
   - Complete system architecture visualization

3. **📊 Analytics Dashboard**
   - All existing analytics features
   - KPIs (Total entries, allowed, denied, allow rate)
   - Interactive charts and visualizations
   - Live access log table

## Quick Start

### Option 1: Enhanced Dashboard (Recommended for Hackathon Demo)

Run the enhanced dashboard with integrated video upload:

```bash
streamlit run dashboard_enhanced.py
```

Then open your browser to `http://localhost:8501` and:
1. Go to the "📹 Video Upload & Analysis" tab
2. Upload a video file (MP4, AVI, MOV)
3. Click "🚀 Start Processing"
4. Watch the agents work together in real-time!

### Option 2: Traditional Two-Terminal Setup

**Terminal 1:** Run the main application
```bash
python main.py
```

**Terminal 2:** Run the analytics dashboard
```bash
streamlit run dashboard.py
```

## Creating Demo Videos

To create a demo video for testing:

```bash
python create_demo_video.py 10
```

This creates a 10-second demo video with simulated license plates.

## Agent Workflow

The enhanced dashboard shows how the three agents communicate:

```
Video Input → Agent 1 (Vision/OCR) → Agent 2 (Access Control) → Agent 3 (Analytics)
     │              │                         │                        │
     │              ├─ Frame processing      ├─ Authorization         ├─ KPI calculation
     │              ├─ Plate detection       ├─ Decision making       ├─ Visualizations
     │              └─ OCR extraction        └─ Logging               └─ Real-time updates
```

## Hackathon Demo Tips

1. **Start with Enhanced Dashboard**: Use `streamlit run dashboard_enhanced.py` for the best demo experience
2. **Prepare Demo Video**: Create or use a demo video with visible license plates
3. **Show Workflow Tab**: Demonstrate the agent communication visualization
4. **Explain Swarm Intelligence**: Show how agents work together autonomously
5. **Display Real-Time Processing**: Upload video and show live frame analysis

## System Requirements

- Python 3.8+
- Webcam or video file
- All dependencies from requirements.txt

## Troubleshooting

**Issue**: Video processing is slow
- **Solution**: The system processes every 10th frame to reduce load. This is configurable in the code.

**Issue**: No plates detected
- **Solution**: Ensure your video has clear, visible license plates. Use the demo video generator for testing.

**Issue**: Dashboard not updating
- **Solution**: Check that the agents are initialized correctly and the video file is valid.

## What Makes This Special

- **Integrated Interface**: Everything in one dashboard - no need for multiple terminals
- **Visual Workflow**: See how agents communicate and work together
- **Real-Time Processing**: Upload video and see immediate results
- **Hackathon Ready**: Perfect for demonstrations with clear visualizations

For more details, see the main [README.md](README.md).
