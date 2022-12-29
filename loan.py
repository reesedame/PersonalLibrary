class Loan:
    def __init__(self, loan_info):
        self.book = loan_info[0]
        self.borrower = loan_info[1]

    def get_loan_info_from_user():
        loan_info = []

        loan_info.append(input("Title: "))
        loan_info.append(input("Borrower fullname: "))

        return loan_info
