from functools import reduce
from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from accounts.permissions import IsAdmin, IsManager, IsStudent
from .serializers import (BookCreateSerializer,
                          BookCategoryListSerializer, BookListSerializer)
from .models import Category, Book
from utils.response import success_response, error_response


class BookCategoryListAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        categories = Category.objects.all()
        data = BookCategoryListSerializer(categories, many=True).data
        return success_response(data=data)


class BookCreateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        data = BookCreateSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return success_response(message="Book created successfully")
        else:
            return error_response(error=data.errors)


class SetBookUnavailable(APIView):
    permission_classes = [IsManager]

    def post(self, request, book_id):
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return error_repsonse(error="This book does not exist")
        book.available = False
        book.save()
        return success_response(message="{} has been set to unavailable".format(book.title))


class SetBookAvailable(APIView):
    permission_classes = [IsManager]

    def post(self, request, book_id):
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return error_repsonse(error="This book does not exist")
        book.available = True
        book.save()
        return success_response(message="{} has been set to available".format(book.title))


class StudentBookSearchAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        get = request.GET
        author = get.get('author')
        name = get.get('name')
        year = get.get('year')
        categories = get.get('categories')
        books = Book.objects.all()
        if author:
            books = books.filter(author__iexact=author)
        if name:
            books = books.filter(title__iexact=name)
        if year:
            books = books.filter(year_published=year)
        if categories:
            split_categories = categories.split(',')
            q_list = map(lambda n: Q(categories__name__iexact=n),
                         split_categories)
            q_list = reduce(lambda a, b: a | b, q_list)
            books = books.filter(q_list)
        data = BookListSerializer(books, many=True).data
        return success_response(data=data)
