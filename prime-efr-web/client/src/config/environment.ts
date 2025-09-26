// Environment configuration
const env = {
  isDevelopment: import.meta.env.MODE === 'development',
  isProduction: import.meta.env.MODE === 'production',
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  appEnv: import.meta.env.VITE_APP_ENV || 'development',
};

// Validate required environment variables
const requiredEnvVars = ['VITE_API_URL'];

if (env.isProduction) {
  requiredEnvVars.forEach(varName => {
    if (!import.meta.env[varName]) {
      console.warn(`Missing required environment variable: ${varName}`);
    }
  });
}

export default env;