# 📊 Big Data Web Log Analytics

A full-stack Big Data application that processes Apache web server logs using **Hadoop HDFS** and **Apache Spark**, stores the analytics in **MySQL**, and visualizes the insights via a **Django** backend and **React** frontend.

## 📁 Project Structure

```
Apache/
│
├──web-log-analytics/
│      │
│      ├── 📄 Dockerfile                         # Docker build for Backend/Spark
│      │
│      ├── 📂 backend/                           # Django REST API
│      │   ├── 📄 manage.py                      # Django management script
│      │   ├── 📄 requirements.txt               # Python dependencies
│      │   │
│      │   ├── 📂 analytics/                     # Main Django app
│      │   │   ├── 📄 models.py                  # Database models (3 models)
│      │   │   ├── 📄 views.py                   # API viewsets (3 viewsets)
│      │   │   ├── 📄 serializers.py             # DRF serializers
│      │   │   └── 📄 urls.py                    # API routing
│      │   │
│      │   └── 📂 log_analytics/                 # Django project settings
│      │       └── 📄 settings.py                # Project configuration
│      │
│      ├── 📂 frontend/                          # React application
│      │   ├── 📄 package.json                   # Node dependencies
│      │   ├── 📂 src/
│      │   │   ├── 📄 App.js                     # Main dashboard component
│      │   │   └── 📂 services/
│      │   │       └── 📄 api.js                 # API client
│      │
│      └── 📂 scripts/                           # Big Data Processing
│          ├── 📄 process_logs_spark.py          # PySpark Log Analyzer
│          ├── 📄 load_data_spark.py             # Spark Job Runner & DB Loader
│          └── 📄 requirements.txt               # Script dependencies
│
├── docker-compose.yml                           # Container Orchestration
├── Apache_2k.log                                # Sample Log File 1
└── Apache_access_sample.log                     # Sample Log File 2
```

## 🔑 Key Components

### Big Data Layer (Hadoop & Spark)
- **HDFS (Hadoop Distributed File System)**: Stores raw log files distributedly.
- **Apache Spark (PySpark)**: Processes logs in parallel using RDDs/DataFrames.
- **Spark Master/Worker**: Distributed computing cluster managed via Docker.

### Backend (Django)
- **REST API**: Serves analyzed data to the frontend.
- **MySQL Database**: Stores aggregated results (Downloads, Bandwidth, Traffic).
- **Dockerized**: Runs in a container connected to the Spark cluster.

### Frontend (React)
- **Dashboard**: Visualizes data using Chart.js (Bar, Pie, Line charts).
- **Real-time**: Fetches data from the Django API.

## 🎯 Data Flow

```
Apache Log File
      ↓
[Hadoop HDFS] (Storage)
      ↓
[process_logs_spark.py] (PySpark Job)
      ↓
  Spark Cluster (Processing)
      ↓
[load_data_spark.py] (Driver)
      ↓
  MySQL Database
      ↓
[Django REST API]
      ↓
   JSON Response
      ↓
[React Frontend]
      ↓
Interactive Charts
```

## 🚀 How to Run

### 1. Start the Docker Cluster
```powershell
docker-compose up -d --build
```

### 2. Upload Logs to HDFS
Copy your log file into the Hadoop NameNode and put it into HDFS:
```powershell
docker cp Apache/Apache_2k.log namenode:/tmp/Apache_2k.log
docker-compose exec namenode hdfs dfs -mkdir -p /logs
docker-compose exec namenode hdfs dfs -put /tmp/Apache_2k.log /logs/Apache_2k.log
```

### 3. Run Spark Analysis
Trigger the Spark job to process the file and load data into MySQL:
```powershell
docker-compose run backend python scripts/load_data_spark.py hdfs://namenode:9000/logs/Apache_2k.log
```

### 4. View Dashboard
- **Backend API**: http://localhost:8000/api/
- **Frontend**: Run locally:
  ```powershell
  cd Apache/web-log-analytics/frontend
  npm start
  ```
  Access at: http://localhost:3000

## 📊 Database Schema

### FileDownload
- `file_path`: Unique path of the file.
- `download_count`: Number of times downloaded.
- `total_bytes`: Total data transferred.

### BandwidthUsage
- `ip_address`: Client IP.
- `total_bytes`: Total bandwidth consumed.
- `request_count`: Total requests made.

### TrafficHour
- `hour`: Hour of the day (0-23).
- `request_count`: Requests during this hour.
- `total_bytes`: Data transferred during this hour.

## 💻 Technology Stack

- **Big Data**: Apache Hadoop 3.2, Apache Spark 3.5 (PySpark)
- **Backend**: Django 4.2, Django REST Framework, MySQL
- **Frontend**: React 18, Chart.js, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose
