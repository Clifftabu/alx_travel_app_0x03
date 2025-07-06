from rest_framework import serializers
from .models import User, Listing, Booking, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = serializers.CharField()

    class Meta:
        model = Review
        fields = ['review_id', 'property', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'listing_id', 'host', 'name', 'description', 'location',
            'pricepernight', 'created_at', 'updated_at', 'reviews', 'review_count'
        ]

    def get_review_count(self, obj):
        return obj.reviews.count()

    def validate_pricepernight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0")
        return value


class BookingSerializer(serializers.ModelSerializer):
    property = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    duration_nights = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'property', 'user', 'checkin', 'checkout',
            'total_price', 'status', 'created_at', 'duration_nights'
        ]

    def get_duration_nights(self, obj):
        if obj.checkin and obj.checkout:
            return (obj.checkout - obj.checkin).days
        return 0

    def validate(self, data):
        checkin = data.get('checkin')
        checkout = data.get('checkout')

        if checkin and checkout:
            if checkin >= checkout:
                raise serializers.ValidationError("Check-out date must be after check-in date")

            from datetime import date
            if checkin < date.today():
                raise serializers.ValidationError("Check-in date cannot be in the past")

        return data
