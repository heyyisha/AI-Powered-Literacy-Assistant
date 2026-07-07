from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from database import get_db_connection

lesson_bp = Blueprint("lesson_bp", __name__)


@lesson_bp.route("/api/lessons", methods=["GET"])
@jwt_required()
def get_all_lessons():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            curriculum_id,
            language_id,
            title,
            category,
            description,
            difficulty,
            estimated_time,
            xp_points,
            lesson_order
        FROM lessons
        WHERE is_active=1
        ORDER BY lesson_order
    """)

    lessons = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Lessons fetched successfully.",
        "total_lessons": len(lessons),
        "lessons": lessons
    }), 200


@lesson_bp.route("/api/lessons/<int:curriculum_id>", methods=["GET"])
@jwt_required()
def get_lessons_by_curriculum(curriculum_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            title,
            category,
            difficulty,
            estimated_time,
            xp_points,
            lesson_order
        FROM lessons
        WHERE curriculum_id=%s
        AND is_active=1
        ORDER BY lesson_order
    """, (curriculum_id,))

    lessons = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Lessons fetched successfully.",
        "curriculum_id": curriculum_id,
        "total_lessons": len(lessons),
        "lessons": lessons
    }), 200


@lesson_bp.route("/api/lesson/<int:lesson_id>", methods=["GET"])
@jwt_required()
def get_lesson_details(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM lessons
        WHERE id=%s
    """, (lesson_id,))

    lesson = cursor.fetchone()

    cursor.close()
    connection.close()

    if not lesson:
        return jsonify({
            "message": "Lesson not found."
        }), 404

    return jsonify({
        "message": "Lesson fetched successfully.",
        "lesson": lesson
    }), 200