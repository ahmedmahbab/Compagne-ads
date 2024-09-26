import streamlit as st
import json
from datetime import datetime, timedelta

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

def save_accounts(accounts):
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

def save_campaigns(campaigns):
    with open('campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=4)

def add_campaign_page():
    st.title("إضافة حملة جديدة")

    accounts = load_accounts()
    campaigns = load_campaigns()

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account:
        customer_name = st.text_input("اسم الزبون")
        campaign_amount = st.number_input("المبلغ للحملة", min_value=0.0, format="%.2f")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة", value=datetime.today())
        end_date = start_date + timedelta(days=campaign_days)
        st.write(f"تاريخ نهاية الحملة: {end_date}")

        if st.button("تسجيل الحملة"):
            campaign_id = accounts[selected_account]["next_campaign_id"]
            campaigns[selected_account] = campaigns.get(selected_account, [])
            campaigns[selected_account].append({
                "id": campaign_id,
                "customer_name": customer_name,
                "amount": round(campaign_amount, 2),
                "days": campaign_days,
                "start_date": str(start_date),
                "end_date": str(end_date)
            })
            accounts[selected_account]["next_campaign_id"] += 1
            save_accounts(accounts)
            save_campaigns(campaigns)

            st.success("تم تسجيل الحملة بنجاح!")
