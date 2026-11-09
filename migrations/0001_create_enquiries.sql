-- Enquiries submitted through the website form.
-- created_at is ISO 8601 in India Standard Time, e.g. 2026-11-09T22:30:05+05:30
CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  course TEXT NOT NULL,
  level TEXT,
  preferred_time TEXT NOT NULL,
  message TEXT,
  source_page TEXT,
  user_agent TEXT,
  ip_hash TEXT,
  synced_to_sheet INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_enquiries_ip_time ON enquiries (ip_hash, created_at);
CREATE INDEX IF NOT EXISTS idx_enquiries_unsynced ON enquiries (synced_to_sheet, id);
