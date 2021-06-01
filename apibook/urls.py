from django.contrib import admin
from django.urls import path
from .views import book_list,book_details,\
    BookListView,BookDetailView,\
    BookMixinView,BookDetailMixinView,\
    LoginApi

urlpatterns = [
    path("books",book_list,name="books"),
    path("books/<int:id>",book_details,name="bookdetails"),
    path("cbooks",BookListView.as_view(),name="cbooks"),
    path("cbooks/<int:id>",BookDetailView.as_view(),name="cdetail"),
    path("mbooks",BookMixinView.as_view(),name="mbooks"),
    path("mbooks/<int:pk>",BookDetailMixinView.as_view(),name="mdetail"),
    path("login",LoginApi.as_view(),name="login")
]
