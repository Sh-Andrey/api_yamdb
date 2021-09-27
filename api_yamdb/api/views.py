from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .models import Category, Genre, Title, User, Review
from .permissions import IsSuperuserOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitlesCreateSerializer, TitlesSerializer,
                          EmailSerializer, ConfirmSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer)


class CreateListDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(CreateListDeleteViewSet):
    permission_classes = (IsSuperuserOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CreateListDeleteViewSet):
    permission_classes = (IsSuperuserOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperuserOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'rating'
    )
    pagination_class = PageNumberPagination
    serializer_class = TitlesSerializer
    filterset_class = TitlesFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializer
        return TitlesCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


def send_mail(confirm_key, user):
    message = f'Ваш токен для входа систему {confirm_key}'
    user.email_user('CONFIRM', message, from_email=None)


class UserMeViewset(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        return super(UserMeViewset, self).update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class APICreateUser(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        username = email.rsplit('@')[0]
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirm_key = default_token_generator.make_token(user)
        send_mail(confirm_key, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApiGetToken(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_key = serializer.data.get('confirm_key')
        user = User.objects.get(email=serializer.data.get('email'))
        if default_token_generator.check_token(user, confirm_key):
            token = str(AccessToken.for_user(user))
            return Response(token, status=status.HTTP_201_CREATED)
        return Response('отказано', status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
