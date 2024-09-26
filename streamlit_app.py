import streamlit as st
from pages.Accueil import accueil_page
from pages.manage_accounts import manage_accounts_page
from pages.add_campaign import add_campaign_page
from pages.view_campaigns import view_campaigns_page

st.sidebar.title("التنقل")

# إضافة التنقل الجانبي
page = st.sidebar.radio("اختر صفحة:", ["الصفحة الرئيسية", "إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

# استدعاء الصفحة المختارة
if page == "الصفحة الرئيسية":
    accueil_page()
elif page == "إدارة الحسابات":
    manage_accounts_page()
elif page == "إضافة حملة":
    add_campaign_page()
elif page == "عرض الحملات":
    view_campaigns_page()
