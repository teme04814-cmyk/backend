-- Create partnerships tables for PostgreSQL

-- Create Company table
CREATE TABLE IF NOT EXISTS partnerships_company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(64),
    license_number VARCHAR(64),
    license_expiry_date DATE,
    country VARCHAR(64),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    owner_id BIGINT REFERENCES users_customuser(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS partnerships_company_owner_id_idx ON partnerships_company(owner_id);

-- Create Partnership table
CREATE TABLE IF NOT EXISTS partnerships_partnership (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id BIGINT NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE,
    main_contractor_id INTEGER REFERENCES partnerships_company(id) ON DELETE CASCADE,
    partner_company_id INTEGER REFERENCES partnerships_company(id) ON DELETE CASCADE,
    partnership_type VARCHAR(32) NOT NULL DEFAULT 'joint_venture',
    ownership_ratio_main NUMERIC(5,2) NOT NULL DEFAULT 60.00,
    ownership_ratio_partner NUMERIC(5,2) NOT NULL DEFAULT 40.00,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    start_date DATE,
    end_date DATE,
    qr_code VARCHAR(100),
    certificate_number VARCHAR(64) UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registration_data JSONB,
    partners_data JSONB
);

CREATE INDEX IF NOT EXISTS partnerships_partnership_owner_id_idx ON partnerships_partnership(owner_id);
CREATE INDEX IF NOT EXISTS partnerships_partnership_main_contractor_id_idx ON partnerships_partnership(main_contractor_id);
CREATE INDEX IF NOT EXISTS partnerships_partnership_partner_company_id_idx ON partnerships_partnership(partner_company_id);

-- Create PartnershipDocument table
CREATE TABLE IF NOT EXISTS partnerships_partnershipdocument (
    id SERIAL PRIMARY KEY,
    partnership_id UUID NOT NULL REFERENCES partnerships_partnership(id) ON DELETE CASCADE,
    document_type VARCHAR(64) NOT NULL,
    file VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS partnerships_partnershipdocument_partnership_id_idx ON partnerships_partnershipdocument(partnership_id);

-- Create PartnershipApprovalLog table
CREATE TABLE IF NOT EXISTS partnerships_partnershipapprovallog (
    id SERIAL PRIMARY KEY,
    partnership_id UUID NOT NULL REFERENCES partnerships_partnership(id) ON DELETE CASCADE,
    action VARCHAR(64) NOT NULL,
    actor_id BIGINT REFERENCES users_customuser(id) ON DELETE SET NULL,
    actor_role VARCHAR(32),
    actor_identifier VARCHAR(64),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS partnerships_partnershipapprovallog_partnership_id_idx ON partnerships_partnershipapprovallog(partnership_id);
CREATE INDEX IF NOT EXISTS partnerships_partnershipapprovallog_actor_id_idx ON partnerships_partnershipapprovallog(actor_id);
