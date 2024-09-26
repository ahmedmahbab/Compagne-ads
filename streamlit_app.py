import streamlit as st
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
