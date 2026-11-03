from rest_framework import serializers
from .models import User, Setup, Review
from .azure_vision import analyze_hardware_tags

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

    hardware_tags = serializers.JSONField(read_only=True, required=False)

    class Meta:
        model = Setup
        fields = ['id', 'owner', 'title', 'description', 'image', 'hardware_tags', 'created_at', 'reviews', 'average_rating']
        read_only_fields = ['owner', 'hardware_tags', 'created_at', 'reviews', 'average_rating']

    def create(self, validated_data):
        if 'hardware_tags' not in validated_data:
            image = validated_data.get('image')
            validated_data['hardware_tags'] = analyze_hardware_tags(image) if image else []
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'image' in validated_data and validated_data['image'] and 'hardware_tags' not in validated_data:
            validated_data['hardware_tags'] = analyze_hardware_tags(validated_data['image'])
        return super().update(instance, validated_data)

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0