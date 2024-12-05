from app import app, db
from app import views  # Import views to ensure all routes are loaded before running the app

if __name__ == "__main__":
    with app.app_context():
        # Ensure all tables are created before running the application
        db.create_all()

    # Run the app
    app.run(host='127.0.0.1', port=1300, debug=True)
