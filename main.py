import os
from fastapi import FastAPI
import psycopg2
import time

app = FastAPI()
def connect_db():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "myapi"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "9866115169@Ag")
            )
            print("Connected to database")
            return conn
        except Exception as e:
            print(f"Database not ready, retrying... {retries} attempts left")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to database")

conn = connect_db()


@app.get("/")
def root():
    return{"message": "Hello World"}

@app.get("/users")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append({"id": row[0], "name": row[1], "age": row[2]})
    return {"users": users}

@app.post("/users")
def create_user(name: str, age: int):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    return {"message": "User created"}
@app.put("/users/{id}")
def update_user(id:int, name: str, age: int):
    cursor = conn.cursor()
    cursor.execute("Update users SET name=%s, age=%s WHERE id=%s",(name,age,id))
    conn.commit()
    return{"message": "User updated"}

@app.delete("/users/{id}")
def dlete_user(id:int):
    cursor=conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s",(id,))
    conn.commit()
    return{"message": "User deleted"}