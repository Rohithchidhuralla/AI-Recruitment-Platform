import streamlit as st
from modules.user_database import UserDatabase
from modules.security import Security


class Register:

    def show(self):

        db = UserDatabase()

        st.title("📝 Create Recruiter Account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        role = st.selectbox(
            "Role",
            ["Recruiter", "Admin"],
            key="register_role"
        )

        if st.button(
            "Create Account",
            key="register_button"
        ):

            if not name or not email or not password:
                st.error("Please fill all fields.")
                return

            if password != confirm:
                st.error("Passwords do not match.")
                return

            hashed = Security.hash_password(password)

            try:
                db.register_user(
                    name,
                    email,
                    hashed,
                    role
                )

                st.success("✅ Account created successfully!")

            except Exception:
                st.error("Email already exists.")
