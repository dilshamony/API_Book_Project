from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Book
from .serializers import BookSerializer
from django.http import JsonResponse
#___________________________________

from .serializers import BookModelSerializer
from rest_framework.views import APIView
#___________________________________
from rest_framework import mixins, generics

#Authentication==>Session Authentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

#Authentication==>Token Authentication
from .serializers import LoginSerializer
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication



#                                      FUNCTION BASED VIEWS
#=======================================================================================================================

#Create,List,View,Update & Delete Book

#LIST
@csrf_exempt
def book_list(request):
    #2 methods: get & post
    if request.method =="GET":
        books = Book.objects.all()#need to send this books to the client.but can't send directly. so need to serialize them
        #form= is replacing
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
#CREATE
    elif request.method=="POST":
        data=JSONParser().parse(request)
        serializer=BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.data,status=400)

#DETAILS
@csrf_exempt
def book_details(request,id):
    book=Book.objects.get(id=id)
    if request.method =="GET":
        serializer=BookSerializer(book)
        return JsonResponse(serializer.data)
#UPDATE
    elif request.method =="PUT":
        data=JSONParser().parse(request)
        serializer=BookSerializer(book,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.data,status=400)
    elif request.method =="DELETE":
        book.delete()
        return JsonResponse({"Message":"Deleted"})




#                                      CLASS BASED VIEWS
#=======================================================================================================================
#LIST
class BookListView(APIView):
    def get(self,request):
        books=Book.objects.all()
        serializer=BookModelSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
#CREATE
    def post(self,request):
        serializer=BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.data, status=400)
#DETAILS & SESSION AUTHENTICATION
class BookDetailView(APIView):
    authentication_classes = [TokenAuthentication]#[BasicAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]#[IsAuthenticated,IsAdminUser]
    def get_object(self,id):
        return Book.objects.get(id=id)
    def get(self,request,id):
        book=self.get_object(id)
        serializer=BookModelSerializer(book)
        return JsonResponse(serializer.data, status=201)
    def put(self,request,id):
        book = self.get_object(id)
        serializer = BookModelSerializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.data, status=400)
    def delete(self,request,id):
        book = self.get_object(id)
        book.delete()
        return JsonResponse({"Message":"Deleted"})


#Token Authentication
#LOGIN
class LoginApi(APIView):
    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                return JsonResponse({"token":token.key})
            else:
                print("No User")
                return JsonResponse({"Message":"Failed"})

# "token": "0ac413853a645c6f1c3f603ecf77b042221634e4"


#                                     MIXIN CLASSES
#=======================================================================================================================
#LIST
class BookMixinView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset=Book.objects.all()
    serializer_class = BookModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return self.list( request, *args, **kwargs)
#CREATE
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
#DETAIL
class BookDetailMixinView(generics.GenericAPIView,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return self.retrieve(request,*args,**kwargs)
#UPDATE
    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)
#DELETE
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)