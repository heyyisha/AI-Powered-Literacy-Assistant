from flask import Flask
from routes.language_routes import language_bp
from routes.user_routes import user_bp
from flask_jwt_extended import JWTManager
from routes.curriculum_routes import curriculum_bp
from datetime import timedelta
from flask_jwt_extended import JWTManager
from routes.lesson_routes import lesson_bp
from routes.lesson_material_routes import lesson_material_bp
from routes.progress_routes import progress_bp
from routes.assessment_routes import assessment_bp
from routes.leaderboard_routes import leaderboard_bp
from routes.certificate_routes import certificate_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(language_bp)
app.register_blueprint(user_bp)
app.register_blueprint(curriculum_bp)
app.register_blueprint(lesson_bp)
app.register_blueprint(lesson_material_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(certificate_bp)

# --- ADD THIS BLOCK ---
with app.app_context():
    print("--- REGISTERED ROUTES ---")
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule.rule} | Methods: {rule.methods}")
    print("-------------------------")
# ----------------------

@app.route('/')
def home():
    return "AI Powered Literacy Assistant Backend Running!"

if __name__ == "__main__":
    app.run(debug=True)