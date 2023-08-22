from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)

from .filters import TitlesFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReadOnlyTitleSerializer, ReviewSerializer, TitleSerializer,
)
from reviews.models import Category, Genre, Review, Title


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин для представлений, позволяющий выполнять операции списка,
    создания и удаления.
    """
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """
    API-представление для управления произведениями.
    """
    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score'))
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """
        Возвращает соответствующий класс сериализатора
        в зависимости от действия.
        """
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    API-представление для управления категориями.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """
    API-представление для управления жанрами.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получение списка комментариев и создание нового комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Возвращает queryset комментариев для определенного отзыва.
        """
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Сохранение нового комментария с указанным отзывом и текущим
        пользователем в качестве автора.
        """
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        serializer.save(review=review, author=self.request.user)

    def get_permissions(self):
        """
        Возвращает список прав доступа в зависимости от метода запроса.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthorOrAdminOrModerator()]
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение списка отзывов и создание нового отзыва"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Возвращает queryset отзывов для определенного произведения.
        """
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        """
        Возвращает список прав доступа в зависимости от метода запроса.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthorOrAdminOrModerator()]
        return super().get_permissions()
