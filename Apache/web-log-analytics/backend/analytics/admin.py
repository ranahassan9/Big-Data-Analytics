from django.contrib import admin
from .models import FileDownload, BandwidthUsage, TrafficHour


@admin.register(FileDownload)
class FileDownloadAdmin(admin.ModelAdmin):
    list_display = ['file_path', 'download_count', 'total_bytes', 'last_updated']
    search_fields = ['file_path']
    ordering = ['-download_count']


@admin.register(BandwidthUsage)
class BandwidthUsageAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'total_bytes', 'request_count', 'last_updated']
    search_fields = ['ip_address']
    ordering = ['-total_bytes']


@admin.register(TrafficHour)
class TrafficHourAdmin(admin.ModelAdmin):
    list_display = ['hour', 'request_count', 'total_bytes', 'last_updated']
    ordering = ['hour']
