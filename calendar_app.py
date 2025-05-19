import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from event_categories import CATEGORIES
from utils import format_currency, parse_event_date, load_image_from_url

def render_dashboard_view(events, selected_categories):
    """
    Render a dashboard view with analytics about events
    """
    # Display dashboard image
    dashboard_image_url = "https://pixabay.com/get/g05391bed28ee0c400ad8a592f6ac4c89003a8e7a7a940fc861b97aa03cb06ecfe060279fdb3e6364247ff9cb260997e91e94e41912838390dfe32f82dd8bdddc_1280.jpg"
    dashboard_col1, dashboard_col2 = st.columns([1, 3])
    
    with dashboard_col1:
        st.image(load_image_from_url(dashboard_image_url), width=150)
    
    with dashboard_col2:
        st.header("Events Analytics Dashboard")
        st.markdown("Key metrics and distribution of upcoming events")
    
    # Handle empty events list
    if not events:
        st.warning("No events found with the current filters. Try adjusting your filters.")
        return
    
    # Convert events to DataFrame for easier analysis
    df = events_to_dataframe(events)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Events", len(df))
    
    with col2:
        # Calculate total trading volume
        total_volume = df['trading_volume'].sum()
        st.metric("Total Volume", format_currency(total_volume))
    
    with col3:
        # Calculate percent of verified events
        verified_pct = (df['verified'].sum() / len(df)) * 100
        st.metric("Verified Events", f"{verified_pct:.1f}%")
    
    with col4:
        # Calculate average volume per event
        avg_volume = total_volume / len(df)
        st.metric("Avg. Volume/Event", format_currency(avg_volume))
    
    # Create two columns for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Events by Category")
        render_category_distribution(df)
    
    with chart_col2:
        st.subheader("Volume by Category")
        render_volume_by_category(df)
    
    # Events over time
    st.subheader("Events Timeline")
    render_events_timeline(df)
    
    # Top events table
    st.subheader("Top Events by Trading Volume")
    render_top_events_table(df)
    
    # Events verification status
    verification_col1, verification_col2 = st.columns(2)
    
    with verification_col1:
        st.subheader("Verification Status")
        render_verification_chart(df)
    
    with verification_col2:
        st.subheader("Upcoming Events by Date")
        render_upcoming_events_chart(df)

def events_to_dataframe(events):
    """
    Convert events list to pandas DataFrame for analysis
    """
    df_data = []
    
    for event in events:
        # Parse date
        event_date = parse_event_date(event.get('date', datetime.now().isoformat()))
        
        df_data.append({
            'id': event.get('id', ''),
            'title': event.get('title', 'Unknown Event'),
            'category': event.get('category', 'Uncategorized'),
            'trading_volume': event.get('trading_volume', 0),
            'date': event_date,
            'date_str': event_date.strftime('%Y-%m-%d'),
            'verified': event.get('verified', False),
            'url': event.get('url', ''),
            'source_url': event.get('source_url', '')
        })
    
    return pd.DataFrame(df_data)

def render_category_distribution(df):
    """
    Render a pie chart showing the distribution of events by category
    """
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    
    # Add colors
    category_counts['color'] = category_counts['category'].map(CATEGORIES)
    
    fig = px.pie(
        category_counts, 
        names='category', 
        values='count',
        color='category',
        color_discrete_map={cat: col for cat, col in CATEGORIES.items()},
        hole=0.4
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_volume_by_category(df):
    """
    Render a bar chart showing trading volume by category
    """
    volume_by_category = df.groupby('category')['trading_volume'].sum().reset_index()
    volume_by_category = volume_by_category.sort_values('trading_volume', ascending=False)
    
    fig = px.bar(
        volume_by_category,
        x='category',
        y='trading_volume',
        color='category',
        color_discrete_map=CATEGORIES,
        labels={'trading_volume': 'Trading Volume ($)', 'category': 'Category'}
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title=None,
        height=300
    )
    
    # Format y-axis to show currency
    fig.update_yaxes(tickprefix='$', tickformat=',.0f')
    
    st.plotly_chart(fig, use_container_width=True)

def render_events_timeline(df):
    """
    Render a line chart showing events distribution over time
    """
    # Ensure dates are datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Group by date and category, count events
    timeline_data = df.groupby(['date_str', 'category']).size().reset_index(name='count')
    timeline_data['date'] = pd.to_datetime(timeline_data['date_str'])
    timeline_data = timeline_data.sort_values('date')
    
    # Create line chart
    fig = px.line(
        timeline_data,
        x='date',
        y='count',
        color='category',
        color_discrete_map=CATEGORIES,
        labels={'count': 'Number of Events', 'date': 'Date'}
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title=None,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_top_events_table(df):
    """
    Render a table of top events by trading volume
    """
    # Sort by trading volume and select top events
    top_events = df.sort_values('trading_volume', ascending=False).head(10)
    
    # Create a formatted table
    table_data = []
    for _, row in top_events.iterrows():
        table_data.append({
            "Event": row['title'],
            "Category": row['category'],
            "Date": row['date'].strftime('%b %d, %Y'),
            "Trading Volume": format_currency(row['trading_volume']),
            "Verified": "✅" if row['verified'] else "❌"
        })
    
    # Display as a Streamlit table
    st.table(pd.DataFrame(table_data))

def render_verification_chart(df):
    """
    Render a chart showing verification status distribution
    """
    verified_counts = df['verified'].value_counts().reset_index()
    verified_counts.columns = ['verified', 'count']
    verified_counts['status'] = verified_counts['verified'].map({True: 'Verified', False: 'Unverified'})
    
    fig = px.pie(
        verified_counts,
        names='status',
        values='count',
        color='status',
        color_discrete_map={'Verified': '#4CAF50', 'Unverified': '#FFC107'},
        hole=0.6
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=300,
        showlegend=False,
        annotations=[dict(text='Verification<br>Status', x=0.5, y=0.5, font_size=15, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_upcoming_events_chart(df):
    """
    Render a chart showing upcoming events by date
    """
    # Filter to only upcoming dates
    today = datetime.now().date()
    upcoming_df = df[df['date'].dt.date >= today]
    
    # Group by date and count events
    upcoming_counts = upcoming_df.groupby('date_str').size().reset_index(name='count')
    upcoming_counts['date'] = pd.to_datetime(upcoming_counts['date_str'])
    upcoming_counts = upcoming_counts.sort_values('date')
    
    # Limit to next 14 days
    end_date = today + timedelta(days=14)
    upcoming_counts = upcoming_counts[upcoming_counts['date'].dt.date <= end_date]
    
    # Create bar chart
    fig = px.bar(
        upcoming_counts,
        x='date',
        y='count',
        labels={'count': 'Number of Events', 'date': 'Date'},
        color_discrete_sequence=['#1E88E5']
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title=None,
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
