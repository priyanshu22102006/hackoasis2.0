from fastapi import FastAPI, UploadFile, File
import sqlite3, datetime, hashlib

app = FastAPI()
DB = "docs.db"

# init DB
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                doc_hash TEXT,
                status TEXT,
                reasons TEXT,
                processed_at TEXT
            )""")
conn.commit()
conn.close()

def log_result(filename, doc_hash, status, reasons):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO documents (filename, doc_hash, status, reasons, processed_at) VALUES (?,?,?,?,?)",
              (filename, doc_hash, status, reasons, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    doc_hash = hashlib.sha256(contents).hexdigest()
    
    # --- Dummy verification for now ---
    status = "Verified" if "cert" in file.filename.lower() else "Rejected"
    reasons = "" if status == "Verified" else "File name did not contain 'cert'"
    
    log_result(file.filename, doc_hash, status, reasons)
    return {"filename": file.filename, "status": status, "hash": doc_hash, "reasons": reasons}

@app.get("/status/")
async def get_status():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM documents ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return {"documents": rows}
