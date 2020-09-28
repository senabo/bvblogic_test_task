from django.urls import path

from .views import (
    ListTopicView,
    ListUserTopicsView,
    EditTopicView,
    DeleteTopicView,
    CreateCommentView,
    EditCommentView,
    DeleteCommentView,
    AttachModeratorView,
)

app_name = "forum"

urlpatterns = [
    path("topics/", ListTopicView.as_view(), name="list_create_topics"),
    path("topics/my/", ListUserTopicsView.as_view(), name="list_create_own_topics"),
    path("topics/<int:pk>/edit/", EditTopicView.as_view(), name="get_update_topic"),
    path("topics/<int:pk>/delete/", DeleteTopicView.as_view(), name="delete_topic"),
    path(
        "topics/<int:topic>/comments/",
        CreateCommentView.as_view(),
        name="create_comment",
    ),
    path("topics/comment/<int:pk>/", EditCommentView.as_view(), name="edit_comment"),
    path(
        "topics/comment/<int:pk>/delete/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path("topics/<int:pk>/moderator/", AttachModeratorView.as_view(), name="attaching_moderator"),

]
