from django.db import models


class FileDownload(models.Model):
    """
    Model to store file download analytics
    
    Tracks the number of times each file/endpoint was accessed
    and the total bytes transferred for that file.
    """
    file_path = models.CharField(max_length=500, unique=True)
    download_count = models.IntegerField(default=0)
    total_bytes = models.BigIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-download_count']

    def __str__(self):
        return f"{self.file_path} - {self.download_count} downloads"


class BandwidthUsage(models.Model):
    """
    Model to store bandwidth usage per IP address
    
    Tracks total bytes consumed and request count for each
    unique IP address accessing the server.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    total_bytes = models.BigIntegerField(default=0)
    request_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_bytes']

    def __str__(self):
        return f"{self.ip_address} - {self.total_bytes} bytes"


class TrafficHour(models.Model):
    """
    Model to store traffic distribution by hour of day
    
    Aggregates request count and bytes transferred for each
    hour (0-23) to identify peak traffic periods.
    """
    hour = models.IntegerField()  # 0-23
    request_count = models.IntegerField(default=0)
    total_bytes = models.BigIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-request_count', '-total_bytes']
        unique_together = ['hour']

    def __str__(self):
        return f"Hour {self.hour} - {self.request_count} requests"
