import 'dotenv/config';

const config = {
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || '0.0.0.0',
    env: process.env.NODE_ENV || 'development',
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'your-secret-key-change-in-production',
  },
  supabase: {
    url: process.env.SUPABASE_URL || '',
    key: process.env.SUPABASE_KEY || '',
  },
  gemini: {
    apiKey: process.env.GEMINI_API_KEY || '',
  },
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:3001',
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info',
  },
};

export default config;
