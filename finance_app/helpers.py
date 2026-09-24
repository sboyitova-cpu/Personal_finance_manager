"""Arayüzden bağımsız veri dönüştürme, filtreleme ve doğrulama yardımcıları."""

import pandas as pd

CATEGORIES = ["Maaş", "Yemek", "Ulaşım", "Alışveriş", "Fatura", "Diğer"]
TRANSACTION_TYPES = ["Gelir", "Gider"]
DATAFRAME_COLUMNS = ["ID", "Tür", "Kategori", "Miktar", "Açıklama", "Tarih"]


def transactions_to_dataframe(transactions):
    """İşlem satırlarını Türkçe sütun adlarına sahip bir DataFrame'e dönüştürür."""
    return pd.DataFrame(transactions, columns=DATAFRAME_COLUMNS)


def validate_transaction(amount, description):
    """Tutar ve açıklama geçerliyse None, değilse hata mesajı döndürür."""
    if amount <= 0:
        return "Miktar 0 TL'den büyük olmalıdır."
    if not description.strip():
        return "Lütfen işlem için bir açıklama girin."
    return None


def filter_transactions(df, selected_type, selected_category, start_date, end_date):
    """İşlemleri tür, kategori ve tarih seçimine göre süzer."""
    filtered_df = df.copy()
    if selected_type != "Tümü":
        filtered_df = filtered_df[filtered_df["Tür"] == selected_type]
    if selected_category != "Tümü":
        filtered_df = filtered_df[filtered_df["Kategori"] == selected_category]

    if start_date > end_date:
        return filtered_df.iloc[0:0]

    filtered_dates = pd.to_datetime(filtered_df["Tarih"], errors="coerce").dt.date
    return filtered_df[
        filtered_dates.notna()
        & (filtered_dates >= start_date)
        & (filtered_dates <= end_date)
    ]

