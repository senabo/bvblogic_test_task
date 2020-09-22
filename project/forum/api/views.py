from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from forum.models import Comment, Topic
from .permissions import IsOwnerOrReadOnly, IsModeratorOrOwner
from .serializer import (
    TopicSerializer,
    CommentSerializer,
    CommentEditSerializer,
    DeleteCommentSerializer,
    AttachModeratorSerializer,
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


class ListUserTopicsView(ListCreateAPIView):
    """Get only login user topics. Can create new topic"""

    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EditTopicView(RetrieveUpdateAPIView):
    """
    You can get and update topic if you are owner or moderator
    """

    serializer_class = TopicSerializer
    permission_classes = (IsModeratorOrOwner,)
    queryset = Topic.objects.all()


class DeleteTopicView(DestroyAPIView):
    """Delete your topic"""

    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Topic.objects.all()


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


class AttachModeratorView(UpdateAPIView):
    """Attaching user to topic as moderator """

    permission_classes = (IsAdminUser,)
    serializer_class = AttachModeratorSerializer
    queryset = Topic.objects.all()
