import sqlalchemy
from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    print("Checking MySQL connection...")
    try:
        # First, try to connect without a database to CREATE the database if it doesn't exist!
        engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/')
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("CREATE DATABASE IF NOT EXISTS phishing_db"))
        print("MySQL 'phishing_db' database is ready!")
    except Exception as e:
        print("Could not connect to MySQL. Falling back to SQLite.")

    with app.app_context():
        print("Creating tables...")
        # Create all tables (in MySQL if available, else SQLite)
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
