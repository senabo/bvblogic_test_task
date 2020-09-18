from django.urls import path

from .views import (
    ListTopicView,
    EditTopicView,
    CreateCommentView,
    EditCommentView,
    DeleteCommentView,
)

app_name = "forum"

own_topic_list = EditTopicView.as_view({"get": "list", "post": "create"})
own_topic_edit = EditTopicView.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)


urlpatterns = [
    path("topics/", ListTopicView.as_view(), name="list_create_topics"),
    path("topics/my/", own_topic_list, name="list_create_own_topics"),
    path("topics/my/<int:pk>/", own_topic_edit, name="get_update_topic"),
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
]
