from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from database import get_db_connection

leaderboard_bp = Blueprint("leaderboard_bp", __name__)

@leaderboard_bp.route("/api/leaderboard", methods=["GET"])
@jwt_required()
def get_leaderboard():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id,
            u.full_name,
            lp.total_xp,
            lp.completed_lessons,
            lp.current_streak,
            lp.proficiency_level
        FROM users u
        INNER JOIN learner_profiles lp
            ON u.id = lp.user_id
        ORDER BY
            lp.total_xp DESC,
            lp.completed_lessons DESC,
            lp.current_streak DESC
    """)

    leaderboard = cursor.fetchall()

    # Add Rank
    for index, user in enumerate(leaderboard, start=1):
        user["rank"] = index

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Leaderboard fetched successfully.",
        "total_users": len(leaderboard),
        "leaderboard": leaderboard
    }), 200