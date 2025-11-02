# Quick Start Guide - Dashboard Video Upload

## 30-Second Start 🚀

```bash
pip install -r requirements.txt
streamlit run dashboard_enhanced.py
```

Open `http://localhost:8501` and upload a video!

## What You Get

### One Dashboard, Three Tabs, All Features

**Tab 1: Video Upload & Analysis** 📹
- Upload videos (drag & drop)
- Watch real-time processing
- See license plates detected
- View access decisions (ALLOW/DENY)

**Tab 2: Analytics** 📊
- KPI metrics
- Interactive charts
- Access logs
- Export to CSV

**Tab 3: Workflow** 🔄
- Agent communication diagram
- System architecture
- Activity timeline

## How It Works

1. **Upload** a video file
2. **Agent 1** detects license plates
3. **Agent 2** checks authorization
4. **Agent 3** analyzes and visualizes
5. **You** see everything in real-time!

## Demo Video

Don't have a video? Create one:

```bash
python create_demo_video.py 10
```

This creates a 10-second demo video with license plates.

## Authorized Plates

Edit `authorized_plates.csv` to add authorized vehicles:

```csv
plate_number,owner_name,vehicle_type
ABC123,John Doe,Car
XYZ789,Jane Smith,Truck
```

## System Requirements

- Python 3.8+
- 4GB RAM (8GB recommended)
- Modern web browser
- Video file or camera

## Troubleshooting

**Dashboard won't start?**
→ Install dependencies: `pip install -r requirements.txt`

**Video won't upload?**
→ Check format (MP4, AVI, MOV, MKV)

**No plates detected?**
→ Use demo video: `python create_demo_video.py 10`

**Slow processing?**
→ Normal - processes every 10th frame for speed

## Full Documentation

- **Complete Guide**: See `DASHBOARD_VIDEO_UPLOAD_GUIDE.md`
- **Demo Script**: See `DEMO_SCRIPT.md`
- **Technical Details**: See `IMPLEMENTATION_COMPLETE.md`

## Features

✅ Video upload through web interface  
✅ Real-time license plate detection  
✅ OCR text extraction  
✅ Access control decisions  
✅ Multi-agent architecture  
✅ Live analytics and KPIs  
✅ Interactive visualizations  
✅ Agent communication timeline  
✅ CSV export  
✅ Search and filter logs  

## Architecture

```
Video → Agent 1 (Vision/OCR) → Agent 2 (Access) → Agent 3 (Analytics) → Dashboard
```

Three specialized agents work together in a swarm intelligence pattern.

## Support

For detailed help, see:
- `DASHBOARD_VIDEO_UPLOAD_GUIDE.md` - Complete user guide
- `DEMO_SCRIPT.md` - Presentation guide
- `README.md` - Full project documentation

## That's It! 🎉

You're ready to use the dashboard. Upload a video and watch the magic happen!

---

**Need Help?** Check the full documentation in `DASHBOARD_VIDEO_UPLOAD_GUIDE.md`
