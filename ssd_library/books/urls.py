from django.urls import path

from .views import BookDetail, BookList, BookRent, BookRentedList, BookListAdmin

urlpatterns = [
    path('<str:pk>/', BookDetail.as_view()), #libro specifico
    path('', BookList.as_view()), #index
    path('my-books', BookRentedList.as_view()),
    path('rent/<str:isbn>/', BookRent.rent_book), #noleggio libro
    path('admin/<str:pk>/', BookListAdmin.as_view())
]

