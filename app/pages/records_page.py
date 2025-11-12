import streamlit as st
from datetime import datetime
import json
from app.services.records import create_record, get_records, update_record, delete_record

def show_records():
    st.title("📝 Records Management")

    if 'user' not in st.session_state:
        st.warning("Please login to manage records")
        return

    user_id = st.session_state['user']['id']

    tab1, tab2 = st.tabs(["View Records", "Add New Record"])

    with tab1:
        st.subheader("Your Records")

        records = get_records(user_id)

        if records:
            for record in records:
                with st.expander(f"📄 {record['title']} - {record['category']} (${record['value']})"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Category:** {record['category']}")
                        st.write(f"**Value:** ${record['value']}")
                        timestamp = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                        st.write(f"**Date:** {timestamp.strftime('%Y-%m-%d %H:%M')}")

                        if record.get('metadata') and record['metadata'] != {}:
                            st.write(f"**Metadata:** {json.dumps(record['metadata'], indent=2)}")

                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{record['id']}"):
                            st.session_state['editing_record'] = record
                            st.rerun()

                        if st.button("🗑️ Delete", key=f"delete_{record['id']}"):
                            if delete_record(record['id'], user_id):
                                st.success("Record deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete record")
        else:
            st.info("No records found. Create your first record in the 'Add New Record' tab!")

        if 'editing_record' in st.session_state:
            st.divider()
            st.subheader("Edit Record")

            record = st.session_state['editing_record']

            with st.form("edit_record_form"):
                title = st.text_input("Title", value=record['title'])
                category = st.text_input("Category", value=record['category'])
                value = st.number_input("Value", value=float(record['value']), step=0.01)

                timestamp = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                record_date = st.date_input("Date", value=timestamp.date())
                record_time = st.time_input("Time", value=timestamp.time())

                metadata_str = st.text_area("Metadata (JSON)", value=json.dumps(record.get('metadata', {}), indent=2))

                col1, col2 = st.columns(2)

                with col1:
                    submit = st.form_submit_button("Update Record")

                with col2:
                    cancel = st.form_submit_button("Cancel")

                if submit:
                    try:
                        metadata = json.loads(metadata_str) if metadata_str else {}
                        new_timestamp = datetime.combine(record_date, record_time)

                        updated = update_record(
                            record['id'],
                            user_id,
                            title=title,
                            category=category,
                            value=value,
                            timestamp=new_timestamp,
                            metadata=metadata
                        )

                        if updated:
                            st.success("Record updated successfully!")
                            del st.session_state['editing_record']
                            st.rerun()
                        else:
                            st.error("Failed to update record")
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in metadata field")
                    except Exception as e:
                        st.error(f"Error updating record: {str(e)}")

                if cancel:
                    del st.session_state['editing_record']
                    st.rerun()

    with tab2:
        st.subheader("Create New Record")

        with st.form("create_record_form"):
            title = st.text_input("Title")
            category = st.text_input("Category")
            value = st.number_input("Value", value=0.0, step=0.01)

            col1, col2 = st.columns(2)
            with col1:
                record_date = st.date_input("Date", value=datetime.now())
            with col2:
                record_time = st.time_input("Time", value=datetime.now().time())

            metadata_str = st.text_area("Metadata (JSON, optional)", placeholder='{"key": "value"}')

            submit = st.form_submit_button("Create Record")

            if submit:
                if not title or not category:
                    st.error("Title and category are required")
                else:
                    try:
                        metadata = json.loads(metadata_str) if metadata_str else {}
                        timestamp = datetime.combine(record_date, record_time)

                        record = create_record(
                            user_id,
                            title,
                            category,
                            value,
                            timestamp,
                            metadata
                        )

                        if record:
                            st.success("Record created successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to create record")
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in metadata field")
                    except Exception as e:
                        st.error(f"Error creating record: {str(e)}")
