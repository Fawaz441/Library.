from rest_framework.serializers import ModelSerializer
from .models import Book, BookBorrowRequest, Category


class BookCategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']


class BookCreateSerializer(ModelSerializer):
    class Meta:
        fields = ['title', 'author', 'categories', 'year_published']
        model = Book
        extra_kwargs = {'categories': {'required': True}}


class BookListSerializer(ModelSerializer):
    categories = BookCategoryListSerializer(many=True)

    class Meta:
        fields = ['title', 'author', 'year_published', 'categories']
        model = Book
