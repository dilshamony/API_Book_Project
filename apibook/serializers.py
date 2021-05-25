from rest_framework import serializers
from .models import Book
#________________________________________________________________
from rest_framework.serializers import ModelSerializer


#                                      FUNCTION BASED VIEWS
#=======================================================================================================================

class BookSerializer(serializers.Serializer):
    book_name=serializers.CharField()
    author=serializers.CharField()
    pages=serializers.IntegerField()
    price=serializers.IntegerField()

    def create(self,validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book_name=validated_data.get("book_name")
        instance.author=validated_data.get("author")
        instance.pages=validated_data.get("pages")
        instance.price=validated_data.get("price")
        instance.save()
        return instance


#                                      CLASS BASED VIEWS
#=======================================================================================================================

class BookModelSerializer(ModelSerializer):
    class Meta:
        model=Book
        fields=["book_name","author","pages","price"]