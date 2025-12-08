from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileDownloadViewSet, BandwidthUsageViewSet, TrafficHourViewSet

router = DefaultRouter()
router.register(r'downloads-per-file', FileDownloadViewSet, basename='file-download')
router.register(r'bandwidth-per-ip', BandwidthUsageViewSet, basename='bandwidth-usage')
router.register(r'peak-traffic', TrafficHourViewSet, basename='peak-traffic')

urlpatterns = [
    path('', include(router.urls)),
]
