"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: gene_pool.py  |  Module: Persistent Candidate Store (SQLite)
"""
import os, sqlite3, time

DB_PATH = os.environ.get("VYKTOR_GENEPOOL", "results/gene_pool.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task TEXT NOT NULL,
  code TEXT NOT NULL,
  score REAL NOT NULL,
  ok INTEGER NOT NULL,
  runtime REAL NOT NULL,
  origin TEXT NOT NULL,
  ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_task_score ON candidates(task, score DESC);
"""

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init():
    with _conn() as c:
        c.executescript(SCHEMA)

def add(task, candidate):
    with _conn() as c:
        c.execute(
            "INSERT INTO candidates (task, code, score, ok, runtime, origin, ts) VALUES (?,?,?,?,?,?,?)",
            (task, candidate.code, candidate.score, int(candidate.ok), candidate.runtime, candidate.origin, time.time())
        )
        c.commit()

def top(task, k=5):
    with _conn() as c:
        cur = c.execute(
            "SELECT code, score, ok, runtime, origin, ts FROM candidates WHERE task=? ORDER BY score DESC LIMIT ?",
            (task, k)
        )
        return cur.fetchall()
