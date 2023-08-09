from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WeatherAPIView,
    EventsAPIView,
    GoogleRestaurantAPIView,
    PredictionAPIView,
    HeatMapAPIView,
    AttractionViewSet,
    HotelViewSet,
)


app_name = "api"

router = DefaultRouter()
router.register(r'googleAttractions', AttractionViewSet)
router.register(r'googleHotels', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('googleRestaurants/', GoogleRestaurantAPIView.as_view(), name='google-restaurants'),  # Use a unique name here
    path('events/', EventsAPIView.as_view(), name='events'),
    path('weather/', WeatherAPIView.as_view(), name='weather'),
    path('predict/', PredictionAPIView.as_view(), name='predict'),
    path('heatMap/', HeatMapAPIView.as_view(), name='heat-map'),  # Use a unique name here
]
