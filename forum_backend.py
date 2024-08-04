# forum_backend.py

from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key_here'  # Change this to a secure random key
CORS(app, supports_credentials=True, origins="http://localhost:8501")

login_manager = LoginManager()
login_manager.init_app(app)

# SQLite database connection
engine = create_engine('sqlite:///forum.db', connect_args={'check_same_thread': False})
Base = declarative_base()

# User model
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Post model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    upvotes = Column(Integer, default=0)
    tags = Column(String(100))

# Create all tables
Base.metadata.create_all(engine)

# Session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Load user
@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(User).get(int(user_id))
    session.close()
    return user

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    session = Session()
    try:
        if session.query(User).filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 400
        new_user = User(username=username)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        logger.info(f"User registered successfully: {username}")
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to register user: {str(e)}")
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500
    finally:
        session.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    session_db = Session()
    try:
        user = session_db.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            logger.info(f"User logged in successfully: {username}")
            resp = make_response(jsonify({'message': 'Login successful'}))
            resp.set_cookie('session', app.secret_key, httponly=True, samesite='Lax')
            return resp, 200
        logger.warning(f"Invalid login attempt for user: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Failed to login: {str(e)}")
        return jsonify({'message': 'Failed to login', 'error': str(e)}), 500
    finally:
        session_db.close()

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    logger.info("User logged out successfully")
    resp = make_response(jsonify({'message': 'Logout successful'}))
    resp.set_cookie('session', '', expires=0)
    return resp, 200

@app.route('/posts', methods=['GET'])
@login_required
def get_posts():
    session_db = Session()
    try:
        posts = session_db.query(Post).all()
        logger.info(f"Fetched {len(posts)} posts")
        return jsonify([{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'upvotes': post.upvotes,
            'tags': post.tags
        } for post in posts]), 200
    except Exception as e:
        logger.error(f"Failed to fetch posts: {str(e)}")
        return jsonify({'message': 'Failed to fetch posts', 'error': str(e)}), 500
    finally:
        session_db.close()

@app.route('/posts', methods=['POST'])
@login_required
def create_post():
    session_db = Session()
    try:
        data = request.get_json()
        logger.info(f"Received post data: {data}")
        new_post = Post(
            title=data['title'],
            content=data['content'],
            tags=data['tags']
        )
        session_db.add(new_post)
        session_db.commit()
        logger.info(f"Post created successfully: {new_post.title}")
        return jsonify({'message': 'Post created successfully'}), 201
    except Exception as e:
        session_db.rollback()
        logger.error(f"Failed to create post: {str(e)}")
        return jsonify({'message': 'Failed to create post', 'error': str(e)}), 500
    finally:
        session_db.close()

@app.route('/posts/<int:post_id>/upvote', methods=['POST'])
@login_required
def upvote_post(post_id):
    session_db = Session()
    try:
        post = session_db.query(Post).get(post_id)
        if post:
            post.upvotes += 1
            session_db.commit()
            logger.info(f"Post upvoted successfully: {post.title}")
            return jsonify({'message': 'Post upvoted successfully'}), 200
        logger.warning(f"Attempt to upvote non-existent post: {post_id}")
        return jsonify({'message': 'Post not found'}), 404
    except Exception as e:
        session_db.rollback()
        logger.error(f"Failed to upvote post: {str(e)}")
        return jsonify({'message': 'Failed to upvote post', 'error': str(e)}), 500
    finally:
        session_db.close()

@app.route('/test_auth', methods=['GET'])
@login_required
def test_auth():
    return jsonify({'message': 'Authentication working'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)