-- db/002_kyc_schema.sql
CREATE TABLE IF NOT EXISTS kyc_verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ktp_filename TEXT NOT NULL,
    self_filename TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);