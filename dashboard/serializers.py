import qrcode
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import (
    TeamMemberModel,
    BookModel,
    WeddingCategoryModel,
    PriceModel,
    AboutUsModel,
    WebSocialMedia,
    WebContactInfoModel,
    DashboardStatsModel,
    SALARY_TYPE,
    PriceTypeModel,
    AboutUsHighlightModel,
    PriceHighLightModel, QrCodeModel, PositionModel, NewsModel,
)
from web.models import ContactUsModel
import json
from io import BytesIO
from django.core.files.base import ContentFile


class TeamMemberDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberModel
        fields = ['id', 'first_name', 'last_name', 'position', 'from_working_hours', 'to_working_hours', 'salary_type', 'salary',
                  'work_start_data', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['position'] = instance.position.name
        data['salary_type'] = dict(SALARY_TYPE).get(instance.salary_type, 'Unknown')
        return data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['id', 'book_date', 'category', 'booker_first_name', 'booker_last_name', 'phone_number',
                  'number_of_guests', 'price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingCategoryModel
        fields = ['id', 'name', 'description', 'image']


class DashboardSpecialPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionModel
        fields = ['id', 'name']


class PriceHighlightDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHighLightModel
        fields = ['id', 'description', 'price']


class PriceDashboardSerializer(serializers.ModelSerializer):
    highlight = serializers.SerializerMethodField(source='get_highlight')
    class Meta:
        model = PriceModel
        fields = ['id', 'type', 'price', 'description', 'highlight']

    def get_highlight(self, data):
        highlight = PriceHighLightModel.objects.filter(price=data)
        return PriceHighlightDashboardSerializer(highlight, many=True).data


class CreatePriceDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceModel
        fields = ['id', 'type', 'price', 'description']


class AboutUsHighlightDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsHighlightModel
        fields = ['id', 'title', 'description']


class AboutUsDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsModel
        fields = ['id', 'title', 'description', 'image', 'main_description', 'successful_events',
                  'work_experience']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'message', 'answered']


class UpdateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['id', 'answered']


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSocialMedia
        fields = ['id', 'name', 'url', 'social_media_image']


class WebSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebContactInfoModel
        fields = ['id', 'wedding_hall_name', 'phone_number', 'email', 'open_from', 'close_to',
                  'location', 'location_url']


class DashboardStatsSerializer(serializers.ModelSerializer):
    annual_income = serializers.SerializerMethodField(source='get_annual_income')
    class Meta:
        model = DashboardStatsModel
        fields = ['id', 'employees', 'events', 'annual_income', 'unanswered_messages']

    def to_representation(self, instance):
        employees = TeamMemberModel.objects.all().count()
        events = BookModel.objects.all().count()
        messages = ContactUsModel.objects.filter(answered=False).count()
        data = super().to_representation(instance)
        data['employees'] = employees
        data['events'] = instance.events + events
        data['unanswered_messages'] = messages
        return data

    def get_annual_income(self, data):
        work_experience = AboutUsModel.objects.all().first()
        return work_experience.work_experience


class UnansweredMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'message', 'answered']


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingCategoryModel
        fields = ['id', 'name', 'image']


class UpcomingEventsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = BookModel
        fields = ['id', 'category', 'book_date', 'booker_first_name', 'booker_last_name', 'number_of_guests']

    def get_category(self, obj):
        request = self.context.get('request')
        return CategoryImageSerializer(obj.category, context={'request': request}).data


class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTypeModel
        fields = ['id', 'name']


class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCodeModel
        fields = ['id', 'url', 'image']


class QrCodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCodeModel
        fields = ['id', 'url', 'image']

    def create(self, validated_data):
        url = validated_data.get("url")
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        instance = QrCodeModel(**validated_data)

        filename = f"qr_{instance.id or 'temp'}.png"
        instance.image.save(filename, ContentFile(buffer.read()), save=False)

        buffer.close()
        instance.save()
        return instance


class QrCodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCodeModel
        fields = ['id', 'url', 'image']

    def update(self, instance, validated_data):
        instance.url = validated_data.get("url", instance.url)
        instance.save()
        return instance


class DashboardNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ['id', 'title', 'description', 'image']