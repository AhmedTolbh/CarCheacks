"""
Enhanced Real-Time Multi-Agent AI System Dashboard
Integrated Dashboard with Video Upload and Workflow Visualization

This module provides:
- Video upload capability for real-time analysis
- Live video processing display
- Agent workflow visualization (swarm-like communication)
- Real-time analytics and monitoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import time
import cv2
import tempfile
import numpy as np

# Import agents from main_old.py
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_old import VisionOCRAgent, AccessControlAgent
except ImportError:
    st.error("Error: Could not import agents from main_old.py")
    VisionOCRAgent = None
    AccessControlAgent = None


class EnhancedDashboard:
    """
    Enhanced Dashboard with integrated video upload and agent workflow visualization
    """
    
    def __init__(self):
        self.log_file = "access_log.csv"
        self.agent_logs = []
        self.max_agent_logs = 20
        
    def log_agent_activity(self, agent_name, action, details=""):
        """Log agent activity for workflow visualization"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.agent_logs.append({
            "timestamp": timestamp,
            "agent": agent_name,
            "action": action,
            "details": details
        })
        # Keep only recent logs
        if len(self.agent_logs) > self.max_agent_logs:
            self.agent_logs.pop(0)
    
    def load_analytics_data(self):
        """Load access log data for analytics"""
        if os.path.exists(self.log_file):
            try:
                df = pd.read_csv(self.log_file)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
            except Exception as e:
                st.error(f"Error loading data: {e}")
                return pd.DataFrame(columns=['timestamp', 'plate_number', 'status'])
        else:
            return pd.DataFrame(columns=['timestamp', 'plate_number', 'status'])
    
    def calculate_kpis(self, df):
        """Calculate Key Performance Indicators"""
        if df.empty:
            return {
                'total_entries': 0,
                'total_allowed': 0,
                'total_denied': 0,
                'allow_rate': 0.0
            }
        
        total_entries = len(df)
        total_allowed = len(df[df['status'] == 'ALLOW'])
        total_denied = len(df[df['status'] == 'DENY'])
        allow_rate = (total_allowed / total_entries * 100) if total_entries > 0 else 0
        
        return {
            'total_entries': total_entries,
            'total_allowed': total_allowed,
            'total_denied': total_denied,
            'allow_rate': allow_rate
        }
    
    def create_workflow_diagram(self):
        """Create interactive agent workflow visualization"""
        fig = go.Figure()
        
        # Define agent positions
        agents = {
            "Video Input": {"x": 0, "y": 2, "color": "#636EFA"},
            "Agent 1\nVision & OCR": {"x": 1, "y": 2, "color": "#EF553B"},
            "Agent 2\nAccess Control": {"x": 2, "y": 2, "color": "#00CC96"},
            "Agent 3\nAnalytics": {"x": 3, "y": 2, "color": "#AB63FA"}
        }
        
        # Add nodes
        for name, props in agents.items():
            fig.add_trace(go.Scatter(
                x=[props["x"]],
                y=[props["y"]],
                mode='markers+text',
                marker=dict(size=80, color=props["color"], line=dict(width=2, color='white')),
                text=[name],
                textposition="middle center",
                textfont=dict(size=10, color='white', family='Arial Black'),
                hovertemplate=f'<b>{name}</b><extra></extra>',
                showlegend=False
            ))
        
        # Add arrows/edges
        edges = [
            {"from": "Video Input", "to": "Agent 1\nVision & OCR", "label": "Frames"},
            {"from": "Agent 1\nVision & OCR", "to": "Agent 2\nAccess Control", "label": "Plate #"},
            {"from": "Agent 2\nAccess Control", "to": "Agent 3\nAnalytics", "label": "Logs"}
        ]
        
        for edge in edges:
            from_pos = agents[edge["from"]]
            to_pos = agents[edge["to"]]
            
            fig.add_trace(go.Scatter(
                x=[from_pos["x"], to_pos["x"]],
                y=[from_pos["y"], to_pos["y"]],
                mode='lines',
                line=dict(width=2, color='rgba(150,150,150,0.5)'),
                hovertemplate=f'<b>{edge["label"]}</b><extra></extra>',
                showlegend=False
            ))
            
            # Add arrow annotation
            fig.add_annotation(
                x=to_pos["x"],
                y=to_pos["y"],
                ax=from_pos["x"],
                ay=from_pos["y"],
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='rgba(150,150,150,0.5)',
            )
        
        fig.update_layout(
            title="Multi-Agent Workflow (Swarm Communication)",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[1, 3]),
            plot_bgcolor='rgba(0,0,0,0.05)',
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig


def process_video_file(video_path, vision_agent, access_agent, progress_placeholder, 
                       frame_placeholder, log_placeholder, dashboard):
    """Process uploaded video file with agents"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        st.error("Error: Could not open video file!")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    frame_count = 0
    processed_plates = {}
    
    dashboard.log_agent_activity("System", "Started", "Video processing initiated")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_count += 1
        
        # Update progress
        progress = (frame_count / total_frames) * 100
        progress_placeholder.progress(progress / 100, text=f"Processing: {frame_count}/{total_frames} frames ({progress:.1f}%)")
        
        # Process every 10th frame to reduce load
        if frame_count % 10 != 0:
            continue
        
        dashboard.log_agent_activity("Agent 1", "Processing", f"Analyzing frame {frame_count}")
        
        # Agent 1: Vision & OCR
        result = vision_agent.process_frame(frame.copy())
        
        if result:
            plate_number = result['plate_number']
            annotated_frame = result['frame']
            
            # Check if we've recently processed this plate
            current_time = datetime.now()
            
            if plate_number not in processed_plates or \
               (current_time - processed_plates[plate_number]).seconds > 5:
                
                dashboard.log_agent_activity("Agent 1", "Detected", f"Plate: {plate_number}")
                
                # Agent 2: Access Control
                dashboard.log_agent_activity("Agent 2", "Checking", f"Authorization for {plate_number}")
                decision = access_agent.process_plate(plate_number)
                
                dashboard.log_agent_activity("Agent 2", "Decision", f"{decision['decision']} - {plate_number}")
                dashboard.log_agent_activity("Agent 3", "Logging", f"Recorded access attempt")
                
                processed_plates[plate_number] = current_time
                
                # Display annotated frame
                cv2.putText(annotated_frame, f"Plate: {plate_number}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Status: {decision['decision']}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1,
                           (0, 255, 0) if decision['decision'] == "ALLOW" else (0, 0, 255), 2)
                
                # Convert BGR to RGB for display
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(rgb_frame, caption=f"Frame {frame_count} - Plate Detected: {plate_number}", use_container_width=True)
                
                # Update log display
                log_text = f"🚗 **{plate_number}** - {decision['decision']} - Frame {frame_count}\n"
                log_placeholder.markdown(log_text)
                
                time.sleep(0.5)  # Brief pause to show result
        
        # Limit display rate
        if frame_count % 30 == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(rgb_frame, caption=f"Processing frame {frame_count}...", use_container_width=True)
    
    cap.release()
    dashboard.log_agent_activity("System", "Completed", "Video processing finished")
    progress_placeholder.success(f"✅ Processing complete! Analyzed {frame_count} frames.")


def main():
    """Main dashboard application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Vehicle Access Control - Enhanced Dashboard",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
        }
        .agent-log {
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("🚗 Vehicle Access Control System")
    st.markdown("### Multi-Agent AI Dashboard with Real-Time Video Analysis")
    st.markdown("---")
    
    # Initialize dashboard
    dashboard = EnhancedDashboard()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📹 Video Upload & Analysis", "📊 Analytics Dashboard", "🔄 Agent Workflow"])
    
    # TAB 1: Video Upload and Processing
    with tab1:
        st.header("Video Upload & Real-Time Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Upload Video for Analysis")
            uploaded_file = st.file_uploader(
                "Choose a video file (MP4, AVI, MOV)",
                type=['mp4', 'avi', 'mov', 'mkv'],
                help="Upload a video containing vehicles with visible license plates"
            )
            
            if uploaded_file is not None:
                # Save uploaded file temporarily
                video_path = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        video_path = tmp_file.name
                    
                    st.success(f"✅ Video uploaded: {uploaded_file.name}")
                    
                    # Show video info
                    cap = cv2.VideoCapture(video_path)
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = frame_count / fps if fps > 0 else 0
                    cap.release()
                    
                    st.info(f"📹 Video Info: {frame_count} frames, {fps} FPS, ~{duration:.1f} seconds")
                    
                    # Process button
                    if st.button("🚀 Start Processing", type="primary"):
                        st.markdown("---")
                        st.subheader("Processing Video...")
                        
                        # Initialize agents
                        with st.spinner("Initializing AI agents..."):
                            if VisionOCRAgent and AccessControlAgent:
                                vision_agent = VisionOCRAgent(use_yolo=False)  # Use edge detection for demo
                                access_agent = AccessControlAgent()
                                st.success("✅ Agents initialized successfully!")
                            else:
                                st.error("Error: Could not initialize agents")
                                st.stop()
                        
                        # Create placeholders for dynamic updates
                        progress_placeholder = st.empty()
                        frame_placeholder = st.empty()
                        log_placeholder = st.empty()
                        
                        # Process video
                        try:
                            process_video_file(
                                video_path, 
                                vision_agent, 
                                access_agent,
                                progress_placeholder,
                                frame_placeholder,
                                log_placeholder,
                                dashboard
                            )
                        except Exception as e:
                            st.error(f"Error processing video: {e}")
                finally:
                    # Cleanup temp file
                    if video_path and os.path.exists(video_path):
                        try:
                            os.remove(video_path)
                        except Exception:
                            pass  # Ignore errors during cleanup
        
        with col2:
            st.subheader("Agent Activity Log")
            
            # Display agent logs
            if dashboard.agent_logs:
                log_html = '<div class="agent-log">'
                for log in reversed(dashboard.agent_logs):
                    color = "#00CC96" if log['agent'] == "Agent 1" else \
                           "#EF553B" if log['agent'] == "Agent 2" else \
                           "#AB63FA" if log['agent'] == "Agent 3" else "#636EFA"
                    log_html += f'<div style="margin-bottom: 8px;">'
                    log_html += f'<span style="color: gray;">[{log["timestamp"]}]</span> '
                    log_html += f'<span style="color: {color}; font-weight: bold;">{log["agent"]}</span>: '
                    log_html += f'{log["action"]}'
                    if log["details"]:
                        log_html += f' - <i>{log["details"]}</i>'
                    log_html += '</div>'
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
            else:
                st.info("No agent activity yet. Upload and process a video to see agent communication.")
    
    # TAB 2: Analytics Dashboard
    with tab2:
        st.header("Real-Time Analytics Dashboard")
        
        # Load analytics data
        df = dashboard.load_analytics_data()
        
        if df.empty:
            st.warning("⚠️ No access log data available yet. Process a video to generate analytics.")
        else:
            # Calculate KPIs
            kpis = dashboard.calculate_kpis(df)
            
            # Display KPIs
            st.subheader("📊 Key Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Entries", kpis['total_entries'])
            
            with col2:
                st.metric("Total Allowed", kpis['total_allowed'])
            
            with col3:
                st.metric("Total Denied", kpis['total_denied'])
            
            with col4:
                st.metric("Allow Rate", f"{kpis['allow_rate']:.1f}%")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Permission Status Distribution")
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['status', 'count']
                
                fig_pie = px.pie(
                    status_counts,
                    values='count',
                    names='status',
                    title='ALLOW vs DENY Distribution',
                    color='status',
                    color_discrete_map={'ALLOW': '#00CC96', 'DENY': '#EF553B'},
                    hole=0.3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("📊 Top 10 Vehicles")
                vehicle_counts = df['plate_number'].value_counts().head(10).reset_index()
                vehicle_counts.columns = ['plate_number', 'count']
                
                fig_bar = px.bar(
                    vehicle_counts,
                    x='plate_number',
                    y='count',
                    title='Most Frequent Vehicles',
                    labels={'plate_number': 'License Plate', 'count': 'Attempts'},
                    color='count',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_xaxis(tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("---")
            
            # Live Log Table
            st.subheader("📋 Live Access Log")
            
            # Sort by timestamp (newest first)
            display_df = df.sort_values('timestamp', ascending=False)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn(
                        "Timestamp",
                        format="YYYY-MM-DD HH:mm:ss"
                    ),
                    "plate_number": "License Plate",
                    "status": "Status"
                }
            )
    
    # TAB 3: Agent Workflow Visualization
    with tab3:
        st.header("Agent Workflow & Communication")
        
        st.subheader("Multi-Agent System Architecture")
        st.markdown("""
        This system uses a **swarm intelligence** approach where three specialized agents work together:
        
        - **Agent 1 (Vision & OCR)**: Processes video frames, detects license plates, extracts text
        - **Agent 2 (Access Control)**: Checks authorization, makes decisions, triggers actions
        - **Agent 3 (Analytics)**: Processes logs, generates insights, visualizes data
        
        The agents communicate through data pipelines, creating an efficient distributed processing system.
        """)
        
        # Display workflow diagram
        fig_workflow = dashboard.create_workflow_diagram()
        st.plotly_chart(fig_workflow, use_container_width=True)
        
        st.markdown("---")
        
        # Agent Details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🔍 Agent 1: Vision & OCR
            **Capabilities:**
            - Frame capture & preprocessing
            - License plate detection
            - OCR text extraction
            - Text cleaning & validation
            
            **Technologies:**
            - OpenCV
            - EasyOCR
            - YOLOv8 (optional)
            """)
        
        with col2:
            st.markdown("""
            #### 🚦 Agent 2: Access Control
            **Capabilities:**
            - Whitelist management
            - Authorization decisions
            - Gate/alarm control
            - Access logging
            
            **Technologies:**
            - CSV-based whitelist
            - Real-time decision engine
            - Event logging system
            """)
        
        with col3:
            st.markdown("""
            #### 📊 Agent 3: Analytics
            **Capabilities:**
            - Real-time data ingestion
            - KPI calculations
            - Interactive visualizations
            - Pattern detection
            
            **Technologies:**
            - Pandas
            - Plotly
            - Streamlit
            """)
        
        st.markdown("---")
        
        # Recent Activity Timeline
        st.subheader("Recent Agent Communication Timeline")
        
        if dashboard.agent_logs:
            # Create timeline visualization
            timeline_data = []
            for idx, log in enumerate(dashboard.agent_logs):
                timeline_data.append({
                    'Time': log['timestamp'],
                    'Agent': log['agent'],
                    'Activity': f"{log['action']} - {log['details']}"
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df, use_container_width=True, hide_index=True)
        else:
            st.info("Process a video to see agent communication timeline")
    
    # Sidebar
    st.sidebar.header("System Information")
    st.sidebar.markdown(f"**Status:** 🟢 Online")
    st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Load data for sidebar stats
    df = dashboard.load_analytics_data()
    st.sidebar.markdown(f"**Total Records:** {len(df)}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Actions")
    
    if st.sidebar.button("🔄 Refresh Dashboard"):
        st.rerun()
    
    if st.sidebar.button("🗑️ Clear Logs"):
        if os.path.exists("access_log.csv"):
            # Backup before clearing
            backup_name = f"access_log_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            os.rename("access_log.csv", backup_name)
            st.sidebar.success(f"Logs backed up to {backup_name}")
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info("""
    **Vehicle Access Control System**
    
    Multi-Agent AI system for intelligent vehicle access control using computer vision and machine learning.
    
    Built for Hackathon demonstration.
    """)


if __name__ == "__main__":
    main()
