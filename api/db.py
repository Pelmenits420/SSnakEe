import sqlite3

DATABASE_NAME = "game.db"

def init_db():
    """Izveido tabulu, ja tā vēl neeksistē."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_score(player: str, score: int):
    """Ievieto jaunu rekordu datubāzē."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # SVARĪGI: Lietojam ? lai pasargātu no SQL injekcijām!
    cursor.execute("INSERT INTO scores (player, score) VALUES (?, ?)", (player, score))
    conn.commit()
    conn.close()

def get_top_scores():
    """Nolasa 10 labākos rezultātus."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT player, score FROM scores ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    # Pārvēršam par sarakstu ar vārdnīcām, lai FastAPI to var atgriezt
    return [{"player": row[0], "score": row[1]} for row in rows]

def get_player_stats(name: str):
    """Atgriež spēlētāja statistiku (spēļu skaits, labākais rezultāts)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), MAX(score) FROM scores WHERE player = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return {"games_played": row[0], "best_score": row[1] if row[1] is not None else 0}