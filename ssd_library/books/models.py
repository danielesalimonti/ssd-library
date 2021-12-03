import json

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from urllib3.util.wait import select_wait_for_socket


class Book(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True,
                            validators=[RegexValidator(regex=r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$',
                                                       message="Doesn't match ISBN pattern")])
    author = models.CharField(max_length=100,
                              validators=[RegexValidator(regex=r'^[a-zA-Z ]+$', message="Invalid author")])

    title = models.CharField(max_length=100,
                             validators=[RegexValidator(regex=r'^[a-zA-Z0-9 ]+$', message="Invalid title")])

    preview = models.CharField(max_length=60, default='',
                               validators=[
                                   RegexValidator(regex=r'^[a-zA-Z0-9,.?! ]+$', message="Invalid preview")])

    description = models.TextField(max_length=1000,
                                   validators=[
                                       RegexValidator(regex=r'^[a-zA-Z0-9,.?! ]+$', message="Invalid description")])

    published_date = models.DateField()
    num_pages = models.IntegerField(validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=10000)])

    _user_rented = models.TextField(default=json.dumps({'users': []}))

    def __str__(self):
        return str(self.title) + " - " + str(self.author)

    @property
    def user_rented(self):
        return json.loads(self._user_rented)['users']

    def add_user_rent(self, username):
        if username not in self.user_rented:
            self._user_rented = json.dumps({'users': self.user_rented + [username]})
            #TODO salvare nel db
            self.save()
            print(self._user_rented)

