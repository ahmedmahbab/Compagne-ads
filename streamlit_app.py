import json
import streamlit as st

# تحميل الحسابات من ملف JSON
try:
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    accounts = {}

# عرض الحسابات المتاحة
selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

# تحقق من وجود الحساب
if selected_account in accounts:
    # تعيين القيمة الافتراضية للرقم التسلسلي
    if "next_campaign_id" not in accounts[selected_account]:
        accounts[selected_account]["next_campaign_id"] = 1

    # تأكد من وجود مفتاح الحملات في الحساب
    if "campaigns" not in accounts[selected_account]:
        accounts[selected_account]["campaigns"] = []

    # إدخال بيانات الحملة
    campaign_amount = st.number_input("أدخل المبلغ للحملة")
    campaign_days = st.number_input("عدد الأيام", min_value=1)  # حد أدنى لعدد الأيام
    campaign_account_name = selected_account
    start_date = st.date_input("تاريخ بداية الحملة")
    end_date = st.date_input("تاريخ نهاية الحملة")

    # تسجيل الحملة عند الضغط على الزر
    if st.button("تسجيل الحملة"):
        campaign_id = accounts[selected_account]["next_campaign_id"]
        # أضف الحملة إلى الحساب
        accounts[selected_account]["campaigns"].append({
            "id": campaign_id,
            "amount": campaign_amount,
            "days": campaign_days,
            "account_name": campaign_account_name,
            "start_date": str(start_date),
            "end_date": str(end_date)
        })
        # تحديث الرقم التسلسلي
        accounts[selected_account]["next_campaign_id"] += 1
        
        # حفظ البيانات
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)

        st.success("تم تسجيل الحملة بنجاح!")
else:
    st.error("الحساب المحدد غير موجود.")
