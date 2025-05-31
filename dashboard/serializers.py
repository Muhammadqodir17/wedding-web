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
)
from web.models import ContactUsModel


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingCategoryModel
        fields = ['id', 'name', 'description', 'image']


class PriceDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceModel
        fields = ['id', 'type', 'price', 'description', 'highlights']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = instance.get_type_display()
        data['highlights'] = instance.highlights.description
        return data


class AboutUsDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsModel
        fields = ['id', 'title', 'description', 'image', 'highlight', 'main_description', 'successful_events',
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
        fields = ['id', 'wedding_hall_name', 'phone_number', 'email', 'open_from', 'close_to', 'location']


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

