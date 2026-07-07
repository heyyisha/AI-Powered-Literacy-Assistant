from flask import Blueprint, jsonify
from database import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

curriculum_bp = Blueprint("curriculum_bp", __name__)

# Get all curriculum categories
@curriculum_bp.route("/api/curriculum", methods=["GET"])
def get_curriculum():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM curriculum ORDER BY id ASC")
    curriculum = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(curriculum)

# Get all lessons for a specific curriculum ID
@curriculum_bp.route("/api/curriculum/<int:id>/lessons", methods=["GET"])
def get_lessons_by_curriculum(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lessons WHERE curriculum_id = %s", (id,))
    lessons = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(lessons)

@curriculum_bp.route("/api/lessons/<int:lesson_id>", methods=["GET"])
def get_lesson_detail(lesson_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch details for the specific lesson
    cursor.execute("SELECT * FROM lessons WHERE id = %s", (lesson_id,))
    lesson = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if lesson:
        return jsonify(lesson), 200
    else:
        return jsonify({"message": "Lesson not found"}), 404
    
    from flask_jwt_extended import jwt_required, get_jwt_identity

@curriculum_bp.route("/api/lessons/<int:lesson_id>/complete", methods=["POST"])
@jwt_required()
def complete_lesson(lesson_id):
    user_id = get_jwt_identity()
    connection = get_db_connection()
    cursor = connection.cursor()

    # 1. Increment total_xp (e.g., +10 per lesson) and completed_lessons
    cursor.execute("""
        UPDATE learner_profiles 
        SET total_xp = total_xp + 10, 
            completed_lessons = completed_lessons + 1 
        WHERE user_id = %s
    """, (user_id,))
    
    # 2. Record this in a progress table (optional but recommended)
    # This prevents the user from clicking "Complete" 100 times to farm XP
    cursor.execute("""
        INSERT INTO user_lesson_progress (user_id, lesson_id, status) 
        VALUES (%s, %s, 'completed')
        ON DUPLICATE KEY UPDATE status='completed'
    """, (user_id, lesson_id))
    
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Lesson completed! XP earned."}), 200