import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from app.services.records import get_records, get_record_statistics

def show_dashboard():
    st.title("📊 Dashboard")

    if 'user' not in st.session_state:
        st.warning("Please login to view the dashboard")
        return

    user_id = st.session_state['user']['id']

    st.sidebar.header("Filters")

    categories_data = get_records(user_id)
    all_categories = list(set([r['category'] for r in categories_data]))
    all_categories.insert(0, "All Categories")

    category_filter = st.sidebar.selectbox("Category", all_categories)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    category = None if category_filter == "All Categories" else category_filter

    records = get_records(user_id, category, start_datetime, end_datetime)
    stats = get_record_statistics(user_id, category, start_datetime, end_datetime)

    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", stats['count'])

    with col2:
        st.metric("Total Value", f"${stats['sum']:,.2f}")

    with col3:
        st.metric("Average Value", f"${stats['average']:,.2f}")

    with col4:
        if stats['count'] > 0:
            st.metric("Value Range", f"${stats['min']:.2f} - ${stats['max']:.2f}")
        else:
            st.metric("Value Range", "N/A")

    if records:
        st.subheader("📈 Value Over Time")

        df = pd.DataFrame(records)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        fig_time = px.line(df, x='timestamp', y='value', color='category',
                           title='Record Values Over Time',
                           labels={'value': 'Value', 'timestamp': 'Date'},
                           template='plotly_white')

        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)

        st.subheader("📊 Category Breakdown")

        category_summary = df.groupby('category').agg({
            'value': ['sum', 'count', 'mean']
        }).reset_index()

        category_summary.columns = ['category', 'total_value', 'count', 'avg_value']

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = px.pie(category_summary, values='total_value', names='category',
                            title='Value Distribution by Category')
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(category_summary, x='category', y='count',
                            title='Record Count by Category',
                            labels={'count': 'Number of Records', 'category': 'Category'},
                            template='plotly_white')
            fig_bar.update_layout(height=350)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Recent Records")
        recent_df = df[['title', 'category', 'value', 'timestamp']].head(10)
        recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(recent_df, use_container_width=True, hide_index=True)

    else:
        st.info("No records found for the selected filters. Create some records to see your dashboard come to life!")
