from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db_connection

certificate_bp = Blueprint("certificate_bp", __name__)

@certificate_bp.route("/api/generate-certificate", methods=["POST"])
@jwt_required()
def generate_certificate():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    curriculum_id = data.get("curriculum_id")

    if not curriculum_id:
        return jsonify({
            "message": "curriculum_id is required."
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Check learner profile
    cursor.execute("""
        SELECT completed_lessons
        FROM learner_profiles
        WHERE user_id=%s
    """, (user_id,))
    profile = cursor.fetchone()

    if not profile:
        cursor.close()
        connection.close()
        return jsonify({
            "message": "Profile not found."
        }), 404

    # Check total lessons in curriculum
    cursor.execute("""
        SELECT COUNT(*) AS total_lessons
        FROM lessons
        WHERE curriculum_id=%s
        AND is_active=1
    """, (curriculum_id,))

    total_lessons = cursor.fetchone()["total_lessons"]

    if profile["completed_lessons"] < total_lessons:
        cursor.close()
        connection.close()
        return jsonify({
            "message": "Complete all lessons before generating the certificate."
        }), 400

    # Prevent duplicate certificates
    cursor.execute("""
        SELECT id
        FROM certificates
        WHERE user_id=%s
        AND curriculum_id=%s
    """, (user_id, curriculum_id))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        connection.close()
        return jsonify({
            "message": "Certificate already generated.",
            "certificate_id": existing["id"]
        }), 200

    title = "AI Powered Literacy Assistant Certificate"

    cursor.execute("""
        INSERT INTO certificates
        (
            user_id,
            curriculum_id,
            certificate_title
        )
        VALUES(%s,%s,%s)
    """, (
        user_id,
        curriculum_id,
        title
    ))

    connection.commit()

    certificate_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({

        "message": "Certificate generated successfully.",

        "certificate": {
            "certificate_id": certificate_id,
            "title": title,
            "curriculum_id": curriculum_id
        }

    }), 201