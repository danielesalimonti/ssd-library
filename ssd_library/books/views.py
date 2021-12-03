from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics

from .models import Book
from .serializers import BookSerializer
from django.http import HttpResponse


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRent(generics.UpdateAPIView):
    @staticmethod
    def rent_book(request, isbn):
        book = Book.objects.filter(ISBN=isbn)
        response = HttpResponse()
        if len(book) == 0:
            response.status_code = 404
        else:
            response.status_code = 200

        Book(book).add_user_rent(str(request.user))
        return response
