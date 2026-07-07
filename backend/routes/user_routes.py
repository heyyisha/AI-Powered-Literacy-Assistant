from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    required_fields = [
        "full_name",
        "email",
        "password",
        "preferred_language_id"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "message": f"{field} is required."
            }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE email=%s",
        (data["email"],)
    )

    if cursor.fetchone():
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Email already registered."
        }), 400

    password_hash = generate_password_hash(data["password"])

    query = """
    INSERT INTO users
    (
        full_name,
        email,
        password_hash,
        age,
        gender,
        education_level,
        preferred_language_id
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["full_name"],
        data["email"],
        password_hash,
        data.get("age"),
        data.get("gender"),
        data.get("education_level"),
        data["preferred_language_id"]
    )

    cursor.execute(query, values)

    user_id = cursor.lastrowid

    # Automatically create learner profile
    cursor.execute("""
    INSERT INTO learner_profiles (user_id)
    VALUES (%s)
    """, (user_id,))

    connection.commit()

    return jsonify({
    "message": "User registered successfully.",
        "user_id": user_id
    }), 201

@user_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({
            "message": "Email and password are required."
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (data["email"],)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    # verify password
    if not check_password_hash(user["password_hash"], data["password"]):
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    # create JWT token
    access_token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "user": {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"]
        }
    }), 200

@user_bp.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user_id=int(user_id)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, full_name, email, age, gender, education_level, preferred_language_id
        FROM users
        WHERE id=%s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user": user
    }), 200

@user_bp.route("/api/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    user_id = int(get_jwt_identity())
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT total_xp, current_streak, completed_lessons, proficiency_level
        FROM learner_profiles
        WHERE user_id=%s
    """, (user_id,))

    dashboard_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if not dashboard_data:
        return jsonify({"message": "Dashboard data not found"}), 404

    return jsonify({
    "message": "Dashboard fetched successfully.",
    "dashboard": {
        "total_xp": dashboard_data["total_xp"],
        "current_streak": dashboard_data["current_streak"],
        "completed_lessons": dashboard_data["completed_lessons"],
        "proficiency_level": dashboard_data["proficiency_level"]
    }
}), 200