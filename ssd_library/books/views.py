from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics

from .models import Book
from .permissions import AreRentedBook
from .serializers import BookSerializer, BookSerializerForRentedBooks
from django.http import HttpResponse


class BookListAdmin(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRentedList(generics.ListAPIView):
    serializer_class = BookSerializerForRentedBooks

    def get_queryset(self):
        return Book.objects.filter(_user_rented__contains=self.request.user)


class BookRentedDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializerForRentedBooks
    permission_classes = [AreRentedBook]


class BookRent:

    @staticmethod
    def rent_book(request, isbn):
        book = Book.objects.get(ISBN=isbn)
        response = HttpResponse()
        if book is None:
            response.status_code = 404
            return response
        else:
            response.status_code = 200

        book.add_user_rent(str(request.user))
        return redirect('/../../api/v1/')
