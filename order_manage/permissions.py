from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners admin access.
    """

    def has_object_permission(self, request, view, obj):
        # 所有用户都可以提交新订单
        print(request.method)
        if request.method == 'POST':
            print(request.user)
            return True

        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
