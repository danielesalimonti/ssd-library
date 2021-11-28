from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ISBN', 'title', 'author', 'description', 'num_pages', 'published_date')
        model = Book