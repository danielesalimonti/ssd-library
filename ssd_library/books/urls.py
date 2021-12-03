from django.urls import path

from .views import BookDetail, BookList, BookRent

urlpatterns = [
    path('<str:pk>/', BookDetail.as_view()), #libro specifico
    path('', BookList.as_view()), #index
    path('rent/<str:isbn>/', BookRent.rent_book), #noleggio libro
]

