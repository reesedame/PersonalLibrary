class Book:
    def __init__(self, book_info):
        self.title = book_info[0]
        self.author = book_info[1]
        self.status = 1

    def get_book_info_from_user():
        book_info = []

        book_info.append(input("Title: "))
        book_info.append(input("Author: "))

        return book_info
