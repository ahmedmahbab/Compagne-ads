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

# حفظ الحسابات في ملف JSON
def save_accounts(accounts):
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)

# تحميل البيانات في البداية
accounts = load_accounts()

# زر التنقل بين الصفحات
st.sidebar.title("التنقل")
if st.sidebar.button("الصفحة الرئيسية"):
    st.session_state.page = "الصفحة الرئيسية"
if st.sidebar.button("إدارة الحسابات"):
    st.session_state.page = "إدارة الحسابات"
if st.sidebar.button("إدارة الحملات"):
    st.session_state.page = "إدارة الحملات"
if st.sidebar.button("عرض الحملات المسجلة"):
    st.session_state.page = "عرض الحملات"

# تعيين الصفحة الافتراضية
if 'page' not in st.session_state:
    st.session_state.page = "الصفحة الرئيسية"

# الصفحة الرئيسية
if st.session_state.page == "الصفحة الرئيسية":
    st.title("الصفحة الرئيسية")
    st.write("مرحبًا بك في التطبيق!")
    st.write("اختر من القائمة الجانبية للانتقال إلى الصفحات الأخرى.")

# إدارة الحسابات
elif st.session_state.page == "إدارة الحسابات":
    st.title("إدارة الحسابات")
    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()) + ["إضافة حساب جديد"])

    # إضافة حساب جديد
    if selected_account == "إضافة حساب جديد":
        new_account_name = st.text_input("أدخل اسم الحساب الجديد")
        if st.button("إضافة حساب"):
            if new_account_name:
                if new_account_name not in accounts:
                    accounts[new_account_name] = {"next_campaign_id": 1, "campaigns": []}
                    save_accounts(accounts)
                    st.success("تم إضافة الحساب الجديد بنجاح!")
                else:
                    st.error("هذا الحساب موجود بالفعل.")
            else:
                st.error("يرجى إدخال اسم الحساب.")
    else:
        # تعديل الحساب
        st.write(f"تعديل الحساب: {selected_account}")
        new_limit = st.number_input("تعديل المبلغ المحدد", value=accounts[selected_account].get("limit", 0))
        new_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(accounts[selected_account].get("date", pd.Timestamp.now())))
        if st.button("تحديث الحساب"):
            accounts[selected_account]["limit"] = new_limit
            accounts[selected_account]["date"] = str(new_date)
            save_accounts(accounts)
            st.success("تم تحديث الحساب بنجاح!")

# إدارة الحملات
elif st.session_state.page == "إدارة الحملات":
    st.title("إدارة الحملات")
    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account in accounts:
        # عرض الحملات المسجلة
        st.write("الحملات المسجلة:")
        campaigns = accounts[selected_account]["campaigns"]
        
        if campaigns:
            for campaign in campaigns:
                with st.expander(f"حملة ID: {campaign['id']}"):
                    st.write(f"**المبلغ:** {campaign['amount']}")
                    st.write(f"**عدد الأيام:** {campaign['days']}")
                    st.write(f"**تاريخ بداية الحملة:** {pd.to_datetime(campaign['start_date']).date()}")
                    end_date = pd.to_datetime(campaign['start_date']) + timedelta(days=campaign['days'])
                    st.write(f"**تاريخ نهاية الحملة:** {end_date.date()}")

                    campaign_amount = st.number_input("المبلغ", value=campaign['amount'], key=f"amount_{campaign['id']}")
                    campaign_days = st.number_input("عدد الأيام", value=campaign['days'], key=f"days_{campaign['id']}")
                    start_date = st.date_input("تاريخ بداية الحملة", value=pd.to_datetime(campaign['start_date']).date(), key=f"start_{campaign['id']}")

                    if st.button("تحديث الحملة", key=f"update_{campaign['id']}"):
                        campaign['amount'] = campaign_amount
                        campaign['days'] = campaign_days
                        campaign['start_date'] = str(start_date)

                        save_accounts(accounts)

                        st.success("تم تحديث الحملة بنجاح!")

                    if st.button("حذف الحملة", key=f"delete_{campaign['id']}"):
                        campaigns.remove(campaign)
                        save_accounts(accounts)
                        st.success("تم حذف الحملة بنجاح!")
                        break  # للخروج من الحلقة بعد الحذف
        else:
            st.write("لا توجد حملات مسجلة لهذا الحساب.")

        # إضافة حملة جديدة
        st.write("إضافة حملة جديدة")
        campaign_amount = st.number_input("أدخل المبلغ للحملة")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة")

        if st.button("تسجيل الحملة"):
            campaign_id = accounts[selected_account]["next_campaign_id"]
            accounts[selected_account]["campaigns"].append({
                "id": campaign_id,
                "amount": campaign_amount,
                "days": campaign_days,
                "start_date": str(start_date),
            })
            accounts[selected_account]["next_campaign_id"] += 1

            save_accounts(accounts)

            st.success("تم تسجيل الحملة بنجاح!")

# عرض الحملات المسجلة
elif st.session_state.page == "عرض الحملات المسجلة":
    st.title("عرض الحملات المسجلة")
    
    # إعداد البيانات للعرض في جدول
    all_campaigns = []
    for account_name, account_data in accounts.items():
        campaigns = account_data.get("campaigns", [])
        for campaign in campaigns:
            end_date = pd.to_datetime(campaign['start_date']) + timedelta(days=campaign['days'])
            all_campaigns.append({
                "الرقم التسلسلي": campaign['id'],
                "تاريخ تسجيل الحملة": campaign['start_date'],
                "تاريخ إطلاق الحملة": end_date.date(),
                "المبلغ": campaign['amount'],
                "الحساب": account_name,
                "عدد الأيام": campaign['days'],
            })
    
    # إنشاء جدول باستخدام pandas
    if all_campaigns:
        df = pd.DataFrame(all_ca
