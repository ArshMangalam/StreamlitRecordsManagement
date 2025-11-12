import streamlit as st
from app.utils.auth import register_user, login_user, create_guest_user

def show_auth():
    st.title("🔐 Welcome")

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Guest Mode"])

    with tab1:
        st.subheader("Login to Your Account")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if not email or not password:
                    st.error("Please provide both email and password")
                else:
                    user = login_user(email, password)
                    if user:
                        st.session_state['user'] = user
                        st.session_state['authenticated'] = True
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

    with tab2:
        st.subheader("Create New Account")

        with st.form("register_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")

            if submit:
                if not email or not password:
                    st.error("Please provide both email and password")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    user = register_user(email, password)
                    if user:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Email might already be in use.")

    with tab3:
        st.subheader("Continue as Guest")
        st.info("Guest mode allows you to try the app without creating an account. Your data will be tied to a temporary guest account.")

        if st.button("Continue as Guest", type="primary"):
            user = create_guest_user()
            if user:
                st.session_state['user'] = user
                st.session_state['authenticated'] = True
                st.success("Guest account created!")
                st.rerun()
            else:
                st.error("Failed to create guest account. Please try again.")
