import hashlib
from modules.database import get_users, save_users
import streamlit as st

from modules.security import Security
from modules.user_database import UserDatabase
from modules.icons import svg


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    users = get_users()

    # check if user exists
    for user in users:
        if user["username"] == username:
            return False, "User already exists"

    users.append({
        "username": username,
        "password": hash_password(password)
    })

    save_users(users)
    return True, "Registration successful"


def login_user(username, password):
    users = get_users()
    hashed = hash_password(password)

    for user in users:
        if user["username"] == username and user["password"] == hashed:
            return True

    return False


class Auth:

    def __init__(self):

        self.db = UserDatabase()

    def login(self):

        left, center, right = st.columns([1, 1.3, 1])

        with center:

            st.markdown(
                f"""
                <div class="auth-wrap">
                    <div class="auth-logo">{svg('sparkles', 22, color='#ffffff')}</div>
                    <h1 class="auth-title">Welcome back</h1>
                    <p class="auth-subtitle">Sign in to your recruiter workspace to continue screening candidates.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.container(border=True):

                with st.form(key="login_form", border=False):

                    email = st.text_input(
                        "Email",
                        key="login_email",
                        placeholder="you@company.com"
                    )

                    password = st.text_input(
                        "Password",
                        type="password",
                        key="login_password",
                        placeholder="Enter your password"
                    )

                    submitted = st.form_submit_button(
                        "Sign In",
                        use_container_width=True
                    )

                if submitted:

                    if not email or not password:
                        st.error("Please enter your email and password.")
                        return

                    user = self.db.login(
                        email,
                        password
                    )

                    if not user:
                        st.error("Invalid email or password.")
                        return

                    stored_password = user[3]

                    if not Security.verify_password(
                        password,
                        stored_password
                    ):
                        st.error("Invalid email or password.")
                        return

                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2],
                        "role": user[4]
                    }

                    st.success("Login successful. Redirecting to your workspace...")
                    st.rerun()

            st.markdown(
                """
                <p class="auth-foot">New to AI Recruit? Use the "Register" tab above to create an account.</p>
                """,
                unsafe_allow_html=True
            )

    def logout(self):

        if st.button(
            "🚪 Logout",
            key="logout_button"
        ):

            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.rerun()
