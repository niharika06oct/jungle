from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create the Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jungle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import and register blueprints
from app.routes import main
app.register_blueprint(main.bp)

# Initialize database
with app.app_context():
    db.create_all()

# This is no longer needed as we're creating the app directly
# def create_app():
#     return app 