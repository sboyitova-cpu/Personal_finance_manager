"""Kenar çubuğu filtrelerinin Streamlit arayüzü."""

from datetime import date as date_type

import pandas as pd
import streamlit as st

from finance_app.helpers import TRANSACTION_TYPES, filter_transactions


def render_sidebar_filters(df):
    """Filtreleri gösterir ve tarih, tür ve kategoriye göre süzülmüş veriyi döndürür."""
    st.sidebar.header("🔎 Filtreler")
    selected_type = st.sidebar.selectbox("İşlem türü", ["Tümü"] + TRANSACTION_TYPES)
    category_options = ["Tümü"] + sorted(df["Kategori"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Kategori", category_options)

    parsed_dates = pd.to_datetime(df["Tarih"], errors="coerce").dropna()
    if parsed_dates.empty:
        default_start = date_type.today()
        default_end = date_type.today()
    else:
        default_start = parsed_dates.min().date()
        default_end = parsed_dates.max().date()

    start_date = st.sidebar.date_input("Başlangıç tarihi", value=default_start)
    end_date = st.sidebar.date_input("Bitiş tarihi", value=default_end)
    if start_date > end_date:
        st.sidebar.warning("Başlangıç tarihi bitiş tarihinden sonra olamaz.")

    return filter_transactions(df, selected_type, selected_category, start_date, end_date)

