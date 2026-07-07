from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from database import get_db_connection

lesson_material_bp = Blueprint("lesson_material_bp", __name__)


@lesson_material_bp.route("/api/lesson-materials/<int:lesson_id>", methods=["GET"])
@jwt_required()
def get_materials(lesson_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM lesson_materials
        WHERE lesson_id=%s
        AND is_active=1
        ORDER BY display_order
    """, (lesson_id,))

    materials = cursor.fetchall()

    cursor.close()
    connection.close()

    if not materials:
        return jsonify({
            "message": "No lesson materials found."
        }), 404

    return jsonify({
        "message": "Lesson materials fetched successfully.",
        "total_materials": len(materials),
        "lesson_materials": materials
    }), 200