import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch top downloaded files
 * @param {number} limit - Number of top results to return
 * @returns {Promise} Response data
 */
export const getTopDownloads = async (limit = 10) => {
  try {
    const response = await api.get('/downloads-per-file/top/', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching top downloads:', error);
    throw error;
  }
};

/**
 * Fetch top IPs by bandwidth usage
 * @param {number} limit - Number of top results to return
 * @returns {Promise} Response data
 */
export const getTopBandwidth = async (limit = 10) => {
  try {
    const response = await api.get('/bandwidth-per-ip/top/', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching top bandwidth:', error);
    throw error;
  }
};

/**
 * Fetch peak traffic hours data
 * @returns {Promise} Response data
 */
export const getPeakTraffic = async () => {
  try {
    const response = await api.get('/peak-traffic/');
    return response.data;
  } catch (error) {
    console.error('Error fetching peak traffic:', error);
    throw error;
  }
};

export default api;
