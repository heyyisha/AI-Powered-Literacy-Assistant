from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db_connection

assessment_bp = Blueprint("assessment_bp", __name__)

@assessment_bp.route("/api/submit-assessment", methods=["POST"])
@jwt_required()
def submit_assessment():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    lesson_id = data.get("lesson_id")
    reading_score = float(data.get("reading_score", 0))
    writing_score = float(data.get("writing_score", 0))
    comprehension_score = float(data.get("comprehension_score", 0))

    if not lesson_id:
        return jsonify({
            "message": "lesson_id is required."
        }), 400

    # Validate scores
    if not (0 <= reading_score <= 100):
        return jsonify({
            "message": "Reading score must be between 0 and 100."
        }), 400

    if not (0 <= writing_score <= 100):
        return jsonify({
            "message": "Writing score must be between 0 and 100."
        }), 400

    if not (0 <= comprehension_score <= 100):
        return jsonify({
            "message": "Comprehension score must be between 0 and 100."
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Check lesson exists
    cursor.execute("""
        SELECT id
        FROM lessons
        WHERE id=%s
        AND is_active=1
    """, (lesson_id,))

    lesson = cursor.fetchone()

    if not lesson:
        cursor.close()
        connection.close()
        return jsonify({
            "message": "Lesson not found."
        }), 404

    # Calculate overall score
    overall_score = round(
        (reading_score + writing_score + comprehension_score) / 3,
        2
    )

    # Decide proficiency level
    if overall_score >= 70:
        proficiency = "Advanced"
    elif overall_score >= 40:
        proficiency = "Intermediate"
    else:
        proficiency = "Beginner"

    # Save assessment
    cursor.execute("""
        INSERT INTO assessment_results
        (
            user_id,
            lesson_id,
            reading_score,
            writing_score,
            comprehension_score,
            overall_score
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        user_id,
        lesson_id,
        reading_score,
        writing_score,
        comprehension_score,
        overall_score
    ))

    # Update learner profile
    cursor.execute("""
        UPDATE learner_profiles
        SET
            reading_score=%s,
            writing_score=%s,
            comprehension_score=%s,
            overall_score=%s,
            proficiency_level=%s
        WHERE user_id=%s
    """, (
        reading_score,
        writing_score,
        comprehension_score,
        overall_score,
        proficiency,
        user_id
    ))

    connection.commit()

    # Fetch updated profile
    cursor.execute("""
        SELECT
            reading_score,
            writing_score,
            comprehension_score,
            overall_score,
            proficiency_level
        FROM learner_profiles
        WHERE user_id=%s
    """, (user_id,))

    profile = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Assessment submitted successfully.",
        "profile": profile
    }), 200