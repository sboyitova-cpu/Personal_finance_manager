"""Streamlit uygulamasının başlangıç noktası."""

import streamlit as st

from finance_app.database import get_transactions, initialize_database
from finance_app.helpers import transactions_to_dataframe
from finance_app.ui.analytics import render_analytics_tab
from finance_app.ui.dashboard import render_dashboard
from finance_app.ui.sidebar import render_sidebar_filters
from finance_app.ui.transactions import render_new_transaction_form, render_transactions_tab


def main():
    """Sayfa ayarlarını yapar, verileri yükler ve uygulama sekmelerini gösterir."""
    st.set_page_config(page_title="Kişisel Finans", page_icon="💰", layout="wide")

    st.title("💰 Kişisel Finans Yönetimi")
    st.caption("Gelir ve giderlerinizi tek bir yerden takip edin.")

    conn = initialize_database()
    render_new_transaction_form(conn)

    transactions = get_transactions(conn)
    df = transactions_to_dataframe(transactions)
    filtered_df = render_sidebar_filters(df)

    dashboard_tab, transactions_tab, analytics_tab = st.tabs(
        ["📊 Dashboard", "🧾 İşlemler", "📈 Analiz"]
    )
    with dashboard_tab:
        render_dashboard(filtered_df)
    with transactions_tab:
        render_transactions_tab(conn, transactions, filtered_df)
    with analytics_tab:
        render_analytics_tab(filtered_df)


if __name__ == "__main__":
    main()
