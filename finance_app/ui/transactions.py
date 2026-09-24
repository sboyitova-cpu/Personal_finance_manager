"""Yeni işlem formu, işlem listesi ve kayıt yönetimi arayüzü."""

from datetime import date as date_type
from io import BytesIO

import pandas as pd
import streamlit as st

from finance_app.database import add_transaction, delete_transaction, update_transaction
from finance_app.helpers import CATEGORIES, TRANSACTION_TYPES, validate_transaction


def render_new_transaction_form(conn):
    """Yeni işlem formunu gösterir, doğrular ve geçerli kaydı ekler."""
    with st.expander("➕ Yeni işlem ekle", expanded=False):
        with st.form("new_transaction_form"):
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                transaction_type = st.selectbox("İşlem türü", TRANSACTION_TYPES)
                category = st.selectbox("Kategori", CATEGORIES)
                amount = st.number_input("Miktar (TL)", min_value=0.0, step=0.01)
            with form_col2:
                description = st.text_input("Açıklama")
                transaction_date = st.date_input("Tarih", value=date_type.today())
            submitted = st.form_submit_button("Kaydet", type="primary")

        if submitted:
            error_message = validate_transaction(amount, description)
            if error_message:
                st.error(error_message)
            else:
                add_transaction(
                    conn, transaction_type, category, amount,
                    description.strip(), transaction_date
                )
                st.success("İşlem başarıyla kaydedildi!")


def render_transaction_editor(conn, transactions):
    """Silme ve düzenleme alanlarını gösterir ve değişiklikleri kaydeder."""
    st.divider()
    st.subheader("🗑️ İşlem sil")
    delete_id = st.number_input("Silinecek işlemin ID'si", min_value=1, step=1)
    if st.button("İşlemi sil"):
        if delete_transaction(conn, delete_id):
            st.success("İşlem silindi!")
            st.rerun()
        else:
            st.error("Bu ID'ye ait işlem bulunamadı. Lütfen geçerli bir ID girin.")

    st.divider()
    st.subheader("✏️ İşlem düzenle")
    if not transactions:
        st.info("Düzenlenecek işlem yok. Önce bir işlem ekleyin.")
        return

    transaction_options = {row[0]: row for row in transactions}
    edit_id = st.selectbox(
        "Düzenlenecek işlem",
        options=list(transaction_options),
        format_func=lambda transaction_id: (
            f"ID {transaction_id} · {transaction_options[transaction_id][1]} · "
            f"{transaction_options[transaction_id][2]} · "
            f"{transaction_options[transaction_id][3]:.2f} TL · "
            f"{transaction_options[transaction_id][5]}"
        ),
    )
    selected_transaction = transaction_options[edit_id]

    with st.form(f"edit_transaction_{edit_id}"):
        edit_type = st.selectbox(
            "İşlem türü", TRANSACTION_TYPES,
            index=TRANSACTION_TYPES.index(selected_transaction[1]),
            key=f"edit_type_{edit_id}",
        )
        edit_category = st.selectbox(
            "Kategori", CATEGORIES,
            index=(CATEGORIES.index(selected_transaction[2])
                   if selected_transaction[2] in CATEGORIES else CATEGORIES.index("Diğer")),
            key=f"edit_category_{edit_id}",
        )
        edit_amount = st.number_input(
            "Miktar (TL)", min_value=0.0, step=0.01,
            value=float(selected_transaction[3] or 0), key=f"edit_amount_{edit_id}",
        )
        edit_description = st.text_input(
            "Açıklama", value=selected_transaction[4] or "",
            key=f"edit_description_{edit_id}",
        )
        try:
            current_date = date_type.fromisoformat(selected_transaction[5])
        except (TypeError, ValueError):
            current_date = date_type.today()
        edit_date = st.date_input(
            "Tarih", value=current_date, key=f"edit_date_{edit_id}",
        )
        submitted = st.form_submit_button("Güncelle", type="primary")

    if submitted:
        error_message = validate_transaction(edit_amount, edit_description)
        if error_message:
            st.error(error_message)
        elif update_transaction(
            conn, edit_id, edit_type, edit_category, edit_amount,
            edit_description.strip(), edit_date
        ):
            st.success("İşlem başarıyla güncellendi!")
            st.rerun()
        else:
            st.error("Bu ID'ye ait işlem bulunamadı. Lütfen listeden tekrar seçin.")


def render_transactions_tab(conn, transactions, filtered_df):
    """İşlem tablosunu, dışa aktarma düğmelerini ve kayıt yönetimini gösterir."""
    st.subheader("İşlem kayıtları")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSV indir", data=csv_data,
        file_name="finans_islemleri.csv", mime="text/csv",
    )

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="İşlemler")
    st.download_button(
        "📥 Excel indir", data=excel_buffer.getvalue(),
        file_name="finans_islemleri.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    render_transaction_editor(conn, transactions)

