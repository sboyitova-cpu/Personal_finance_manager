"""SQLite bağlantısı ve kişisel finans kayıt işlemleri."""

import sqlite3
import random
from datetime import date, timedelta
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "finance.db"


def _add_demo_transactions_if_empty(conn):
    """Boş veritabanına arayüzü göstermek için 100 sentetik işlem ekler."""
    if conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] > 0:
        return

    rng = random.Random(20261001)
    expenses = [
        ("Yemek", "Market alışverişi"),
        ("Yemek", "Öğle yemeği"),
        ("Ulaşım", "Toplu taşıma"),
        ("Fatura", "Elektrik faturası"),
        ("Alışveriş", "Ev ihtiyaçları"),
        ("Diğer", "Eczane harcaması"),
    ]
    incomes = [("Maaş", "Aylık maaş"), ("Diğer", "Ek gelir"), ("Diğer", "Proje ödemesi")]
    today = date.today()
    transactions = []

    for index in range(100):
        is_expense = index < 70
        category, description = rng.choice(expenses if is_expense else incomes)
        amount = round(
            rng.uniform(80, 6500) if is_expense else rng.uniform(1500, 52000), 2
        )
        transaction_date = today - timedelta(days=rng.randrange(365))
        transactions.append(
            (
                "Gider" if is_expense else "Gelir",
                category,
                amount,
                description,
                transaction_date.isoformat(),
            )
        )

    conn.executemany(
        """INSERT INTO transactions(type, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?)""",
        transactions,
    )
    conn.commit()


def initialize_database():
    """Veritabanı bağlantısı kurar ve gerekli tabloyu oluşturur."""
    # Resolve the database relative to the project, not Streamlit's launch directory.
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            category TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )"""
    )
    conn.commit()
    _add_demo_transactions_if_empty(conn)
    return conn


def get_transactions(conn):
    """Veritabanındaki tüm işlemleri satır listesi olarak döndürür."""
    cursor = conn.execute(
        "SELECT id, type, category, amount, description, date FROM transactions"
    )
    return cursor.fetchall()


def add_transaction(conn, transaction_type, category, amount, description, transaction_date):
    """Yeni bir işlemi veritabanına kaydeder."""
    conn.execute(
        """INSERT INTO transactions(type, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?)""",
        (transaction_type, category, amount, description, str(transaction_date)),
    )
    conn.commit()


def delete_transaction(conn, transaction_id):
    """ID ile işlemi siler; silme başarılı olduysa True döndürür."""
    cursor = conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    return cursor.rowcount > 0


def update_transaction(
    conn, transaction_id, transaction_type, category, amount, description, transaction_date
):
    """Bir işlemin alanlarını günceller; güncelleme başarılıysa True döndürür."""
    cursor = conn.execute(
        """UPDATE transactions
        SET type = ?, category = ?, amount = ?, description = ?, date = ?
        WHERE id = ?""",
        (
            transaction_type,
            category,
            amount,
            description,
            str(transaction_date),
            transaction_id,
        ),
    )
    conn.commit()
    return cursor.rowcount > 0

