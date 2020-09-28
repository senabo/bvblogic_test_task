from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user


class IsModeratorOrOwner(permissions.BasePermission):
    """
    Permission is grant if user is owner or moderator
    """

    # def has_permission(self, request, view):
    #     #if user isn't authenticated permission denied
    #     if not bool(request.user and request.user.is_authenticated):
    #         return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        owner =  obj.author == request.user
        moderator = obj.moderator == request.user

        if owner or moderator:
            return True
        else:
            return False