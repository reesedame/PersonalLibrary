import sqlite3
from book import Book
from borrower import Borrower
from loan import Loan


class PersonalLibrary:
    def __init__(self):
        self.conn = sqlite3.connect("personalLibrary.db")
        self.c = self.conn.cursor()

    def initialize_tables(self):
        # Creates table books for all books the user owns
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS books(
            book_id integer PRIMARY KEY,
            title text NOT NULL,
            author text,
            status integer
        )"""
        )

        # Creates table borrowers for those who will be borrowing books
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS borrowers(
            borrower_id integer PRIMARY KEY,
            first_name text,
            last_name text,
            email text
        )"""
        )

        # Creates table loans for loans - keeping track of which book & who borrowed it
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS loans(
                loan_id integer PRIMARY KEY,
                book_id integer NOT NULL,
                borrower_id integer NOT NULL,
                returned integer,
                FOREIGN KEY (book_id) REFERENCES myLibrary (book_id),
                FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id)
        )"""
        )

    def get_book_id(self, title):
        with self.conn:
            self.c.execute(
                "SELECT book_id FROM books WHERE title=:title", {"title": title}
            )
            return self.c.fetchall()

    def get_borrower_id(self, name):
        name_list = name.split()

        with self.conn:
            self.c.execute(
                "SELECT borrower_id FROM borrowers WHERE first_name=:first_name AND last_name=:last_name",
                {"first_name": name_list[0], "last_name": name_list[1]},
            )
            return self.c.fetchall()

    # Functions for books table

    def add_book(self, book):
        with self.conn:
            self.c.execute(
                "INSERT INTO books VALUES (:book_id, :title, :author, :status)",
                {
                    "book_id": None,
                    "title": book.title,
                    "author": book.author,
                    "status": book.status,
                },
            )

    def remove_book(self, book_title):
        with self.conn:
            self.c.execute(
                "DELETE FROM books WHERE title=:title",
                {"title": book_title},
            )

    def get_books_by_status(self, book_status="Not specified"):
        # If optional parameter is not given, all books are returned
        if book_status == "Not specified":
            self.c.execute("SELECT title, author FROM books")
            return self.c.fetchall()

        # If book_status == 0, ie book is not available
        # All loaned books are returned
        elif book_status == 0:
            self.c.execute("SELECT title, author FROM books WHERE status=0")
            return self.c.fetchall()

        # Else all books that are available are returned
        else:
            self.c.execute("SELECT title, author FROM books WHERE status=1")
            return self.c.fetchall()

    # Functions for borrowers table

    def add_borrower(self, borrower):
        with self.conn:
            self.c.execute(
                "INSERT INTO borrowers VALUES (:borrower_id, :first_name, :last_name, :email)",
                {
                    "borrower_id": None,
                    "first_name": borrower.first_name,
                    "last_name": borrower.last_name,
                    "email": borrower.email,
                },
            )

    def remove_borrower(self, borrower_fname, borrower_lname):
        with self.conn:
            self.c.execute(
                "DELETE FROM borrowers WHERE first_name=:first_name AND last_name=:last_name",
                {"first_name": borrower_fname, "last_name": borrower_lname},
            )

    def get_all_borrowers(self):
        self.c.execute(
            "SELECT first_name, last_name, email FROM borrowers ORDER BY last_name"
        )
        return self.c.fetchall()

    # Functions for loans table

    def add_loan(self, loan):
        book_id = self.get_book_id(loan.book)[0][0]
        borrower_id = self.get_borrower_id(loan.borrower)[0][0]

        with self.conn:
            self.c.execute(
                "INSERT INTO loans VALUES (:loan_id, :book_id, :borrower_id, :returned)",
                {
                    "loan_id": None,
                    "book_id": book_id,
                    "borrower_id": borrower_id,
                    "returned": 0,
                },
            )
            self.c.execute(
                "UPDATE books SET status=0 WHERE book_id=:book_id", {"book_id": book_id}
            )

    def remove_loan(self, loan_id):
        with self.conn:
            self.c.execute(
                "UPDATE books SET status=1 WHERE book_id IN (SELECT book_id FROM loans WHERE loan_id=:loan_id)",
                {"loan_id": loan_id},
            )
            self.c.execute(
                "DELETE FROM loans WHERE loan_id=:loan_id", {"loan_id": loan_id}
            )

    def complete_loan(self, loan_id):
        with self.conn:
            self.c.execute(
                "UPDATE books SET status=1 WHERE book_id IN (SELECT book_id FROM loans WHERE loan_id=:loan_id)",
                {"loan_id": loan_id},
            )
            self.c.execute(
                "UPDATE loans SET returned=1 WHERE loan_id=:loan_id",
                {"loan_id": loan_id},
            )

    def get_loans_by_status(self, loan_status="Not specified"):
        # If optional parameter is not given, all loans are returned
        if loan_status == "Not specified":
            self.c.execute(
                """SELECT
                    loans.loan_id,
                    books.title,
                    borrowers.first_name,
                    borrowers.last_name,
                    loans.returned
                FROM loans
                JOIN books
                    ON loans.book_id = books.book_id
                JOIN borrowers
                    ON loans.borrower_id = borrowers.borrower_id;"""
            )
            return self.c.fetchall()
        # If loan_status == 0, ie the book has not been returned
        # All active loans are returned
        elif loan_status == 0:
            self.c.execute(
                """SELECT
                    loans.loan_id,
                    books.title,
                    borrowers.first_name,
                    borrowers.last_name,
                    loans.returned
                FROM loans
                JOIN books
                    ON loans.book_id = books.book_id
                JOIN borrowers
                    ON loans.borrower_id = borrowers.borrower_id
                WHERE loans.returned = 0;"""
            )
            return self.c.fetchall()
        # If loan_status == 1, ie the book has been returned
        # All completed loans are returned
        elif loan_status == 1:
            self.c.execute(
                """SELECT
                    loans.loan_id,
                    books.title,
                    borrowers.first_name,
                    borrowers.last_name,
                    loans.returned
                FROM loans
                JOIN books
                    ON loans.book_id = books.book_id
                JOIN borrowers
                    ON loans.borrower_id = borrowers.borrower_id
                WHERE loans.returned = 1;"""
            )
            return self.c.fetchall()
