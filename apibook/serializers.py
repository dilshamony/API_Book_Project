from rest_framework import serializers



class BookSerializer(serializers.Serializer):
    book_name=serializers.CharField()
    author=serializers.CharField()
    pages=serializers.IntegerField()
    price=serializers.IntegerField()