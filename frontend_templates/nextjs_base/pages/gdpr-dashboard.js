import React, { useEffect } from "react";

export default function GdprDashboard() {
  useEffect(() => {
    async function fetchMetrics() {
      try {
        const dashboardRes = await fetch('/api/gdpr/ops/dashboard/metrics');
        const dashboard = dashboardRes.ok ? await dashboardRes.json() : {};
        const statsRes = await fetch('/api/gdpr/metrics');
        const stats = statsRes.ok ? await statsRes.json() : {};
        document.getElementById('metrics').innerHTML = `
          <div class="metric"><h2>Compliance Score</h2><div class="metric-value">${dashboard.compliance_score ?? '-'}</div></div>
          <div class="metric"><h2>Active Consents</h2><div class="metric-value">${stats.consents_active ?? dashboard.active_consents ?? '-'}</div></div>
          <div class="metric"><h2>Expired Consents</h2><div class="metric-value">${stats.consents_expired ?? '-'}</div></div>
          <div class="metric"><h2>Export Requests</h2><div class="metric-value">${stats.exports_requested ?? '-'}</div></div>
          <div class="metric"><h2>Completed Exports</h2><div class="metric-value">${stats.exports_completed ?? '-'}</div></div>
          <div class="metric"><h2>Deletion Requests</h2><div class="metric-value">${stats.deletions_requested ?? dashboard.pending_requests ?? '-'}</div></div>
          <div class="metric"><h2>Completed Deletions</h2><div class="metric-value">${stats.deletions_completed ?? '-'}</div></div>
          <div class="metric"><h2>Breach Notified</h2><div class="metric-value">${stats.breach_notified ?? '-'}</div></div>
          <div class="metric"><h2>Audit Logs</h2><div class="metric-value">${stats.audit_logs_count ?? (dashboard.recent_audits ? dashboard.recent_audits.length : '-')}</div></div>
          <div class="metric"><h2>DPO Requests</h2><div class="metric-value">${stats.dpo_requests ?? '-'}</div></div>
          <div class="metric"><h2>DPO Resolved</h2><div class="metric-value">${stats.dpo_resolved ?? '-'}</div></div>
          <div class="metric"><h2>Data Retention</h2><div class="metric-value">${dashboard.data_retention_status ?? '-'}</div></div>
        `;
        const audits = dashboard.recent_audits || [];
        document.getElementById('recent-audits').innerHTML = audits.length ? audits.map(a => `<li>${a}</li>`).join('') : '<li>No recent audits</li>';
        const alerts = dashboard.security_alerts || [];
        document.getElementById('security-alerts').innerHTML = alerts.length ? alerts.map(a => `<li>${a}</li>`).join('') : '<li>No security alerts</li>';
      } catch (e) {
        document.getElementById('error').textContent = 'Failed to load metrics. Please check backend/API.';
      }
    }
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container" style={{ maxWidth: 900, margin: '2em auto', background: '#fff', borderRadius: 10, boxShadow: '0 2px 8px #0001', padding: '2em', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', color: '#2d3a4a' }}>GDPR Compliance Dashboard</h1>
      <div id="error" className="error" style={{ color: '#b00', textAlign: 'center' }}></div>
      <div className="metrics" id="metrics" style={{ display: 'flex', flexWrap: 'wrap', gap: '2em', justifyContent: 'space-between' }}>
        {/* Metrics will be loaded here */}
      </div>
      <div className="section" style={{ marginTop: '2em' }}>
        <h2>Recent Audits</h2>
        <ul id="recent-audits"></ul>
      </div>
      <div className="section" style={{ marginTop: '2em' }}>
        <h2>Security Alerts</h2>
        <ul id="security-alerts"></ul>
      </div>
      <style jsx>{`
        .metric { flex: 1 1 250px; background: #f0f4f8; border-radius: 8px; padding: 1.5em; margin-bottom: 1em; box-shadow: 0 1px 4px #0001; }
        .metric h2 { margin-top: 0; font-size: 1.2em; color: #3b4a5a; }
        .metric-value { font-size: 2.2em; color: #1a7f37; font-weight: bold; }
        ul { padding-left: 1.2em; }
        @media (max-width: 700px) { .metrics { flex-direction: column; } }
      `}</style>
    </div>
  );
}
