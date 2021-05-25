from django.contrib import admin
from django.urls import path
from .views import book_list,book_details

urlpatterns = [
    path("books",book_list,name="books"),
    path("books/<int:id>",book_details,name="bookdetails")
]
