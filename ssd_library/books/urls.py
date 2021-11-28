from django.urls import path

from books.views import BookDetail, BookList

urlpatterns = [
    path('<int:pk>/', BookDetail.as_view()),
    path('', BookList.as_view()),
]

