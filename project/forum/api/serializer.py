from rest_framework import serializers

from forum.models import Topic, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for list or create Comment"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content", "author", "status", "created", "updated", "topic")
        read_only_fields = ("topic", "status")


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for crud Topic"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "description",
            "image",
            "author",
            "created",
            "updated",
            "is_active",
            "closed",
            "comment_set",
        )


class CommentEditSerializer(serializers.ModelSerializer):
    """Serializer for editing comment"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("content", "author", "status", "created", "updated", "topic")
        read_only_fields = ("topic", "status")

    def update(self, instance, validated_data):
        if instance.topic.closed:
            msg = "Topic is closed. You can not leave comment here"
            raise serializers.ValidationError(msg)
        for field, value in validated_data.items():
            if value:
                setattr(instance, field, value)

        instance.update_comment()
        instance.save()
        return instance


class DeleteCommentSerializer(serializers.ModelSerializer):
    """Serializer for deleting comment"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("content", "author", "status", "created", "updated", "topic")
        read_only_fields = ("topic", "status", "content")

    def update(self, instance, validated_data):
        instance.delete_comment()
        instance.save()
        return instance
