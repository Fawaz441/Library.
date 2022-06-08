from functools import reduce
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView
from accounts.permissions import IsAdmin, IsManager, IsStudent
from .serializers import (BookCreateSerializer,
                          BookCategoryListSerializer, BookListSerializer,
                          BookRequestSerializer, BookRequestActionSerializer,
                          BookBorrowRequestListSerializer, ManagerBookListSerializer,
                          BookLogSerializer, BookReturnSerializer, AuthorSerializer)
from .models import Category, Book, BookBorrowRequest, BookLog, APPROVED, REJECTED, PENDING
from .utils import create_book_log
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
        if book.current_borrower:
            return error_response(error="This book has been borrowed so it cannot be set as unavailable")
        if BookBorrowRequest.objects.filter(status="PENDING", book=book).count() > 0:
            return error_response(error="This book has pending borrow requests")
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
        books = Book.objects.filter(
            available=True, current_borrower__isnull=True)
        if author:
            books = books.filter(author__icontains=author)
        if name:
            books = books.filter(title__icontains=name)
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


class ManagerBookFilterAPIView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        is_available = request.GET.get('is_available')
        is_borrowed = request.GET.get('is_borrowed')
        books = Book.objects.all()
        if is_available == 'true':
            books = books.filter(available=True)
        if is_available == 'false':
            books = books.filter(available=False)
        if is_borrowed == 'true':
            books = books.filter(current_borrower__isnull=False)
        if is_borrowed == 'false':
            books = books.filter(current_borrower__isnull=True)
        data = ManagerBookListSerializer(books, many=True).data
        return success_response(data=data)


class BookBorrowRequestAPIView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        data = BookRequestSerializer(data=request.data)
        if data.is_valid():
            book = data.validated_data.get('title')
            pending_borrow_requests = BookBorrowRequest.objects.filter(
                status=PENDING, student=request.user)
            if pending_borrow_requests.count() > 0:
                return error_response(error="You already have a pending borrow request")
            prev_borrowed_book = Book.objects.filter(
                current_borrower=request.user).first()
            if prev_borrowed_book:
                return error_response(error="You have not returned this book : {}".format(prev_borrowed_book.title))
            if book.current_borrower:
                return error_response(error="You cannot borrow this book at the moment")
            BookBorrowRequest.objects.create(
                book=book,
                student=request.user,
            )
            create_book_log(book, "Student {} made a borrow request".format(
                request.user.username))
            return success_response(message="Your request has been submitted successfully")
        else:
            return error_response(error=data.errors)


class PendingBookRequests(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        pending_book_requests = BookBorrowRequest.objects.filter(
            status=PENDING
        )
        data = BookBorrowRequestListSerializer(
            pending_book_requests, many=True).data
        return success_response(data=data)


class BookBorrowRequestApproveOrReject(APIView):
    permission_classes = [IsManager]

    def post(self, request):
        data = BookRequestActionSerializer(data=request.data)
        if data.is_valid():
            action = data.validated_data.get('action')
            borrow_request = data.validated_data.get('request')
            if action == 'approve':
                borrow_request.approve()
                BookBorrowRequest.objects.filter(
                    status=PENDING, book=borrow_request.book).update(status=REJECTED)
                create_book_log(borrow_request.book, "Borrow request from {0} was approved by {1}".format(
                    borrow_request.student.username,
                    request.user.username
                ))
                return success_response(message="Request approved successfully")
            if action == 'reject':
                borrow_request.reject()
                create_book_log(borrow_request.book, "Borrow request from {0} was rejected by {1}".format(
                    borrow_request.student.username,
                    request.user.username
                ))
                return success_response(message="Request rejected successfully")
        else:
            return error_response(error=data.errors)


class BookLogs(APIView):
    permission_classes = [IsManager]

    def get(self, request, book_id):
        logs = BookLog.objects.filter(book__id=book_id)
        data = BookLogSerializer(logs, many=True).data
        return success_response(data=data)


class ReturnBook(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        data = BookReturnSerializer(data=request.data)
        if data.is_valid():
            book = data.validated_data.get('book')
            if not book.current_borrower == request.user:
                return error_response(error="Invalid. You are not currently borrowing this book")
            approved_book_request = BookBorrowRequest.objects.filter(
                book=book,
                student=request.user,
                status=APPROVED
            ).latest('approved_date')
            if(timezone.now() < (approved_book_request.approved_date + timezone.timedelta(days=3))):
                book.return_to_library()
                approved_book_request.book_returned = True
                approved_book_request.save()
                return success_response(message="Book returned successfully")
            else:
                request.user.is_active = False
                request.user.save()
                return error_response(error="You have been suspended from the library. Books are to be returned before 72 hours from the borrowed time")
        else:
            return error_response(error=data.errors)


class CreateAuthor(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        data = AuthorSerializer(data=request.data)
        if data.is_valid():
            author = data.save()
            return success_response(
                data=AuthorSerializer(author).data,
                message="Author created successfully"
            )
        return error_response(error=data.errors)
