import hashlib
from modules.database import get_users, save_users
import streamlit as st

from modules.security import Security
from modules.user_database import UserDatabase


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

        st.title("🔐 Recruiter Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
        ):

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

            st.success("Login successful.")
            st.rerun()

    def logout(self):

        if st.button(
            "Logout",
            key="logout_button"
        ):

            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.rerun()
