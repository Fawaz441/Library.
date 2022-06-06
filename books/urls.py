from .views import (BookCreateAPIView, BookCategoryListAPIView,
                    SetBookUnavailable, SetBookAvailable, StudentBookSearchAPIView,
                    ManagerBookFilterAPIView, BookBorrowRequestAPIView,
                    BookBorrowRequestApproveOrReject, PendingBookRequests,
                    BookLogs, ReturnBook, CreateAuthor)
from django.urls import path

urlpatterns = [
    path('create', BookCreateAPIView.as_view()),
    path('categories', BookCategoryListAPIView.as_view()),
    path('set-book-unavailable/<int:book_id>', SetBookUnavailable.as_view()),
    path('set-book-available/<int:book_id>', SetBookAvailable.as_view()),
    path('filter-books', StudentBookSearchAPIView.as_view()),
    path('manager/filter-books', ManagerBookFilterAPIView.as_view()),
    path('request', BookBorrowRequestAPIView.as_view()),
    path('handle-request', BookBorrowRequestApproveOrReject.as_view()),
    path('pending-requests', PendingBookRequests.as_view()),
    path('<int:book_id>/logs', BookLogs.as_view(), name='logs'),
    path('return-book', ReturnBook.as_view()),
    path('create-author', CreateAuthor.as_view())
]
