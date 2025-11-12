import streamlit as st
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from app.pages.auth import show_auth
from app.pages.dashboard import show_dashboard
from app.pages.records_page import show_records
from app.pages.reports_page import show_reports
from app.pages.jobs_page import show_jobs
from app.services.background_jobs import fetch_external_data

load_dotenv()

st.set_page_config(
    page_title="Streamlit CRUD App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_scheduler():
    if 'scheduler' not in st.session_state:
        scheduler = BackgroundScheduler()
        external_api_url = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/posts")
        job_interval = int(os.getenv("JOB_INTERVAL_MIN", "5"))

        scheduler.add_job(
            func=lambda: fetch_external_data(external_api_url),
            trigger="interval",
            minutes=job_interval,
            id="fetch_external_data",
            name="Fetch External Data",
            replace_existing=True
        )

        scheduler.start()
        st.session_state['scheduler'] = scheduler

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if 'user' not in st.session_state:
        st.session_state['user'] = None

    if not st.session_state['authenticated']:
        show_auth()
        return

    init_scheduler()

    st.sidebar.title("📊 Streamlit App")

    user_email = st.session_state['user']['email']
    is_guest = st.session_state['user'].get('is_guest', False)

    if is_guest:
        st.sidebar.info(f"👤 Guest User")
    else:
        st.sidebar.info(f"👤 {user_email}")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        if 'editing_record' in st.session_state:
            del st.session_state['editing_record']
        st.rerun()

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Records", "Reports", "Background Jobs"],
        label_visibility="collapsed"
    )

    if page == "Dashboard":
        show_dashboard()
    elif page == "Records":
        show_records()
    elif page == "Reports":
        show_reports()
    elif page == "Background Jobs":
        show_jobs()

if __name__ == "__main__":
    main()
