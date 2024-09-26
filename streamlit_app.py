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

# تهيئة الصفحة المختارة في حالة الجلسة
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# وظيفة لتحديث الصفحة عند النقر
def navigate_to(page_key):
    st.session_state['page'] = page_key

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
            border-radius: 5px;
            cursor: pointer;
        """
    else:
        # النمط العادي
        style = """
            color: black;
            text-align: center;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            cursor: pointer;
        """

    # إنشاء عنصر HTML مع ربط الصفحة
    nav_html = f"""
    <p style="{style}" onclick="window.location.href='/?page={page_key}'">{label}</p>
    """
    
    # عند النقر، تحديث الصفحة المختارة
    if st.sidebar.markdown(nav_html, unsafe_allow_html=True):
        navigate_to(page_key)

# عرض التنقل الجانبي
st.sidebar.title("التنقل")

# ربط الصفحات بالعناوين
nav_item("الصفحة الرئيسية", "home")
nav_item("إدارة الحسابات", "manage_accounts")
nav_item("إضافة حملة", "add_campaign")
nav_item("عرض الحملات", "view_campaigns")

# عرض الصفحة المختارة
if st.session_state['page'] == 'home':
    accueil_page()
elif st.session_state['page'] == 'manage_accounts':
    manage_accounts_page()
elif st.session_state['page'] == 'add_campaign':
    add_campaign_page()
elif st.session_state['page'] == 'view_campaigns':
    view_campaigns_page()
