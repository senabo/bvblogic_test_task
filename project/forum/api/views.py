from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from forum.models import Comment, Topic
from .permissions import IsOwnerOrReadOnly
from .serializer import (
    TopicSerializer,
    CommentSerializer,
    CommentEditSerializer,
    DeleteCommentSerializer,
)


class ListTopicView(ListCreateAPIView):
    """
    List or create topics.

    Possibility search the topics by title: just add "?search=" parameter at the end of the url
    """

    queryset = Topic.objects.filter(is_active=True)

    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EditTopicView(ModelViewSet):
    """
    Get only login user topics.

    You can create, update and delete your topic
    """

    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CreateCommentView(ListCreateAPIView):
    """List or create comments for the topic"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(topic=self.kwargs.get("topic"))

    def perform_create(self, serializer):
        topic = get_object_or_404(Topic, pk=self.kwargs.get("topic"))

        if topic.closed:
            msg = "The topic is closed"
            raise PermissionDenied(msg)

        serializer.save(author=self.request.user, topic=topic)


class EditCommentView(RetrieveUpdateAPIView):
    """Get or update comment"""

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CommentEditSerializer
    queryset = Comment.objects.all()


class DeleteCommentView(UpdateAPIView):
    """
    Delete comment.

    You have to send an empty put request
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = DeleteCommentSerializer
    queryset = Comment.objects.all()
