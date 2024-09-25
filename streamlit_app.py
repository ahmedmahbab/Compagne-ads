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

# صفحة إدارة الحسابات
if page == "إدارة الحسابات":
    st.header("إدارة الحسابات")

    # إضافة حساب جديد
    st.subheader("إضافة حساب جديد")
    new_account_name = st.text_input("اسم الحساب الجديد")
    new_limit = st.number_input("المبلغ المحدد", min_value=0.0, format="%.2f")
    new_date = st.date_input("التاريخ المحدد")

    if st.button("تأكيد إضافة الحساب"):
        if new_account_name and new_account_name not in accounts:
            accounts[new_account_name] = {"next_campaign_id": 1, "limit": round(new_limit, 2), "date": str(new_date), "campaigns": []}
            save_accounts(accounts)
            st.success(f"تم إضافة الحساب {new_account_name} بنجاح!")
        else:
            st.error("يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

    # تعديل الحسابات القديمة
    st.subheader("تعديل الحسابات القديمة")
    selected_account = st.selectbox("اختر حسابًا لتعديله", list(accounts.keys()))

    if selected_account:
        st.write(f"تعديل الحساب: {selected_account}")
        
        # التحقق من وجود المبلغ المحدد للحساب
        account_limit = accounts[selected_account].get("limit", 0.0)  # تعيين قيمة افتراضية إذا كانت البيانات مفقودة

        # تعديل المبلغ المحدد والتاريخ
        updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0.0, value=float(account_limit), format="%.2f")
        updated_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(accounts[selected_account]["date"]))

        # زر لتأكيد التعديلات
        if st.button(f"تأكيد التعديلات على الحساب {selected_account}"):
            accounts[selected_account]["limit"] = round(updated_limit, 2)
            accounts[selected_account]["date"] = str(updated_date)
            save_accounts(accounts)
            st.success(f"تم تعديل الحساب {selected_account} بنجاح!")

# صفحة إضافة حملة
elif page == "إضافة حملة":
    st.header("إضافة حملة")

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))
    
    if selected_account:
        # إضافة خانة لاسم الزبون
        customer_name = st.text_input("اسم الزبون")
        
        campaign_amount = st.number_input("المبلغ للحملة", min_value=0.0, format="%.2f")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة", value=datetime.today())
        end_date = start_date + timedelta(days=campaign_days)  # تاريخ نهاية الحملة
        st.write(f"تاريخ نهاية الحملة: {end_date}")

        if st.button("تسجيل الحملة"):
            campaign_id = accounts[selected_account]["next_campaign_id"]
            campaigns[selected_account] = campaigns.get(selected_account, [])
            campaigns[selected_account].append({
                "id": campaign_id,
                "customer_name": customer_name,
                "amount": round(campaign_amount, 2),
                "days": campaign_days,
                "start_date": str(start_date),
                "end_date": str(end_date)
            })
            accounts[selected_account]["next_campaign_id"] += 1
            save_accounts(accounts)
            save_campaigns(campaigns)
            st.success("تم تسجيل الحملة بنجاح!")

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

        # إضافة عمود جديد لتسجيل الحملة أوتوماتيكياً
        df["تاريخ تسجيل الحملة"] = pd.to_datetime("today").strftime("%Y-%m-%d")

        # تسمية الأعمدة
        df.columns = ["اسم الزبون", "المبلغ", "عدد الأيام", "تاريخ البداية", "تاريخ النهاية", "تاريخ تسجيل الحملة"]

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
