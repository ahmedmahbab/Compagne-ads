import json
import streamlit as st
import pandas as pd
from datetime import timedelta

# تحميل الحسابات من ملف JSON
def load_accounts():
    try:
        with open('accounts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# تحميل الحملات من ملف JSON
def load_campaigns():
    try:
        with open('campaigns.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# حفظ الحسابات إلى ملف JSON
def save_accounts(accounts):
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)

# حفظ الحملات إلى ملف JSON
def save_campaigns(campaigns):
    with open('campaigns.json', 'w') as f:
        json.dump(campaigns, f)

# تحميل البيانات
accounts = load_accounts()
campaigns = load_campaigns()

# واجهة المستخدم
st.title("إدارة الحسابات والحملات")

# التنقل بين الصفحات
if st.sidebar.button("الحسابات"):
    st.header("إدارة الحسابات")
    
    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()) + ["إضافة حساب جديد"])

    if selected_account == "إضافة حساب جديد":
        new_account_name = st.text_input("أدخل اسم الحساب الجديد")
        new_limit = st.number_input("أدخل المبلغ المحدد", min_value=0)
        new_date = st.date_input("أدخل التاريخ المحدد", value=pd.Timestamp.now())

        if st.button("إضافة حساب"):
            if new_account_name:
                if new_account_name not in accounts:
                    accounts[new_account_name] = {
                        "next_campaign_id": 1,
                        "campaigns": [],
                        "limit": new_limit,
                        "date": str(new_date)
                    }
                    save_accounts(accounts)
                    st.success("تم إضافة الحساب الجديد بنجاح!")
                else:
                    st.error("هذا الحساب موجود بالفعل.")
            else:
                st.error("يرجى إدخال اسم الحساب.")
    else:
        current_limit = accounts[selected_account].get("limit", 0)
        current_date = accounts[selected_account].get("date", "غير محدد")
        
        st.write(f"المبلغ المحدد: {current_limit}")
        st.write(f"تاريخ المحدد: {current_date}")

        new_limit = st.number_input("تعديل المبلغ المحدد", value=current_limit)
        new_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(current_date))

        if st.button("تحديث الحساب"):
            accounts[selected_account]["limit"] = new_limit
            accounts[selected_account]["date"] = str(new_date)
            save_accounts(accounts)
            st.success("تم تحديث الحساب بنجاح!")

# إدارة الحملات
if st.sidebar.button("إدارة الحملات"):
    st.header("إدارة الحملات")

    selected_account = st.selectbox("اختر حسابًا لإدارة الحملات", list(accounts.keys()))

    if selected_account:
        campaign_amount = st.number_input("أدخل المبلغ للحملة")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة")
        end_date = start_date + timedelta(days=campaign_days)

        # تسجيل الحملة عند الضغط على الزر
        if st.button("تسجيل الحملة"):
            campaign_id = accounts[selected_account]["next_campaign_id"]
            
            # إضافة الحملة إلى الحساب
            if selected_account not in campaigns:
                campaigns[selected_account] = []

            campaigns[selected_account].append({
                "id": campaign_id,
                "amount": campaign_amount,
                "days": campaign_days,
                "account_name": selected_account,
                "start_date": str(start_date),
                "end_date": str(end_date)
            })

            # تحديث الرقم التسلسلي
            accounts[selected_account]["next_campaign_id"] += 1
            
            # حفظ البيانات
            save_accounts(accounts)
            save_campaigns(campaigns)

            st.success("تم تسجيل الحملة بنجاح!")

        # عرض الحملات المسجلة
        if selected_account in campaigns:
            st.write("الحملات المسجلة:")
            campaign_data = campaigns[selected_account]

            # تحويل البيانات إلى جدول
            campaign_table = []
            for campaign in campaign_data:
                campaign_table.append([
                    campaign["id"],
                    campaign["start_date"],
                    campaign["end_date"],
                    campaign["amount"],
                    campaign["account_name"],
                    campaign["days"]
                ])

            # عرض الجدول باستخدام Streamlit
            st.table(campaign_table)

            # حذف حملة
            campaign_id_to_delete = st.number_input("أدخل رقم الحملة لحذفها", min_value=1)
            if st.button("حذف الحملة"):
                for campaign in campaigns[selected_account]:
                    if campaign["id"] == campaign_id_to_delete:
                        campaigns[selected_account].remove(campaign)
                        save_campaigns(campaigns)
                        st.success("تم حذف الحملة بنجاح!")
                        break
                else:
                    st.error("رقم الحملة غير موجود.")
