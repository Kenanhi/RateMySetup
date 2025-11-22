from rest_framework import serializers
from .models import User, Setup, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'bio', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class SetupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Setup
        fields = ['id', 'owner', 'title', 'description', 'image', 'created_at', 'reviews', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0