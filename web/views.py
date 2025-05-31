from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
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
)
from .serializers import (
    MainPageSerializer,
    AboutUsSerializer,
    AboutUsDetailsSerializer,
    WeddingCategorySerializer,
    GallerySerializer,
    PriceSerializer,
    NewsSerializer,
    TeamMemberSerializer,
    WebContactInfoSerializer,
    WebSocialMediaSerializer,
    ContactUsSerializer,
    CategoriesForFooterSerializer,
    WebContactInfoForFooterSerializer,
    CalendarDataSerializer,
    CalendarDataInfoSerializer, GetCategorySerializer,
)


class WebViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Main Page",
        operation_summary="Get Main Page",
        responses={
            200: MainPageSerializer(),
        },
        tags=['web']
    )
    def get_main_page(self, request, *args, **kwargs):
        main_page = HomeModel.objects.all().first()
        serializer = MainPageSerializer(main_page, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get About Us",
        operation_summary="Get About Us",
        responses={
            200: AboutUsSerializer(),
        },
        tags=['web']
    )
    def about_us(self, request, *args, **kwargs):
        main_page = AboutUsModel.objects.all().first()
        serializer = AboutUsSerializer(main_page, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get About Us Details",
        operation_summary="Get About Us Details",
        responses={
            200: AboutUsDetailsSerializer(),
        },
        tags=['web']
    )
    def about_us_details(self, request, *args, **kwargs):
        main_page = AboutUsModel.objects.all().first()
        serializer = AboutUsDetailsSerializer(main_page, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Our Services(Categories)",
        operation_summary="Get Our Services(Categories)",
        responses={
            200: WeddingCategorySerializer(),
        },
        tags=['web']
    )
    def our_services(self, request, *args, **kwargs):
        main_page = WeddingCategoryModel.objects.all()
        serializer = WeddingCategorySerializer(main_page, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Gallery",
        operation_summary="Get all Gallery",
        responses={
            200: GallerySerializer(),
        },
        tags=['web']
    )
    def gallery(self, request, *args, **kwargs):
        main_page = GalleryModel.objects.all()
        serializer = GallerySerializer(main_page, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Prices",
        operation_summary="Get all Prices",
        responses={
            200: PriceSerializer(),
        },
        tags=['web']
    )
    def prices(self, request, *args, **kwargs):
        main_page = PriceModel.objects.all()
        serializer = PriceSerializer(main_page, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all News",
        operation_summary="Get all News",
        responses={
            200: NewsSerializer(),
        },
        tags=['web']
    )
    def news(self, request, *args, **kwargs):
        main_page = NewsModel.objects.all()
        serializer = NewsSerializer(main_page, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Team Members",
        operation_summary="Get all Team Members",
        responses={
            200: TeamMemberSerializer(),
        },
        tags=['web']
    )
    def our_team(self, request, *args, **kwargs):
        main_page = TeamMemberModel.objects.all()
        serializer = TeamMemberSerializer(main_page, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Category",
        operation_summary="Create Category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='message'),
            },
            required=['first_name', 'last_name', 'phone_number', 'message']
        ),
        responses={201: ContactUsSerializer()},
        tags=['web'],
    )
    def contact_us(self, request, *args, **kwargs):
        serializer = ContactUsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Get all Services(for all)",
        operation_summary="Get all Services(for all)",
        responses={
            200: CategoriesForFooterSerializer(),
        },
        tags=['web']
    )
    def our_services_for_footer(self, request, *args, **kwargs):
        main_page = WeddingCategoryModel.objects.all()
        serializer = CategoriesForFooterSerializer(main_page, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Contact Us Info",
        operation_summary="Get Contact Us Info",
        responses={
            200: WebContactInfoSerializer(),
        },
        tags=['web']
    )
    def contact_us_info(self, request, *args, **kwargs):
        main_page = WebContactInfoModel.objects.all().first()
        serializer = WebContactInfoSerializer(main_page)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Contact Us Info for Footer",
        operation_summary="Get Contact Us Info for Footer",
        responses={
            200: WebContactInfoForFooterSerializer(),
        },
        tags=['web']
    )
    def contact_us_info_for_footer(self, request, *args, **kwargs):
        main_page = WebContactInfoModel.objects.all().first()
        serializer = WebContactInfoForFooterSerializer(main_page)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Web Social Media",
        operation_summary="Get all Web Social Media",
        responses={
            200: WebSocialMediaSerializer(),
        },
        tags=['web']
    )
    def web_social_media(self, request, *args, **kwargs):
        main_page = WebSocialMedia.objects.all()
        serializer = WebSocialMediaSerializer(main_page, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Calendar Datas",
        operation_summary="Get all Calendar Datas",
        responses={
            200: CalendarDataSerializer(),
        },
        tags=['web']
    )
    def calendar_datas(self, request, *args, **kwargs):
        datas = BookModel.objects.all()
        serializer = CalendarDataSerializer(datas, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get calendar data info for a specific date",
        operation_summary="Get calendar data info",
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date to get event info (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: CalendarDataInfoSerializer(),
        },
        tags=['web']
    )
    def calendar_data_info(self, request, *args, **kwargs):
        data = request.GET
        data_info = BookModel.objects.filter(book_date=data.get('date')).first()
        serializer = CalendarDataInfoSerializer(data_info, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Galleries By Category Id",
        operation_summary="Get all Galleries By Category Id",
        responses={
            200: GallerySerializer(),
        },
        tags=['web']
    )
    def get_gallery_by_id(self, request, *args, **kwargs):
        galleries = GalleryModel.objects.filter(category__id=kwargs['pk'])
        serializer = GallerySerializer(galleries, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get all Categories",
        operation_summary="Get all Categories",
        responses={
            200: CalendarDataSerializer(),
        },
        tags=['web']
    )
    def get_categories(self, request, *args, **kwargs):
        categories = WeddingCategoryModel.objects.all()
        serializer = GetCategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
