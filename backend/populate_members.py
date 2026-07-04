"""
Seed sample library members.
Run from backend directory: python populate_members.py
"""
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine
from app.models.models import Base, Member, MembershipPlan
from seed_catalog import seed_catalog

SAMPLE_MEMBERS = [
    {
        "member_code": "MEM001",
        "full_name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "phone_number": "555-0101",
        "postal_address": "123 Oak Street, Springfield, IL 62701",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 10,
    },
    {
        "member_code": "MEM002",
        "full_name": "Robert Chen",
        "email": "robert.chen@email.com",
        "phone_number": "555-0102",
        "postal_address": "456 Maple Avenue, Portland, OR 97201",
        "plan_name": "Standard",
        "status": "active",
        "months_until_expiry": 8,
    },
    {
        "member_code": "MEM003",
        "full_name": "Maria Garcia",
        "email": "maria.garcia@email.com",
        "phone_number": "555-0103",
        "postal_address": "789 Pine Road, Austin, TX 78701",
        "plan_name": "Standard",
        "status": "active",
        "months_until_expiry": 11,
    },
    {
        "member_code": "MEM004",
        "full_name": "James Wilson",
        "email": "james.wilson@email.com",
        "phone_number": "555-0104",
        "postal_address": "321 Elm Lane, Denver, CO 80202",
        "plan_name": "Basic",
        "status": "active",
        "months_until_expiry": 4,
    },
    {
        "member_code": "MEM005",
        "full_name": "Emily Davis",
        "email": "emily.davis@email.com",
        "phone_number": "555-0105",
        "postal_address": "654 Cedar Court, Seattle, WA 98101",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 12,
    },
    {
        "member_code": "MEM006",
        "full_name": "Michael Brown",
        "email": "michael.brown@email.com",
        "phone_number": "555-0106",
        "postal_address": "987 Birch Boulevard, Boston, MA 02108",
        "plan_name": "Standard",
        "status": "suspended",
        "months_until_expiry": 6,
    },
    {
        "member_code": "MEM007",
        "full_name": "Sarah Martinez",
        "email": "sarah.martinez@email.com",
        "phone_number": "555-0107",
        "postal_address": "147 Willow Way, Miami, FL 33101",
        "plan_name": "Basic",
        "status": "active",
        "months_until_expiry": 2,
    },
    {
        "member_code": "MEM008",
        "full_name": "David Thompson",
        "email": "david.thompson@email.com",
        "phone_number": "555-0108",
        "postal_address": "258 Spruce Street, Chicago, IL 60601",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 9,
    },
    {
        "member_code": "MEM009",
        "full_name": "Jennifer Lee",
        "email": "jennifer.lee@email.com",
        "phone_number": "555-0109",
        "postal_address": "369 Ash Drive, San Francisco, CA 94102",
        "plan_name": "Standard",
        "status": "expired",
        "months_until_expiry": -2,
    },
    {
        "member_code": "MEM010",
        "full_name": "Christopher Taylor",
        "email": "chris.taylor@email.com",
        "phone_number": "555-0110",
        "postal_address": "741 Poplar Place, Nashville, TN 37201",
        "plan_name": "Basic",
        "status": "active",
        "months_until_expiry": 5,
    },
    {
        "member_code": "MEM011",
        "full_name": "Amanda White",
        "email": "amanda.white@email.com",
        "phone_number": "555-0111",
        "postal_address": "852 Hickory Hill, Atlanta, GA 30301",
        "plan_name": "Standard",
        "status": "active",
        "months_until_expiry": 7,
    },
    {
        "member_code": "MEM012",
        "full_name": "Daniel Harris",
        "email": None,
        "phone_number": "555-0112",
        "postal_address": "963 Walnut Walk, Phoenix, AZ 85001",
        "plan_name": "Basic",
        "status": "active",
        "months_until_expiry": 3,
    },
    {
        "member_code": "MEM013",
        "full_name": "Lisa Anderson",
        "email": "lisa.anderson@email.com",
        "phone_number": "555-0113",
        "postal_address": "159 Chestnut Circle, Philadelphia, PA 19102",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 11,
    },
    {
        "member_code": "MEM014",
        "full_name": "Kevin Moore",
        "email": "kevin.moore@email.com",
        "phone_number": None,
        "postal_address": "357 Sycamore Square, Dallas, TX 75201",
        "plan_name": "Standard",
        "status": "suspended",
        "months_until_expiry": 5,
    },
    {
        "member_code": "MEM015",
        "full_name": "Rachel Clark",
        "email": "rachel.clark@email.com",
        "phone_number": "555-0115",
        "postal_address": "486 Magnolia Lane, Charlotte, NC 28202",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 12,
    },
    {
        "member_code": "MEM016",
        "full_name": "Brian Lewis",
        "email": "brian.lewis@email.com",
        "phone_number": "555-0116",
        "postal_address": "597 Dogwood Drive, Minneapolis, MN 55401",
        "plan_name": "Basic",
        "status": "expired",
        "months_until_expiry": -1,
    },
    {
        "member_code": "MEM017",
        "full_name": "Nicole Walker",
        "email": "nicole.walker@email.com",
        "phone_number": "555-0117",
        "postal_address": "618 Redwood Road, San Diego, CA 92101",
        "plan_name": "Standard",
        "status": "active",
        "months_until_expiry": 6,
    },
    {
        "member_code": "MEM018",
        "full_name": "Thomas Hall",
        "email": "thomas.hall@email.com",
        "phone_number": "555-0118",
        "postal_address": "729 Juniper Junction, Detroit, MI 48201",
        "plan_name": "Premium",
        "status": "active",
        "months_until_expiry": 10,
    },
    {
        "member_code": "MEM019",
        "full_name": "Patricia Allen",
        "email": "patricia.allen@email.com",
        "phone_number": "555-0119",
        "postal_address": "830 Cypress Court, Houston, TX 77001",
        "plan_name": "Standard",
        "status": "active",
        "months_until_expiry": 9,
    },
    {
        "member_code": "MEM020",
        "full_name": "Steven Young",
        "email": "steven.young@email.com",
        "phone_number": "555-0120",
        "postal_address": "941 Laurel Lane, Columbus, OH 43201",
        "plan_name": "Basic",
        "status": "active",
        "months_until_expiry": 1,
    },
]


def populate_members(reset: bool = False):
    seed_catalog()
    db = SessionLocal()
    try:
        if reset:
            print("Clearing existing members...")
            db.query(Member).delete()
            db.commit()

        plans = {plan.name: plan for plan in db.query(MembershipPlan).all()}
        if not plans:
            raise RuntimeError("No membership plans found. Run seed_catalog.py first.")

        created = 0
        skipped = 0

        for member_data in SAMPLE_MEMBERS:
            existing = db.query(Member).filter(
                Member.member_code == member_data["member_code"]
            ).first()
            if existing:
                skipped += 1
                continue

            plan = plans.get(member_data["plan_name"])
            if not plan:
                raise RuntimeError(f"Missing plan: {member_data['plan_name']}")

            expiry_date = date.today() + timedelta(days=30 * member_data["months_until_expiry"])
            member = Member(
                member_code=member_data["member_code"],
                full_name=member_data["full_name"],
                email=member_data["email"],
                phone_number=member_data["phone_number"],
                postal_address=member_data["postal_address"],
                membership_plan_id=plan.id,
                status=member_data["status"],
                registration_date=date.today() - timedelta(days=30),
                expiry_date=expiry_date,
            )
            db.add(member)
            created += 1

        db.commit()
        total = db.query(Member).count()
        print(f"Members seeded: {created} added, {skipped} skipped, {total} total in database")
    except Exception as exc:
        db.rollback()
        print(f"Error populating members: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_members(reset=False)
