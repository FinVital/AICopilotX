import streamlit as st
import backend as sb
import home

def session(user_id):
    st.session_state["id"] = user_id
    st.session_state["logged_in"] = True
    st.success("Successfully logged in!")
    st.rerun()

def sign_check(name, email, password):
    col = sb.check()
    user_ids = [record["id"] for record in col]

    if email in user_ids:
        st.error("This user already exists")
    else:
        sb.sign_up(email, name, email, password)
        session(email)

def login_check(email, password):
    col = sb.check()
    user_ids = [record["id"] for record in col]
    user_passwords = {record["id"]: record["Password"] for record in col}

    if email in user_ids:
        if password == user_passwords[email]:
            session(email)
        else:
            st.error("Wrong Password")
    else:
        st.error("User not found. Please sign up first.")

def main():
    st.title("Welcome to AICopilotX")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        action = st.sidebar.radio("Choose action", ["Sign Up", "Log In"])

        if action == "Sign Up":
            with st.form("signup_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    sign_check(name, email, password)

        elif action == "Log In":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In")
                if submitted:
                    login_check(email, password)
    else:
        home.main(st.session_state["id"], [])

        st.sidebar.success(f"Logged in as {st.session_state['id']}")
        # Display logout option on the left sidebar
        if st.sidebar.button("Logout"):
            st.session_state["id"] = None
            st.sidebar.text("Logged out")
            st.rerun()
        
if __name__ == "__main__":
    main()
