import streamlit as st
from datetime import datetime, timedelta
from app.services.records import get_records, get_record_statistics
from app.services.reports import generate_csv, generate_excel, generate_pdf_summary

def show_reports():
    st.title("📊 Reports")

    if 'user' not in st.session_state:
        st.warning("Please login to generate reports")
        return

    user_id = st.session_state['user']['id']

    st.sidebar.header("Report Filters")

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

    st.subheader("Report Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", stats['count'])
    with col2:
        st.metric("Total Value", f"${stats['sum']:,.2f}")
    with col3:
        st.metric("Average Value", f"${stats['average']:,.2f}")

    st.divider()

    st.subheader("📥 Download Reports")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**CSV Export**")
        st.write("Download records as a CSV file for use in Excel, Google Sheets, or other tools.")

        if st.button("Generate CSV", type="primary", use_container_width=True):
            try:
                csv_data = generate_csv(records)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                st.success(f"CSV ready! ({len(records)} records)")
            except Exception as e:
                st.error(f"Error generating CSV: {str(e)}")

    with col2:
        st.write("**Excel Export**")
        st.write("Download records as an Excel workbook with formatted sheets.")

        if st.button("Generate Excel", type="primary", use_container_width=True):
            try:
                excel_data = generate_excel(records)
                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_data,
                    file_name=f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.success(f"Excel ready! ({len(records)} records)")
            except Exception as e:
                st.error(f"Error generating Excel: {str(e)}")

    with col3:
        st.write("**PDF Summary**")
        st.write("Download a formatted PDF report with statistics and recent records.")

        if st.button("Generate PDF", type="primary", use_container_width=True):
            try:
                pdf_data = generate_pdf_summary(records, stats)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_data,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("PDF report ready!")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

    if records:
        st.divider()
        st.subheader("Preview Data")

        import pandas as pd
        df = pd.DataFrame(records)
        df = df[['title', 'category', 'value', 'timestamp']]
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')

        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No records found for the selected filters.")
