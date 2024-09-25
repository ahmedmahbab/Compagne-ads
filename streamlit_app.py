import streamlit as st
import json
from datetime import datetime, timedelta

# ملف لحفظ الحسابات والحملات
ACCOUNTS_FILE = "accounts.json"

# تحميل الحسابات من ملف JSON
def load_accounts():
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# حفظ الحسابات في ملف JSON
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f)

# تحميل الحسابات الموجودة
accounts = load_accounts()

# إعداد الصفحة
st.set_page_config(page_title="إدارة الحسابات والحملات", page_icon="📊", layout="centered")

# --- إدخال أو تعديل الحسابات ---
st.markdown("<h2 style='text-align: center;'>إضافة أو تعديل حساب</h2>", unsafe_allow_html=True)

account_name = st.text_input("أدخل اسم الحساب")
max_amount = st.number_input("أدخل السقف المحدد للحساب (المبلغ)", min_value=0.0)
max_date = st.date_input("أدخل التاريخ المحدد للحساب", value=datetime.today() + timedelta(days=30))

# زر لإضافة الحساب أو تعديله
if st.button("إضافة/تعديل الحساب"):
    if account_name:
        if account_name not in accounts:
            # إضافة حساب جديد
            accounts[account_name] = {"max_amount": max_amount, "max_date": str(max_date), "current_amount": 0, "campaigns": [], "next_campaign_id": 1}
        else:
            # تعديل حساب موجود
            accounts[account_name]["max_amount"] = max_amount
            accounts[account_name]["max_date"] = str(max_date)
        
        save_accounts(accounts)  # حفظ الحسابات بعد التعديل
        st.success(f"تم إضافة أو تعديل الحساب: {account_name}")
    else:
        st.error("يرجى إدخال اسم الحساب.")

# --- إدخال حملة جديدة ---
st.markdown("<h2 style='text-align: center;'>إدخال حملة جديدة</h2>", unsafe_allow_html=True)

if accounts:
    selected_account = st.selectbox("اختر الحساب", options=accounts.keys())
    campaign_amount = st.number_input("المبلغ", min_value=0.0)
    days = st.number_input("عدد الأيام", min_value=1, value=7)
    start_date = st.date_input("تاريخ البداية", value=datetime.today())

    # حساب تاريخ النهاية
    end_date = start_date + timedelta(days=days)

    # زر لتسجيل الحملة
    if st.button("تسجيل الحملة"):
        if selected_account in accounts:
            # تحديث المبلغ الحالي للحساب وإضافة الحملة
            accounts[selected_account]["current_amount"] += campaign_amount
            campaign_id = accounts[selected_account]["next_campaign_id"]  # الرقم التسلسلي للحملة
            campaign = {
                "id": campaign_id,
                "amount": campaign_amount,
                "days": days,
                "start_date": str(start_date),
                "end_date": str(end_date)
            }
            accounts[selected_account]["campaigns"].append(campaign)
            accounts[selected_account]["next_campaign_id"] += 1  # تحديث الرقم التسلسلي للحملة التالية
            save_accounts(accounts)  # حفظ الحسابات والحملات بعد التعديل

            # عرض تفاصيل الحملة
            st.markdown("<h3>تفاصيل الحملة:</h3>", unsafe_allow_html=True)
            st.write(f"رقم الحملة: {campaign_id}")
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
            if end_date >= datetime.strptime(account_info["max_date"], "%Y-%m-%d") - timedelta(days=2):
                warning_message += f"⚠️ تحذير: تاريخ نهاية الحملة ({end_date}) يقترب من الحد الزمني للحساب ({account_info['max_date']}).\n"

            # إذا تم الوصول إلى الحد
            if warning_message:
                st.warning(warning_message)
                st.write("🔄 سيتم إعادة تعيين الحساب عند الوصول إلى الحد.")
                accounts[selected_account]["current_amount"] = 0
                save_accounts(accounts)  # حفظ التعديلات
            else:
                st.success("✅ الحملة تم تسجيلها بنجاح.")
else:
    st.error("يرجى إضافة حساب أولاً قبل تسجيل حملة.")

# --- عرض جميع الحملات لحساب محدد ---
st.markdown("<h2 style='text-align: center;'>عرض الحملات</h2>", unsafe_allow_html=True)

if accounts:
    selected_account_for_view = st.selectbox("اختر حساب لعرض الحملات", options=accounts.keys())

    if selected_account_for_view in accounts and accounts[selected_account_for_view]["campaigns"]:
        st.markdown("<h3>الحملات المسجلة:</h3>", unsafe_allow_html=True)
        for campaign in accounts[selected_account_for_view]["campaigns"]:
            st.write(f"🔹 رقم الحملة: {campaign['id']} | المبلغ: {campaign['amount']} DZD | تاريخ البداية: {campaign['start_date']} | تاريخ النهاية: {campaign['end_date']}")
    else:
        st.write("لا توجد حملات مسجلة لهذا الحساب.")
