import streamlit as st
import json
import pandas as pd
from datetime import datetime

def load_accounts():
    try:
        with open('accounts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_campaigns():
    try:
        with open('campaigns.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_campaigns(campaigns):
    with open('campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=4)

def view_campaigns_page():
    st.title("عرض الحملات")

    accounts = load_accounts()
    campaigns = load_campaigns()

    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])
        df = df.drop(columns=["id"])
        df["تاريخ تسجيل الحملة"] = pd.to_datetime("today").strftime("%Y-%m-%d")
        df.columns = ["اسم الزبون", "المبلغ", "عدد الأيام", "تاريخ البداية", "تاريخ النهاية", "تاريخ تسجيل الحملة"]
        df["المبلغ"] = df["المبلغ"].map(lambda x: f"{x:,.2f} $")
        df["عدد الأيام"] = df["عدد الأيام"].map(lambda x: f"{x} يوم")

        st.write(df)

        # منطق التعديل والحذف كما في الكود السابق.
