-- STAKC GDPR Template Database Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create basic tables for GDPR compliance
CREATE TABLE IF NOT EXISTS gdpr_consent_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    consent_type VARCHAR(100),
    consent_given BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

CREATE TABLE IF NOT EXISTS gdpr_data_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    request_type VARCHAR(50), -- 'export', 'delete', 'update'
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    notes TEXT
);

SELECT 'STAKC GDPR Database Ready' as status;
