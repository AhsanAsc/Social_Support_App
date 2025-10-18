create table if not exists applications (
  id uuid primary key default gen_random_uuid(),
  applicant_full_name text not null,
  applicant_national_id text,
  household_size int,
  monthly_income numeric(12,2),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists documents (
  id uuid primary key default gen_random_uuid(),
  application_id uuid not null references applications(id) on delete cascade,
  doc_type text not null,           -- e.g., "eid_front", "bank_statement", "credit_report"
  filename text not null,
  storage_path text not null,       -- absolute path inside container/host
  content_type text,
  size_bytes bigint,
  created_at timestamptz not null default now()
);

create table if not exists audit_log (
  id bigserial primary key,
  application_id uuid,
  actor text not null,              -- system|user|agent_name
  action text not null,             -- created_application|uploaded_document|validated|scored
  payload jsonb,
  created_at timestamptz not null default now()
);

-- basic indexes
create index if not exists idx_documents_app on documents(application_id);
create index if not exists idx_audit_app on audit_log(application_id);
