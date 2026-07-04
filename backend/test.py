from sqlalchemy import create_engine

engine = create_engine(
    "mysql://root:one8commune%4018@localhost:3306/library_management_db"
)

with engine.connect() as conn:
    print("Database connected successfully!")