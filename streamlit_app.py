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
    
    # عرض اسم الشركة
    st.header("Al Nour Elite")
    
    # العنوان الفرعي
    st.subheader("إدارة الحملات بسهولة وفعالية")

    st.write("اختر من القائمة الجانبية للبدء في العمل.")

# إدارة الحسابات
def manage_accounts_page():
    st.header("إدارة الحسابات")

    accounts = load_accounts()

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
        account_limit = accounts[selected_account].get("limit", 0.0)
        updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0.0, value=float(account_limit), format="%.2f")
        updated_date = st.date_input("تعديل التاريخ المحدد", value=pd.to_datetime(accounts[selected_account]["date"]))

        if st.button(f"تأكيد التعديلات على الحساب {selected_account}"):
            accounts[selected_account]["limit"] = round(updated_limit, 2)
            accounts[selected_account]["date"] = str(updated_date)
            save_accounts(accounts)
            st.success(f"تم تعديل الحساب {selected_account} بنجاح!")

# إضافة حملة
def add_campaign_page():
    st.header("إضافة حملة جديدة")

    accounts = load_accounts()
    campaigns = load_campaigns()

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account:
        customer_name = st.text_input("اسم الزبون")
        campaign_amount = st.number_input("المبلغ للحملة", min_value=0.0, format="%.2f")
        campaign_days = st.number_input("عدد الأيام", min_value=1)
        start_date = st.date_input("تاريخ بداية الحملة", value=datetime.today())
        end_date = start_date + timedelta(days=campaign_days)
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

# عرض الحملات
def view_campaigns_page():
    st.header("عرض الحملات")

    accounts = load_accounts()
    campaigns = load_campaigns()

    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])
        df = df.drop(columns=["id"])
        df["تاريخ تسجيل الحملة"] = pd.to_datetime("today").strftime("%Y-%m-%d")
        df.columns = ["اسم الزبون", "المبلغ", "عدد الأيام", "تاريخ البداية", "تاريخ النهاية", "تاريخ تسجيل الحملة"]
        df["المبلغ"] = df["المبلغ"].map(lambda x: f"{x:,.2f} $")
        df["عدد الأيام"] = df["عدد الأيام"].map(lambda x: f"{x} يوم")

        st.write(df)

# تشغيل التطبيق

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content .widget {
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
        padding: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.title("التنقل")

# استخدام selectbox لتقديم قائمة أنيقة
page = st.sidebar.selectbox("اختر صفحة:", ["الصفحة الرئيسية", "إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

# استدعاء الصفحة المختارة
if page == "الصفحة الرئيسية":
    accueil_page()
elif page == "إدارة الحسابات":
    manage_accounts_page()
elif page == "إضافة حملة":
    add_campaign_page()
elif page == "عرض الحملات":
    view_campaigns_page()
