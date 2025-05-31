from django.urls import path
from .views import WebViewSet

urlpatterns = [
    path('get_main_page/', WebViewSet.as_view({'get': 'get_main_page'}), name='get_main_page'),
    path('get_about_us/', WebViewSet.as_view({'get': 'about_us'}), name='get_about_us'),
    path('get_about_us_details/', WebViewSet.as_view({'get': 'about_us_details'}), name='get_about_us_details'),
    path('get_our_services/', WebViewSet.as_view({'get': 'our_services'}), name='get_our_services'),
    path('get_gallery/', WebViewSet.as_view({'get': 'gallery'}), name='get_gallery'),
    path('get_prices/', WebViewSet.as_view({'get': 'prices'}), name='get_prices'),
    path('get_news/', WebViewSet.as_view({'get': 'news'}), name='get_news'),
    path('get_our_team/', WebViewSet.as_view({'get': 'our_team'}), name='get_our_team'),
    path('contact_us/', WebViewSet.as_view({'post': 'contact_us'}), name='contact_us'),
    path('get_our_services_for_footer/', WebViewSet.as_view({'get': 'our_services_for_footer'}),
         name='get_our_services_for_footer'),
    path('get_contact_us_info/', WebViewSet.as_view({'get': 'contact_us_info'}), name='get_contact_us_info'),
    path('get_contact_us_info_for_footer/', WebViewSet.as_view({'get': 'contact_us_info_for_footer'}),
         name='get_contact_us_info_for_footer'),
    path('get_web_social_media/', WebViewSet.as_view({'get': 'web_social_media'}), name='get_web_social_media'),
    path('get_calendar_datas/', WebViewSet.as_view({'get': 'calendar_datas'}), name='get_calendar_datas'),
    path('get_calendar_data_info/', WebViewSet.as_view({'get': 'calendar_data_info'}), name='get_calendar_data_info'),
    path('get_gallery_by_id/<int:pk>/', WebViewSet.as_view({'get': 'get_gallery_by_id'}), name='get_gallery_by_id'),
    path('get_categories/', WebViewSet.as_view({'get': 'get_categories'}), name='get_categories'),
]
