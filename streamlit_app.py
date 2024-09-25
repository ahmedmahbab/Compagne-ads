import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

# تحميل الحسابات من ملف JSON
def load_accounts():
    try:
        with open('accounts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# حفظ الحسابات إلى ملف JSON
def save_accounts(accounts):
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)

# تحميل الحملات من ملف JSON
def load_campaigns():
    try:
        with open('campaigns.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# حفظ الحملات إلى ملف JSON
def save_campaigns(campaigns):
    with open('campaigns.json', 'w') as f:
        json.dump(campaigns, f)

# إعداد البيانات
accounts = load_accounts()
campaigns = load_campaigns()

# واجهة المستخدم
st.title("إدارة الحملات")

# زر إضافة حساب
if st.button("إضافة حساب"):
    account_name = st.text_input("اسم الحساب")
    if st.button("تأكيد إضافة الحساب"):
        if account_name and account_name not in accounts:
            accounts[account_name] = {"next_campaign_id": 1, "campaigns": []}
            save_accounts(accounts)
            st.success("تم إضافة الحساب بنجاح!")
        else:
            st.error("يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

# عرض الحسابات
st.sidebar.title("الحسابات")
selected_account = st.sidebar.selectbox("اختر حسابًا", list(accounts.keys()))

if selected_account:
    st.write(f"حساب: {selected_account}")
    if "next_campaign_id" not in accounts[selected_account]:
        accounts[selected_account]["next_campaign_id"] = 1

    # إضافة حملة
    st.write("إضافة حملة")
    campaign_amount = st.number_input("المبلغ للحملة")
    campaign_days = st.number_input("عدد الأيام")
    start_date = st.date_input("تاريخ بداية الحملة", value=datetime.today())
    end_date = start_date + timedelta(days=int(campaign_days))  # تاريخ نهاية الحملة
    st.write("تاريخ نهاية الحملة:", end_date)

    if st.button("تسجيل الحملة"):
        campaign_id = accounts[selected_account]["next_campaign_id"]
        campaigns[selected_account] = campaigns.get(selected_account, [])
        campaigns[selected_account].append({
            "id": campaign_id,
            "amount": campaign_amount,
            "days": campaign_days,
            "start_date": str(start_date),
            "end_date": str(end_date)
        })
        accounts[selected_account]["next_campaign_id"] += 1
        save_accounts(accounts)
        save_campaigns(campaigns)
        st.success("تم تسجيل الحملة بنجاح!")

# عرض الحملات المسجلة
st.write("الحملات المسجلة")
if selected_account in campaigns and campaigns[selected_account]:
    df = pd.DataFrame(campaigns[selected_account])
    st.dataframe(df)
else:
    st.write("لا توجد حملات مسجلة.")

