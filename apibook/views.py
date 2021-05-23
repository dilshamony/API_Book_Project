from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from django.http import JsonResponse

# Create your views here.

#Create,List,View,Update & Delete Book

#CREATE BOOK
def book_list(request):
    #2 methods: get & post
    if request.method =="GET":
        books = Book.objects.all()#need to send this books to the client.but can't send directly. so need to serialize them
        #form= is replacing
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)