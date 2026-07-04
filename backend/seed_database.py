"""
Seed the full library database: catalog, books, and members.
Run from backend directory: python seed_database.py

Options:
  python seed_database.py          # Add missing records only
  python seed_database.py --reset  # Clear books/members and re-seed
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed_catalog import seed_catalog
from populate_books import populate_books
from populate_members import populate_members


def seed_database(reset: bool = False):
    print("=" * 50)
    print("Library Management System - Database Seeder")
    print("=" * 50)

    print("\n[1/3] Seeding catalog (languages, genres, plans)...")
    seed_catalog()

    print("\n[2/3] Seeding books (with authors and genres)...")
    populate_books(reset=reset)

    print("\n[3/3] Seeding members...")
    populate_members(reset=reset)

    print("\nDatabase seeding complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the library database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing books and members before seeding",
    )
    args = parser.parse_args()
    seed_database(reset=args.reset)
