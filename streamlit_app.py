import streamlit as st
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="إدارة الحسابات والحملات", page_icon="📊", layout="centered")

# قائمة لتخزين الحسابات وحدودها
accounts = {}

# إدخال أو تعديل الحسابات
st.markdown("<h2 style='text-align: center;'>إضافة أو تعديل حساب</h2>", unsafe_allow_html=True)

account_name = st.text_input("أدخل اسم الحساب")
max_amount = st.number_input("أدخل السقف المحدد للحساب (المبلغ)", min_value=0.0)
max_date = st.date_input("أدخل التاريخ المحدد للحساب", value=datetime.today() + timedelta(days=30))

# زر لإضافة الحساب أو تعديله
if st.button("إضافة/تعديل الحساب"):
    accounts[account_name] = {"max_amount": max_amount, "max_date": max_date, "current_amount": 0}
    st.success(f"تم إضافة أو تعديل الحساب: {account_name}")

# إدخال حملة جديدة
st.markdown("<h2 style='text-align: center;'>إدخال حملة جديدة</h2>", unsafe_allow_html=True)

if accounts:
    selected_account = st.selectbox("اختر الحساب", options=accounts.keys())
    campaign_amount = st.number_input("المبلغ", min_value=0.0)
    days = st.number_input("عدد الأيام", min_value=1, value=7)
    start_date = st.date_input("تاريخ البداية", value=datetime.today())

    # حساب تاريخ النهاية
    end_date = start_date + timedelta(days=days)

    # تحديث المبلغ الحالي للحساب
    if st.button("تسجيل الحملة"):
        accounts[selected_account]["current_amount"] += campaign_amount

        # عرض تفاصيل الحملة
        st.markdown("<h3>تفاصيل الحملة:</h3>", unsafe_allow_html=True)
        st.write(f"الحساب: {selected_account}")
        st.write(f"المبلغ: {campaign_amount} DZD")
        st.write(f"عدد الأيام: {days} يوم")
        st.write(f"تاريخ البداية: {start_date}")
        st.write(f"تاريخ النهاية: {end_date}")

        # الحصول على حدود الحساب
        account_info = accounts[selected_account]
        warning_message = ""

        # تحقق من المبلغ
        if account_info["current_amount"] >= 0.9 * account_info["max_amount"]:
            warning_message += f"⚠️ تحذير: المبلغ الحالي ({account_info['current_amount']} DZD) يقترب من الحد الأقصى للحساب ({account_info['max_amount']} DZD).\n"

        # تحقق من التاريخ
        if end_date >= account_info["max_date"] - timedelta(days=2):
            warning_message += f"⚠️ تحذير: تاريخ نهاية الحملة ({end_date}) يقترب من الحد الزمني للحساب ({account_info['max_date']}).\n"

        # إذا تم الوصول إلى الحد
        if warning_message:
            st.warning(warning_message)
            st.write("🔄 سيتم إعادة تعيين الحساب عند الوصول إلى الحد.")
            accounts[selected_account]["current_amount"] = 0
        else:
            st.success("✅ الحملة تم تسجيلها بنجاح.")
else:
    st.error("يرجى إضافة حساب أولاً قبل تسجيل حملة.")
