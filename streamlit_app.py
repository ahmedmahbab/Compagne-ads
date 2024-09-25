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

# جهة التنقل
page = st.sidebar.radio("اختر صفحة:", ["إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

if page == "إدارة الحسابات":
    st.header("إدارة الحسابات")

    # إضافة حساب
    account_name = st.text_input("اسم الحساب")
    if st.button("تأكيد إضافة الحساب"):
        if account_name and account_name not in accounts:
            accounts[account_name] = {"next_campaign_id": 1, "campaigns": []}
            save_accounts(accounts)
            st.success("تم إضافة الحساب بنجاح!")
        else:
            st.error("يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

    # تعديل الحسابات
    st.header("تعديل حسابات موجودة")
    selected_account = st.selectbox("اختر حسابًا للتعديل", list(accounts.keys()))

    if selected_account:
        # عرض تفاصيل الحساب
        st.write(f"حساب: {selected_account}")
        next_campaign_id = accounts[selected_account]["next_campaign_id"]
        st.write(f"رقم الحملة التالية: {next_campaign_id}")

        # تعديل تفاصيل الحساب
        new_amount = st.number_input("المبلغ المحدد للحساب", min_value=0, value=next_campaign_id)
        if st.button("تعديل المبلغ المحدد"):
            accounts[selected_account]["next_campaign_id"] = new_amount
            save_accounts(accounts)
            st.success("تم تعديل المبلغ المحدد بنجاح!")

elif page == "إضافة حملة":
    st.header("إضافة حملة")
    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account:
        campaign_amount = st.number_input("المبلغ للحملة")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة", value=datetime.today())
        end_date = start_date + timedelta(days=campaign_days)  # تاريخ نهاية الحملة
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

elif page == "عرض الحملات":
    st.header("الحملات المسجلة")
    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])
        st.dataframe(df)
    else:
        st.write("لا توجد حملات مسجلة.")
