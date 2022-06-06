from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"


class Category(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Author(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500, unique=True)
    authors = models.ManyToManyField(Author, blank=True)
    created = models.DateTimeField(auto_now=True)
    current_borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    available = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        Category)
    year_published = models.IntegerField()

    def __str__(self):
        return self.title

    def return_to_library(self):
        self.current_borrower = None
        self.available = True
        self.save()


BORROW_REQUEST_STATUS_CHOICES = (
    (PENDING, PENDING),
    (APPROVED, APPROVED),
    (REJECTED, REJECTED),
)


class BookBorrowRequest(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='book_borrow_requests')
    status = models.CharField(
        choices=BORROW_REQUEST_STATUS_CHOICES, default=PENDING, max_length=100)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    book_returned = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username if self.student else str(self.id)

    def approve(self):
        self.status = APPROVED
        self.approved_date = timezone.now()
        self.save()
        self.book.current_borrower = self.student
        self.book.save()

    def reject(self):
        self.status = REJECTED
        self.save()


class BookLog(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='logs')
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
