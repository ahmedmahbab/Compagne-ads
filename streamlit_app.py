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
    # محتوى صفحة إدارة الحسابات (ضع الكود الخاص بك هنا)

# إضافة حملة
def add_campaign_page():
    st.header("إضافة حملة جديدة")
    # محتوى صفحة إضافة حملة (ضع الكود الخاص بك هنا)

# عرض الحملات
def view_campaigns_page():
    st.header("عرض الحملات")
    # محتوى صفحة عرض الحملات (ضع الكود الخاص بك هنا)

# تشغيل التطبيق

# تهيئة الصفحة المختارة في حالة الجلسة
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# وظيفة لإنشاء عنصر تنقل
def nav_item(label, page_key):
    # تحقق مما إذا كانت هذه هي الصفحة المختارة
    if st.session_state['page'] == page_key:
        # تطبيق نمط الصفحة المختارة
        style = """
            background: linear-gradient(to right, #2E86C1, #85C1E9);
            color: white;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            margin-bottom: 5px;
            cursor: pointer;
            border-radius: 5px;
        """
    else:
        # النمط العادي
        style = """
            color: black;
            text-align: center;
            padding: 10px;
            margin-bottom: 5px;
            cursor: pointer;
            border-radius: 5px;
        """

    # إنشاء عنصر HTML قابل للنقر
    nav_html = f"""
    <p style="{style}" onclick="location.href='/?page={page_key}'">{label}</p>
    """

    st.sidebar.markdown(nav_html, unsafe_allow_html=True)

# عرض التنقل الجانبي
st.sidebar.title("التنقل")

# تعريف الصفحات
pages = {
    "الصفحة الرئيسية": "home",
    "إدارة الحسابات": "manage_accounts",
    "إضافة حملة": "add_campaign",
    "عرض الحملات": "view_campaigns"
}

# قراءة المعلمة 'page' من عنوان URL
query_params = st.experimental_get_query_params()
if 'page' in query_params and query_params['page'][0] in pages.values():
    st.session_state['page'] = query_params['page'][0]

# عرض عناصر التنقل
for label, page_key in pages.items():
    nav_item(label, page_key)

# عرض الصفحة المختارة
if st.session_state['page'] == 'home':
    accueil_page()
elif st.session_state['page'] == 'manage_accounts':
    manage_accounts_page()
elif st.session_state['page'] == 'add_campaign':
    add_campaign_page()
elif st.session_state['page'] == 'view_campaigns':
    view_campaigns_page()
