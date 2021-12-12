import json

from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Book
from .permissions import AreRentedBook
from .serializers import BookSerializer, BookSerializerForRentedBooks
from django.http import HttpResponse


class BookListAdmin(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRentedList(generics.ListAPIView):
    serializer_class = BookSerializerForRentedBooks
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(_user_rented__contains=self.request.user)


class BookRentedDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializerForRentedBooks
    permission_classes = [AreRentedBook, IsAuthenticated]


class BookRent:

    @staticmethod
    def rent_book(request, isbn):
        if request.user.is_authenticated:
            try:
                book = Book.objects.get(ISBN=isbn)
            except Book.DoesNotExist:
                return HttpResponse(json.dumps({'detail': 'Book not found'}), content_type="application/json",
                                    status=404)

            book.add_user_rent(str(request.user))
            return redirect('/../../api/v1/')

        return HttpResponse(json.dumps({'detail': 'Authentication credentials were not provided.'}),
                            content_type="application/json", status=403)
