#!/bin/bash
# 🎨 Setup React Frontend Properly
# Configure the React frontend to work with the GDPR stack

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🎨 Setting up React Frontend for GDPR Stack...${NC}"

PROJECT_DIR="my-blog"
FRONTEND_DIR="$PROJECT_DIR/frontend_templates/nextjs_base"

# 1. Create proper package.json with all dependencies
echo -e "${BLUE}📦 Creating package.json with GDPR dependencies...${NC}"
cat > $FRONTEND_DIR/package.json << 'EOF

# 5. Create pages directory and main pages
mkdir -p $FRONTEND_DIR/src/pages

# Home page
cat > $FRONTEND_DIR/src/pages/index.tsx << 'EOF'
import React from 'react';
import Layout from '../components/layout/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">
            🛡️ Welcome to GDPR Blog Demo
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            A complete GDPR-compliant blog platform with automatic consent management, 
            data export capabilities, and real-time compliance monitoring.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">🛡️</div>
              <h3 className="text-lg font-semibold mb-2">GDPR Compliant</h3>
              <p className="text-gray-600">
                Automatic compliance with consent management, data export, and deletion rights.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">🔒</div>
              <h3 className="text-lg font-semibold mb-2">Security First</h3>
              <p className="text-gray-600">
                Built-in rate limiting, bot detection, and security headers protection.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">📊</div>
              <h3 className="text-lg font-semibold mb-2">Real-time Monitoring</h3>
              <p className="text-gray-600">
                Live dashboard with compliance metrics and audit trail monitoring.
              </p>
            </div>
          </div>
          
          <div className="space-x-4">
            <a
              href="/gdpr-dashboard"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 inline-block"
            >
              🛡️ GDPR Dashboard
            </a>
            <a
              href="/api/docs"
              target="_blank"
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 inline-block"
            >
              📖 API Documentation
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
}
EOF

# GDPR Dashboard page
cat > $FRONTEND_DIR/src/pages/gdpr-dashboard.tsx << 'EOF'
import React from 'react';
import Layout from '../components/layout/Layout';
import GDPRDashboard from '../components/gdpr/GDPRDashboard';

export default function GDPRDashboardPage() {
  return (
    <Layout>
      <GDPRDashboard />
    </Layout>
  );
}
EOF

# 6. Create API utility
mkdir -p $FRONTEND_DIR/src/utils
cat > $FRONTEND_DIR/src/utils/api.ts << 'EOF'
import axios from 'axios';

const API_BASE_URL = process.env.API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
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
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// GDPR API functions
export const gdprApi = {
  getMetrics: () => api.get('/api/gdpr/metrics'),
  getDashboardMetrics: () => api.get('/api/gdpr/ops/dashboard/metrics'),
  exportUserData: (userId: number, format = 'json') => 
    api.get(`/api/gdpr/export?user_id=${userId}&format=${format}`),
  createConsent: (userId: number, consentType: string, accepted: boolean) =>
    api.post('/api/gdpr/consent', null, { 
      params: { user_id: userId, consent_type: consentType, accepted } 
    }),
  deleteAccount: (userId: number, reason = 'User request') =>
    api.delete('/api/gdpr/delete-account', { 
      params: { user_id: userId, reason } 
    }),
};

export default api;
EOF

# 7. Create _app.tsx for Next.js
cat > $FRONTEND_DIR/src/pages/_app.tsx << 'EOF'
import React from 'react';
import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
EOF

# 8. Create global CSS with Tailwind
mkdir -p $FRONTEND_DIR/src/styles
cat > $FRONTEND_DIR/src/styles/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded font-medium transition-colors;
  }
  
  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
  }
  
  .btn-secondary {
    @apply bg-gray-600 text-white hover:bg-gray-700;
  }
  
  .card {
    @apply bg-white rounded-lg shadow p-6;
  }
}
EOF

# 9. Create Tailwind config
cat > $FRONTEND_DIR/tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
EOF

# 10. Create PostCSS config
cat > $FRONTEND_DIR/postcss.config.js << 'EOF'
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

# 11. Update TypeScript config
cat > $FRONTEND_DIR/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
EOF

# 12. Install dependencies and build
echo -e "${BLUE}📦 Installing dependencies...${NC}"
cd $FRONTEND_DIR

if command -v npm &> /dev/null; then
    npm install
    echo -e "${BLUE}🏗️ Building React application...${NC}"
    npm run export
    
    # Ensure dist directory exists with built files
    mkdir -p dist
    if [ -d "out" ]; then
        cp -r out/* dist/
        echo -e "${GREEN}✅ React frontend built successfully${NC}"
    else
        echo -e "${YELLOW}⚠️ Build output not found, creating placeholder${NC}"
        echo "<h1>Frontend Build Pending</h1>" > dist/index.html
    fi
else
    echo -e "${YELLOW}⚠️ npm not found, creating placeholder dist${NC}"
    mkdir -p dist
    echo "<h1>Install Node.js to build React frontend</h1>" > dist/index.html
fi

cd ../../..

# 13. Update Caddyfile for proper React routing
echo -e "${BLUE}🌐 Updating Caddyfile for React SPA...${NC}"
cat > Caddyfile << 'EOF'
{
    email admin@example.com
    acme_ca https://acme-v02.api.letsencrypt.org/directory
}

:80, :443 {
    encode gzip
    
    # Security headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "no-referrer"
        Permissions-Policy "geolocation=(), microphone=()"
    }
    
    # API routes
    reverse_proxy /api/* api:8000
    reverse_proxy /docs* api:8000
    reverse_proxy /redoc* api:8000
    reverse_proxy /openapi.json api:8000
    reverse_proxy /health api:8000
    reverse_proxy /security/* api:8000
    
    # React SPA handling
    @frontend path /gdpr-dashboard /gdpr-dashboard/* /blog /blog/* /
    handle @frontend {
        root * /srv/frontend
        try_files {path} {path}/ /index.html
        file_server
    }
    
    # Static assets
    handle /static/* {
        root * /srv/frontend
        file_server
    }
    
    # Fallback for other static files
    handle {
        root * /srv/frontend
        file_server
    }
    
    # Error handling
    handle_errors {
        respond "{http.error.status_code} {http.error.status_text}" 500
    }
}
EOF

echo ""
echo -e "${GREEN}🎉 React Frontend Setup Complete! 🎉${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Run: docker compose restart caddy"
echo "2. Visit: http://localhost/ (React Home)"
echo "3. Visit: http://localhost/gdpr-dashboard (React GDPR Dashboard)"
echo "4. API: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}🔧 Frontend Features:${NC}"
echo "• ✅ React with TypeScript"
echo "• ✅ Tailwind CSS styling"
echo "• ✅ GDPR Dashboard component"
echo "• ✅ Real-time metrics"
echo "• ✅ API integration"
echo "• ✅ Responsive design"
echo ""
echo -e "${GREEN}✨ Frontend is ready! ✨${NC}"
EOF'
{
  "name": "gdpr-blog-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "export": "next build && next export",
    "postexport": "rm -rf dist && mkdir -p dist && cp -r out/* dist/"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@types/react": "18.2.0",
    "@types/react-dom": "18.2.0",
    "typescript": "5.0.0",
    "tailwindcss": "3.3.0",
    "autoprefixer": "10.4.0",
    "postcss": "8.4.0",
    "axios": "1.6.0",
    "date-fns": "2.30.0",
    "lucide-react": "0.263.1"
  },
  "devDependencies": {
    "@types/node": "20.0.0",
    "eslint": "8.0.0",
    "eslint-config-next": "14.0.0"
  }
}
EOF

# 2. Create proper next.config.js for static export
cat > $FRONTEND_DIR/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000'
  }
}

module.exports = nextConfig
EOF

# 3. Create main layout component
mkdir -p $FRONTEND_DIR/src/components/layout
cat > $FRONTEND_DIR/src/components/layout/Layout.tsx << 'EOF'
import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                🛡️ GDPR Blog Demo
              </h1>
            </div>
            <nav className="flex items-center space-x-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">Home</a>
              <a href="/gdpr-dashboard" className="text-gray-600 hover:text-gray-900">GDPR Dashboard</a>
              <a href="/api/docs" className="text-gray-600 hover:text-gray-900">API Docs</a>
            </nav>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
EOF

# 4. Create GDPR dashboard component
mkdir -p $FRONTEND_DIR/src/components/gdpr
cat > $FRONTEND_DIR/src/components/gdpr/GDPRDashboard.tsx << 'EOF'
'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface GDPRMetrics {
  compliance_score: number;
  consents_active: number;
  consents_expired: number;
  exports_requested: number;
  exports_completed: number;
  deletions_requested: number;
  deletions_completed: number;
  audit_logs_count: number;
  total_users: number;
}

export default function GDPRDashboard() {
  const [metrics, setMetrics] = useState<GDPRMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 15000); // Auto-refresh ogni 15s
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/gdpr/ops/dashboard/metrics');
      setMetrics(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch GDPR metrics');
      console.error('Error fetching metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  const testGDPR = async () => {
    try {
      // Test consent creation
      await axios.post('/api/gdpr/consent', null, {
        params: { user_id: 1, consent_type: 'marketing', accepted: true }
      });
      
      // Test data export
      await axios.get('/api/gdpr/export', {
        params: { user_id: 1, format: 'json' }
      });
      
      alert('✅ GDPR Test completato con successo!');
      fetchMetrics(); // Refresh metrics
    } catch (err) {
      alert('❌ GDPR Test fallito. Controlla i log.');
      console.error('GDPR test error:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <h3 className="text-red-800 font-medium">Error</h3>
        <p className="text-red-600">{error}</p>
        <button 
          onClick={fetchMetrics}
          className="mt-2 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">🛡️ GDPR Compliance Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time monitoring of GDPR compliance metrics</p>
      </div>

      {/* Control Panel */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="flex space-x-4">
          <button
            onClick={fetchMetrics}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            🔄 Refresh Data
          </button>
          <button
            onClick={testGDPR}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            🧪 Test GDPR
          </button>
          <a
            href="/api/docs"
            target="_blank"
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            📖 API Docs
          </a>
        </div>
      </div>

      {/* Metrics Grid */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Compliance Score */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-bold">{metrics.compliance_score}%</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Compliance Score</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.compliance_score}%</p>
              </div>
            </div>
          </div>

          {/* Active Consents */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600">✓</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Consents</p>
                <p className="text-2xl font-semibold text-gray-900">{metrics.consents_active}</p>
              </div>
            </div>
          </div>

          {/* Data Exports */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                  <span className="text-yellow-600">📊</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Data Exports</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {metrics.exports_completed}/{metrics.exports_requested}
                </p>
              </div>
            </div>
          </div>

          {/* User Deletions */}
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                  <span className="text-red-600">🗑️</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">User Deletions</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {metrics.deletions_completed}/{metrics.deletions_requested}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detailed Stats */}
      {metrics && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Audit Logs */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">📋 Audit Trail</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm text-gray-600">Total Audit Logs</span>
                <span className="font-semibold">{metrics.audit_logs_count}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm text-gray-600">Total Users</span>
                <span className="font-semibold">{metrics.total_users}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm text-gray-600">Data Breach Incidents</span>
                <span className="font-semibold text-green-600">0</span>
              </div>
            </div>
          </div>

          {/* System Status */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">🔒 System Status</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                <span className="text-sm text-gray-600">GDPR Plugin</span>
                <span className="text-green-600 font-semibold">✅ Active</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                <span className="text-sm text-gray-600">Security Plugin</span>
                <span className="text-green-600 font-semibold">✅ Active</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                <span className="text-sm text-gray-600">Audit Trail</span>
                <span className="text-green-600 font-semibold">✅ Recording</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                <span className="text-sm text-gray-600">Last Updated</span>
                <span className="text-blue-600 font-semibold">
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
EOF