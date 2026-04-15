from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Categorie,Replie,Comment,Post
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id", "categorie_name"]



class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Replie
        fields = ["id", "author", "text", "date_added"]




class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "created_date", "replies"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categorie = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_read_later = serializers.SerializerMethodField()

    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        source='categorie',
        write_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "image",
            "author",
            "categorie",
            "categorie_id",
            "date_posted",
            "comments",
            "total_likes",
            "is_liked",
            "is_read_later",
        ]

    def get_total_likes(self, obj):
        return obj.liked.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.liked.filter(id=request.user.id).exists()
        return False

    def get_is_read_later(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.read_later.filter(id=request.user.id).exists()
        return False