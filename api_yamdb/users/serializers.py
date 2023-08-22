from rest_framework import serializers

from .models import User


class UserAdminSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя для административных целей."""

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""
    role = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Создает нового пользователя.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    def validate_username(self, value):
        """
        Проверяет валидность значения поля username.
        """
        if value == 'me':
            raise serializers.ValidationError('Invalid username')
        return value

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role'
                  ]
