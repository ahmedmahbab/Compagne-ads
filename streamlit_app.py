import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

# تحميل الحسابات من ملف JSON
def load_accounts():
    try:
        with open('accounts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# حفظ الحسابات إلى ملف JSON
def save_accounts(accounts):
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

# تحميل الحملات من ملف JSON
def load_campaigns():
    try:
        with open('campaigns.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# حفظ الحملات إلى ملف JSON
def save_campaigns(campaigns):
    with open('campaigns.json', 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=4)

# الصفحة الرئيسية
def accueil_page():
    st.title("مرحبًا بكم في تطبيق إدارة الحملات")
    st.header("Al Nour Elite")
    st.subheader("إدارة الحملات بسهولة وفعالية")
    st.write("اختر من القائمة الجانبية للبدء في العمل.")

# إدارة الحسابات
def manage_accounts_page():
    st.header("إدارة الحسابات")
    st.write("محتوى صفحة إدارة الحسابات")

# إضافة حملة
def add_campaign_page():
    st.header("إضافة حملة جديدة")
    st.write("محتوى صفحة إضافة حملة")

# عرض الحملات
def view_campaigns_page():
    st.header("عرض الحملات")
    st.write("محتوى صفحة عرض الحملات")

# تعديل الحملات
def edit_campaigns_page():
    st.header("تعديل أو حذف الحملات")

    # تحميل الحسابات والحملات
    accounts = load_accounts()
    campaigns = load_campaigns()

    # اختيار الحساب
    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    # عرض الحملات المسجلة في الحساب المحدد
    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])

        # إضافة عمود جديد لخيارات التعديل والحذف
        df["تعديل"] = df.index
        df["حذف"] = df.index

        # عرض جدول الحملات
        st.dataframe(df)

        # تحديد الحملة لتعديلها
        selected_campaign = st.selectbox("اختر حملة لتعديلها", df.index)

        # تعديل الحملة
        if st.button("تعديل الحملة"):
            campaign = campaigns[selected_account][selected_campaign]
            new_customer_name = st.text_input("اسم الزبون", value=campaign['customer_name'])
            new_amount = st.number_input("المبلغ", min_value=0.0, value=float(campaign['amount']))
            new_days = st.number_input("عدد الأيام", min_value=1, value=int(campaign['days']))
            new_start_date = st.date_input("تاريخ بداية الحملة", value=pd.to_datetime(campaign['start_date']))

            # حساب تاريخ نهاية الحملة بناءً على عدد الأيام
            new_end_date = new_start_date + timedelta(days=new_days)

            if st.button("حفظ التعديلات"):
                campaigns[selected_account][selected_campaign] = {
                    "customer_name": new_customer_name,
                    "amount": new_amount,
                    "days": new_days,
                    "start_date": str(new_start_date),
                    "end_date": str(new_end_date)
                }
                save_campaigns(campaigns)
                st.success("تم تعديل الحملة بنجاح!")

        # حذف الحملة
        if st.button("حذف الحملة"):
            campaigns[selected_account].pop(selected_campaign)
            save_campaigns(campaigns)
            st.success("تم حذف الحملة بنجاح!")

# تهيئة الصفحة المختارة في حالة الجلسة
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# استخدام أزرار في الشريط الجانبي للتنقل
st.sidebar.title("التنقل")

if st.sidebar.button("الصفحة الرئيسية"):
    st.session_state['page'] = 'home'

if st.sidebar.button("إدارة الحسابات"):
    st.session_state['page'] = 'manage_accounts'

if st.sidebar.button("إضافة حملة"):
    st.session_state['page'] = 'add_campaign'

if st.sidebar.button("عرض الحملات"):
    st.session_state['page'] = 'view_campaigns'

if st.sidebar.button("تعديل الحملات"):
    st.session_state['page'] = 'edit_campaigns'

# ربط الصفحة المختارة بعرض المحتوى المناسب
if st.session_state['page'] == 'home':
    accueil_page()
elif st.session_state['page'] == 'manage_accounts':
    manage_accounts_page()
elif st.session_state['page'] == 'add_campaign':
    add_campaign_page()
elif st.session_state['page'] == 'view_campaigns':
    view_campaigns_page()
elif st.session_state['page'] == 'edit_campaigns':
    edit_campaigns_page()
