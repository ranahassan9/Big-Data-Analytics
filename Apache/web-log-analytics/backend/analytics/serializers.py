from rest_framework import serializers
from .models import FileDownload, BandwidthUsage, TrafficHour


class FileDownloadSerializer(serializers.ModelSerializer):
    """Serializer for FileDownload model"""
    class Meta:
        model = FileDownload
        fields = ['id', 'file_path', 'download_count', 'total_bytes', 'last_updated']


class BandwidthUsageSerializer(serializers.ModelSerializer):
    """Serializer for BandwidthUsage model"""
    bandwidth_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = BandwidthUsage
        fields = ['id', 'ip_address', 'total_bytes', 'bandwidth_mb', 'request_count', 'last_updated']
    
    def get_bandwidth_mb(self, obj):
        """Convert bytes to MB"""
        return round(obj.total_bytes / (1024 * 1024), 2)


class TrafficHourSerializer(serializers.ModelSerializer):
    """Serializer for TrafficHour model"""
    hour_label = serializers.SerializerMethodField()
    
    class Meta:
        model = TrafficHour
        fields = ['id', 'hour', 'hour_label', 'request_count', 'total_bytes', 'last_updated']
    
    def get_hour_label(self, obj):
        """Format hour for display"""
        return f"{obj.hour:02d}:00"
