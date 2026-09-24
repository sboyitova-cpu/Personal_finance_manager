"""Kategori gider grafiği ve aylık analiz arayüzü."""

import pandas as pd
import streamlit as st

from finance_app.helpers import TRANSACTION_TYPES


def render_analytics_tab(filtered_df):
    """Kategori harcama grafiği ile aylık gelir, gider ve bakiye analizini gösterir."""
    st.subheader("Kategori bazında harcamalar")
    expense_df = filtered_df[filtered_df["Tür"] == "Gider"]
    category_expenses = expense_df.groupby("Kategori")["Miktar"].sum()
    st.bar_chart(category_expenses)

    st.divider()
    st.subheader("📅 Aylık finans analizi")
    monthly_df = filtered_df.copy()
    monthly_df["Ay"] = pd.to_datetime(monthly_df["Tarih"], errors="coerce").dt.to_period("M")
    monthly_df = monthly_df.dropna(subset=["Ay"])

    if monthly_df.empty:
        st.info("Seçili filtrelerde aylık analiz için işlem bulunamadı.")
        return

    monthly_summary = monthly_df.pivot_table(
        index="Ay", columns="Tür", values="Miktar", aggfunc="sum", fill_value=0,
    )
    for monthly_type in TRANSACTION_TYPES:
        if monthly_type not in monthly_summary.columns:
            monthly_summary[monthly_type] = 0

    monthly_summary["Bakiye"] = monthly_summary["Gelir"] - monthly_summary["Gider"]
    monthly_summary.index = monthly_summary.index.astype(str)
    monthly_summary.index.name = "Ay"
    monthly_summary = monthly_summary[["Gelir", "Gider", "Bakiye"]]
    st.dataframe(monthly_summary, use_container_width=True)
    st.line_chart(monthly_summary)

