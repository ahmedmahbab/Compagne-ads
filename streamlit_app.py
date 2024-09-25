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

# حساب الفرق بين تاريخ اليوم والتاريخ المحدد
def calculate_days_left(account_date):
    today = datetime.today().date()
    account_date = pd.to_datetime(account_date).date()
    return (account_date - today).days

# إعداد البيانات
accounts = load_accounts()
campaigns = load_campaigns()

# واجهة المستخدم
st.title("إدارة الحملات")

# جهة التنقل
page = st.sidebar.radio("اختر صفحة:", ["إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

# صفحة عرض الحملات
if page == "عرض الحملات":
    st.header("الحملات المسجلة")

    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        # حساب حالة الحساب بناءً على الفارق بين التاريخ المحدد واليوم الحالي
        days_left = calculate_days_left(accounts[selected_account]["date"])
        if days_left > 0:
            st.info(f"حساب {selected_account}: باقي {days_left} يوم/أيام حتى تاريخ الدفع.")
        elif days_left == 0:
            st.warning(f"حساب {selected_account}: اليوم هو آخر يوم لتاريخ الدفع.")
        else:
            st.error(f"حساب {selected_account}: لقد تجاوزت تاريخ الدفع منذ {-days_left} يوم/أيام.")

        df = pd.DataFrame(campaigns[selected_account])

        # حذف العمود الأول (ID)
        df = df.drop(columns=["id"])

        # تسمية الأعمدة
        df.columns = ["اسم الزبون", "المبلغ", "عدد الأيام", "تاريخ البداية", "تاريخ النهاية"]

        # تنسيق الأرقام لتكون برقمين بعد الفاصلة وإضافة فراغ بين الرقم والوحدة
        df["المبلغ"] = df["المبلغ"].map(lambda x: f"{x:,.2f} د.ج")
        df["عدد الأيام"] = df["عدد الأيام"].map(lambda x: f"{x} يوم")

        # تنسيق الألوان الهادئة وتوسيط الأعمدة
        df_style = df.style.set_properties(**{
            'text-align': 'center',
            'background-color': '#f0f8ff',  # لون خلفية هادئ
            'color': 'black',
            'border-color': 'white'
        }).set_table_styles([
            {
                'selector': 'thead th',
                'props': [('background-color', '#b0c4de'), ('color', 'white')]  # خلفية هادئة لرأس الجدول
            },
            {
                'selector': 'tbody tr:nth-child(even)',
                'props': [('background-color', '#e6f2ff')]  # صفوف متناوبة
            },
            {
                'selector': 'tbody tr:hover',
                'props': [('background-color', '#dcdcdc')]  # تأثير عند التمرير
            }
        ])

        # عرض الجدول
        st.write(df_style)
    else:
        st.write("لا توجد حملات مسجلة.")
