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
        json.dump(accounts, f, ensure_ascii=False, indent=4)

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
        json.dump(campaigns, f, ensure_ascii=False, indent=4)

# إعداد البيانات
accounts = load_accounts()

# واجهة المستخدم
st.title("إدارة الحسابات")

# إضافة حساب جديد
st.subheader("إضافة حساب جديد")
new_account_name = st.text_input("اسم الحساب الجديد")
new_limit = st.number_input("المبلغ المحدد", min_value=0.0, format="%.2f")
new_date = st.date_input("التاريخ المحدد")

if st.button("تأكيد إضافة الحساب"):
    if new_account_name and new_account_name not in accounts:
        accounts[new_account_name] = {"next_campaign_id": 1, "limit": round(new_limit, 2), "date": str(new_date), "campaigns": []}
        save_accounts(accounts)
        st.success(f"تم إضافة الحساب {new_account_name} بنجاح!")
    else:
        st.error("يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

# تعديل الحسابات القديمة
st.subheader("تعديل الحسابات القديمة")
selected_account = st.selectbox("اختر حسابًا لتعديله", list(accounts.keys()))

if selected_account:
    st.write(f"تعديل الحساب: {selected_account}")
    
    # تعديل المبلغ المحدد والتاريخ
    updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0.0, value=accounts[selected_account]["limit"], format="%.2f")
    updated_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(accounts[selected_account]["date"]))

    # زر لتأكيد التعديلات
    if st.button(f"تأكيد التعديلات على الحساب {selected_account}"):
        accounts[selected_account]["limit"] = round(updated_limit, 2)
        accounts[selected_account]["date"] = str(updated_date)
        save_accounts(accounts)
        st.success(f"تم تعديل الحساب {selected_account} بنجاح!")

# تحميل الحملات من ملف JSON لصفحة الحملات الأخرى
campaigns = load_campaigns()
