from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Book(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True,
                            validators=[RegexValidator(regex=r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$',
                                                       message="Doesn't match ISBN pattern")])
    author = models.CharField(max_length=100,
                              validators=[RegexValidator(regex=r'^[a-zA-Z ]+$', message="Invalid author")])

    title = models.CharField(max_length=100,
                             validators=[RegexValidator(regex=r'^[a-zA-Z0-9 ]+$', message="Invalid title")])

    preview = models.CharField(max_length=60,
                               validators=[
                                   RegexValidator(regex=r'^[a-zA-Z0-9,.?! ]+$', message="Invalid preview")])

    description = models.TextField(max_length=1000,
                                   validators=[
                                       RegexValidator(regex=r'^[a-zA-Z0-9,.?! ]+$', message="Invalid description")])

    published_date = models.DateField()
    num_pages = models.IntegerField(validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=10000)])

    def __str__(self):
        return self.title + " - " + self.author


class BookPurchase(models.Model):
    book = models.ForeignKey(to=Book)

    #purchased_by = models.charField()
