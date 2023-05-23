from django.urls import path, include
from .views import BookAPI, BooksAPI, helloAPI, bookAPI, booksAPI

urlpatterns = [
    path("hello/", helloAPI),
    path("fbv/books/", booksAPI),
    path("fbv/book/<int:bid>/", bookAPI),
    path("fbv/Books/", BooksAPI.as_view()),
    path("fbv/Book/<int:bid>/", BookAPI.as_view()),
]

