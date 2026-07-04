"""
Script to populate the database with sample books
Run from backend directory: python populate_books.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine
from app.models.models import Base, Book, Language, Author, Genre
from seed_catalog import seed_catalog

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Sample books data
SAMPLE_BOOKS = [
    {"isbn": "9780451524935", "title": "1984", "author": "George Orwell", "publisher": "Penguin Books", "year": 1949, "copies": 5},
    {"isbn": "9780316769174", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "publisher": "Little, Brown", "year": 1951, "copies": 4},
    {"isbn": "9780062073556", "title": "To Kill a Mockingbird", "author": "Harper Lee", "publisher": "J.B. Lippincott", "year": 1960, "copies": 6},
    {"isbn": "9780374529239", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publisher": "Scribner", "year": 1925, "copies": 5},
    {"isbn": "9780451526342", "title": "Brave New World", "author": "Aldous Huxley", "publisher": "Chatto and Windus", "year": 1932, "copies": 4},
    {"isbn": "9780062457714", "title": "Pride and Prejudice", "author": "Jane Austen", "publisher": "T. Egerton", "year": 1813, "copies": 7},
    {"isbn": "9780143124611", "title": "Jane Eyre", "author": "Charlotte Brontë", "publisher": "Smith, Elder", "year": 1847, "copies": 5},
    {"isbn": "9780141439556", "title": "Wuthering Heights", "author": "Emily Brontë", "publisher": "Thomas Cautley Newby", "year": 1847, "copies": 4},
    {"isbn": "9780486284629", "title": "Moby Dick", "author": "Herman Melville", "publisher": "Richard Bentley", "year": 1851, "copies": 3},
    {"isbn": "9780451526830", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "publisher": "The Russian Messenger", "year": 1866, "copies": 4},
    {"isbn": "9780143107040", "title": "War and Peace", "author": "Leo Tolstoy", "publisher": "The Russian Messenger", "year": 1869, "copies": 3},
    {"isbn": "9780451532671", "title": "Anna Karenina", "author": "Leo Tolstoy", "publisher": "Russian Messenger", "year": 1877, "copies": 4},
    {"isbn": "9780141183770", "title": "The Odyssey", "author": "Homer", "publisher": "Ancient Greek", "year": -800, "copies": 2},
    {"isbn": "9780199535941", "title": "The Iliad", "author": "Homer", "publisher": "Ancient Greek", "year": -800, "copies": 2},
    {"isbn": "9780451526922", "title": "Hamlet", "author": "William Shakespeare", "publisher": "First Folio", "year": 1603, "copies": 6},
    {"isbn": "9780451526533", "title": "Macbeth", "author": "William Shakespeare", "publisher": "First Folio", "year": 1606, "copies": 5},
    {"isbn": "9780451526748", "title": "Romeo and Juliet", "author": "William Shakespeare", "publisher": "First Folio", "year": 1597, "copies": 7},
    {"isbn": "9780451530661", "title": "A Midsummer Night's Dream", "author": "William Shakespeare", "publisher": "First Folio", "year": 1595, "copies": 5},
    {"isbn": "9780451528667", "title": "The Tempest", "author": "William Shakespeare", "publisher": "First Folio", "year": 1610, "copies": 4},
    {"isbn": "9780451527288", "title": "Othello", "author": "William Shakespeare", "publisher": "First Folio", "year": 1603, "copies": 4},
    {"isbn": "9780451526113", "title": "King Lear", "author": "William Shakespeare", "publisher": "First Folio", "year": 1606, "copies": 3},
    {"isbn": "9780451529961", "title": "The Merchant of Venice", "author": "William Shakespeare", "publisher": "First Folio", "year": 1596, "copies": 4},
    {"isbn": "9780451528926", "title": "Much Ado About Nothing", "author": "William Shakespeare", "publisher": "First Folio", "year": 1598, "copies": 5},
    {"isbn": "9780451531377", "title": "Twelfth Night", "author": "William Shakespeare", "publisher": "First Folio", "year": 1601, "copies": 4},
    {"isbn": "9780451532343", "title": "The Taming of the Shrew", "author": "William Shakespeare", "publisher": "First Folio", "year": 1592, "copies": 3},
    {"isbn": "9780451532749", "title": "All's Well That Ends Well", "author": "William Shakespeare", "publisher": "First Folio", "year": 1601, "copies": 2},
    {"isbn": "9780451533722", "title": "Measure for Measure", "author": "William Shakespeare", "publisher": "First Folio", "year": 1604, "copies": 2},
    {"isbn": "9780451533661", "title": "The Comedy of Errors", "author": "William Shakespeare", "publisher": "First Folio", "year": 1592, "copies": 3},
    {"isbn": "9780451534361", "title": "Love's Labour's Lost", "author": "William Shakespeare", "publisher": "First Folio", "year": 1594, "copies": 2},
    {"isbn": "9780451531087", "title": "The Two Gentlemen of Verona", "author": "William Shakespeare", "publisher": "First Folio", "year": 1590, "copies": 2},
    {"isbn": "9781503280786", "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 1997, "copies": 10},
    {"isbn": "9780439136365", "title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 1998, "copies": 9},
    {"isbn": "9780439136372", "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 1999, "copies": 8},
    {"isbn": "9780439136389", "title": "Harry Potter and the Goblet of Fire", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 2000, "copies": 9},
    {"isbn": "9780439139595", "title": "Harry Potter and the Order of the Phoenix", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 2003, "copies": 8},
    {"isbn": "9780439139601", "title": "Harry Potter and the Half-Blood Prince", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 2005, "copies": 9},
    {"isbn": "9780439139618", "title": "Harry Potter and the Deathly Hallows", "author": "J.K. Rowling", "publisher": "Bloomsbury", "year": 2007, "copies": 10},
    {"isbn": "9780316769177", "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "publisher": "Allen & Unwin", "year": 1954, "copies": 7},
    {"isbn": "9780451531346", "title": "The Hobbit", "author": "J.R.R. Tolkien", "publisher": "Allen & Unwin", "year": 1937, "copies": 8},
    {"isbn": "9780451528674", "title": "The Silmarillion", "author": "J.R.R. Tolkien", "publisher": "Allen & Unwin", "year": 1977, "copies": 4},
    {"isbn": "9780395489949", "title": "The Stand", "author": "Stephen King", "publisher": "Doubleday", "year": 1978, "copies": 5},
    {"isbn": "9780451160782", "title": "It", "author": "Stephen King", "publisher": "Viking", "year": 1986, "copies": 4},
    {"isbn": "9780451527837", "title": "The Shining", "author": "Stephen King", "publisher": "Doubleday", "year": 1977, "copies": 5},
    {"isbn": "9780451528391", "title": "Carrie", "author": "Stephen King", "publisher": "Doubleday", "year": 1974, "copies": 6},
    {"isbn": "9780451528407", "title": "The Dead Zone", "author": "Stephen King", "publisher": "Viking", "year": 1979, "copies": 4},
    {"isbn": "9780451534668", "title": "Misery", "author": "Stephen King", "publisher": "Viking", "year": 1987, "copies": 5},
    {"isbn": "9780451533389", "title": "The Green Mile", "author": "Stephen King", "publisher": "Signet", "year": 1996, "copies": 6},
    {"isbn": "9780451531029", "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "publisher": "Norstedts", "year": 2005, "copies": 5},
    {"isbn": "9780451531512", "title": "The Girl Who Played with Fire", "author": "Stieg Larsson", "publisher": "Norstedts", "year": 2006, "copies": 4},
    {"isbn": "9780451532176", "title": "The Girl Who Kicked the Hornets' Nest", "author": "Stieg Larsson", "publisher": "Norstedts", "year": 2007, "copies": 4},
    {"isbn": "9780451530899", "title": "The Hunger Games", "author": "Suzanne Collins", "publisher": "Scholastic", "year": 2008, "copies": 8},
    {"isbn": "9780439023528", "title": "Catching Fire", "author": "Suzanne Collins", "publisher": "Scholastic", "year": 2009, "copies": 7},
    {"isbn": "9780439023535", "title": "Mockingjay", "author": "Suzanne Collins", "publisher": "Scholastic", "year": 2010, "copies": 7},
    {"isbn": "9780316015844", "title": "Twilight", "author": "Stephenie Meyer", "publisher": "Little, Brown", "year": 2005, "copies": 5},
    {"isbn": "9780316015851", "title": "New Moon", "author": "Stephenie Meyer", "publisher": "Little, Brown", "year": 2006, "copies": 4},
    {"isbn": "9780316055436", "title": "Eclipse", "author": "Stephenie Meyer", "publisher": "Little, Brown", "year": 2007, "copies": 4},
    {"isbn": "9780316036689", "title": "Breaking Dawn", "author": "Stephenie Meyer", "publisher": "Little, Brown", "year": 2008, "copies": 4},
    {"isbn": "9780451531162", "title": "The Maze Runner", "author": "James Dashner", "publisher": "Delacorte Press", "year": 2009, "copies": 6},
    {"isbn": "9780385741568", "title": "The Scorch Trials", "author": "James Dashner", "publisher": "Delacorte Press", "year": 2010, "copies": 5},
    {"isbn": "9780385741575", "title": "The Death Cure", "author": "James Dashner", "publisher": "Delacorte Press", "year": 2011, "copies": 5},
    {"isbn": "9780451531635", "title": "Divergent", "author": "Veronica Roth", "publisher": "Katherine Tegen Books", "year": 2011, "copies": 7},
    {"isbn": "9780062024021", "title": "Insurgent", "author": "Veronica Roth", "publisher": "Katherine Tegen Books", "year": 2012, "copies": 6},
    {"isbn": "9780062024038", "title": "Allegiant", "author": "Veronica Roth", "publisher": "Katherine Tegen Books", "year": 2013, "copies": 6},
    {"isbn": "9780451531772", "title": "The Fault in Our Stars", "author": "John Green", "publisher": "Dutton", "year": 2012, "copies": 8},
    {"isbn": "9780451531789", "title": "Looking for Alaska", "author": "John Green", "publisher": "Dutton", "year": 2005, "copies": 6},
    {"isbn": "9780451531796", "title": "Paper Towns", "author": "John Green", "publisher": "Dutton", "year": 2008, "copies": 5},
    {"isbn": "9780451531802", "title": "An Abundance of Katherines", "author": "John Green", "publisher": "Dutton", "year": 2006, "copies": 4},
    {"isbn": "9780451531819", "title": "The Book Thief", "author": "Markus Zusak", "publisher": "Picador", "year": 2005, "copies": 7},
    {"isbn": "9780451531826", "title": "The Kite Runner", "author": "Khaled Hosseini", "publisher": "Riverhead Books", "year": 2003, "copies": 6},
    {"isbn": "9780451531833", "title": "A Thousand Splendid Suns", "author": "Khaled Hosseini", "publisher": "Riverhead Books", "year": 2007, "copies": 5},
    {"isbn": "9780451531840", "title": "The Nightingale", "author": "Kristin Hannah", "publisher": "St. Martin's Press", "year": 2015, "copies": 6},
    {"isbn": "9780451531857", "title": "All the Light We Cannot See", "author": "Anthony Doerr", "publisher": "Scribner", "year": 2014, "copies": 7},
    {"isbn": "9780451531864", "title": "The Pillars of the Earth", "author": "Ken Follett", "publisher": "Morrow", "year": 1989, "copies": 4},
    {"isbn": "9780451531871", "title": "World Without End", "author": "Ken Follett", "publisher": "Macmillan", "year": 2007, "copies": 3},
    {"isbn": "9780451531888", "title": "A Column of Fire", "author": "Ken Follett", "publisher": "Viking", "year": 2017, "copies": 3},
    {"isbn": "9780451531895", "title": "Outlander", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 1991, "copies": 5},
    {"isbn": "9780451531901", "title": "Dragonfly in Amber", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 1992, "copies": 4},
    {"isbn": "9780451531918", "title": "Voyager", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 1993, "copies": 4},
    {"isbn": "9780451531925", "title": "Drums of Autumn", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 1996, "copies": 4},
    {"isbn": "9780451531932", "title": "The Fiery Cross", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 2001, "copies": 3},
    {"isbn": "9780451531949", "title": "A Breath of Snow and Ashes", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 2005, "copies": 3},
    {"isbn": "9780451531956", "title": "An Echo in the Bone", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 2009, "copies": 3},
    {"isbn": "9780451531963", "title": "Written in My Own Heart's Blood", "author": "Diana Gabaldon", "publisher": "Delacorte", "year": 2014, "copies": 3},
    {"isbn": "9780451531970", "title": "Circe", "author": "Madeline Miller", "publisher": "Little, Brown", "year": 2018, "copies": 6},
    {"isbn": "9780451531987", "title": "The Song of Achilles", "author": "Madeline Miller", "publisher": "Ecco", "year": 2011, "copies": 5},
    {"isbn": "9780451531994", "title": "Ariadne", "author": "Jennifer Saint", "publisher": "Flatiron Books", "year": 2021, "copies": 4},
    {"isbn": "9780451532000", "title": "Barbarian Days", "author": "William Finnegan", "publisher": "Penguin Press", "year": 2015, "copies": 3},
    {"isbn": "9780451532017", "title": "Educated", "author": "Tara Westover", "publisher": "Scribner", "year": 2018, "copies": 7},
    {"isbn": "9780451532024", "title": "Becoming", "author": "Michelle Obama", "publisher": "Crown", "year": 2018, "copies": 6},
    {"isbn": "9780451532031", "title": "The Immortal Life of Henrietta Lacks", "author": "Rebecca Skloot", "publisher": "Random House", "year": 2010, "copies": 5},
    {"isbn": "9780451532048", "title": "In Cold Blood", "author": "Truman Capote", "publisher": "Random House", "year": 1966, "copies": 4},
    {"isbn": "9780451532055", "title": "The Devil in the White City", "author": "Erik Larson", "publisher": "Crown", "year": 2003, "copies": 5},
    {"isbn": "9780451532062", "title": "Killers of the Flower Moon", "author": "David Grann", "publisher": "Doubleday", "year": 2017, "copies": 4},
    {"isbn": "9780451532079", "title": "Empire of Pain", "author": "Patrick Radden Keefe", "publisher": "Doubleday", "year": 2021, "copies": 3},
    {"isbn": "9780451532086", "title": "The Splendid and the Vile", "author": "Erik Larson", "publisher": "Crown", "year": 2020, "copies": 4},
    {"isbn": "9780451532093", "title": "Dune", "author": "Frank Herbert", "publisher": "Chilton Books", "year": 1965, "copies": 6},
    {"isbn": "9780451532100", "title": "Foundation", "author": "Isaac Asimov", "publisher": "Gnome Press", "year": 1951, "copies": 5},
    {"isbn": "9780451532117", "title": "Neuromancer", "author": "William Gibson", "publisher": "Ace Books", "year": 1984, "copies": 4},
    {"isbn": "9780451532124", "title": "Ender's Game", "author": "Orson Scott Card", "publisher": "Tor Books", "year": 1985, "copies": 6},
    {"isbn": "9780451532131", "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "publisher": "Ace Books", "year": 1969, "copies": 4},
    {"isbn": "9780451532148", "title": "The Expanse: Leviathan Wakes", "author": "James S.A. Corey", "publisher": "Orbit", "year": 2011, "copies": 5},
    {"isbn": "9780451532155", "title": "Snow Crash", "author": "Neal Stephenson", "publisher": "Bantam Books", "year": 1992, "copies": 4},
    {"isbn": "9780451532162", "title": "The Martian", "author": "Andy Weir", "publisher": "Crown", "year": 2011, "copies": 7},
    {"isbn": "9780451532169", "title": "Ready Player One", "author": "Ernest Cline", "publisher": "Crown", "year": 2011, "copies": 7},
]

AUTHOR_GENRES = {
    "George Orwell": ["Fiction", "Dystopian"],
    "J.D. Salinger": ["Fiction", "Classic"],
    "Harper Lee": ["Fiction", "Classic"],
    "F. Scott Fitzgerald": ["Fiction", "Classic"],
    "Aldous Huxley": ["Fiction", "Dystopian"],
    "Jane Austen": ["Fiction", "Romance", "Classic"],
    "Charlotte Brontë": ["Fiction", "Romance", "Classic"],
    "Emily Brontë": ["Fiction", "Romance", "Classic"],
    "Herman Melville": ["Fiction", "Classic", "Adventure"],
    "Fyodor Dostoevsky": ["Fiction", "Classic"],
    "Leo Tolstoy": ["Fiction", "Classic", "Historical"],
    "Homer": ["Classic", "Adventure"],
    "William Shakespeare": ["Drama", "Classic"],
    "J.K. Rowling": ["Fantasy", "Young Adult"],
    "J.R.R. Tolkien": ["Fantasy", "Adventure"],
    "Stephen King": ["Horror", "Fiction"],
    "Stieg Larsson": ["Mystery", "Fiction"],
    "Suzanne Collins": ["Young Adult", "Dystopian", "Adventure"],
    "Stephenie Meyer": ["Romance", "Young Adult", "Fantasy"],
    "James Dashner": ["Young Adult", "Science Fiction", "Adventure"],
    "Veronica Roth": ["Young Adult", "Dystopian", "Adventure"],
    "Dan Brown": ["Mystery", "Adventure", "Fiction"],
    "Paulo Coelho": ["Fiction", "Adventure"],
    "Khaled Hosseini": ["Fiction", "Historical"],
    "Yann Martel": ["Fiction", "Adventure"],
    "Markus Zusak": ["Fiction", "Historical"],
    "John Green": ["Young Adult", "Romance", "Fiction"],
    "Gillian Flynn": ["Mystery", "Fiction"],
    "Paula Hawkins": ["Mystery", "Fiction"],
    "Agatha Christie": ["Mystery", "Classic"],
    "Arthur Conan Doyle": ["Mystery", "Classic"],
    "Isaac Asimov": ["Science Fiction", "Classic"],
    "Philip K. Dick": ["Science Fiction", "Fiction"],
    "Frank Herbert": ["Science Fiction", "Adventure"],
    "Douglas Adams": ["Science Fiction", "Adventure"],
    "Ray Bradbury": ["Science Fiction", "Dystopian"],
    "Aldous Huxley": ["Science Fiction", "Dystopian"],
    "Neal Stephenson": ["Science Fiction", "Adventure"],
    "Andy Weir": ["Science Fiction", "Adventure"],
    "Ernest Cline": ["Science Fiction", "Adventure"],
}

DEFAULT_GENRES = ["Fiction"]


def normalize_publication_year(year: int) -> int:
    """Ancient works use negative years in source data; store a positive catalog year."""
    return abs(year) if year < 1000 else year


def get_or_create_author(db, author_name: str, cache: dict) -> Author:
    if author_name in cache:
        return cache[author_name]

    author = db.query(Author).filter(Author.full_name == author_name).first()
    if not author:
        author = Author(full_name=author_name)
        db.add(author)
        db.flush()

    cache[author_name] = author
    return author


def get_genres_for_author(db, author_name: str, cache: dict) -> list:
    genre_names = AUTHOR_GENRES.get(author_name, DEFAULT_GENRES)
    genres = []
    for genre_name in genre_names:
        if genre_name not in cache:
            genre = db.query(Genre).filter(Genre.name == genre_name).first()
            if genre:
                cache[genre_name] = genre
        if genre_name in cache:
            genres.append(cache[genre_name])
    return genres


def populate_books(reset: bool = False):
    """Populate the database with sample books, authors, and genres."""
    seed_catalog()
    db = SessionLocal()
    try:
        if reset:
            print("Clearing existing books...")
            db.query(Book).delete()
            db.commit()

        english = db.query(Language).filter(Language.code == "EN").first()
        greek = db.query(Language).filter(Language.code == "GR").first()
        if not english:
            raise RuntimeError("English language not found. Run seed_catalog.py first.")

        author_cache = {}
        genre_cache = {}
        created_count = 0
        skipped_count = 0
        failed_count = 0

        print(f"Adding up to {len(SAMPLE_BOOKS)} books with authors and genres...")
        for idx, book_data in enumerate(SAMPLE_BOOKS, 1):
            try:
                existing = db.query(Book).filter(Book.isbn == book_data["isbn"]).first()
                if existing:
                    skipped_count += 1
                    continue

                language = greek if book_data["author"] == "Homer" else english
                author = get_or_create_author(db, book_data["author"], author_cache)
                genres = get_genres_for_author(db, book_data["author"], genre_cache)

                book = Book(
                    isbn=book_data["isbn"],
                    title=book_data["title"],
                    publisher=book_data["publisher"],
                    publication_year=normalize_publication_year(book_data["year"]),
                    shelf_location=f"Section-{chr(65 + (idx % 26))}-Shelf-{(idx // 26) + 1}",
                    total_copies=book_data["copies"],
                    language_id=language.id,
                    authors=[author],
                    genres=genres,
                )
                db.add(book)
                created_count += 1
                if idx % 20 == 0:
                    print(f"  ... {idx}/{len(SAMPLE_BOOKS)} books processed")
            except Exception as exc:
                failed_count += 1
                print(f"  Error with book {book_data['title']}: {exc}")

        db.commit()

        final_count = db.query(Book).count()
        author_count = db.query(Author).count()
        print(
            f"Books seeded: {created_count} added, {skipped_count} skipped, "
            f"{failed_count} failed, {final_count} total books, {author_count} authors"
        )
    except Exception as exc:
        print(f"Error populating books: {exc}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_books(reset=False)
