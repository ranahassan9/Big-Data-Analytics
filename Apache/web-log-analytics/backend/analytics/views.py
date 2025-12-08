from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FileDownload, BandwidthUsage, TrafficHour
from .serializers import FileDownloadSerializer, BandwidthUsageSerializer, TrafficHourSerializer


class FileDownloadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for file downloads analytics
    Endpoint: /api/downloads-per-file
    """
    queryset = FileDownload.objects.all()
    serializer_class = FileDownloadSerializer

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N downloaded files"""
        limit = int(request.query_params.get('limit', 10))
        top_files = self.queryset[:limit]
        serializer = self.get_serializer(top_files, many=True)
        return Response(serializer.data)


class BandwidthUsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for bandwidth usage per IP
    Endpoint: /api/bandwidth-per-ip
    """
    queryset = BandwidthUsage.objects.all()
    serializer_class = BandwidthUsageSerializer

    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N IPs by bandwidth"""
        limit = int(request.query_params.get('limit', 10))
        top_ips = self.queryset[:limit]
        serializer = self.get_serializer(top_ips, many=True)
        return Response(serializer.data)


class TrafficHourViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for peak traffic hours
    Endpoint: /api/peak-traffic
    """
    queryset = TrafficHour.objects.all()
    serializer_class = TrafficHourSerializer

    @action(detail=False, methods=['get'])
    def peak(self, request):
        """Get peak traffic hours"""
        limit = int(request.query_params.get('limit', 5))
        peak_hours = self.queryset.order_by('-request_count')[:limit]
        serializer = self.get_serializer(peak_hours, many=True)
        return Response(serializer.data)
