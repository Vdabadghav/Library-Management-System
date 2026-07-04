"""
Seed catalog data: languages, genres, and membership plans.
Run from backend directory: python seed_catalog.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine
from app.models.models import Base, Language, Genre, MembershipPlan

LANGUAGES = [
    {"name": "English", "code": "EN"},
    {"name": "Spanish", "code": "ES"},
    {"name": "French", "code": "FR"},
    {"name": "German", "code": "DE"},
    {"name": "Ancient Greek", "code": "GR"},
]

GENRES = [
    {"name": "Fiction", "description": "Imaginative literature and novels"},
    {"name": "Classic", "description": "Timeless literary works"},
    {"name": "Drama", "description": "Plays and theatrical works"},
    {"name": "Fantasy", "description": "Magical and fantastical worlds"},
    {"name": "Science Fiction", "description": "Futuristic and speculative fiction"},
    {"name": "Horror", "description": "Suspenseful and frightening stories"},
    {"name": "Romance", "description": "Love and relationship stories"},
    {"name": "Mystery", "description": "Crime and detective fiction"},
    {"name": "Young Adult", "description": "Books for teen and young adult readers"},
    {"name": "Dystopian", "description": "Societies gone wrong"},
    {"name": "Adventure", "description": "Action and exploration stories"},
    {"name": "Historical", "description": "Stories set in past eras"},
]

MEMBERSHIP_PLANS = [
    {
        "name": "Basic",
        "max_books_allowed": 2,
        "max_days_allowed": 14,
        "fine_per_day": 0.50,
        "membership_fee": 10.0,
        "validity_months": 6,
        "description": "Entry-level plan for casual readers",
    },
    {
        "name": "Standard",
        "max_books_allowed": 5,
        "max_days_allowed": 21,
        "fine_per_day": 0.25,
        "membership_fee": 25.0,
        "validity_months": 12,
        "description": "Popular plan for regular library users",
    },
    {
        "name": "Premium",
        "max_books_allowed": 10,
        "max_days_allowed": 30,
        "fine_per_day": 0.10,
        "membership_fee": 50.0,
        "validity_months": 12,
        "description": "Full access plan for avid readers",
    },
]


def seed_catalog():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("Seeding languages...")
        for lang in LANGUAGES:
            existing = db.query(Language).filter(Language.code == lang["code"]).first()
            if not existing:
                db.add(Language(**lang))

        print("Seeding genres...")
        for genre in GENRES:
            existing = db.query(Genre).filter(Genre.name == genre["name"]).first()
            if not existing:
                db.add(Genre(**genre))

        print("Seeding membership plans...")
        for plan in MEMBERSHIP_PLANS:
            existing = db.query(MembershipPlan).filter(MembershipPlan.name == plan["name"]).first()
            if not existing:
                db.add(MembershipPlan(**plan))

        db.commit()
        print(
            f"Catalog ready: "
            f"{db.query(Language).count()} languages, "
            f"{db.query(Genre).count()} genres, "
            f"{db.query(MembershipPlan).count()} membership plans"
        )
    except Exception as exc:
        db.rollback()
        print(f"Error seeding catalog: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_catalog()
