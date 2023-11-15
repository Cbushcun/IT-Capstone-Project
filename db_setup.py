import sqlite3

def setup_database():
    # Create and connect to the SQLite database
    conn = sqlite3.connect("auction_website.db")
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            phone_number TEXT
        )
    ''')

    # Create Roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Roles (
            role_id INTEGER PRIMARY KEY,
            role_name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create UserRoles table to map users to roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserRoles (
            user_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users (user_id),
            FOREIGN KEY (role_id) REFERENCES Roles (role_id)
        )
    ''')

    # Create Auctions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Auctions (
            auction_id INTEGER PRIMARY KEY,
            seller_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            reserve_price REAL,
            FOREIGN KEY (seller_id) REFERENCES Users (user_id)
        )
    ''')

    # Create Bids table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bids (
            bid_id INTEGER PRIMARY KEY,
            auction_id INTEGER,
            user_id INTEGER,
            bid_amount REAL NOT NULL,
            timestamp DATETIME NOT NULL,
            status TEXT,
            FOREIGN KEY (auction_id) REFERENCES Auctions (auction_id),
            FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
    ''')

    # Create Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create Tags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
            tag_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create AuctionCategories table to associate auctions with categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AuctionCategories (
            auction_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (auction_id) REFERENCES Auctions (auction_id),
            FOREIGN KEY (category_id) REFERENCES Categories (category_id)
        )
    ''')

    # Create AuctionTags table to associate auctions with tags
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AuctionTags (
            auction_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (auction_id) REFERENCES Auctions (auction_id),
            FOREIGN KEY (tag_id) REFERENCES Tags (tag_id)
        )
    ''')

    # Create Sessions table for user authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            expiration DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
    ''')

    # Create Admin role and assign it to the admin user
    cursor.execute("INSERT OR IGNORE INTO Roles (role_name) VALUES ('Admin')")
    cursor.execute("SELECT user_id FROM Users WHERE username = 'admin'")
    admin_user_id = cursor.fetchone()
    if admin_user_id:
        cursor.execute("INSERT OR IGNORE INTO UserRoles (user_id, role_id) VALUES (?, (SELECT role_id FROM Roles WHERE role_name = 'Admin'))", (admin_user_id[0],))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
