from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APICreateUser, ApiGetToken, CommentViewSet, ReviewViewSet
from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet, \
    UserViewSet, UserMeViewset

v1_router = DefaultRouter()

v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('users', UserViewSet, basename='user')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/auth/email', APICreateUser.as_view()),
    path('v1/auth/token', ApiGetToken.as_view(), name='token_obtain'),
    path('v1/users/me/', UserMeViewset.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'})),
    path('v1/', include(v1_router.urls)),
    path(r'v1/users/(?P<username>[\w.@+-]+)/$', UserMeViewset),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),

]
