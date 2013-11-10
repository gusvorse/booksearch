from django.contrib import admin
from books.models import Publisher, Author, Book, Review

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
