"""CLI to train models and bootstrap the admin user."""
import os
import sys
import argparse
import getpass


def train(dataset_path: str):
    from app import create_app
    from app.services.trainer import ModelTrainer

    app = create_app()
    with app.app_context():
        trainer = ModelTrainer(app.config["ML_MODEL_PATH"])
        result = trainer.train_all(dataset_path)
        trainer.persist_metrics_to_db()
        print("Training complete.")
        print(f"Best algorithm: {result['best_algorithm']} (F1={result['best_f1']:.4f})")


def create_admin():
    from app import create_app
    from app.extensions import db
    from app.models.user import User

    app = create_app()
    with app.app_context():
        db.create_all()
        email = input("Admin email: ").strip().lower()
        username = input("Admin username: ").strip().lower()
        full_name = input("Full name: ").strip()
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match")
            return
        if User.query.filter_by(email=email).first():
            print("Email already exists")
            return
        user = User(email=email, username=username, full_name=full_name, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{username}' created.")


def main():
    parser = argparse.ArgumentParser(description="AI Phishing Detector CLI")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("init-db", help="Create database tables")
    sub.add_parser("create-admin", help="Create an admin user")
    p = sub.add_parser("train", help="Train all ML models")
    p.add_argument("--dataset", required=True, help="Path to CSV dataset")
    args = parser.parse_args()

    if args.cmd == "init-db":
        from app import create_app
        from app.extensions import db
        app = create_app()
        with app.app_context():
            db.create_all()
            print("Database tables created.")
    elif args.cmd == "create-admin":
        create_admin()
    elif args.cmd == "train":
        train(args.dataset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
