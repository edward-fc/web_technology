from app import app, db

# Set up the application context
with app.app_context():
    # Drop all tables
    db.drop_all()
    # Create all tables
    db.create_all()

print("Database has been reset.")