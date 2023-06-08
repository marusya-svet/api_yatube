from rest_framework import serializers
import re
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Group, Comment, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для Post"""
    text = serializers.StringRelatedField(many=False, read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'author', 'image', 'group', 'pub_date']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для Group"""

    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Comment"""
    text = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']
