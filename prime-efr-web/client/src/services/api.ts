import axios from 'axios';

// Get API URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const enrollmentAPI = {
  process: (data: any, config: any) => 
    api.post('/enrollment/process', { data, config }),
  
  getSummary: () => 
    api.get('/enrollment/summary'),
  
  export: (format: string, tabData: any) => 
    api.post('/enrollment/export', { format, tabData }),
};

export const validationAPI = {
  validate: (sourceData: any, tabData: any, config: any) =>
    api.post('/validation/validate', { sourceData, tabData, config }),
  
  getRules: () =>
    api.get('/validation/rules'),
  
  applyFix: (issueId: string, fix: any) =>
    api.post('/validation/apply-fix', { issueId, fix }),
};

export const configAPI = {
  getAll: () =>
    api.get('/config'),
  
  updatePlanMappings: (mappings: any) =>
    api.post('/config/plan-mappings', { mappings }),
  
  addPlanMapping: (code: string, type: string) =>
    api.post('/config/plan-mappings/add', { code, type }),
  
  removePlanMapping: (code: string) =>
    api.delete(`/config/plan-mappings/${code}`),
  
  export: () =>
    api.get('/config/export'),
  
  import: (config: any) =>
    api.post('/config/import', config),
};

export const uploadAPI = {
  parseFile: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return api.post('/upload/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  validateStructure: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return api.post('/upload/validate-structure', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default api;