from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            print("Creating default admin user...")
            hashed_password = generate_password_hash('admin')
            admin = User(username='admin', password_hash=hashed_password, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully! (Username: admin | Password: admin)")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_database()
    print("Database initialization complete.")
