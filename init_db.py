from db import connect

def init():
    conn = connect()
    cur = conn.cursor()
    with open("schema.sql", "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init()
