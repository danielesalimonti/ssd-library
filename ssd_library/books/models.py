from django.db import models


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField()
    num_pages = models.IntegerField()

    def __str__(self):
        return self.title + " - " + self.author
