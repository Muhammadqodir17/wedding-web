from django.db.models import Count, F, Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from yaml import serialize

from .models import (
    TeamMemberModel,
    BookModel,
    WeddingCategoryModel,
    PriceModel,
    AboutUsModel,
    WebSocialMedia,
    WebContactInfoModel,
    DashboardStatsModel, AboutUsHighlightModel, PriceHighLightModel
)
from .serializers import (
    TeamMemberDashboardSerializer,
    EventSerializer,
    CategorySerializer,
    PriceDashboardSerializer,
    AboutUsDashboardSerializer,
    MessageSerializer,
    SocialMediaSerializer,
    WebSettingsSerializer,
    DashboardStatsSerializer,
    UnansweredMessagesSerializer,
    UpcomingEventsSerializer,
    PriceTypeSerializer, AboutUsHighlightDashboardSerializer, PriceHighlightDashboardSerializer,
)
from web.models import ContactUsModel
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)


class MainPageViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Web Stats",
        operation_summary="Get Web Stats",
        responses={
            200: TeamMemberDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get_web_stats(self, request, *args, **kwargs):
        web_stats = DashboardStatsModel.objects.all().first()
        serializer = DashboardStatsSerializer(web_stats)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Upcoming Events",
        operation_summary="Get all Upcoming Events",
        responses={
            200: UpcomingEventsSerializer(),
        },
        tags=['dashboard']
    )
    def upcoming_events(self, request, *args, **kwargs):
        today = now().date()
        events = BookModel.objects.filter(book_date__gte=today).order_by('book_date')
        serializer = UpcomingEventsSerializer(events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Unanswered Messages",
        operation_summary="Get all Unanswered Messages",
        responses={
            200: UnansweredMessagesSerializer(),
        },
        tags=['dashboard']
    )
    def unanswered_messages(self, request, *args, **kwargs):
        messages = ContactUsModel.objects.filter(answered=False)
        serializer = UnansweredMessagesSerializer(messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Event Stats",
        operation_summary="Get Event Stats",
        responses={
            200: 'ok',
        },
        tags=['dashboard']
    )
    def event_stats(self, request, *args, **kwargs):
        category_stats = (
            BookModel.objects
            .values(category_name=F('category__name'))
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        total = category_stats.aggregate(total=Sum('count'))['total'] or 0
        results = [
            {
                'category': stat['category_name'],
                'count': stat['count'],
                'percent': round((stat['count'] / total) * 100, 1) if total > 0 else 0,
            }
            for stat in category_stats
        ]
        return Response(data=results, status=status.HTTP_200_OK)


class OurTeamViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all Team Members",
        operation_summary="Get all Team Members",
        responses={
            200: TeamMemberDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = TeamMemberModel.objects.all()
        serializer = TeamMemberDashboardSerializer(our_team, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Team Member",
        operation_summary="Create Team Member",
        manual_parameters=[
            openapi.Parameter(
                name='first_name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="first_name"
            ),
            openapi.Parameter(
                name='last_name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="last_name",
            ),
            openapi.Parameter(
                name='position',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="position",
            ),
            openapi.Parameter(
                name='from_working_hours',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="from_working_hours",
            ),
            openapi.Parameter(
                name='to_working_hours',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="to_working_hours",
            ),
            openapi.Parameter(
                name='salary_type',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="salary_type",
            ),
            openapi.Parameter(
                name='salary',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                format='float',
                required=True,
                description="salary",
            ),
            openapi.Parameter(
                name='work_start_data',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="work_start_data",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="image",
            ),
        ],
        responses={201: TeamMemberDashboardSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = TeamMemberDashboardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Create Team Member",
        operation_summary="Create Team Member",
        manual_parameters=[
            openapi.Parameter(
                name='first_name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="first_name"
            ),
            openapi.Parameter(
                name='last_name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="last_name",
            ),
            openapi.Parameter(
                name='position',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="position",
            ),
            openapi.Parameter(
                name='from_working_hours',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="from_working_hours",
            ),
            openapi.Parameter(
                name='to_working_hours',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="to_working_hours",
            ),
            openapi.Parameter(
                name='salary_type',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="salary_type",
            ),
            openapi.Parameter(
                name='salary',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                format='float',
                required=False,
                description="salary",
            ),
            openapi.Parameter(
                name='work_start_data',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="work_start_data",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="image",
            ),
        ],
        responses={200: TeamMemberDashboardSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = TeamMemberModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Team Member not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamMemberDashboardSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Team Member",
        operation_summary="Delete Team Member",
        responses={
            200: 'Successfully deleted',
            404: 'Team Member not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = TeamMemberModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Team Member not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Team Member successfully deleted'}, status=status.HTTP_200_OK)


class EventsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all Events",
        operation_summary="Get all Events",
        responses={
            200: EventSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = BookModel.objects.all()
        serializer = EventSerializer(our_team, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Event",
        operation_summary="Create Event",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'book_date': openapi.Schema(type=openapi.TYPE_STRING, description='book_date'),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='category'),
                'booker_first_name': openapi.Schema(type=openapi.TYPE_STRING, description='booker_first_name'),
                'booker_last_name': openapi.Schema(type=openapi.TYPE_STRING, description='booker_last_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'number_of_guests': openapi.Schema(type=openapi.TYPE_INTEGER, description='number_of_guests'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='price'),
            },
            required=['book_date', 'category', 'booker_first_name', 'booker_last_name',
                      'phone_number', 'number_of_guests', 'price']
        ),
        responses={201: EventSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Event",
        operation_summary="Update Event",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'book_date': openapi.Schema(type=openapi.TYPE_STRING, description='book_date'),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='category'),
                'booker_first_name': openapi.Schema(type=openapi.TYPE_STRING, description='booker_first_name'),
                'booker_last_name': openapi.Schema(type=openapi.TYPE_STRING, description='booker_last_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'number_of_guests': openapi.Schema(type=openapi.TYPE_INTEGER, description='number_of_guests'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='price'),
            },
            required=[]
        ),
        responses={200: EventSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = BookModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Event",
        operation_summary="Delete Event",
        responses={
            200: 'Successfully deleted',
            404: 'Event not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = BookModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Event successfully deleted'}, status=status.HTTP_200_OK)


class CategoriesViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all Categories",
        operation_summary="Get all Categories",
        responses={
            200: CategorySerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = WeddingCategoryModel.objects.all()
        serializer = CategorySerializer(our_team, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Category",
        operation_summary="Create Category",
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="name"
            ),
            openapi.Parameter(
                name='description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="description",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="image",
            ),
        ],
        responses={201: CategorySerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Category",
        operation_summary="Update Category",
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="name"
            ),
            openapi.Parameter(
                name='description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="description",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="image",
            ),
        ],
        responses={200: CategorySerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = WeddingCategoryModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Category",
        operation_summary="Delete Category",
        responses={
            200: 'Successfully deleted',
            404: 'Category not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = WeddingCategoryModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Category successfully deleted'}, status=status.HTTP_200_OK)


class PricesViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all Prices",
        operation_summary="Get all Prices",
        responses={
            200: PriceDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = PriceModel.objects.all()
        serializer = PriceDashboardSerializer(our_team, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Price",
        operation_summary="Create Price",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='type'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='price'),
            },
            required=['type', 'description', 'price']
        ),
        responses={201: PriceDashboardSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = PriceDashboardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Price",
        operation_summary="Update Price",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='type'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='price'),
            },
            required=[]
        ),
        responses={200: PriceDashboardSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = PriceModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Price not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PriceDashboardSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Price",
        operation_summary="Delete Price",
        responses={
            200: 'Successfully deleted',
            404: 'Price not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = PriceModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Price not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Price successfully deleted'}, status=status.HTTP_200_OK)


class AboutUsViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all About Us",
        operation_summary="Get all About Us",
        responses={
            200: AboutUsDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = AboutUsModel.objects.all()
        serializer = AboutUsDashboardSerializer(our_team, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create About Us",
        operation_summary="Create About Us",
        manual_parameters=[
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="title"
            ),
            openapi.Parameter(
                name='description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="description",
            ),
            openapi.Parameter(
                name='main_description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="main_description",
            ),
            openapi.Parameter(
                name='successful_events',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="successful_events",
            ),
            openapi.Parameter(
                name='work_experience',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="work_experience",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="image",
            ),
        ],
        responses={201: AboutUsDashboardSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = AboutUsDashboardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Create About Us",
        operation_summary="Create About Us",
        manual_parameters=[
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="title"
            ),
            openapi.Parameter(
                name='description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="description",
            ),
            openapi.Parameter(
                name='main_description',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="main_description",
            ),
            openapi.Parameter(
                name='successful_events',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="successful_events",
            ),
            openapi.Parameter(
                name='work_experience',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=False,
                description="work_experience",
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="image",
            ),
        ],
        responses={20: AboutUsDashboardSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = AboutUsModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'About Us not  found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AboutUsDashboardSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete About Us",
        operation_summary="Delete About Us",
        responses={
            200: 'Successfully deleted',
            404: 'About Us not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = AboutUsModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'About Us not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'About Us successfully deleted'}, status=status.HTTP_200_OK)


class MessagesViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all Messages",
        operation_summary="Get all Messages",
        responses={
            200: MessageSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = ContactUsModel.objects.all()
        serializer = MessageSerializer(our_team, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update Message",
        operation_summary="Update Message",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='message'),
                'answered': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='answered'),
            },
            required=[]
        ),
        responses={200: MessageSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = ContactUsModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Message not  found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Message",
        operation_summary="Delete Message",
        responses={
            200: 'Successfully deleted',
            404: 'Message not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = ContactUsModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Message successfully deleted'}, status=status.HTTP_200_OK)


class SocialMediasViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all Social Medias",
        operation_summary="Get all Social Medias",
        responses={
            200: SocialMediaSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = WebSocialMedia.objects.all()
        serializer = SocialMediaSerializer(our_team, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Social Medias",
        operation_summary="Create Social Medias",
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="name"
            ),
            openapi.Parameter(
                name='url',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="url",
            ),
            openapi.Parameter(
                name='social_media_image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="social_media_image",
            ),
        ],
        responses={201: SocialMediaSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = SocialMediaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Social Medias",
        operation_summary="Update Social Medias",
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="name"
            ),
            openapi.Parameter(
                name='url',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="url",
            ),
            openapi.Parameter(
                name='social_media_image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="social_media_image",
            ),
        ],
        responses={201: SocialMediaSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = WebSocialMedia.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Social Media not  found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SocialMediaSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Social Media",
        operation_summary="Delete Social Media",
        responses={
            200: 'Successfully deleted',
            404: 'Social Media not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = WebSocialMedia.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Social Media not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Social Media successfully deleted'}, status=status.HTTP_200_OK)


class WebSettingsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Contact Info",
        operation_summary="Get Contact Info",
        responses={
            200: WebSettingsSerializer(),
        },
        tags=['dashboard']
    )
    def get_all(self, request, *args, **kwargs):
        our_team = WebContactInfoModel.objects.all()
        serializer = WebSettingsSerializer(our_team, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Contact Info",
        operation_summary="Create Contact Info",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'wedding_hall_name': openapi.Schema(type=openapi.TYPE_STRING, description='wedding_hall_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'open_from': openapi.Schema(type=openapi.TYPE_STRING, description='open_from'),
                'close_to': openapi.Schema(type=openapi.TYPE_STRING, description='close_to'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='location'),
                'location_url': openapi.Schema(type=openapi.TYPE_STRING, description='location_url'),
            },
            required=['wedding_hall_name', 'phone_number', 'email', 'open_from', 'close_to', 'location',
                      'location_url']
        ),
        responses={201: WebSettingsSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = WebSettingsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Contact Info",
        operation_summary="Update Contact Info",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'wedding_hall_name': openapi.Schema(type=openapi.TYPE_STRING, description='wedding_hall_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'open_from': openapi.Schema(type=openapi.TYPE_STRING, description='open_from'),
                'close_to': openapi.Schema(type=openapi.TYPE_STRING, description='close_to'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='location'),
                'location_url': openapi.Schema(type=openapi.TYPE_STRING, description='location_url'),
            },
            required=[]
        ),
        responses={200: WebSettingsSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        our_team = WebContactInfoModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Contact Info not  found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebSettingsSerializer(our_team, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Contact Info",
        operation_summary="Delete Contact Info",
        responses={
            200: 'Successfully deleted',
            404: 'Contact Info not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        our_team = WebContactInfoModel.objects.filter(id=kwargs['pk']).first()
        if our_team is None:
            return Response(data={'error': 'Contact Info not found'}, status=status.HTTP_404_NOT_FOUND)
        our_team.delete()
        return Response(data={'message': 'Contact Info successfully deleted'}, status=status.HTTP_200_OK)


class PriceHighlightViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all Price Highlights",
        operation_summary="Get all Price Highlights",
        responses={
            200: PriceHighlightDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get(self, request, *args, **kwargs):
        highlight = PriceHighLightModel.objects.all()
        serializer = PriceHighlightDashboardSerializer(highlight, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Price Highlights",
        operation_summary="Create Price Highlights",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
            },
            required=['description']
        ),
        responses={201: PriceHighlightDashboardSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = PriceHighlightDashboardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update Price Highlights",
        operation_summary="Update Price Highlights",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
            },
            required=[]
        ),
        responses={200: PriceHighlightDashboardSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        highlight = PriceHighLightModel.objects.filter(id=kwargs['pk']).first()
        if highlight is None:
            return Response(data={'error': 'Highlight not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PriceHighlightDashboardSerializer(highlight, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete Price Highlights",
        operation_summary="Delete Price Highlights",
        responses={
            200: 'Successfully deleted',
            404: 'Price Highlights not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        highlight = PriceHighLightModel.objects.filter(id=kwargs['pk']).first()
        if highlight is None:
            return Response(data={'error': 'Highlight not found'}, status=status.HTTP_404_NOT_FOUND)
        highlight.delete()
        return Response(data={'message': 'Highlight successfully deleted'})


class AboutUsHighlightViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all About Us Highlights",
        operation_summary="Get all About Us Highlights",
        responses={
            200: AboutUsHighlightDashboardSerializer(),
        },
        tags=['dashboard']
    )
    def get(self, request, *args, **kwargs):
        highlight = AboutUsHighlightModel.objects.all()
        serializer = AboutUsHighlightDashboardSerializer(highlight, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create About Us Highlights",
        operation_summary="Create About Us Highlights",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
            },
            required=['description', 'title']
        ),
        responses={201: AboutUsHighlightDashboardSerializer()},
        tags=['dashboard'],
    )
    def create(self, request, *args, **kwargs):
        serializer = AboutUsHighlightDashboardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update About Us Highlights",
        operation_summary="Update About Us Highlights",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
            },
            required=[]
        ),
        responses={200: AboutUsHighlightDashboardSerializer()},
        tags=['dashboard'],
    )
    def update(self, request, *args, **kwargs):
        highlight = AboutUsHighlightModel.objects.filter(id=kwargs['pk']).first()
        if highlight is None:
            return Response(data={'error': 'Highlight not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AboutUsHighlightDashboardSerializer(highlight, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete About Us Highlights",
        operation_summary="Delete About Us Highlights",
        responses={
            200: 'Successfully deleted',
            404: 'About Us not found',
        },
        tags=['dashboard']
    )
    def delete(self, request, *args, **kwargs):
        highlight = AboutUsHighlightModel.objects.filter(id=kwargs['pk']).first()
        if highlight is None:
            return Response(data={'error': 'Highlight not found'}, status=status.HTTP_404_NOT_FOUND)
        highlight.delete()
        return Response(data={'message': 'Highlight successfully deleted'})



