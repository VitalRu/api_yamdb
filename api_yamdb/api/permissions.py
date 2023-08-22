from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Права доступа, позволяющие только администраторам выполнять действия.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь права доступа администратора.
        """
        return request.user.is_authenticated and (request.user.is_superuser
                                                  or request.user.is_admin)


class IsAuthor(permissions.BasePermission):
    """
    Права доступа, позволяющие только автору выполнять действия.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь автором объекта.
        """
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Права доступа, позволяющие только владельцу выполнять изменяющие действия,
    а остальным - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь право доступа к объекту.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsModeratorOrAdmin(permissions.BasePermission):
    """
    Право доступа для модератора или администратора.

    Разрешает доступ только аутентифицированным пользователям с ролью
    "moderator" или "admin".
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право доступа.
        """
        return request.user.is_authenticated and (request.user.is_moderator
                                                  or request.user.is_admin
                                                  or request.user.is_superuser
                                                  )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Право доступа для администратора или только чтения.
    Разрешает доступ только аутентифицированным пользователям с ролью "admin"
    или только для чтения.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право доступа.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.is_admin
                                                  or request.user.is_superuser)


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """
    Право доступа для автора, администратора или модератора.
    Разрешает доступ только аутентифицированным пользователям,
    являющимся автором объекта, или с ролью "admin" или "moderator".
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь право доступа к объекту.
        """
        return request.user.is_authenticated and (obj.author == request.user
                                                  or request.user.is_moderator
                                                  or request.user.is_admin
                                                  or request.user.is_superuser)
