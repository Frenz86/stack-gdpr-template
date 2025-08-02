import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-4xl mx-auto text-center p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          🛡️ My GDPR Blog
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          A GDPR-compliant blog platform with automatic compliance monitoring
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl mb-4">🛡️</div>
            <h3 className="font-semibold mb-2">GDPR Compliant</h3>
            <p className="text-gray-600">Automatic consent management and data protection</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl mb-4">🔒</div>
            <h3 className="font-semibold mb-2">Secure</h3>
            <p className="text-gray-600">Built-in security features and monitoring</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-2xl mb-4">📊</div>
            <h3 className="font-semibold mb-2">Monitored</h3>
            <p className="text-gray-600">Real-time compliance dashboard</p>
          </div>
        </div>
        
        <div className="space-x-4">
          <a
            href="/api/docs"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
          >
            📖 API Documentation
          </a>
          <a
            href="/api/gdpr/metrics"
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700"
          >
            🛡️ GDPR Metrics
          </a>
        </div>
      </div>
    </div>
  );
}
