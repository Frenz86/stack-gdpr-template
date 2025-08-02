#!/bin/bash
# 🎨 Deploy GDPR Dashboard - Ultimo step per completare la demo

echo "🎨 Deploying GDPR Dashboard..."

# 1. Crea la directory per il frontend
mkdir -p public

# 2. Crea la dashboard HTML completa
cat > public/gdpr-dashboard.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDPR Compliance Dashboard - Live Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .dashboard-header {
            background: linear-gradient(135deg, #2d3748, #4a5568);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }

        .dashboard-header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .status-indicator {
            display: inline-block;
            padding: 8px 20px;
            background: #10b981;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .dashboard-content {
            padding: 30px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .metric-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            border-left: 5px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }

        .metric-card.compliance { border-left-color: #10b981; color: #10b981; }
        .metric-card.consents { border-left-color: #3b82f6; color: #3b82f6; }
        .metric-card.exports { border-left-color: #f59e0b; color: #f59e0b; }
        .metric-card.deletions { border-left-color: #ef4444; color: #ef4444; }
        .metric-card.audit { border-left-color: #8b5cf6; color: #8b5cf6; }
        .metric-card.security { border-left-color: #06b6d4; color: #06b6d4; }

        .metric-label {
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
            position: relative;
            z-index: 1;
        }

        .metric-description {
            font-size: 0.85em;
            color: #6b7280;
            line-height: 1.4;
        }

        .details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 40px;
        }

        .detail-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        }

        .detail-section h3 {
            font-size: 1.3em;
            margin-bottom: 20px;
            color: #374151;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }

        .audit-list, .alert-list {
            list-style: none;
        }

        .audit-list li, .alert-list li {
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
            font-size: 0.9em;
            color: #6b7280;
            display: flex;
            align-items: center;
        }

        .audit-list li:last-child, .alert-list li:last-child {
            border-bottom: none;
        }

        .audit-list li::before {
            content: '📋';
            margin-right: 10px;
        }

        .alert-list li::before {
            content: '🔐';
            margin-right: 10px;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #6b7280;
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #e5e7eb;
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: spin 1s ease-in-out infinite;
            margin-left: 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .error {
            text-align: center;
            padding: 40px;
            color: #ef4444;
            background: #fef2f2;
            border-radius: 10px;
            margin: 20px 0;
        }

        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            font-size: 0.9em;
            color: white;
        }

        .btn-primary { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
        .btn-success { background: linear-gradient(135deg, #10b981, #059669); }
        .btn-warning { background: linear-gradient(135deg, #f59e0b, #d97706); }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .refresh-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 0.8em;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .refresh-indicator.show {
            opacity: 1;
        }

        @media (max-width: 768px) {
            .dashboard-container {
                margin: 10px;
                border-radius: 15px;
            }

            .metrics-grid {
                grid-template-columns: 1fr;
            }

            .details-grid {
                grid-template-columns: 1fr;
            }

            .controls {
                flex-direction: column;
                align-items: center;
            }
        }

        .compliance-score {
            position: relative;
            display: inline-block;
        }

        .score-ring {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: conic-gradient(#10b981 0deg, #10b981 calc(var(--score) * 3.6deg), #e5e7eb calc(var(--score) * 3.6deg));
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .score-ring::before {
            content: '';
            width: 60px;
            height: 60px;
            background: white;
            border-radius: 50%;
            position: absolute;
        }

        .score-text {
            position: relative;
            z-index: 1;
            font-weight: 700;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1>🛡️ GDPR Compliance Dashboard</h1>
            <div class="status-indicator" id="systemStatus">
                ✅ Sistema Operativo - Live Demo
            </div>
        </div>

        <div class="dashboard-content">
            <div class="controls">
                <button class="btn btn-primary" onclick="refreshDashboard()">🔄 Aggiorna Dati</button>
                <a href="/docs" class="btn btn-success" target="_blank">📖 API Docs</a>
                <button class="btn btn-warning" onclick="runGDPRTests()">🧪 Test GDPR</button>
                <a href=":8025" class="btn btn-primary" target="_blank">📧 MailHog</a>
            </div>

            <div id="loading" class="loading">
                Caricamento dashboard GDPR in corso...
            </div>

            <div id="error" class="error" style="display: none;">
                ❌ Errore nel caricamento dei dati. Verifica che l'API sia in esecuzione
            </div>

            <div id="dashboard-metrics" style="display: none;">
                <div class="metrics-grid">
                    <div class="metric-card compliance">
                        <div class="metric-label">Compliance Score</div>
                        <div class="metric-value">
                            <div class="compliance-score">
                                <div class="score-ring" id="complianceRing">
                                    <div class="score-text" id="complianceScore">-</div>
                                </div>
                            </div>
                        </div>
                        <div class="metric-description">Punteggio complessivo conformità GDPR</div>
                    </div>

                    <div class="metric-card consents">
                        <div class="metric-label">Consensi Attivi</div>
                        <div class="metric-value" id="activeConsents">-</div>
                        <div class="metric-description">Consensi utente attivi vs scaduti</div>
                    </div>

                    <div class="metric-card exports">
                        <div class="metric-label">Export Richiesti</div>
                        <div class="metric-value" id="exportRequests">-</div>
                        <div class="metric-description">Richieste export dati utente</div>
                    </div>

                    <div class="metric-card deletions">
                        <div class="metric-label">Cancellazioni</div>
                        <div class="metric-value" id="deletionRequests">-</div>
                        <div class="metric-description">Richieste cancellazione account</div>
                    </div>

                    <div class="metric-card audit">
                        <div class="metric-label">Audit Logs</div>
                        <div class="metric-value" id="auditLogs">-</div>
                        <div class="metric-description">Operazioni registrate nel sistema</div>
                    </div>

                    <div class="metric-card security">
                        <div class="metric-label">Security Status</div>
                        <div class="metric-value" id="securityStatus">🔐</div>
                        <div class="metric-description">Rate limiting e protezioni attive</div>
                    </div>
                </div>

                <div class="details-grid">
                    <div class="detail-section">
                        <h3>📋 Audit Trail Recenti</h3>
                        <ul class="audit-list" id="recentAudits">
                            <li>Caricamento audit logs...</li>
                        </ul>
                    </div>

                    <div class="detail-section">
                        <h3>🔐 Security Alerts</h3>
                        <ul class="alert-list" id="securityAlerts">
                            <li>Caricamento security status...</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="refresh-indicator" id="refreshIndicator">
        📊 Dashboard aggiornata
    </div>

    <script>
        const API_BASE = '/api';
        let refreshInterval;

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeDashboard();
        });

        async function initializeDashboard() {
            try {
                await fetchDashboardData();
                startAutoRefresh();
                showRefreshIndicator();
            } catch (error) {
                showError();
            }
        }

        async function fetchDashboardData() {
            try {
                // Try the operational dashboard endpoint first
                let response = await fetch(`${API_BASE}/gdpr/ops/dashboard/metrics`);
                
                if (!response.ok) {
                    // Fallback to basic metrics
                    response = await fetch(`${API_BASE}/gdpr/metrics`);
                }

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                updateDashboard(data);
                hideLoading();
                showDashboard();
            } catch (error) {
                console.error('Dashboard fetch error:', error);
                throw error;
            }
        }

        function updateDashboard(data) {
            // Update compliance score with animated ring
            const score = data.compliance_score || 0;
            document.getElementById('complianceScore').textContent = `${score}%`;
            
            const ring = document.getElementById('complianceRing');
            ring.style.setProperty('--score', score);

            // Update metrics
            document.getElementById('activeConsents').textContent = data.consents_active || data.active_consents || 0;
            document.getElementById('exportRequests').textContent = 
                `${data.exports_completed || 0}/${data.exports_requested || 0}`;
            document.getElementById('deletionRequests').textContent = 
                `${data.deletions_completed || 0}/${data.deletions_requested || 0}`;
            document.getElementById('auditLogs').textContent = data.audit_logs_count || 0;

            // Update security status
            const securityEl = document.getElementById('securityStatus');
            if (data.security_alerts && data.security_alerts.length > 0) {
                securityEl.textContent = '⚠️';
                securityEl.parentElement.querySelector('.metric-description').textContent = 
                    `${data.security_alerts.length} alerts attivi`;
            } else {
                securityEl.textContent = '🔐';
                securityEl.parentElement.querySelector('.metric-description').textContent = 
                    'Tutte le protezioni attive';
            }

            // Update audit trail
            updateAuditTrail(data.recent_audits || []);

            // Update security alerts
            updateSecurityAlerts(data.security_alerts || []);
        }

        function updateAuditTrail(audits) {
            const auditList = document.getElementById('recentAudits');
            
            if (audits.length === 0) {
                auditList.innerHTML = '<li>Nessun audit recente disponibile</li>';
                return;
            }

            auditList.innerHTML = audits.slice(0, 8).map(audit => {
                const auditText = typeof audit === 'string' ? audit : 
                    `${audit.action || 'Unknown'} - ${audit.timestamp || 'Recent'}`;
                return `<li>${auditText}</li>`;
            }).join('');
        }

        function updateSecurityAlerts(alerts) {
            const alertList = document.getElementById('securityAlerts');
            
            if (alerts.length === 0) {
                alertList.innerHTML = '<li>Nessun alert di sicurezza</li>';
                return;
            }

            alertList.innerHTML = alerts.slice(0, 6).map(alert => 
                `<li>${alert}</li>`
            ).join('');
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('error').style.display = 'none';
        }

        function showDashboard() {
            document.getElementById('dashboard-metrics').style.display = 'block';
        }

        function showError() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('error').style.display = 'block';
            document.getElementById('dashboard-metrics').style.display = 'none';
        }

        function showRefreshIndicator() {
            const indicator = document.getElementById('refreshIndicator');
            indicator.classList.add('show');
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }

        function startAutoRefresh() {
            // Refresh every 15 seconds
            refreshInterval = setInterval(async () => {
                try {
                    await fetchDashboardData();
                    showRefreshIndicator();
                } catch (error) {
                    console.warn('Auto-refresh failed:', error);
                }
            }, 15000);
        }

        async function refreshDashboard() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('dashboard-metrics').style.display = 'none';
            
            try {
                await fetchDashboardData();
                showRefreshIndicator();
            } catch (error) {
                showError();
            }
        }

        async function runGDPRTests() {
            const testButton = event.target;
            const originalText = testButton.textContent;
            testButton.textContent = '🔄 Testing...';
            testButton.disabled = true;

            const tests = [
                { name: 'Test Consenso Marketing', test: () => testCreateConsent(1, 'marketing', true) },
                { name: 'Test Export Dati', test: () => testDataExport(1) },
                { name: 'Test API Health', test: () => testApiHealth() }
            ];

            let results = [];

            for (const { name, test } of tests) {
                try {
                    await test();
                    results.push(`✅ ${name}: Passed`);
                } catch (error) {
                    results.push(`❌ ${name}: Failed - ${error.message}`);
                }
                await new Promise(resolve => setTimeout(resolve, 500));
            }

            alert(`🧪 Risultati Test GDPR:\n\n${results.join('\n')}`);
            
            testButton.textContent = originalText;
            testButton.disabled = false;
            
            setTimeout(refreshDashboard, 1000);
        }

        async function testCreateConsent(userId, type, accepted) {
            const response = await fetch(`${API_BASE}/gdpr/consent`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, consent_type: type, accepted })
            });

            if (!response.ok) {
                throw new Error(`Consent API failed: ${response.status}`);
            }

            const result = await response.json();
            if (result.status !== 'success') {
                throw new Error('Consent creation failed');
            }
        }

        async function testDataExport(userId) {
            const response = await fetch(`${API_BASE}/gdpr/export?user_id=${userId}&format=json`);
            
            if (!response.ok) {
                throw new Error(`Export API failed: ${response.status}`);
            }

            const result = await response.json();
            if (!result.user_profile) {
                throw new Error('Export data incomplete');
            }
        }

        async function testApiHealth() {
            const response = await fetch('/health');
            
            if (!response.ok) {
                throw new Error(`Health check failed: ${response.status}`);
            }

            const result = await response.json();
            if (result.status !== 'healthy') {
                throw new Error('API not healthy');
            }
        }

        // Cleanup on page unload
        window.addEventListener('beforeunload', function() {
            if (refreshInterval) {
                clearInterval(refreshInterval);
            }
        });
    </script>
</body>
</html>
EOF

# 3. Aggiorna Caddyfile per servire la dashboard
cat > Caddyfile << 'EOF'
# Caddyfile per GDPR Demo
{
    email admin@example.com
    acme_ca https://acme-v02.api.letsencrypt.org/directory
}

:80, :443 {
    encode gzip
    log {
        output file /var/log/caddy/access.log
    }
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "no-referrer"
        Permissions-Policy "geolocation=(), microphone=()"
    }
    
    # Serve GDPR dashboard
    handle /gdpr-dashboard {
        root * /srv/public
        rewrite * /gdpr-dashboard.html
        file_server
    }
    
    # API proxy
    reverse_proxy /api/* api:8000
    reverse_proxy /docs api:8000
    reverse_proxy /redoc api:8000
    reverse_proxy /health api:8000
    
    # Default homepage
    handle {
        respond "🛡️ GDPR Blog Demo - Vai alla dashboard: /gdpr-dashboard"
    }
    
    handle_errors {
        respond "{http.error.status_code} {http.error.status_text}" 500
    }
}
EOF

# 4. Aggiorna docker-compose per montare la dashboard
if ! grep -q "/srv/public" docker-compose.yml; then
    # Aggiungi mount per la dashboard
    sed -i '/caddy_config:\/config/a\      - ./public:/srv/public:ro' docker-compose.yml
fi

# 5. Restart Caddy per applicare le modifiche
echo "🔄 Restarting Caddy to serve dashboard..."
docker compose restart caddy

# 6. Wait for services
sleep 5

echo ""
echo "🎉 GDPR Dashboard deployed successfully!"
echo ""
echo "🌐 Access URLs:"
echo "• 🛡️ GDPR Dashboard: http://18.171.217.18/gdpr-dashboard"
echo "• 📖 API Docs: http://18.171.217.18:8000/docs"
echo "• 🔍 Health Check: http://18.171.217.18:8000/health"
echo "• 📧 MailHog: http://18.171.217.18:8025"
echo ""
echo "✨ Dashboard features:"
echo "• Real-time metrics every 15 seconds"
echo "• Interactive GDPR testing"
echo "• Compliance scoring"
echo "• Audit trail monitoring"
echo ""
echo "🧪 Test the dashboard by clicking 'Test GDPR' button!"
EOF
