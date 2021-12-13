import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


def test_book_ISBN_doesnt_mach_pattern(db):
    book = mixer.blend('books.Book', ISBN='978-3-16-148410-0edd')
    try:
        book.full_clean(exclude=['title', 'preview', 'author', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_author_more_than_50_char(db):
    book = mixer.blend('books.Book', author='A'*51)
    try:
        book.full_clean(exclude=['title', 'preview', 'ISBN', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_author_with_special_char(db):
    book = mixer.blend('books.Book', author='ciao ?!')
    try:
        book.full_clean(exclude=['title', 'preview', 'ISBN', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_title_more_than_50_char(db):
    book = mixer.blend('books.Book', title='A'*51)
    try:
        book.full_clean(exclude=['author', 'preview', 'ISBN', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_title_special_char(db):
    book = mixer.blend('books.Book', title='<script>alert(42)</script>')
    try:
        book.full_clean(exclude=['author', 'preview', 'ISBN', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_preview_special_char(db):
    book = mixer.blend('books.Book', preview='<script>alert(42)</script>')
    try:
        book.full_clean(exclude=['author', 'title', 'ISBN', 'num_pages', 'text', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_text_special_char(db):
    book = mixer.blend('books.Book', text='<script>alert(42)</script>')
    try:
        book.full_clean(exclude=['author', 'title', 'ISBN', 'num_pages', 'preview', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_zero_num_pages(db):
    book = mixer.blend('books.Book', num_pages=0)
    try:
        book.full_clean(exclude=['author', 'title', 'ISBN', 'text', 'preview', 'published_date'])
        assert False
    except ValidationError:
        assert True


def test_too_much_num_pages(db):
    book = mixer.blend('books.Book', num_pages=9999999999999)
    try:
        book.full_clean(exclude=['author', 'title', 'ISBN', 'text', 'preview', 'published_date'])
        assert False
    except ValidationError:
        assert True






