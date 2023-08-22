from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserView, get_token, signup


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

auth_urls = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/users/me/', UserView.as_view(), name='user_view'),
    path('v1/', include(router.urls)),
]
