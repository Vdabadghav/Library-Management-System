"""
Script to create an admin user in the database
"""
import sys
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.models import Base, User
from app.core.security import hash_password
from datetime import datetime

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_admin():
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@library.com",
            full_name="Admin User",
            password_hash=hash_password("admin123"),
            role="admin",
            status="active"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Email: admin@library.com")
        print(f"   Role: admin")
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
