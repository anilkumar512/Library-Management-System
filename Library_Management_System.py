from time import sleep


import sqlite3

class LibraryDB:
    def __init__(self):
        self.conn = sqlite3.connect("library.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # books table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS books (
                            title TEXT PRIMARY KEY,
                            total_copies INTEGER,
                            available_copies INTEGER)''')

        # members table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS members (
                            member_id TEXT PRIMARY KEY,
                            name TEXT)''')

        # borrowed books table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS borrowed (
                            member_id TEXT,
                            book_title TEXT,
                            PRIMARY KEY(member_id, book_title),
                            FOREIGN KEY(member_id) REFERENCES members(member_id),
                            FOREIGN KEY(book_title) REFERENCES books(title))''')

        self.conn.commit()

    def add_book(self, title, copies):
        self.cur.execute("SELECT * FROM books WHERE title=?", (title,))
        result = self.cur.fetchone()
        if result:
            self.cur.execute("UPDATE books SET total_copies=total_copies+?, available_copies=available_copies+? WHERE title=?",
                             (copies, copies, title))
        else:
            self.cur.execute("INSERT INTO books (title, total_copies, available_copies) VALUES (?, ?, ?)",
                             (title, copies, copies))
        self.conn.commit()
        sleep(0.2)
        print(f"{copies} copy/copies of '{title}' added.\n")

    def register_member(self, member_id, name):
        self.cur.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
        sleep(0.2)
        if self.cur.fetchone():
            print("Member already exists!\n")
        else:
            self.cur.execute("INSERT INTO members (member_id, name) VALUES (?, ?)", (member_id, name))
            self.conn.commit()
            print(f"Member '{name}' registered successfully.\n")

    def borrow_book(self, member_id, title):
        self.cur.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
        sleep(0.2)
        if not self.cur.fetchone():
            print("Member not registered.\n")
            return
        self.cur.execute("SELECT available_copies FROM books WHERE title=?", (title,))
        book = self.cur.fetchone()
        if not book:
            print("Book not found.\n")
            return
        if book[0] <= 0:
            print(f"'{title}' is currently unavailable.\n")
            return
        self.cur.execute("SELECT * FROM borrowed WHERE member_id=? AND book_title=?", (member_id, title))
        if self.cur.fetchone():
            print(f"Book already borrowed by this member.\n")
            return
        self.cur.execute("INSERT INTO borrowed (member_id, book_title) VALUES (?, ?)", (member_id, title))
        self.cur.execute("UPDATE books SET available_copies = available_copies - 1 WHERE title=?", (title,))
        self.conn.commit()
        print(f"'{title}' issued to Member ID {member_id}.\n")

    def return_book(self, member_id, title):
        self.cur.execute("SELECT * FROM borrowed WHERE member_id=? AND book_title=?", (member_id, title))
        sleep(0.2)
        if not self.cur.fetchone():
            print("This book was not borrowed by the member.\n")
            return
        self.cur.execute("DELETE FROM borrowed WHERE member_id=? AND book_title=?", (member_id, title))
        self.cur.execute("UPDATE books SET available_copies = available_copies + 1 WHERE title=?", (title,))
        self.conn.commit()
        print(f"'{title}' returned by Member ID {member_id}.\n")

    def view_books(self):
        sleep(0.2)
        print("\nAvailable Books:")
        for row in self.cur.execute("SELECT * FROM books"):
            sleep(0.4)
            print(f"{row[0]} (Available: {row[2]}/{row[1]})")
        print()

    def view_members(self):
        sleep(0.2)
        print("\nRegistered Members:")
        for row in self.cur.execute("SELECT * FROM members"):
            sleep(0.4)
            print(f"{row[1]} (ID: {row[0]})")
        print()

    def view_borrowed_books(self):
        sleep(0.2)
        print("\nBorrowed Books:")
        for row in self.cur.execute('''
            SELECT members.name, borrowed.book_title 
            FROM borrowed 
            JOIN members ON borrowed.member_id = members.member_id
        '''):
            sleep(0.4)
            print(f"{row[0]} borrowed '{row[1]}'")
        print()

    def close(self):
        self.conn.close()

def main():
    db = LibraryDB()
    while True:
        print("====== Library Management with SQLite ======")
        sleep(0.4)
        print("1. Add Book")
        sleep(0.4)
        print("2. Register Member")
        sleep(0.4)
        print("3. Borrow Book")
        sleep(0.4)
        print("4. Return Book")
        sleep(0.4)
        print("5. View Available Books")
        sleep(0.4)
        print("6. View Members")
        sleep(0.4)
        print("7. View Borrowed Books")
        sleep(0.4)
        print("8. Exit")
        sleep(0.4)
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            sleep(0.1)
            title = input("Enter book title: ")
            sleep(0.1)
            copies = int(input("Enter number of copies: "))
            db.add_book(title, copies)

        elif choice == '2':
            sleep(0.1)
            member_id = input("Enter member ID: ")
            sleep(0.1)
            name = input("Enter member name: ")
            db.register_member(member_id, name)

        elif choice == '3':
            sleep(0.1)
            member_id = input("Enter member ID: ")
            sleep(0.1)
            title = input("Enter book title to borrow: ")
            db.borrow_book(member_id, title)

        elif choice == '4':
            sleep(0.1)
            member_id = input("Enter member ID: ")
            sleep(0.1)
            title = input("Enter book title to return: ")
            db.return_book(member_id, title)

        elif choice == '5':
            db.view_books()

        elif choice == '6':
            db.view_members()

        elif choice == '7':
            db.view_borrowed_books()

        elif choice == '8':
            db.close()
            sleep(0.1)
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Try again!\n")



main()
