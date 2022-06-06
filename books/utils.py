from books.models import BookLog


def create_book_log(book, text):
    BookLog.objects.create(book=book, text=text)
