class Borrower:
    def __init__(self, borrower_info):
        self.first_name = borrower_info[0]
        self.last_name = borrower_info[1]
        self.email = borrower_info[2]

    def get_borrower_info_from_user():
        borrower_info = []

        borrower_info.append(input("First Name: "))
        borrower_info.append(input("Last Name: "))
        borrower_info.append(input("Email: "))

        return borrower_info
