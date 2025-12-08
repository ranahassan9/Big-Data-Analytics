import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { getTopDownloads, getTopBandwidth, getPeakTraffic } from './services/api';
import './App.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

function App() {
  const [downloads, setDownloads] = useState([]);
  const [bandwidth, setBandwidth] = useState([]);
  const [traffic, setTraffic] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [downloadsData, bandwidthData, trafficData] = await Promise.all([
        getTopDownloads(10),
        getTopBandwidth(10),
        getPeakTraffic(),
      ]);

      setDownloads(downloadsData);
      setBandwidth(bandwidthData);
      setTraffic(trafficData.results || trafficData);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch data. Please ensure the backend is running.');
      setLoading(false);
      console.error('Error fetching data:', err);
    }
  };

  // Bar Chart - Downloads per File
  const downloadsChartData = {
    labels: downloads.map(d => {
      const path = d.file_path;
      return path.length > 30 ? '...' + path.slice(-27) : path;
    }),
    datasets: [
      {
        label: 'Download Count',
        data: downloads.map(d => d.download_count),
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  };

  const downloadsChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Top 10 Downloaded Files',
        font: {
          size: 16,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  // Pie Chart - Bandwidth Usage
  const bandwidthChartData = {
    labels: bandwidth.map(b => b.ip_address),
    datasets: [
      {
        label: 'Bandwidth (MB)',
        data: bandwidth.map(b => b.bandwidth_mb),
        backgroundColor: [
          'rgba(239, 68, 68, 0.7)',
          'rgba(249, 115, 22, 0.7)',
          'rgba(234, 179, 8, 0.7)',
          'rgba(34, 197, 94, 0.7)',
          'rgba(59, 130, 246, 0.7)',
          'rgba(147, 51, 234, 0.7)',
          'rgba(236, 72, 153, 0.7)',
          'rgba(20, 184, 166, 0.7)',
          'rgba(251, 146, 60, 0.7)',
          'rgba(132, 204, 22, 0.7)',
        ],
        borderColor: 'rgba(255, 255, 255, 1)',
        borderWidth: 2,
      },
    ],
  };

  const bandwidthChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Top 10 IPs by Bandwidth Usage',
        font: {
          size: 16,
        },
      },
    },
  };

  // Line Chart - Traffic by Hour
  const trafficChartData = {
    labels: traffic.map(t => `${String(t.hour).padStart(2, '0')}:00`),
    datasets: [
      {
        label: 'Request Count',
        data: traffic.map(t => t.request_count),
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const trafficChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Traffic Distribution by Hour',
        font: {
          size: 16,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  // Calculate statistics
  const totalDownloads = downloads.reduce((sum, d) => sum + d.download_count, 0);
  const totalBandwidth = bandwidth.reduce((sum, b) => sum + b.bandwidth_mb, 0);
  const totalRequests = traffic.reduce((sum, t) => sum + t.request_count, 0);
  const peakHour = traffic.length > 0 
    ? traffic.reduce((max, t) => t.request_count > max.request_count ? t : max, traffic[0])
    : null;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">⚠️ {error}</div>
          <button
            onClick={fetchData}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">📊 Web Log Analytics Dashboard</h1>
          <p className="text-blue-100 mt-2">Apache Access Log Analysis using Pandas & Django REST Framework</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="stat-card">
            <div className="text-blue-100 text-sm uppercase tracking-wide">Total Downloads</div>
            <div className="text-3xl font-bold mt-2">{totalDownloads.toLocaleString()}</div>
          </div>
          
          <div className="stat-card bg-gradient-to-br from-green-500 to-green-600">
            <div className="text-green-100 text-sm uppercase tracking-wide">Total Requests</div>
            <div className="text-3xl font-bold mt-2">{totalRequests.toLocaleString()}</div>
          </div>
          
          <div className="stat-card bg-gradient-to-br from-purple-500 to-purple-600">
            <div className="text-purple-100 text-sm uppercase tracking-wide">Total Bandwidth</div>
            <div className="text-3xl font-bold mt-2">{totalBandwidth.toFixed(2)} MB</div>
          </div>
          
          <div className="stat-card bg-gradient-to-br from-orange-500 to-orange-600">
            <div className="text-orange-100 text-sm uppercase tracking-wide">Peak Hour</div>
            <div className="text-3xl font-bold mt-2">
              {peakHour ? `${String(peakHour.hour).padStart(2, '0')}:00` : 'N/A'}
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Downloads Bar Chart */}
          <div className="card">
            <div className="h-96">
              <Bar data={downloadsChartData} options={downloadsChartOptions} />
            </div>
          </div>

          {/* Bandwidth Pie Chart */}
          <div className="card">
            <div className="h-96">
              <Pie data={bandwidthChartData} options={bandwidthChartOptions} />
            </div>
          </div>

          {/* Traffic Line Chart */}
          <div className="card lg:col-span-2">
            <div className="h-96">
              <Line data={trafficChartData} options={trafficChartOptions} />
            </div>
          </div>
        </div>

        {/* Data Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          {/* Top Downloads Table */}
          <div className="card">
            <h3 className="card-title">Top Downloads Details</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Count</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {downloads.slice(0, 5).map((item, index) => (
                    <tr key={index}>
                      <td className="px-4 py-3 text-sm text-gray-900 truncate max-w-xs" title={item.file_path}>
                        {item.file_path}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">{item.download_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Top Bandwidth Table */}
          <div className="card">
            <h3 className="card-title">Top Bandwidth Consumers</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bandwidth (MB)</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {bandwidth.slice(0, 5).map((item, index) => (
                    <tr key={index}>
                      <td className="px-4 py-3 text-sm text-gray-900">{item.ip_address}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{item.bandwidth_mb} MB</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Refresh Button */}
        <div className="text-center mt-8">
          <button
            onClick={fetchData}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition shadow-md"
          >
            🔄 Refresh Data
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 mt-12">
        <div className="container mx-auto px-4 py-6 text-center">
          <p>Built with React, Django REST Framework, Pandas, and MySQL</p>
          <p className="text-sm mt-2">Big Data Analytics Project</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
