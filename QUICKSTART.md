# Quick Start Guide - ANPR System

This guide will help you get started with the Automatic Number Plate Recognition system.

## Prerequisites

1. Python 3.8 or higher
2. A video file with vehicles (e.g., traffic footage)
3. A trained YOLOv8 license plate detector model

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/AhmedTolbh/CarCheacks.git
cd CarCheacks
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download SORT Tracker
```bash
git clone https://github.com/abewley/sort.git
```

### Step 4: Prepare Models

#### Download YOLOv8 Models
The general YOLOv8 model (yolov8n.pt) will be downloaded automatically on first run.

#### Get License Plate Detector
You need a trained license plate detector model. Options:

1. **Download a pre-trained model** (if available from the original project)
2. **Train your own** using [this guide](https://github.com/computervisioneng/train-yolov8-custom-dataset-step-by-step-guide) and [this dataset](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/dataset/4)

Place the model at: `./models/license_plate_detector.pt`

### Step 5: Prepare Video
Place your input video as `sample.mp4` in the project directory.

You can download sample traffic videos from:
- [Pexels - Traffic Flow](https://www.pexels.com/video/traffic-flow-in-the-highway-2103099/)

## Usage Workflow

### Complete Pipeline

```bash
# 1. Run detection and tracking
python main.py

# 2. Interpolate missing data
python add_missing_data.py

# 3. Generate annotated video
python visualize.py
```

After these steps, you'll have:
- `test.csv` - Raw detection results
- `test_interpolated.csv` - Interpolated tracking data
- `out.mp4` - Annotated output video

### What Each Script Does

#### 1. main.py
**Purpose**: Detect vehicles and license plates, read text

**Input**: 
- `sample.mp4` (video file)
- `yolov8n.pt` (vehicle detector - auto-downloaded)
- `./models/license_plate_detector.pt` (license plate detector)

**Output**: 
- `test.csv` (detection results)

**What it does**:
- Detects vehicles (cars, trucks, buses, motorcycles)
- Tracks each vehicle with a unique ID
- Detects license plates on each vehicle
- Reads license plate text using OCR
- Validates and formats the text
- Saves all detections to CSV

#### 2. add_missing_data.py
**Purpose**: Fill gaps in tracking data

**Input**: 
- `test.csv`

**Output**: 
- `test_interpolated.csv`

**What it does**:
- Identifies frames where a vehicle was tracked but license plate wasn't detected
- Uses linear interpolation to estimate bounding boxes for missing frames
- Creates a complete tracking dataset for smooth visualization

#### 3. visualize.py
**Purpose**: Create annotated output video

**Input**: 
- `sample.mp4` (original video)
- `test_interpolated.csv` (interpolated data)

**Output**: 
- `out.mp4` (annotated video)

**What it does**:
- Draws green corner markers around tracked vehicles
- Draws red boxes around license plates
- Displays license plate text above each vehicle
- Shows the license plate crop in high resolution

## Understanding the Output

### test.csv Format
```csv
frame_nmr,car_id,car_bbox,license_plate_bbox,license_plate_bbox_score,license_number,license_number_score
0,1.0,[100 200 300 400],[150 250 200 280],0.95,AB12CDE,0.89
```

Columns:
- `frame_nmr`: Video frame number (0-indexed)
- `car_id`: Unique vehicle tracking ID
- `car_bbox`: Vehicle position [x1, y1, x2, y2]
- `license_plate_bbox`: License plate position [x1, y1, x2, y2]
- `license_plate_bbox_score`: Confidence of plate detection (0-1)
- `license_number`: Detected text
- `license_number_score`: OCR confidence (0-1)

### Visualization Features

The output video (`out.mp4`) includes:
- **Green corner markers**: Outline of detected vehicles
- **Red rectangles**: License plate locations
- **Text overlay**: Detected license plate number
- **Plate preview**: Zoomed-in view of the license plate

## Troubleshooting

### "No module named 'sort.sort'"
**Solution**: Make sure you've cloned the SORT repository:
```bash
git clone https://github.com/abewley/sort.git
```

### "No such file or directory: './models/license_plate_detector.pt'"
**Solution**: You need to obtain a trained license plate detector model. See Step 4 above.

### "No such file or directory: './sample.mp4'"
**Solution**: Place your input video as `sample.mp4` or modify the path in `main.py`:
```python
cap = cv2.VideoCapture('./your_video_name.mp4')
```

### "No such file or directory: 'test.csv'" (in add_missing_data.py)
**Solution**: Run `main.py` first to generate the detection results.

### "No such file or directory: 'test_interpolated.csv'" (in visualize.py)
**Solution**: Run `add_missing_data.py` first to generate interpolated data.

### Low Detection Accuracy
**Tips**:
- Use higher quality video
- Ensure good lighting in the source video
- Train a custom license plate detector for your region's plate format
- Adjust detection confidence thresholds in `main.py`

### Video Processing is Slow
**Tips**:
- Use a GPU for faster processing
- Reduce video resolution
- Process only every Nth frame (modify the frame reading loop)

## Customization

### License Plate Format
Edit `util.py`, function `license_complies_format()` to match your region's format.

Current format: `AA00AAA` (2 letters, 2 digits, 3 letters)

### Vehicle Classes
Edit `main.py`, variable `vehicles`:
```python
vehicles = [2, 3, 5, 7]  # car, motorcycle, bus, truck
```

COCO class IDs:
- 2: car
- 3: motorcycle  
- 5: bus
- 7: truck

### Detection Thresholds
YOLOv8 uses default confidence thresholds. To adjust:
```python
detections = coco_model(frame, conf=0.3)[0]  # 0.3 = 30% confidence
```

## Next Steps

1. **Analyze Results**: Open `test_interpolated.csv` in Excel or pandas to analyze detection statistics
2. **Improve Accuracy**: Train a custom license plate detector on your specific plate formats
3. **Integration**: Use the CSV output for access control, parking management, or traffic analysis
4. **Extend**: Add features like database storage, real-time processing, or web interface

## Legacy Multi-Agent System

This repository previously had a multi-agent system with dashboard. Those files are still available with `_old` suffix:
- `main_old.py` - Multi-agent access control system
- `dashboard.py` / `dashboard_enhanced.py` - Analytics dashboards

See `README_old.md` for documentation on the legacy system.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the original project: [automatic-number-plate-recognition-python-yolov8](https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8)
- Watch the tutorial: [YouTube Video](https://www.youtube.com/watch?v=fyJB1t0o0ms)
