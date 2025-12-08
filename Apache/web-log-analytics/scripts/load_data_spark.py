
import os
import sys
import django
from dotenv import load_dotenv

# Setup Django environment
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_dir)

env_path = os.path.join(backend_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_analytics.settings')
django.setup()

from analytics.models import FileDownload, BandwidthUsage, TrafficHour
from process_logs_spark import ApacheLogAnalyzerSpark

def load_data_from_spark(hdfs_path):
    print(f"Starting Spark Job for: {hdfs_path}")
    
    analyzer = ApacheLogAnalyzerSpark(hdfs_path)
    
    try:
        # 1. Process Logs (Distributed)
        df = analyzer.process_logs()
        
        # 2. Compute Aggregations (Distributed)
        downloads_df = analyzer.get_downloads_per_file(df)
        bandwidth_df = analyzer.get_bandwidth_per_ip(df)
        traffic_df = analyzer.get_traffic_per_hour(df)
        
        # 3. Collect Results to Driver (Local)
        # We collect() here because the aggregated results are small enough 
        # to fit in memory and insert into Django.
        print("Collecting results from Spark...")
        downloads_data = downloads_df.collect()
        bandwidth_data = bandwidth_df.collect()
        traffic_data = traffic_df.collect()
        
        # 4. Load into Django Database
        print("Loading into Database...")
        
        # -- Downloads --
        FileDownload.objects.all().delete()
        FileDownload.objects.bulk_create([
            FileDownload(
                file_path=row['endpoint'],
                download_count=row['download_count'],
                total_bytes=row['total_bytes'] if row['total_bytes'] is not None else 0
            ) for row in downloads_data if row['endpoint']
        ])
        
        # -- Bandwidth --
        BandwidthUsage.objects.all().delete()
        BandwidthUsage.objects.bulk_create([
            BandwidthUsage(
                ip_address=row['ip'],
                total_bytes=row['total_bytes'] if row['total_bytes'] is not None else 0,
                request_count=row['request_count']
            ) for row in bandwidth_data if row['ip']
        ])
        
        # -- Traffic --
        TrafficHour.objects.all().delete()
        TrafficHour.objects.bulk_create([
            TrafficHour(
                hour=row['hour'] if row['hour'] is not None else 0,
                request_count=row['request_count'],
                total_bytes=row['total_bytes'] if row['total_bytes'] is not None else 0
            ) for row in traffic_data
        ])
        
        print("Successfully loaded all data from HDFS/Spark!")
        
    finally:
        analyzer.stop()

if __name__ == "__main__":
    # Default to environment variable if argument not provided
    default_hdfs = os.getenv('HDFS_URL')
    
    if len(sys.argv) < 2:
        if default_hdfs:
            hdfs_path = f"{default_hdfs}/logs/access.log"
            print(f"No path provided. Using default from env: {hdfs_path}")
        else:
            print("Usage: python load_data_spark.py <hdfs_path>")
            print("Example: python load_data_spark.py hdfs://namenode:9000/logs/access.log")
            sys.exit(1)
    else:
        hdfs_path = sys.argv[1]

    load_data_from_spark(hdfs_path)
