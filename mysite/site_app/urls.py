from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Weather', views.WeatherViewSet)
router.register(r'Yield', views.YieldViewSet)
router.register(r'Results', views.ResultsViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
]
