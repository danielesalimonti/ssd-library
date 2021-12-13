import json
import random
import string

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def books(db):
    return [
        mixer.blend('books.Book'),
        mixer.blend('books.Book'),
        mixer.blend('books.Book'),
    ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def test_books_get_list_not_authenticated(books):
    path = reverse('books')
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_books_get_list_authenticated(books):
    path = reverse('books')
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK


def test_get_non_mine_book(books):
    path = reverse('my-books') + books[0].ISBN + '/'
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_rent_and_get_mine_book(books):
    path = '/api/v1/rent/' + books[0].ISBN + '/'
    user = mixer.blend(get_user_model())
    client = get_client(user)
    client.get(path)
    path = reverse('my-books') + books[0].ISBN + '/'
    response = client.get(path)
    print(books[0].ISBN)
    assert response.status_code == HTTP_200_OK


def test_rent_book_not_authenticated(books):
    path = '/api/v1/rent/' + books[0].ISBN + '/'
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN


def test_rent_non_existent_book(books):
    path = '/api/v1/rent/' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) + '/'
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_404_NOT_FOUND
