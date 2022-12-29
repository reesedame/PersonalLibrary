import os
from personalLibrary import PersonalLibrary
from book import Book
from borrower import Borrower
from loan import Loan


def display_main_menu():
    print("\n" + "* * * MAIN MENU * * *" + "\n")
    print("1. Books")
    print("2. Borrowers")
    print("3. Loans")
    print("4. Quit")
    print("\n" + "* * * * * * * * * * *" + "\n")


def display_book_menu():
    print("\n" + "* * * BOOK MENU * * *" + "\n")
    print("1. Add book")
    print("2. Remove book")
    print("3. View books")
    print("4. Go back to main menu")
    print("\n" + "* * * * * * * * * * *" + "\n")


def display_view_books_menu():
    print("\n" + "* * BOOK DISPLAY MENU * *" + "\n")
    print("1. View all books")
    print("2. View available books")
    print("3. View loaned books")
    print("\n" + "* * * * * * * * * * *" + "\n")


def print_books(books):
    print("\nBooks:\n")
    for book in books:
        print(book[0])
        print("By: " + book[1])
        print("\n")


def display_borrowers_menu():
    print("\n" + "* * BORROWER MENU * *" + "\n")
    print("1. Add borrower")
    print("2. Remove borrower")
    print("3. View borrowers")
    print("4. Go back to main menu")
    print("\n" + "* * * * * * * * * * *" + "\n")


def print_borrowers(borrowers):
    print("\nBorrowers:\n")
    for borrower in borrowers:
        print("Name: " + borrower[0] + " " + borrower[1])
        print("Email: " + borrower[2])
        print("\n")


def display_view_loans_menu():
    print("\n" + "* * LOAN VIEW MENU * *" + "\n")
    print("1. View all loans")
    print("2. View current loans")
    print("3. View completed loans")
    print("\n" + "* * * * * * * * * * *" + "\n")


def display_loan_menu():
    print("\n" + "* * * LOAN MENU * * *" + "\n")
    print("1. Add loan")
    print("2. Cancel loan")
    print("3. Complete loan")
    print("4. View loans")
    print("5. Go back to main menu")
    print("\n" + "* * * * * * * * * * *" + "\n")


def print_loans(loans):
    print("\nLoans:\n")
    for loan in loans:
        print("Loan_id: " + str(loan[0]))
        print("Book: " + loan[1])
        print("Borrower: " + loan[2] + " " + loan[3])
        if loan[4] == 1:
            print("Returned: True")
        else:
            print("Returned: False")
        print("\n")


def main():
    if os.path.isfile("personalLibrary.db"):
        library = PersonalLibrary()
        print("Hello and welcome back to your personal library!")
    else:
        library = PersonalLibrary()
        library.initialize_tables()

    while True:
        display_main_menu()
        menu_option = (input("Menu option: ")).strip()

        # Books
        if menu_option == "1":
            display_book_menu()
            menu_option = (input("Menu option: ")).strip()

            # Add book
            if menu_option == "1":
                new_book_info = Book.get_book_info_from_user()
                new_book = Book(new_book_info)
                library.add_book(new_book)
                print(
                    "{title} has been added to your library".format(
                        title=new_book.title
                    )
                )
            # Remove book
            elif menu_option == "2":
                book_to_remove = input(
                    "What is the title of the book you want to remove?: "
                )
                library.remove_book(book_to_remove)
                print(
                    "{title} has been removed from your library".format(
                        title=book_to_remove
                    )
                )
            # View books
            elif menu_option == "3":
                display_view_books_menu()
                menu_option = (input("Menu option: ")).strip()

                # View all books
                if menu_option == "1":
                    print_books(library.get_books_by_status())
                # View available books
                elif menu_option == "2":
                    print_books(library.get_books_by_status(1))
                # View loaned books
                elif menu_option == "3":
                    print_books(library.get_books_by_status(0))
            # Go back to main menu
            elif menu_option == "4":
                pass

        # Borrowers
        elif menu_option == "2":
            display_borrowers_menu()
            menu_option = (input("Menu option: ")).strip()

            # Add borrower
            if menu_option == "1":
                new_borrower_info = Borrower.get_borrower_info_from_user()
                new_borrower = Borrower(new_borrower_info)
                library.add_borrower(new_borrower)
                print(
                    "{first_name} {last_name} has been added to your borrowers".format(
                        first_name=new_borrower.first_name,
                        last_name=new_borrower.last_name,
                    )
                )
            # Remove borrower
            elif menu_option == "2":
                borrower_to_remove_fname = input(
                    "What is the first name of the borrower you want to remove?: "
                )
                borrower_to_remove_lname = input(
                    "What is the last name of the borrower you want to remove?: "
                )
                library.remove_borrower(
                    borrower_to_remove_fname, borrower_to_remove_lname
                )
                print(
                    "{first_name} {last_name} has been removed from your library".format(
                        first_name=borrower_to_remove_fname,
                        last_name=borrower_to_remove_lname,
                    )
                )
            # View borrowers
            elif menu_option == "3":
                print_borrowers(library.get_all_borrowers())
            # Go back to main menu
            elif menu_option == "4":
                pass

        # Loans
        elif menu_option == "3":
            display_loan_menu()
            menu_option = menu_option = (input("Menu option: ")).strip()

            # Add loan
            if menu_option == "1":
                new_loan_info = Loan.get_loan_info_from_user()
                new_loan = Loan(new_loan_info)
                library.add_loan(new_loan)
                print(
                    "A new loan has been added that shows {borrower} is borrowing {title}".format(
                        borrower=new_loan.borrower, title=new_loan.book
                    )
                )
            # Cancel loan
            elif menu_option == "2":
                loan_id_to_be_removed = input("Loan_id: ")
                library.remove_loan(loan_id_to_be_removed)
                print(
                    "Loan with id {loan_id} has been cancelled. Book status has been updated to available.".format(
                        loan_id=loan_id_to_be_removed
                    )
                )
            # Complete loan
            elif menu_option == "3":
                loan_id_to_be_completed = input("Loan_id: ")
                library.complete_loan(loan_id_to_be_completed)
                print(
                    "Loan with id {loan_id} has been set to returned. Book status has been updated to available.".format(
                        loan_id=loan_id_to_be_completed
                    )
                )
            # View loans
            elif menu_option == "4":
                display_view_loans_menu()
                menu_option = (input("Menu option: ")).strip()

                # View all loans
                if menu_option == "1":
                    print_loans(library.get_loans_by_status())
                # View current loans
                elif menu_option == "2":
                    print_loans(library.get_loans_by_status(0))
                # View completed loans
                elif menu_option == "3":
                    print_loans(library.get_loans_by_status(1))
            # Go back to main menu
            elif menu_option == "5":
                pass

        # Exit
        elif menu_option == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number from the provided menu.")


main()
