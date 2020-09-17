from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from accounts.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    """Base profile serializer"""

    class Meta:
        model = UserProfile
        fields = ("name", "about", "avatar", "user")
        read_only_fields = ("user",)


class CreateProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating user and user's profile"""

    profile = ProfileSerializer()

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="has already been taken by other user",
            )
        ],
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", "")

        #creating user
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        #creating profile
        name = profile_data.get("name", "")
        about = profile_data.get("about", "")
        avatar = profile_data.get("avatar", "")

        UserProfile.objects.create(user=user, name=name, about=about, avatar=avatar)

        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user and user's profile"""

    profile = ProfileSerializer()
    current_password = serializers.CharField(allow_blank=True, write_only=True)
    new_password = serializers.CharField(allow_blank=True, write_only=True, default="")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "current_password",
            "new_password",
            "email",
            "profile",
        )
        read_only_fields = ("username",)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        profile = instance.profile

        password = validated_data.get('current_password')
        new_password = validated_data.get('new_password')
        validated_data.pop('current_password', None)
        validated_data.pop('new_password', None)

        if not password and new_password:
            msg = ('Must provide current password')
            raise serializers.ValidationError(msg, code='authorization')

        # If current password's correct set new password
        if password and new_password:
            if instance.check_password(password):
                instance.set_password(new_password)
            else:
                msg = ('Sorry, you entered wrong password')
                raise serializers.ValidationError(msg, code='authorization')

        # Update profile fields
        if profile_data != None:
            for field, value in profile_data.items():
                if value:
                    setattr(profile, field, value)

        # Update user fields
        for field, value in validated_data.items():
            if value:
                setattr(instance, field, value)

        profile.save()
        instance.save()
        return instance
