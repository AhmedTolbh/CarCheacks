# Migration Guide: Multi-Agent System to Reference ANPR

This document explains the changes made to restructure the CarCheacks repository to match the reference automatic-number-plate-recognition-python-yolov8 implementation.

## What Changed?

### Old System (Multi-Agent AI)
The previous system was a complex multi-agent AI system for vehicle access control with:
- Real-time webcam/IP camera support
- Access control logic (allow/deny based on whitelist)
- Interactive Streamlit dashboards
- Multiple agents (Vision, Access Control, Analytics)
- Demo video generation
- Extensive logging and analytics

### New System (Reference ANPR)
The new system is a focused ANPR implementation that:
- Processes video files (not real-time streams)
- Uses YOLOv8 + SORT for vehicle tracking
- Uses a specialized license plate detector
- Outputs results to CSV files
- Provides visualization tools
- Follows the reference implementation structure

## File Changes

### New Files
| File | Purpose |
|------|---------|
| `util.py` | OCR utilities, license plate validation, CSV writing |
| `visualize.py` | Creates annotated output videos from CSV data |
| `add_missing_data.py` | Interpolates missing tracking data |
| `verify_setup.py` | Verification script to check setup |
| `models/README.md` | Instructions for obtaining license plate detector model |
| `QUICKSTART.md` | New quick start guide for ANPR system |

### Modified Files
| File | Changes |
|------|---------|
| `main.py` | Completely rewritten to follow reference implementation |
| `README.md` | Updated to document ANPR system instead of multi-agent system |
| `requirements.txt` | Added scipy and filterpy for SORT tracker |
| `.gitignore` | Added patterns for ANPR output files |

### Preserved Files (with _old suffix)
| Original File | Backup File | Purpose |
|---------------|-------------|---------|
| `main.py` | `main_old.py` | Original multi-agent system |
| `README.md` | `README_old.md` | Original documentation |
| `QUICKSTART.md` | `QUICKSTART_old.md` | Original quick start |

### Unchanged Files (Legacy System)
These files from the old multi-agent system are still available:
- `dashboard.py` - Original analytics dashboard
- `dashboard_enhanced.py` - Enhanced dashboard with video upload
- `create_demo_video.py` - Demo video generator
- `generate_demo_data.py` - Demo data generator
- `test_system.py` - System tests
- `test_enhanced_dashboard.py` - Dashboard tests
- `validate_system.py` - System validation
- All documentation files (DEMO_GUIDE.md, ENHANCED_DASHBOARD_GUIDE.md, etc.)

## Workflow Comparison

### Old Workflow (Multi-Agent)
```bash
# Terminal 1: Start main application
python main.py
# Choose video source (webcam, IP camera, or file)
# System runs continuously, making access control decisions

# Terminal 2: Start dashboard
streamlit run dashboard_enhanced.py
# View real-time analytics
```

### New Workflow (Reference ANPR)
```bash
# Step 1: Process video
python main.py
# Outputs: test.csv

# Step 2: Interpolate data
python add_missing_data.py
# Outputs: test_interpolated.csv

# Step 3: Create visualization
python visualize.py
# Outputs: out.mp4
```

## Feature Comparison

| Feature | Old System | New System |
|---------|------------|------------|
| **Input** | Webcam, IP camera, video file | Video file only |
| **Vehicle Detection** | YOLOv8 (general) or edge detection | YOLOv8 (COCO classes) |
| **License Plate Detection** | Edge detection or general YOLOv8 | Custom trained YOLOv8 |
| **Vehicle Tracking** | None (per-frame detection) | SORT tracker |
| **OCR** | EasyOCR | EasyOCR |
| **Plate Format Validation** | Basic cleaning | Strict format checking (AA00AAA) |
| **Access Control** | Yes (whitelist-based) | No (detection only) |
| **Real-time Processing** | Yes | No (batch processing) |
| **Output** | access_log.csv, console output | test.csv, test_interpolated.csv, out.mp4 |
| **Visualization** | Live video display | Post-processing video generation |
| **Dashboard** | Streamlit web interface | None (CSV output only) |
| **Analytics** | Real-time KPIs and charts | Manual analysis of CSV data |

## Dependencies Comparison

### New Dependencies
- `scipy>=1.10.1` - For interpolation in add_missing_data.py
- `filterpy>=1.4.5` - Required by SORT tracker
- SORT tracker (git clone from external repo)

### Kept Dependencies
All existing dependencies are preserved for backward compatibility with legacy dashboard features.

## Migration Steps

### If You Want to Use the New ANPR System

1. **Clone SORT tracker:**
   ```bash
   git clone https://github.com/abewley/sort.git
   ```

2. **Get license plate detector model:**
   - Train your own or obtain a pre-trained model
   - Place at `./models/license_plate_detector.pt`

3. **Prepare input video:**
   - Place video as `sample.mp4`

4. **Run the workflow:**
   ```bash
   python main.py
   python add_missing_data.py
   python visualize.py
   ```

See `QUICKSTART.md` for detailed instructions.

### If You Want to Continue Using the Old Multi-Agent System

1. **Use the old main file:**
   ```bash
   python main_old.py
   ```

2. **Reference old documentation:**
   - See `README_old.md` for full documentation
   - See `QUICKSTART_old.md` for quick start guide

3. **All dashboard files still work:**
   ```bash
   streamlit run dashboard_enhanced.py
   ```

## Key Technical Differences

### License Plate Detection

**Old System:**
- Used edge detection (Canny + contours)
- Or general YOLOv8n (not specialized for plates)
- Lower accuracy but no model training required

**New System:**
- Uses custom trained YOLOv8 model
- Specialized for license plate detection
- Higher accuracy but requires obtaining/training model

### Vehicle Tracking

**Old System:**
- No tracking (each frame processed independently)
- Could detect same vehicle multiple times
- No continuous ID assignment

**New System:**
- SORT tracker maintains vehicle IDs across frames
- Associates license plates with tracked vehicles
- Enables interpolation of missing data

### Output Format

**Old System (access_log.csv):**
```csv
timestamp,plate_number,decision
2024-01-01 10:30:00,ABC123,ALLOW
```

**New System (test.csv):**
```csv
frame_nmr,car_id,car_bbox,license_plate_bbox,license_plate_bbox_score,license_number,license_number_score
0,1.0,[100 200 300 400],[150 250 200 280],0.95,AB12CDE,0.89
```

### Processing Model

**Old System:**
- Real-time, continuous processing
- Immediate decisions
- Stream-oriented

**New System:**
- Batch processing
- Post-processing analysis
- File-oriented

## When to Use Which System?

### Use New ANPR System When:
- Processing pre-recorded videos
- Need accurate vehicle tracking
- Want professional visualizations
- Analyzing traffic patterns
- Need to track specific vehicles across frames
- Have or can obtain a trained license plate detector

### Use Old Multi-Agent System When:
- Need real-time access control
- Working with live camera feeds
- Want interactive dashboards
- Need allow/deny decisions
- Working with webcams or IP cameras
- Don't have a specialized plate detector model

## Getting Help

- **New ANPR System:** See `README.md` and `QUICKSTART.md`
- **Old Multi-Agent System:** See `README_old.md` and `QUICKSTART_old.md`
- **General Questions:** Open an issue on GitHub
- **Original Reference:** https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8

## Credits

The new ANPR implementation is based on:
- [automatic-number-plate-recognition-python-yolov8](https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8) by Computer Vision Engineer
- [SORT tracker](https://github.com/abewley/sort) by Alex Bewley

The old multi-agent system remains available for those who need its features.
