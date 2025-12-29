from flask import Flask, jsonify, request
from dotenv import load_dotenv
from db import get_conn

load_dotenv(dotenv_path=".env")

def create_app()-> Flask:
    app = Flask(__name__)
    
    @app.get("/health")
    def health():
        return jsonify(status="ok")
    
    @app.get("/db-health")
    def db_health():
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return jsonify(status="error", reason="DATABASE_URL missing"), 500
        try:
            with psycopg.connect(db_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1;")
                    cursor.fetchone()
            return jsonify(status="ok")
        except Exception as e:
            return jsonify(status="error", reason=str(e)), 500
        
         # Create note
    @app.post("/api/notes")
    def create_note():
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return jsonify(error="title and content are required"), 400

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO notes (title, content)
                    VALUES (%s, %s)
                    RETURNING id, title, content, created_at;
                    """,
                    (title, content),
                )
                row = cur.fetchone()

        note = {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3].isoformat(),
        }
        return jsonify(note), 201

    # List notes (latest first)
    @app.get("/api/notes")
    def list_notes():
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, content, created_at
                    FROM notes
                    ORDER BY created_at DESC
                    LIMIT 50;
                    """
                )
                rows = cur.fetchall()

        notes = [
            {
                "id": r[0],
                "title": r[1],
                "content": r[2],
                "created_at": r[3].isoformat(),
            }
            for r in rows
        ]
        return jsonify(notes)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
        
    
