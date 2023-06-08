import os
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, Group
from django.shortcuts import get_object_or_404
from django.conf import settings

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для Post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenided('нельзя так!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        filepath = f'{settings.MEDIA_ROOT}/{instance.file.name}'
        if os.path.exists(filepath):
            os.remove(filepath)
        instance.delete()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet для Group"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для Comment"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_queryset(self):
        return self.get_post().comments
