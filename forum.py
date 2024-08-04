# forum.py
import streamlit as st
import requests

backend_url = "http://127.0.0.1:5000"

def register(username, password):
    try:
        response = requests.post(f"{backend_url}/register", json={'username': username, 'password': password})
        response.raise_for_status()
        st.success("User registered successfully")
        st.session_state['registration_success'] = True  # Set flag to indicate successful registration
        return True, "User registered successfully"
    except requests.exceptions.RequestException as e:
        return False, f"Registration failed: {str(e)}"

def login(username, password):
    try:
        response = requests.post(f"{backend_url}/login", json={'username': username, 'password': password})
        response.raise_for_status()
        st.session_state['session_cookie'] = response.cookies.get('session')
        st.session_state['username'] = username  # Store the username in session state
        return True, "Login successful"
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return False, "Incorrect username or password"
        else:
            return False, f"Login failed: {str(e)}"
    except requests.exceptions.RequestException as e:
        return False, f"Login failed: {str(e)}"

def logout():
    try:
        response = requests.post(f"{backend_url}/logout", cookies={'session': st.session_state.get('session_cookie', '')})
        response.raise_for_status()
        st.session_state.pop('session_cookie', None)
        st.session_state.pop('username', None)  # Clear the username from session state
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Logout error: {str(e)}")
        return False

def fetch_posts():
    try:
        response = requests.get(f"{backend_url}/posts", cookies={'session': st.session_state.get('session_cookie', '')})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching posts: {str(e)}")
        return []

def create_post(title, content, tags):
    post_data = {
        'title': title,
        'content': content,
        'tags': tags
    }
    try:
        response = requests.post(f"{backend_url}/posts", json=post_data, cookies={'session': st.session_state.get('session_cookie', '')})
        response.raise_for_status()
        return True, "Post created successfully"
    except requests.exceptions.RequestException as e:
        return False, f"Failed to create post: {str(e)}"

def upvote_post(post_id):
    try:
        response = requests.post(f"{backend_url}/posts/{post_id}/upvote", cookies={'session': st.session_state.get('session_cookie', '')})
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error upvoting post: {str(e)}")
        return False

def test_auth():
    try:
        response = requests.get(f"{backend_url}/test_auth", cookies={'session': st.session_state.get('session_cookie', '')})
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def forum():
    st.header("Community Forum")

    if 'session_cookie' not in st.session_state:
        # Check if registration was successful and redirect to login
        if st.session_state.get('registration_success', False):
            st.session_state.pop('registration_success')  # Reset the flag
            option = "Login"
            st.success("Please log in with your new account.")
        else:
            option = st.selectbox("Choose an option", ["Login", "Register"])

        if option == "Login":
            with st.form("login"):
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    success, message = login(username, password)
                    if success:
                        st.success(message)
                        st.experimental_rerun()
                    else:
                        st.error(message)
        else:
            with st.form("register"):
                st.subheader("Register")
                new_username = st.text_input("New Username")
                new_password = st.text_input("New Password", type="password")
                submitted = st.form_submit_button("Register")
                if submitted:
                    success, message = register(new_username, new_password)
                    if success:
                        st.experimental_rerun()  # Rerun to display the login screen
                    else:
                        st.error(message)
    else:
        username = st.session_state.get('username', 'User')  # Retrieve username from session state
        st.subheader(f"Welcome, {username}")  # Display the username
        if st.button("Logout"):
            if logout():
                st.success("Logout successful")
                st.experimental_rerun()
            else:
                st.error("Logout failed")

        with st.form("new_post"):
            st.subheader("Create a New Post")
            title = st.text_input("Title")
            content = st.text_area("Content")
            tags = st.text_input("Tags (comma-separated)")
            submitted = st.form_submit_button("Submit")

            if submitted:
                success, message = create_post(title, content, tags)
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(f"Error creating post: {message}")
                    if not test_auth():
                        st.error("Authentication failed. Please log in again.")
                        st.session_state.pop('session_cookie', None)
                        st.experimental_rerun()

        st.subheader("Posts")
        posts = fetch_posts()
        for post in posts:
            st.markdown(f"### {post['title']}")
            st.markdown(f"**Tags:** {post['tags']}")
            st.markdown(post['content'])
            st.markdown(f"**Upvotes:** {post['upvotes']}")
            if st.button("Upvote", key=post['id']):
                if upvote_post(post['id']):
                    st.experimental_rerun()

if __name__ == "__main__":
    forum()
