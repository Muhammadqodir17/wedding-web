import qrcode
from rest_framework import serializers
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
    PriceHighLightModel, QrCodeModel,
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


class PriceHighlightDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHighLightModel
        fields = ['id', 'description']


class PriceDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceModel
        fields = ['id', 'type', 'price', 'description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = instance.type.name
        return data


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


class UnansweredMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'message', 'answered']


class UpcomingEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = ['id', 'category', 'book_date', 'booker_first_name', 'booker_last_name', 'number_of_guests']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        return data


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
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(instance.url)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Save new QR image to the image field
        filename = f"qr_{instance.id}.png"
        instance.image.save(filename, ContentFile(buffer.read()), save=False)

        buffer.close()
        instance.save()
        return instance
