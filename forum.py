import streamlit as st
import requests

backend_url = "http://localhost:5000"

def register(username, password):
    response = requests.post(f"{backend_url}/register", json={'username': username, 'password': password})
    if response.status_code == 201:
        return True, "User registered successfully"
    try:
        return False, response.json().get('message', 'Registration failed')
    except ValueError:
        return False, 'Server error'

def login(username, password):
    response = requests.post(f"{backend_url}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        st.session_state['session_cookie'] = response.cookies.get('session')
        return True, "Login successful"
    try:
        return False, response.json().get('message', 'Invalid credentials')
    except ValueError:
        return False, 'Server error'

def logout():
    response = requests.post(f"{backend_url}/logout", cookies={'session': st.session_state.get('session_cookie', '')})
    if response.status_code == 200:
        st.session_state.pop('session_cookie', None)
        return True
    return False

def fetch_posts():
    response = requests.get(f"{backend_url}/posts", cookies={'session': st.session_state.get('session_cookie', '')})
    if response.status_code == 200:
        return response.json()
    return []

def create_post(title, content, tags):
    post_data = {
        'title': title,
        'content': content,
        'tags': tags
    }
    response = requests.post(f"{backend_url}/posts", json=post_data, cookies={'session': st.session_state.get('session_cookie', '')})
    if response.status_code == 201:
        return True, "Post created successfully"
    try:
        return False, response.json().get('message', 'Failed to create post')
    except ValueError:
        return False, 'Server error'

def upvote_post(post_id):
    response = requests.post(f"{backend_url}/posts/{post_id}/upvote", cookies={'session': st.session_state.get('session_cookie', '')})
    return response.status_code == 200

def test_auth():
    response = requests.get(f"{backend_url}/test_auth", cookies={'session': st.session_state.get('session_cookie', '')})
    return response.status_code == 200

def forum():
    st.header("Community Forum")

    if 'session_cookie' not in st.session_state:
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
                        st.success(message)
                        st.experimental_rerun()
                    else:
                        st.error(message)
    else:
        st.subheader(f"Welcome, User")
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