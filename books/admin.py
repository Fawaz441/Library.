from django.contrib import admin
from .models import BookBorrowRequest, Book, BookLog, Category, Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'created',
                    'current_borrower', 'available', 'year_published']


class BookBorrowRequestAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'status',
                    'created', 'approved_date', 'book_returned']


class BookLogAdmin(admin.ModelAdmin):
    list_display = ['book', 'text', 'created']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookBorrowRequest, BookBorrowRequestAdmin)
