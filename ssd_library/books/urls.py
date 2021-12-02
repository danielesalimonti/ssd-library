from django.urls import path

from .views import BookDetail, BookList

urlpatterns = [
    path('<int:pk>/', BookDetail.as_view()),
    path('', BookList.as_view()),
]

