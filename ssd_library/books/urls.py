from django.urls import path

from .views import BookDetail, BookList, BookRent, BookRentedList, BookListAdmin, BookRentedDetail

urlpatterns = [
    path('<str:pk>/', BookDetail.as_view()), #libro specifico
    path('', BookList.as_view(), name='books'), #index
    path('my-books', BookRentedList.as_view(), name='my-books'),
    path('rent/<str:isbn>/', BookRent.rent_book), #noleggio libro
    path('admin/<str:pk>/', BookListAdmin.as_view()),
    path('my-book/<str:pk>/', BookRentedDetail.as_view())
]

