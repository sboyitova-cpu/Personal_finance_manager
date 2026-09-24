"""Finans özeti ve karşılaştırma grafiği."""

import pandas as pd
import streamlit as st


def render_dashboard(filtered_df):
    """Özet kartlarını ve gelir-gider karşılaştırma grafiğini gösterir."""
    total_income = filtered_df[filtered_df["Tür"] == "Gelir"]["Miktar"].sum()
    total_expense = filtered_df[filtered_df["Tür"] == "Gider"]["Miktar"].sum()
    balance = total_income - total_expense

    st.subheader("Finans özeti")
    metric_cols = st.columns(4)
    metric_cols[0].metric("💰 Toplam gelir", f"{total_income:.2f} TL")
    metric_cols[1].metric("💸 Toplam gider", f"{total_expense:.2f} TL")
    metric_cols[2].metric("💵 Bakiye", f"{balance:.2f} TL")
    metric_cols[3].metric("🧾 İşlem sayısı", len(filtered_df))

    st.subheader("Gelir ve gider karşılaştırması")
    income_expense = pd.DataFrame(
        {"Tür": ["Gelir", "Gider"], "Miktar": [total_income, total_expense]}
    )
    st.bar_chart(income_expense.set_index("Tür"))

