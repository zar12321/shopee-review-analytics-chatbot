import psycopg2
import os
from dotenv import load_dotenv

DB_HOST=os.getenv("POSTGRES_HOST")
DB_PORT=os.getenv("POSTGRES_PORT")
DB_USER=os.getenv("POSTGRES_USER")
DB_PASSWORD=os.getenv("POSTGRES_PASSWORD")
DB_NAME=os.getenv("POSTGRES_DB")

print("HOST:", repr(DB_HOST))
print("PORT:", repr(DB_PORT))
print("USER:", repr(DB_USER))
print("PASSWORD:", repr(DB_PASSWORD))
print("DB:", repr(DB_NAME))

def get_connection():
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD,
        dbname = DB_NAME
    )

    return conn

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    create table if not exists shopee_reviews (
                review_id serial primary key,
                review_unique_id text unique not null,
                username text not null,
                review_text text not null,
                rating integer not null check (rating >=1 and rating <= 5),
                review_date timestamp,
                reply_text text,
                reply_date timestamp
                );
    """)

    conn.commit()
    cursor.close()
    conn.close()

def insert_reviews(df_clean):
    conn = get_connection()
    cursor = conn.cursor()

    data = [
    (
        row.reviewId,
        row.userName,
        row.content,
        row.score,
        row.at,
        row.replyContent,
        row.repliedAt
    )
    # itertuples berfungsi untuk menghasilkan tuple, sedangkan false agar index tidak dimasukkan ke tuple
    for row in df_clean.itertuples(index=False)
]

    cursor.executemany("""
        insert into shopee_reviews (
                    review_unique_id,
                    username,
                    review_text,
                    rating,
                    review_date,
                    reply_text,
                    reply_date
                    )
        values (%s, %s, %s, %s, %s, %s, %s)
        on conflict (review_unique_id) do nothing
    """, data)

    # Note:
    # on conflict (review_unique_id) do nothing digunakan kalau data yang ingin dimasukkan
    # melanggar constraint tertentu, maka tidak akan error, melainkan akan diabaikan baris tersebut
    conn.commit()
    cursor.close()
    conn.close()
