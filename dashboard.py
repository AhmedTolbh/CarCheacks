"""
Real-Time Multi-Agent AI System for Vehicle Access Control
Dashboard Application - Agent 3

This module implements:
- Agent 3: Data Analytics Agent (Real-time analytics and visualization)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import time


class DataAnalyticsAgent:
    """
    Agent 3: Data Analytics Agent
    
    Responsibilities:
    - Read and process access logs in real-time
    - Calculate key performance indicators (KPIs)
    - Generate visualizations (pie charts, bar charts)
    - Display live log data with search and filter capabilities
    """
    
    def __init__(self, log_file="access_log.csv"):
        """
        Initialize the Data Analytics Agent.
        
        Args:
            log_file: Path to the access log CSV file
        """
        self.log_file = log_file
    
    def load_data(self):
        """
        Load access log data from CSV file.
        
        Returns:
            DataFrame with access log data, or empty DataFrame if file doesn't exist
        """
        if os.path.exists(self.log_file):
            try:
                df = pd.read_csv(self.log_file)
                # Convert timestamp to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
            except Exception as e:
                st.error(f"Error loading data: {e}")
                return pd.DataFrame(columns=['timestamp', 'plate_number', 'status'])
        else:
            # Return empty DataFrame with proper columns
            return pd.DataFrame(columns=['timestamp', 'plate_number', 'status'])
    
    def calculate_kpis(self, df):
        """
        Calculate Key Performance Indicators from the data.
        
        Args:
            df: DataFrame with access log data
            
        Returns:
            Dictionary with KPI values
        """
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
    
    def get_status_distribution(self, df):
        """
        Get the distribution of ALLOW vs DENY status.
        
        Args:
            df: DataFrame with access log data
            
        Returns:
            DataFrame with status counts
        """
        if df.empty:
            return pd.DataFrame({'status': ['ALLOW', 'DENY'], 'count': [0, 0]})
        
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        return status_counts
    
    def get_top_vehicles(self, df, top_n=10):
        """
        Get the top N vehicles by entry attempt frequency.
        
        Args:
            df: DataFrame with access log data
            top_n: Number of top vehicles to return
            
        Returns:
            DataFrame with top vehicles
        """
        if df.empty:
            return pd.DataFrame(columns=['plate_number', 'count'])
        
        vehicle_counts = df['plate_number'].value_counts().head(top_n).reset_index()
        vehicle_counts.columns = ['plate_number', 'count']
        
        return vehicle_counts
    
    def get_hourly_traffic(self, df):
        """
        Get hourly traffic distribution.
        
        Args:
            df: DataFrame with access log data
            
        Returns:
            DataFrame with hourly counts
        """
        if df.empty:
            return pd.DataFrame(columns=['hour', 'count'])
        
        df['hour'] = df['timestamp'].dt.hour
        hourly_counts = df.groupby('hour').size().reset_index(name='count')
        
        return hourly_counts


def create_dashboard():
    """Create and display the Streamlit dashboard."""
    
    # Page configuration
    st.set_page_config(
        page_title="Vehicle Access Control Analytics",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🚗 Vehicle Access Control System - Analytics Dashboard")
    st.markdown("### Real-Time Access Control Analytics (Agent 3)")
    st.markdown("---")
    
    # Initialize Analytics Agent
    analytics_agent = DataAnalyticsAgent()
    
    # Sidebar for controls
    st.sidebar.header("Dashboard Controls")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
    
    if auto_refresh:
        refresh_interval = st.sidebar.slider(
            "Refresh interval (seconds)",
            min_value=3,  # Minimum 3 seconds to prevent excessive refreshing
            max_value=30,
            value=5,
            step=1
        )
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Load data
    df = analytics_agent.load_data()
    
    # Display last update time
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.sidebar.markdown(f"**Total Records:** {len(df)}")
    
    # Check if data exists
    if df.empty:
        st.warning("⚠️ No access log data available yet. Start the main application to begin logging access attempts.")
        st.info("💡 Run `python main.py` in another terminal to start the vehicle access control system.")
    else:
        # Calculate KPIs
        kpis = analytics_agent.calculate_kpis(df)
        
        # Display KPIs
        st.subheader("📊 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Entries",
                value=kpis['total_entries'],
                delta=None
            )
        
        with col2:
            st.metric(
                label="Total Allowed",
                value=kpis['total_allowed'],
                delta=None
            )
        
        with col3:
            st.metric(
                label="Total Denied",
                value=kpis['total_denied'],
                delta=None
            )
        
        with col4:
            st.metric(
                label="Allow Rate",
                value=f"{kpis['allow_rate']:.1f}%",
                delta=None
            )
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Permission Status Distribution")
            
            # Get status distribution
            status_dist = analytics_agent.get_status_distribution(df)
            
            # Create pie chart
            fig_pie = px.pie(
                status_dist,
                values='count',
                names='status',
                title='ALLOW vs DENY Distribution',
                color='status',
                color_discrete_map={'ALLOW': '#00CC96', 'DENY': '#EF553B'},
                hole=0.3
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(showlegend=True)
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📊 Top 10 Vehicles by Entry Attempt")
            
            # Get top vehicles
            top_vehicles = analytics_agent.get_top_vehicles(df, top_n=10)
            
            # Create bar chart
            fig_bar = px.bar(
                top_vehicles,
                x='plate_number',
                y='count',
                title='Most Frequent Vehicles',
                labels={'plate_number': 'License Plate', 'count': 'Number of Attempts'},
                color='count',
                color_continuous_scale='Blues'
            )
            
            fig_bar.update_layout(showlegend=False)
            fig_bar.update_xaxis(tickangle=-45)
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Hourly traffic chart
        st.subheader("📅 Hourly Traffic Distribution")
        
        hourly_data = analytics_agent.get_hourly_traffic(df)
        
        if not hourly_data.empty:
            fig_hourly = px.line(
                hourly_data,
                x='hour',
                y='count',
                title='Access Attempts by Hour of Day',
                labels={'hour': 'Hour (24h format)', 'count': 'Number of Attempts'},
                markers=True
            )
            
            fig_hourly.update_traces(line_color='#636EFA', line_width=3)
            fig_hourly.update_xaxis(tickmode='linear', tick0=0, dtick=1)
            
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        st.markdown("---")
        
        # Live Log Table
        st.subheader("📋 Live Access Log")
        
        # Search and filter options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search by Plate Number", "")
        
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                options=["All", "ALLOW", "DENY"]
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df['plate_number'].str.contains(search_term, case=False, na=False)]
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        # Sort by timestamp (newest first)
        filtered_df = filtered_df.sort_values('timestamp', ascending=False)
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.DatetimeColumn(
                    "Timestamp",
                    format="YYYY-MM-DD HH:mm:ss"
                ),
                "plate_number": st.column_config.TextColumn(
                    "License Plate",
                    width="medium"
                ),
                "status": st.column_config.TextColumn(
                    "Status",
                    width="small"
                )
            }
        )
        
        # Download button for CSV
        st.markdown("---")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"access_log_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Auto-refresh logic
    # Note: st.rerun() is the recommended Streamlit pattern for auto-refresh
    # The sleep ensures we don't hammer the system with constant updates
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    create_dashboard()
