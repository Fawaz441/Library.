from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500, unique=True)
    author = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now=True)
    current_borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    available = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        Category)
    year_published = models.IntegerField()

    def __str__(self):
        return self.title


BORROW_REQUEST_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("APPROVED", "APPROVED"),
    ("REJECTED", "REJECTED"),
)


class BookBorrowRequest(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='book_borrow_requests')
    status = models.CharField(
        choices=BORROW_REQUEST_STATUS_CHOICES, default="PENDING", max_length=100)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.id if self.student else self.id
