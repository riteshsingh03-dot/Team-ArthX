# db/schema.py
from sqlalchemy import text
from db.connection import engine

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    village_name TEXT NOT NULL,
    block TEXT,
    district TEXT NOT NULL,
    state TEXT NOT NULL,
    latitude NUMERIC,
    longitude NUMERIC,
    population INTEGER,
    osm_node_id TEXT,
    created_at TIMESTAMP DEFAULT now()
);


CREATE TABLE IF NOT EXISTS schemes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    state TEXT,
    project_cost_min NUMERIC NOT NULL,
    project_cost_max NUMERIC NOT NULL,
    loan_share NUMERIC NOT NULL,
    max_loan NUMERIC NOT NULL,
    interest_rate NUMERIC NOT NULL,
    tenure_months INTEGER NOT NULL,
    moratorium_months INTEGER NOT NULL DEFAULT 0,
    repayment_frequency TEXT NOT NULL DEFAULT 'monthly',
    source_url TEXT,
    is_illustrative BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS scheme_documents (
    id SERIAL PRIMARY KEY,
    scheme_id INTEGER REFERENCES schemes(id),
    chunk_text TEXT NOT NULL,
    embedding JSONB NOT NULL,
    source TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS market_seed_data (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    business_category TEXT NOT NULL,
    competitor_count INTEGER,
    avg_price NUMERIC,
    notes TEXT,
    source TEXT,
    is_illustrative BOOLEAN NOT NULL DEFAULT TRUE,
    last_updated DATE
);

CREATE TABLE IF NOT EXISTS market_competitors (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    business_category TEXT NOT NULL,
    osm_place_id TEXT,
    name TEXT NOT NULL,
    latitude NUMERIC,
    longitude NUMERIC,
    distance_km NUMERIC,
    business_status TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    source TEXT DEFAULT 'openstreetmap_overpass',
    last_updated TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mandi_prices_raw (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    business_category TEXT NOT NULL,
    commodity TEXT NOT NULL,
    market_name TEXT,
    state TEXT,
    district TEXT,
    min_price NUMERIC,
    max_price NUMERIC,
    modal_price NUMERIC,
    arrival_date TEXT,
    source TEXT DEFAULT 'data_gov_in_agmarknet',
    fetched_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS mandi_prices_avg (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(id),
    business_category TEXT NOT NULL,
    commodity TEXT NOT NULL,
    avg_modal_price NUMERIC,
    sample_size INTEGER,
    is_illustrative BOOLEAN NOT NULL DEFAULT FALSE,
    last_updated DATE,
    UNIQUE (location_id, business_category, commodity)
);

CREATE TABLE IF NOT EXISTS census_district_population (
    id SERIAL PRIMARY KEY,
    state_name TEXT NOT NULL,
    district_name TEXT NOT NULL,
    population BIGINT,
    households BIGINT,
    source TEXT DEFAULT 'census_2011',
    UNIQUE (state_name, district_name)
);

CREATE TABLE IF NOT EXISTS eligibility_rules (
    id SERIAL PRIMARY KEY,
    scheme_id INTEGER NOT NULL REFERENCES schemes(id),
    field TEXT NOT NULL,
    operator TEXT NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS journal_entries (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,
    sales_revenue NUMERIC,
    expenses NUMERIC,
    units_sold NUMERIC,
    notes TEXT,
    created_at TIMESTAMP DEFAULT now()
);

ALTER TABLE census_district_population ADD COLUMN IF NOT EXISTS area_km2 NUMERIC;
"""

with engine.connect() as conn:
    conn.execute(text(CREATE_TABLES_SQL))
    conn.commit()

print("Tables created successfully.")