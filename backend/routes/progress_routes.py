from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db_connection

progress_bp = Blueprint("progress_bp", __name__)

@progress_bp.route("/api/complete-lesson", methods=["POST"])
@jwt_required()
def complete_lesson():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    lesson_id = data.get("lesson_id")

    if not lesson_id:
        return jsonify({"message": "lesson_id is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Check lesson exists
    cursor.execute("""
        SELECT id, xp_points
        FROM lessons
        WHERE id=%s
    """, (lesson_id,))
    lesson = cursor.fetchone()

    if not lesson:
        cursor.close()
        connection.close()
        return jsonify({"message": "Lesson not found"}), 404

    # Check if already completed
    cursor.execute("""
        SELECT id
        FROM lesson_progress
        WHERE user_id=%s
        AND lesson_id=%s
    """, (user_id, lesson_id))

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"message": "Lesson already completed"}), 400

    # Insert progress
    cursor.execute("""
        INSERT INTO lesson_progress
        (user_id, lesson_id)
        VALUES(%s,%s)
    """, (user_id, lesson_id))

    # Update learner profile
    cursor.execute("""
        UPDATE learner_profiles
        SET
            total_xp = total_xp + %s,
            completed_lessons = completed_lessons + 1,
            current_streak = current_streak + 1
        WHERE user_id=%s
    """, (lesson["xp_points"], user_id))

    connection.commit()

    # Fetch updated dashboard
    cursor.execute("""
        SELECT
            total_xp,
            completed_lessons,
            current_streak,
            proficiency_level
        FROM learner_profiles
        WHERE user_id=%s
    """, (user_id,))

    dashboard = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Lesson completed successfully",
        "dashboard": dashboard
    }), 200
@progress_bp.route("/api/my-progress", methods=["GET"])
@jwt_required()
def get_my_progress():

    user_id = int(get_jwt_identity())

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            lp.lesson_id,
            l.title,
            l.category,
            l.difficulty,
            l.xp_points,
            lp.status,
            lp.score,
            lp.completed_at
        FROM lesson_progress lp
        INNER JOIN lessons l
            ON lp.lesson_id = l.id
        WHERE lp.user_id = %s
        ORDER BY lp.completed_at DESC
    """, (user_id,))

    progress = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Progress fetched successfully.",
        "total_completed": len(progress),
        "progress": progress
    }), 200