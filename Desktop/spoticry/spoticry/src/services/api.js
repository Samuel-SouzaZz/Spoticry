import axios from 'axios';
import { config } from '../utils/config'; // Ensure you have a config file with API URL

const api = axios.create({
  baseURL: config.API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
