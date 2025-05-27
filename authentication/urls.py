from django.urls import path
from .views import LoginViewSet

urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'login_user'}), name='login'),
    path('logout/', LoginViewSet.as_view({'post': 'logout', }), name='logout'),
]