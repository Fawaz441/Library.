from .views import (BookCreateAPIView, BookCategoryListAPIView,
                    SetBookUnavailable, SetBookAvailable, StudentBookSearchAPIView)
from django.urls import path

urlpatterns = [
    path('create', BookCreateAPIView.as_view()),
    path('categories', BookCategoryListAPIView.as_view()),
    path('set-book-unavailable/<int:book_id>', SetBookUnavailable.as_view()),
    path('set-book-available/<int:book_id>', SetBookAvailable.as_view()),
    path('filter-books', StudentBookSearchAPIView.as_view())
]
