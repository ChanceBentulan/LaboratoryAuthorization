import axios from 'axios';

// Add a request interceptor
axios.interceptors.request.use(
    function(config) {
        // Retrieve token from localStorage
        const token = localStorage.getItem('token');
        
        // If token exists, set Authorization header
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        if (config.data instanceof FormData) {
            // If FormData, set content type to multipart/form-data
            config.headers['Content-Type'] = 'multipart/form-data';
          } else if (config.data && config.data.constructor === Object) {
            // If JSON object, set content type to application/json
            config.headers['Content-Type'] = 'application/json';
          }
        return config;
    },
    function(error) {
        return Promise.reject(error);
    }
);

export default axios;