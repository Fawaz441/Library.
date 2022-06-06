from django.shortcuts import reverse
from rest_framework.serializers import (
    ModelSerializer, Serializer, CharField, ValidationError, IntegerField, HyperlinkedRelatedField,
    SerializerMethodField, DateTimeField)
from accounts.serializers import StudentSerializer
from .models import (Book, BookBorrowRequest, Category,
                     Author, PENDING, BookLog)


class BookCategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']


class BookCreateSerializer(ModelSerializer):
    class Meta:
        fields = ['title', 'authors', 'categories', 'year_published']
        model = Book
        extra_kwargs = {'categories': {'required': True},
                        'authors': {'required': True}}


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'id']


class BookListSerializer(ModelSerializer):
    categories = BookCategoryListSerializer(many=True)
    authors = AuthorSerializer(many=True)

    class Meta:
        fields = ['title', 'authors', 'year_published', 'categories', 'id']
        model = Book


class ManagerBookListSerializer(BookListSerializer):
    logs = SerializerMethodField()

    class Meta(BookListSerializer.Meta):
        fields = BookListSerializer.Meta.fields + ['logs']
        model = Book

    def get_logs(self, book):
        return reverse('books:logs', kwargs={'book_id': book.id})


class BookRequestSerializer(Serializer):
    title = CharField()

    def validate_title(self, title):
        book = Book.objects.filter(title__iexact=title).first()
        if not book:
            raise ValidationError("This book does not exist")
        return book


class BookRequestActionSerializer(Serializer):
    action = CharField()
    request = IntegerField()

    def validate_action(self, action):
        if not action in ['reject', 'approve']:
            raise ValidationError(
                "Invalid action. Must be either 'approve' or 'reject' ")
        return action

    def validate_request(self, request):
        print(request)
        book_borrow_request = BookBorrowRequest.objects.filter(
            id=request, status=PENDING).first()
        if not book_borrow_request:
            raise ValidationError(
                "This request does not exist or has already been sorted out.")
        return book_borrow_request


class BookBorrowRequestListSerializer(ModelSerializer):
    book = BookListSerializer()
    student = StudentSerializer()

    class Meta:
        model = BookBorrowRequest
        fields = ['book', 'created', 'student', 'id']


class BookLogSerializer(ModelSerializer):
    timestamp = DateTimeField(source='created')

    class Meta:
        model = BookLog
        fields = ['text', 'timestamp']


class BookReturnSerializer(Serializer):
    book = IntegerField()

    def validate_book(self, b):
        book = Book.objects.filter(id=b).first()
        if not book:
            raise ValidationError("Book does not exist", "book")
        return book
