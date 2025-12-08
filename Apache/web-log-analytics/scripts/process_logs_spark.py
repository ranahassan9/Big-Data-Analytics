
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, count, sum as _sum, hour, to_timestamp, when

class ApacheLogAnalyzerSpark:
    """
    Analyzer for Apache access logs using PySpark
    
    Reads logs from HDFS and computes analytics using distributed processing.
    """
    
    def __init__(self, hdfs_file_path):
        """
        Initialize Spark Session
        """
        self.hdfs_file_path = hdfs_file_path
        self.spark = SparkSession.builder \
            .appName("ApacheLogAnalytics") \
            .master("local[*]") \
            .getOrCreate()
            
        # Regex pattern for Apache Combined Log Format
        # 1: IP, 2: Timestamp, 3: Method, 4: Endpoint, 5: Protocol, 6: Status, 7: Bytes
        self.log_pattern = r'^(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s+(\S+)\s+(\S+)" (\d{3}) (\S+)'

    def process_logs(self):
        """
        Read from HDFS, parse logs, and return a structured DataFrame
        """
        # Read raw text from HDFS
        raw_logs = self.spark.read.text(self.hdfs_file_path)
        
        # Extract columns using Regex
        parsed_df = raw_logs.select(
            regexp_extract('value', self.log_pattern, 1).alias('ip'),
            regexp_extract('value', self.log_pattern, 2).alias('timestamp_str'),
            regexp_extract('value', self.log_pattern, 3).alias('method'),
            regexp_extract('value', self.log_pattern, 4).alias('endpoint'),
            regexp_extract('value', self.log_pattern, 6).cast('integer').alias('status'),
            regexp_extract('value', self.log_pattern, 7).alias('bytes_str')
        )

        # Clean up data types
        # Handle '-' in bytes (convert to 0)
        parsed_df = parsed_df.withColumn(
            'bytes', 
            when(col('bytes_str') == '-', 0).otherwise(col('bytes_str').cast('long'))
        )
        
        # Convert timestamp (Format: 10/Oct/2000:13:55:36 -0700)
        # Note: Spark timestamp parsing format might need adjustment based on your specific log locale
        parsed_df = parsed_df.withColumn(
            'timestamp', to_timestamp(col('timestamp_str'), "dd/MMM/yyyy:HH:mm:ss Z")
        )
        
        parsed_df = parsed_df.withColumn('hour', hour(col('timestamp')))
        
        return parsed_df

    def get_downloads_per_file(self, df):
        """Aggregate: Downloads per file"""
        return df.groupBy('endpoint').agg(
            count('*').alias('download_count'),
            _sum('bytes').alias('total_bytes')
        ).orderBy(col('download_count').desc())

    def get_bandwidth_per_ip(self, df):
        """Aggregate: Bandwidth per IP"""
        return df.groupBy('ip').agg(
            _sum('bytes').alias('total_bytes'),
            count('*').alias('request_count')
        ).orderBy(col('total_bytes').desc())

    def get_traffic_per_hour(self, df):
        """Aggregate: Traffic per hour"""
        return df.groupBy('hour').agg(
            count('*').alias('request_count'),
            _sum('bytes').alias('total_bytes')
        ).orderBy('hour')

    def stop(self):
        self.spark.stop()
