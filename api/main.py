from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )

class Book(BaseModel):
    title: str
    author: str
    year: int

@app.get("/books")
def list_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, author, year FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

@app.post("/books")
def add_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
        (book.title, book.author, book.year)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "created"}
