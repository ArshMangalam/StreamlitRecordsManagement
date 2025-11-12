import streamlit as st
import os
from datetime import datetime
from app.services.background_jobs import fetch_external_data, get_last_job_run, get_job_history

def show_jobs():
    st.title("🔄 Background Jobs")

    if 'user' not in st.session_state:
        st.warning("Please login to view background jobs")
        return

    external_api_url = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/posts")
    job_interval = os.getenv("JOB_INTERVAL_MIN", "5")

    st.info(f"Background jobs fetch data from external sources. Configured to run every {job_interval} minutes.")

    st.subheader("Job Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**API URL:** `{external_api_url}`")

    with col2:
        st.write(f"**Interval:** {job_interval} minutes")

    st.divider()

    last_run = get_last_job_run()

    if last_run:
        st.subheader("Last Job Run")

        col1, col2, col3 = st.columns(3)

        with col1:
            fetched_at = datetime.fromisoformat(last_run['fetched_at'].replace('Z', '+00:00'))
            st.metric("Last Run", fetched_at.strftime('%Y-%m-%d %H:%M:%S'))

        with col2:
            status_color = "🟢" if last_run['status'] == 'success' else "🔴"
            st.metric("Status", f"{status_color} {last_run['status'].title()}")

        with col3:
            if last_run['status'] == 'success':
                data = last_run.get('data', {})
                if isinstance(data, dict) and 'items' in data:
                    count = len(data['items'])
                elif isinstance(data, list):
                    count = len(data)
                else:
                    count = 1
                st.metric("Records Fetched", count)
            else:
                st.metric("Records Fetched", "N/A")

        if last_run.get('error_message'):
            st.error(f"**Error:** {last_run['error_message']}")

    else:
        st.info("No jobs have been run yet. Click 'Run Job Now' to fetch data.")

    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("🚀 Run Job Now", type="primary", use_container_width=True):
            with st.spinner("Fetching data..."):
                result = fetch_external_data(external_api_url)

                if result['success']:
                    st.success(result['message'])
                    if 'record_count' in result:
                        st.info(f"Fetched {result['record_count']} records")
                    st.rerun()
                else:
                    st.error(result['message'])

    st.divider()

    st.subheader("Job History")

    history = get_job_history(limit=20)

    if history:
        for job in history:
            fetched_at = datetime.fromisoformat(job['fetched_at'].replace('Z', '+00:00'))
            status_icon = "✅" if job['status'] == 'success' else "❌"

            with st.expander(f"{status_icon} {fetched_at.strftime('%Y-%m-%d %H:%M:%S')} - {job['status'].title()}"):
                st.write(f"**Source URL:** {job['source_url']}")
                st.write(f"**Status:** {job['status']}")

                if job.get('error_message'):
                    st.error(f"**Error:** {job['error_message']}")
                else:
                    data = job.get('data', {})
                    if isinstance(data, dict) and 'items' in data:
                        st.write(f"**Records Fetched:** {len(data['items'])}")
                    elif isinstance(data, list):
                        st.write(f"**Records Fetched:** {len(data)}")

                    st.json(data if isinstance(data, dict) else {'items': data[:3] if isinstance(data, list) else []})
    else:
        st.info("No job history available.")

    st.divider()

    with st.expander("ℹ️ About Background Jobs"):
        st.write("""
        Background jobs automatically fetch data from external APIs at regular intervals.

        **Features:**
        - Configurable API endpoint
        - Automatic retry on failure
        - Job history tracking
        - Manual trigger support

        **Configuration:**
        Set the following environment variables:
        - `EXTERNAL_API_URL`: The API endpoint to fetch from
        - `JOB_INTERVAL_MIN`: Interval in minutes between automatic runs

        Note: In this demo, automatic scheduling runs in-memory and will reset when the app restarts.
        For production, use a persistent job queue like Celery or AWS Lambda.
        """)
