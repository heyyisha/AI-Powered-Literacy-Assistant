from flask import Blueprint, jsonify, request
from database import get_db_connection

language_bp = Blueprint("language_bp", __name__)

@language_bp.route("/api/languages", methods=["GET"])
def get_languages():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM languages
    WHERE is_active = TRUE
    ORDER BY display_order
""")
    languages = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(languages)


@language_bp.route("/api/languages/<int:id>", methods=["GET"])
def get_language_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM languages WHERE id=%s", (id,))
    language = cursor.fetchone()

    cursor.close()
    connection.close()

    if language:
        return jsonify(language)
    else:
        return jsonify({"message": "Language not found"}), 404


@language_bp.route("/api/languages", methods=["POST"])
def add_language():
    data = request.get_json()
    required_fields = [
    "language_code",
    "language_name",
    "native_name",
    "display_order"
]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
            "message": f"{field} is required."
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO languages
    (language_code, language_name, native_name, display_order)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        data["language_code"],
        data["language_name"],
        data["native_name"],
        data["display_order"]
    )

    try:
        cursor.execute(query, values)
        connection.commit()

        new_id = cursor.lastrowid

        return jsonify({
            "message": "Language added successfully",
            "id": new_id
        }), 201

    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({
                "message": "Language code already exists."
            }), 400

        return jsonify({
            "message": "Something went wrong.",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        connection.close()

@language_bp.route("/api/languages/<int:id>", methods=["PUT"])
def update_language(id):

    data = request.get_json()

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE languages
    SET language_code=%s,
        language_name=%s,
        native_name=%s,
        display_order=%s
    WHERE id=%s
    """

    values = (
        data["language_code"],
        data["language_name"],
        data["native_name"],
        data["display_order"],
        id
    )

    try:
        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "message": "Language not found."
            }), 404

        return jsonify({
            "message": "Language updated successfully."
        })

    except Exception as e:

        if "Duplicate entry" in str(e):
            return jsonify({
                "message": "Language code already exists."
            }), 400

        return jsonify({
            "message": "Something went wrong.",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        connection.close()
@language_bp.route("/api/languages/<int:id>", methods=["DELETE"])
def delete_language(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE languages
    SET is_active = FALSE
    WHERE id=%s
    """

    try:
        cursor.execute(query, (id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "message": "Language not found."
            }), 404

        return jsonify({
            "message": "Language deleted successfully."
        })

    except Exception as e:
        return jsonify({
            "message": "Something went wrong.",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        connection.close()