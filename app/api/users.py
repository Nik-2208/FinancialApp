from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.db.database import db_session
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/create_user', methods=['POST'])
def create_user():
    """
    API to create a new user
    """
    try:
        # Extract and validate input data
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({"error": "All fields (username, email, password) are required"}), 400

        # Ensure password meets minimum requirements
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Create and save new user
        new_user = User(username=username, email=email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return jsonify({"message": f"User '{username}' created successfully"}), 201

    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "A user with this email already exists"}), 409

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@user_routes.route('/login', methods=['POST'])
def login_user():
    """
    API to authenticate a user
    """
    try:
        # Extract credentials from request
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"error": "Email and password are required"}), 400

        # Find user in the database
        user = db_session.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({"message": f"Welcome, {user.username}!"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@user_routes.route('/list_users', methods=['GET'])
def list_users():
    """
    API to list all registered users
    """
    try:
        users = db_session.query(User).all()
        user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
