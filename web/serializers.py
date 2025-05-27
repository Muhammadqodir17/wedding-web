from rest_framework import serializers
from dashboard.models import (
    WebSocialMedia,
    WebContactInfoModel,
    TeamMemberModel,
    NewsModel,
    BookModel,
    PriceModel,
    GalleryModel,
    WeddingCategoryModel,
    AboutUsModel,
    HomeModel,
    AboutUsHighlightModel,
    PriceHighLightModel,
)
from .models import ContactUsModel


class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeModel
        fields = ['id', 'title', 'description', 'image']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsModel
        fields = ['id', 'title', 'description', 'highlight', 'image']


class AboutUsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsModel
        fields = ['id', 'main_description', 'successful_events', 'work_experience', 'image']


class WeddingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingCategoryModel
        fields = ['id', 'image', 'name', 'description']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryModel
        fields = ['id', 'image']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceModel
        fields = ['id', 'type', 'price', 'description', 'highlights']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['id']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ['id', 'image', 'created_at', 'title', 'description']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberModel
        fields = ['id', 'image', 'first_name', 'last_name', 'position']


class WebContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebContactInfoModel
        fields = ['id', 'phone_number', 'email', 'location']


class WebSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSocialMedia
        fields = ['id', 'url', 'social_media_image']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'message']


class CategoriesForFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingCategoryModel
        fields = ['id', 'name']


class WebContactInfoForFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebContactInfoModel
        fields = ['id', 'phone_number', 'email', 'location', 'open_from', 'close_to']


class CalendarDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['id', 'book_date']


class CalendarDataInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['id', 'book_date', 'additional_info', 'category']