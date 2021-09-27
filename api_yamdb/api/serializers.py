from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Category, Genre, Title, User, Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlesCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=None,
                                   min_length=None, allow_blank=False)

    class Meta:
        fields = ('email',)
        model = User


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_key = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs'].get('title_id')
        )
        author = self.context['request'].user
        current_title = get_object_or_404(Title, id=title_id)
        if (
                self.context['request'].method == 'POST'
                and current_title.reviews.filter(author=author).exists()
        ):
            raise serializers.ValidationError(
                'Отзыв на это произведение уже существует'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
