from django.urls import path
from .views import (
    MainPageViewSet,
    OurTeamViewSet,
    EventsViewSet,
    CategoriesViewSet,
    PricesViewSet,
    AboutUsViewSet,
    MessagesViewSet,
    SocialMediasViewSet,
    WebSettingsViewSet, PriceHighlightViewSet, AboutUsHighlightViewSet, QRCodeViewSet,
)

urlpatterns = [
    # dashboard stats
    path('get_unanswered_messages/', MainPageViewSet.as_view({'get': 'unanswered_messages'}),
         name='get_unanswered_messages'),
    path('get_upcoming_events/', MainPageViewSet.as_view({'get': 'upcoming_events'}), name='get_upcoming_events'),
    path('get_web_stats/', MainPageViewSet.as_view({'get': 'get_web_stats'}), name='get_web_stats'),
    path('get_event_stats/', MainPageViewSet.as_view({'get': 'event_stats'}), name='get_event_stats'),
    # OurTeam
    path('get_all_our_team/', OurTeamViewSet.as_view({'get': 'get_all'}), name='get_all_our_team'),
    path('create_our_team/', OurTeamViewSet.as_view({'post': 'create'}), name='create_our_team'),
    path('update_our_team/<int:pk>/', OurTeamViewSet.as_view({'patch': 'update'}), name='update_our_team'),
    path('delete_our_team/<int:pk>/', OurTeamViewSet.as_view({'delete': 'delete'}), name='delete_our_team'),
    # Events
    path('get_all_events/', EventsViewSet.as_view({'get': 'get_all'}), name='get_all_events'),
    path('create_event/', EventsViewSet.as_view({'post': 'create'}), name='create_event'),
    path('update_event/<int:pk>/', EventsViewSet.as_view({'patch': 'update'}), name='update_event'),
    path('delete_event/<int:pk>/', EventsViewSet.as_view({'delete': 'delete'}), name='delete_event'),
    # Categories
    path('get_all_categories/', CategoriesViewSet.as_view({'get': 'get_all'}), name='get_all_categories'),
    path('create_category/', CategoriesViewSet.as_view({'post': 'create'}), name='create_category'),
    path('update_category/<int:pk>/', CategoriesViewSet.as_view({'patch': 'update'}), name='update_category'),
    path('delete_category/<int:pk>/', CategoriesViewSet.as_view({'delete': 'delete'}), name='delete_category'),
    # Prices
    path('get_all_prices/', PricesViewSet.as_view({'get': 'get_all'}), name='get_all_prices'),
    path('create_price/', PricesViewSet.as_view({'post': 'create'}), name='create_price'),
    path('update_price/<int:pk>/', PricesViewSet.as_view({'patch': 'update'}), name='update_price'),
    path('delete_price/<int:pk>/', PricesViewSet.as_view({'delete': 'delete'}), name='delete_price'),
    # AboutUs
    path('get_all_about_us/', AboutUsViewSet.as_view({'get': 'get_all'}), name='get_all_about_us'),
    path('create_about_us/', AboutUsViewSet.as_view({'post': 'create'}), name='create_about_us'),
    path('update_about_us/<int:pk>/', AboutUsViewSet.as_view({'patch': 'update'}), name='update_about_us'),
    path('delete_about_us/<int:pk>/', AboutUsViewSet.as_view({'delete': 'delete'}), name='delete_about_us'),
    # Messages
    path('get_all_messages/', MessagesViewSet.as_view({'get': 'get_all'}), name='get_all_messages'),
    path('update_message/<int:pk>/', MessagesViewSet.as_view({'patch': 'update'}), name='update_message'),
    path('delete_message/<int:pk>/', MessagesViewSet.as_view({'delete': 'delete'}), name='delete_message'),
    # SocialMedias
    path('get_all_social_medias/', SocialMediasViewSet.as_view({'get': 'get_all'}), name='get_all_social_medias'),
    path('create_social_media/', SocialMediasViewSet.as_view({'post': 'create'}), name='create_social_media'),
    path('update_social_media/<int:pk>/', SocialMediasViewSet.as_view({'patch': 'update'}), name='update_social_media'),
    path('delete_social_media/<int:pk>/', SocialMediasViewSet.as_view({'delete': 'delete'}),
         name='delete_social_media'),
    # WebSettings
    path('get_all_web_settings/', WebSettingsViewSet.as_view({'get': 'get_all'}), name='get_all_web_settings'),
    path('create_web_setting/', WebSettingsViewSet.as_view({'post': 'create'}), name='create_web_setting'),
    path('update_web_setting/<int:pk>/', WebSettingsViewSet.as_view({'patch': 'update'}), name='update_web_setting'),
    path('delete_web_setting/<int:pk>/', WebSettingsViewSet.as_view({'delete': 'delete'}), name='delete_web_setting'),
    # about us highlight
    path('get_about_us_highlight/', AboutUsHighlightViewSet.as_view({'get': 'get'}), name='get_about_us_highlight'),
    path('create_about_us_highlight/', AboutUsHighlightViewSet.as_view({'create': 'create'}),
         name='create_about_us_highlight'),
    path('update_about_us_highlight/<int:pk>/', AboutUsHighlightViewSet.as_view({'patch': 'update'}),
         name='update_about_us_highlight'),
    path('delete_about_us_highlight/<int:pk>/', AboutUsHighlightViewSet.as_view({'delete': 'delete'}),
         name='delete_about_us_highlight'),
    # price highlight
    path('get_price_highlight/', PriceHighlightViewSet.as_view({'get': 'get'}), name='get_price_highlight'),
    path('create_price_highlight/', PriceHighlightViewSet.as_view({'create': 'create'}), name='create_price_highlight'),
    path('update_price_highlight/<int:pk>/', PriceHighlightViewSet.as_view({'patch': 'update'}),
         name='update_price_highlight'),
    path('delete_price_highlight/<int:pk>/', PriceHighlightViewSet.as_view({'delete': 'delete'}),
         name='delete_price_highlight'),
    # qr code
    path('get_qr_code/', QRCodeViewSet.as_view({'get': 'get'}), name='get_qr_code'),
    path('create_qr_code/', QRCodeViewSet.as_view({'post': 'create'}), name='create_qr_code'),
    path('update_qr_code/<int:pk>/', QRCodeViewSet.as_view({'patch': 'update'}), name='update_qr_code'),
    path('delete_qr_code/<int:pk>/', QRCodeViewSet.as_view({'delete': 'delete'}), name='delete_qr_code'),
]
