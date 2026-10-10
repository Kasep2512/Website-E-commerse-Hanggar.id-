-- db/001_initial_schema.sql

-- Tabel Tiers (Tingkat Akun)
CREATE TABLE IF NOT EXISTS tiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- 'Tier 0', 'Tier 1', 'Tier 2', 'Admin'
    description TEXT
);

-- Tabel Users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL, 
    discord_id TEXT UNIQUE, --Login Discord
    password_hash TEXT,
    tier_id INTEGER NOT NULL DEFAULT 1, -- Default Tier 0 (ID 1)
    full_name TEXT,
    phone_number TEXT UNIQUE,
    trust_score INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(tier_id) REFERENCES tiers(id)
);

-- Tabel Master Katalog 
CREATE TABLE IF NOT EXISTS catalog_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                 -- Contoh: 'RX-78-2 Gundam'
    series TEXT,                        -- Contoh: 'Mobile Suit Gundam'
    grade TEXT,                         -- 'HG', 'RG', 'MG', 'PG', 'SD', dll.
    scale TEXT,                         -- '1/144', '1/100', '1/60'
    manufacturer TEXT DEFAULT 'Bandai',
    product_code TEXT,
    release_year INTEGER,
    msrp_jpy INTEGER,
    features TEXT,                      -- Ciri-ciri keaslian
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);