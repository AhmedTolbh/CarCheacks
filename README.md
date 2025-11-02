# automatic-number-plate-recognition-python-yolov8

Automatic Number Plate Recognition (ANPR) system using Python, YOLOv8, and EasyOCR.

This implementation is based on the [automatic-number-plate-recognition-python-yolov8](https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8) project.

## Overview

This system detects and recognizes license plates from video files using:
- **YOLOv8** for vehicle detection
- **SORT** tracker for multi-object tracking
- **YOLOv8** (custom trained) for license plate detection
- **EasyOCR** for text recognition

## Data

Sample videos for testing can be downloaded from:
- [Traffic flow in the highway](https://www.pexels.com/video/traffic-flow-in-the-highway-2103099/)

## Models

### Vehicle Detection
Uses a YOLOv8 pretrained model (`yolov8n.pt`) to detect vehicles in the COCO dataset classes:
- Class 2: Car
- Class 3: Motorcycle
- Class 5: Bus
- Class 7: Truck

### License Plate Detection
A custom YOLOv8 model trained on license plate data. The model should be placed in `./models/license_plate_detector.pt`.

You can train your own model using [this license plate dataset](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/dataset/4) and following this [step-by-step YOLOv8 training guide](https://github.com/computervisioneng/train-yolov8-custom-dataset-step-by-step-guide).

## Dependencies

### SORT Tracker
The SORT (Simple Online and Realtime Tracking) module needs to be downloaded from the [official repository](https://github.com/abewley/sort):

```bash
git clone https://github.com/abewley/sort.git
```

### Python Packages
Install required packages:

```bash
pip install -r requirements.txt
```

Required packages:
- ultralytics==8.0.114
- pandas==2.0.2
- opencv-python==4.7.0.72
- numpy==1.24.3
- scipy==1.10.1
- easyocr==1.7.0
- filterpy==1.4.5

## Project Structure

```
CarCheacks/
├── main.py                     # Main detection and tracking script
├── util.py                     # Utility functions (OCR, validation, CSV writing)
├── visualize.py                # Visualization script (renders output video)
├── add_missing_data.py         # Interpolation script for missing frames
├── requirements.txt            # Python dependencies
├── sort/                       # SORT tracker (cloned from GitHub)
├── models/
│   └── license_plate_detector.pt  # Custom trained license plate detector
├── sample.mp4                  # Input video file
├── test.csv                    # Detection results (generated)
├── test_interpolated.csv       # Interpolated results (generated)
└── out.mp4                     # Output annotated video (generated)
```

## Usage

### 1. Prepare Your Setup

1. Clone this repository
2. Clone the SORT tracker:
   ```bash
   git clone https://github.com/abewley/sort.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place your trained license plate detector model at `./models/license_plate_detector.pt`
5. Place your input video at `./sample.mp4`

### 2. Run Detection and Tracking

```bash
python main.py
```

This will:
- Process the video frame by frame
- Detect vehicles using YOLOv8
- Track vehicles using SORT
- Detect license plates on tracked vehicles
- Read license plate text using EasyOCR
- Save results to `test.csv`

### 3. Interpolate Missing Data

```bash
python add_missing_data.py
```

This script fills in gaps in the tracking data by interpolating bounding boxes for frames where detection was missed. Output is saved to `test_interpolated.csv`.

### 4. Generate Annotated Video

```bash
python visualize.py
```

This creates an output video (`out.mp4`) with:
- Green bordered boxes around detected vehicles
- Red boxes around license plates
- License plate text displayed above each vehicle

## How It Works

### main.py

The main detection pipeline:

1. **Load Models**
   - YOLOv8n for vehicle detection
   - Custom YOLOv8 model for license plate detection

2. **Process Video**
   - For each frame:
     - Detect vehicles (cars, trucks, buses, motorcycles)
     - Track vehicles using SORT
     - Detect license plates on each vehicle
     - Crop and preprocess license plate regions
     - Apply OCR to extract text
     - Validate and format license plate text
     - Store results with frame number and vehicle ID

3. **Save Results**
   - Write detections to CSV with:
     - Frame number
     - Vehicle ID
     - Vehicle bounding box
     - License plate bounding box
     - License plate text
     - Confidence scores

### util.py

Utility functions:

- **read_license_plate()**: Uses EasyOCR to extract text from license plate images
- **license_complies_format()**: Validates license plate format (7 characters: 2 letters, 2 digits, 3 letters)
- **format_license()**: Corrects common OCR errors (e.g., 'O' → '0', 'I' → '1')
- **get_car()**: Associates detected license plates with tracked vehicles
- **write_csv()**: Saves results to CSV format

### add_missing_data.py

Interpolation script:

- Identifies gaps in vehicle tracking
- Uses linear interpolation to estimate bounding boxes for missing frames
- Ensures smooth tracking across the entire video
- Preserves original detection data while filling gaps

### visualize.py

Visualization script:

- Reads interpolated CSV data
- Draws bounding boxes and annotations on video frames
- Displays license plate text above each vehicle
- Creates professional-looking output video

## Output Files

### test.csv
Raw detection results with columns:
- `frame_nmr`: Frame number
- `car_id`: Unique vehicle tracking ID
- `car_bbox`: Vehicle bounding box [x1, y1, x2, y2]
- `license_plate_bbox`: License plate bounding box [x1, y1, x2, y2]
- `license_plate_bbox_score`: Detection confidence
- `license_number`: Detected text
- `license_number_score`: OCR confidence

### test_interpolated.csv
Same format as test.csv but with interpolated data for missing frames (indicated by score values of '0').

### out.mp4
Annotated video showing:
- Vehicle tracking with green corner markers
- License plate detection with red boxes
- License plate text overlaid above vehicles

## License Plate Format

This implementation expects license plates in the format:
```
AA00AAA
```
Where:
- A = Letter (A-Z)
- 0 = Digit (0-9)

The format can be customized in `util.py` by modifying the `license_complies_format()` function.

## Tips for Better Results

1. **Video Quality**: Higher resolution videos produce better results
2. **Lighting**: Good lighting conditions improve detection and OCR accuracy
3. **Camera Angle**: Front-facing or rear-facing views work best
4. **Model Training**: Train the license plate detector on your specific region's plate formats
5. **OCR Tuning**: Adjust character mapping in `util.py` based on your plate format

## Troubleshooting

### Model Not Found Error
Ensure the license plate detector model is at `./models/license_plate_detector.pt`

### SORT Import Error
Make sure the SORT repository is cloned in the project directory:
```bash
git clone https://github.com/abewley/sort.git
```

### Low Detection Accuracy
- Check video quality
- Verify model is trained on similar license plate formats
- Adjust confidence thresholds in main.py
- Improve lighting conditions in source video

### Memory Issues
For long videos, process in batches or reduce resolution

## Legacy Multi-Agent System

This repository previously contained a multi-agent AI system for vehicle access control. Those files have been preserved with `_old` suffixes:
- `main_old.py` - Original multi-agent system
- `README_old.md` - Original documentation
- Other dashboard and demo files remain available

## Credits

This implementation is based on the work by Computer Vision Engineer:
- [Original Repository](https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8)
- [YouTube Tutorial](https://www.youtube.com/watch?v=fyJB1t0o0ms)

SORT tracker by Alex Bewley:
- [SORT Repository](https://github.com/abewley/sort)

## License

This project is open source and available under the MIT License.
