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
campaigns = load_campaigns()

# واجهة المستخدم
st.title("إدارة الحملات")

# جهة التنقل
page = st.sidebar.radio("اختر صفحة:", ["إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

# صفحة إدارة الحسابات
if page == "إدارة الحسابات":
    st.header("إدارة الحسابات")

    # إضافة حساب جديد
    st.subheader("إضافة حساب جديد")
    new_account_name = st.text_input("اسم الحساب الجديد")
    new_limit = st.number_input("المبلغ المحدد", min_value=0)
    new_date = st.date_input("التاريخ المحدد")

    if st.button("تأكيد إضافة الحساب"):
        if new_account_name and new_account_name not in accounts:
            accounts[new_account_name] = {"next_campaign_id": 1, "limit": new_limit, "date": str(new_date), "campaigns": []}
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
        updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0, value=accounts[selected_account]["limit"])
        updated_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(accounts[selected_account]["date"]))
        
        if st.button("تأكيد تعديل الحساب"):
            accounts[selected_account]["limit"] = updated_limit
            accounts[selected_account]["date"] = str(updated_date)
            save_accounts(accounts)
            st.success(f"تم تعديل الحساب {selected_account} بنجاح!")

# صفحة إضافة حملة
elif page == "إضافة حملة":
    st.header("إضافة حملة")

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))
    
    if selected_account:
        # إضافة خانة لاسم الزبون
        customer_name = st.text_input("اسم الزبون")
        
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
                "customer_name": customer_name,  # إضافة اسم الزبون للحملة
                "amount": campaign_amount,
                "days": campaign_days,
                "start_date": str(start_date),
                "end_date": str(end_date)
            })
            accounts[selected_account]["next_campaign_id"] += 1
            save_accounts(accounts)
            save_campaigns(campaigns)
            st.success("تم تسجيل الحملة بنجاح!")

# صفحة عرض الحملات
elif page == "عرض الحملات":
    st.header("الحملات المسجلة")

    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])
        st.dataframe(df)
    else:
        st.write("لا توجد حملات مسجلة.")
