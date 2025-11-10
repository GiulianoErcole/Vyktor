import os, sqlite3, time
DB_PATH = os.environ.get("VYKTOR_GENEPOOL", "results/gene_pool.sqlite")
SCHEMA = """
CREATE TABLE IF NOT EXISTS candidates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task TEXT, code TEXT, score REAL, ok INTEGER, runtime REAL, origin TEXT, ts REAL
);
CREATE INDEX IF NOT EXISTS idx_task_score ON candidates(task, score DESC);
"""
def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True); return sqlite3.connect(DB_PATH)
def init():
    with _conn() as c: c.executescript(SCHEMA)
def add(task, cand):
    with _conn() as c:
        c.execute("INSERT INTO candidates (task, code, score, ok, runtime, origin, ts) VALUES (?,?,?,?,?,?,?)",
                  (task, cand.code, cand.score, int(cand.ok), cand.runtime, cand.origin, time.time())); c.commit()
def top(task, k=5):
    with _conn() as c:
        cur = c.execute("SELECT code, score, ok, runtime, origin, ts FROM candidates WHERE task=? ORDER BY score DESC LIMIT ?",
                        (task, k)); return cur.fetchall()
