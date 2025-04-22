import sqlite3
from sqlite3 import Error
import os

# Get absolute path to the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct absolute path for the database file
DB_NAME = os.path.join(BASE_DIR, "renters.db")

# Ensure the directory for the database file exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Ensure the database file exists before attempting to connect
if not os.path.exists(DB_NAME):
    open(DB_NAME, 'w').close()

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        return conn
    except Error as e:
        print(e)
    return conn

# Reinitialize the connection after ensuring the database file exists
conn = create_connection()
if conn is None:
    raise ConnectionError("Database connection could not be established.")

def create_tables():
    """ create tables for properties, bookings, and reviews """
    conn = create_connection()
    if conn is None:
        raise ConnectionError("Database connection could not be established.")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        rent INTEGER NOT NULL,
        duration TEXT NOT NULL,
        owner_contact TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        FOREIGN KEY (property_id) REFERENCES properties (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        rating INTEGER NOT NULL,
        FOREIGN KEY (property_id) REFERENCES properties (id)
    )
    """)

    conn.commit()
    conn.close()

def migrate_reviews_table():
    """ Migrate reviews table to add property_id column """
    conn = create_connection()
    cursor = conn.cursor()

    # Check if property_id column exists
    cursor.execute("PRAGMA table_info(reviews)")
    columns = [info[1] for info in cursor.fetchall()]
    if "property_id" in columns:
        conn.close()
        return  # Already migrated

    # Rename old table
    cursor.execute("ALTER TABLE reviews RENAME TO reviews_old")

    # Create new reviews table with property_id column
    cursor.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        rating INTEGER NOT NULL,
        FOREIGN KEY (property_id) REFERENCES properties (id)
    )
    """)

    # Copy data from old table to new table with default property_id = 0
    cursor.execute("""
    INSERT INTO reviews (id, review_text, rating, property_id)
    SELECT id, review_text, rating, 0 FROM reviews_old
    """)

    # Drop old table
    cursor.execute("DROP TABLE reviews_old")

    conn.commit()
    conn.close()

def get_properties(location=None, max_rent=None):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    if location:
        query += " AND location = ?"
        params.append(location)
    if max_rent:
        query += " AND rent <= ?"
        params.append(max_rent)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_booking(property_id, name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (property_id, name, email) VALUES (?, ?, ?)", (property_id, name, email))
    conn.commit()
    conn.close()

def get_bookings_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, p.name, p.location, p.rent, p.duration
        FROM bookings b
        JOIN properties p ON b.property_id = p.id
        WHERE b.email = ?
    """, (email,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def cancel_booking(booking_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

def insert_review(property_id, review_text, rating):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (property_id, review_text, rating) VALUES (?, ?, ?)", (property_id, review_text, rating))
    conn.commit()
    conn.close()

def update_owner_contact():
    """Update owner_contact email for 'Student PG in Vadodara' property"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE properties
        SET owner_contact = ?
        WHERE name = ?
    """, ("abhinav15102003@gmail.com", "Student PG in Vadodara"))
    conn.commit()
    conn.close()

def initialize_sample_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_data = [
            ("Student PG in Vadodara", "Vadodara", 6000, "1 Month", "abhinav15102003@gmail.com"),
            ("1BHK near MSU", "Vadodara", 12000, "3 Months", "Kishan_houses@gmail.com"),
            ("Shared Hostel Room", "Mumbai", 5000, "6 Months", "satyam_pgs@gmail.com"),
            ("2BHK Apartment", "Ahmedabad", 18000, "12 Months", "vijay.rentals@example.com"),
            ("Studio Apartment", "Vadodara", 8000, "3 Months", "info@modernliving.in"),
            ("IIT kanpur", "kanpur (dehat)", 1000, "1 week", "vimal.tiwari@gmail.com")
        ]
        cursor.executemany("INSERT INTO properties (name, location, rent, duration, owner_contact) VALUES (?, ?, ?, ?, ?)", sample_data)
        conn.commit()
    conn.close()

# Initialize tables and sample data on import
create_tables()
migrate_reviews_table()
initialize_sample_data()
update_owner_contact()
