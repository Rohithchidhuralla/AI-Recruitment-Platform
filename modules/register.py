import streamlit as st
from modules.user_database import UserDatabase
from modules.security import Security
from modules.icons import svg


class Register:

    def show(self):

        db = UserDatabase()

        left, center, right = st.columns([1, 1.3, 1])

        with center:

            st.markdown(
                f"""
                <div class="auth-wrap">
                    <div class="auth-logo">{svg('id', 22, color='#ffffff')}</div>
                    <h1 class="auth-title">Create your account</h1>
                    <p class="auth-subtitle">Set up recruiter access to start screening and scoring candidates.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.container(border=True):

                with st.form(key="register_form", border=False):

                    name = st.text_input(
                        "Full Name",
                        key="register_name",
                        placeholder="Jane Doe"
                    )

                    email = st.text_input(
                        "Email",
                        key="register_email",
                        placeholder="you@company.com"
                    )

                    pass_col, confirm_col = st.columns(2)

                    with pass_col:
                        password = st.text_input(
                            "Password",
                            type="password",
                            key="register_password",
                            placeholder="Create a password"
                        )

                    with confirm_col:
                        confirm = st.text_input(
                            "Confirm Password",
                            type="password",
                            key="register_confirm_password",
                            placeholder="Repeat password"
                        )

                    role = st.selectbox(
                        "Role",
                        ["Recruiter", "Admin"],
                        key="register_role"
                    )

                    submitted = st.form_submit_button(
                        "Create Account",
                        use_container_width=True
                    )

                if submitted:

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

                        st.success("✅ Account created successfully! Switch to the Login tab to sign in.")

                    except Exception:
                        st.error("Email already exists.")

            st.markdown(
                """
                <p class="auth-foot">Already have an account? Use the "Login" tab above.</p>
                """,
                unsafe_allow_html=True
            )
