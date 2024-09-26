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

# حساب الأيام المتبقية حتى تاريخ الدفع
def days_until_due(due_date):
    today = datetime.today().date()
    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    return (due_date - today).days

# حساب المبلغ المضاف يوميًا لكل حملة
def daily_campaign_amount(campaign):
    amount = campaign["amount"]
    days = campaign["days"]
    start_date = datetime.strptime(campaign["start_date"], "%Y-%m-%d").date()
    today = datetime.today().date()

    # حساب عدد الأيام منذ بداية الحملة وحتى اليوم
    elapsed_days = (today - start_date).days

    if elapsed_days > days:  # الحملة قد انتهت
        elapsed_days = days

    if elapsed_days < 0:  # الحملة لم تبدأ بعد
        return 0

    # المبلغ المضاف حتى الآن بناءً على الأيام المنقضية
    return (amount / days) * elapsed_days

# حساب المبلغ الإجمالي بناءً على الحملات
def total_campaigns_amount(campaigns):
    return sum(daily_campaign_amount(campaign) for campaign in campaigns)

# عرض التنبيهات بناءً على التاريخ والمبلغ
def show_notifications(account_name, account, campaigns):
    due_date = account["date"]
    days_left = days_until_due(due_date)
    if campaigns:
        total_amount = total_campaigns_amount(campaigns)  # حساب المجموع الكلي للحملات اليومية
    else:
        total_amount = 0.0
    account_limit = account["limit"]

    # تنبيه عند اقتراب تاريخ الدفع (3 أيام قبل الموعد)
    if days_left <= 3 and days_left > 0:
        st.warning(f"حساب {account_name}: تبقى {days_left} يوم/أيام حتى موعد الدفع ({due_date}).")
    elif days_left == 0:
        st.error(f"حساب {account_name}: اليوم هو موعد الدفع ({due_date}).")
    elif days_left < 0:
        st.error(f"حساب {account_name}: لقد تجاوزت تاريخ الدفع منذ {-days_left} يوم/أيام.")

    # تنبيه عند اقتراب المبلغ المحدد
    if total_amount >= account_limit:
        st.warning(f"حساب {account_name}: المبلغ الإجمالي للحملات ({total_amount:,.2f} $) قد بلغ أو تجاوز الحد المحدد ({account_limit:,.2f} $).")
    # تنبيه عند اقتراب المبلغ من الحد المحدد (90%)
    elif total_amount >= 0.9 * account_limit:
        st.info(f"حساب {account_name}: المبلغ الإجمالي ({total_amount:,.2f} $) يقترب من الحد المحدد ({account_limit:,.2f} $).")

# الصفحة الرئيسية
def accueil_page():
    st.title("Al Nour Elite")
    st.header("مرحبًا بك في تطبيق إدارة الحملات")
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
    if st.button("تأكيد إضافة الحساب", key="add_account"):
        if new_account_name and new_account_name not in accounts:
            accounts[new_account_name] = {
                "name": new_account_name,
                "next_campaign_id": 1,
                "limit": round(new_limit, 2),
                "date": new_date.strftime("%Y-%m-%d"),
                "campaigns": []
            }
            save_accounts(accounts)
            st.success(f"تم إضافة الحساب {new_account_name} بنجاح!")
        else:
            st.error("يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

    # تعديل الحسابات القديمة
    st.subheader("تعديل الحسابات القديمة")
    if accounts:
        selected_account = st.selectbox("اختر حسابًا لتعديله", list(accounts.keys()))
        if selected_account:
            st.write(f"تعديل الحساب: {selected_account}")
            account_limit = accounts[selected_account].get("limit", 0.0)
            updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0.0, value=float(account_limit), format="%.2f", key="update_limit")
            updated_date = st.date_input("تعديل التاريخ المحدد", value=datetime.strptime(accounts[selected_account]["date"], "%Y-%m-%d"), key="update_date")
            if st.button(f"تأكيد التعديلات على الحساب {selected_account}", key="update_account"):
                accounts[selected_account]["limit"] = round(updated_limit, 2)
                accounts[selected_account]["date"] = updated_date.strftime("%Y-%m-%d")
                save_accounts(accounts)
                st.success(f"تم تحديث الحساب {selected_account} بنجاح!")
    else:
        st.info("لا توجد حسابات حالياً.")

# إضافة حملة
def add_campaign_page():
    st.header("إضافة حملة")
    accounts = load_accounts()
    campaigns = load_campaigns()

    if accounts:
        selected_account = st.selectbox("اختر حسابًا لإضافة الحملة إليه", list(accounts.keys()))
        if selected_account:
            st.subheader(f"إضافة حملة إلى الحساب: {selected_account}")
            customer_name = st.text_input("اسم الزبون")
            amount = st.number_input("المبلغ", min_value=0.0, format="%.2f")
            days = st.number_input("عدد الأيام", min_value=1, step=1)
            start_date = st.date_input("تاريخ البداية")
            end_date = start_date + timedelta(days=days-1)
            if st.button("تأكيد إضافة الحملة"):
                if selected_account not in campaigns:
                    campaigns[selected_account] = []
                campaign_id = accounts[selected_account]["next_campaign_id"]
                new_campaign = {
                    "id": campaign_id,
                    "customer_name": customer_name,
                    "amount": amount,
                    "days": days,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                campaigns[selected_account].append(new_campaign)
                accounts[selected_account]["next_campaign_id"] += 1
                save_campaigns(campaigns)
                save_accounts(accounts)
                st.success("تم إضافة الحملة بنجاح!")
    else:
        st.info("لا توجد حسابات حالياً. يرجى إضافة حساب أولاً.")

# عرض الحملات
def view_campaigns_page():
    st.header("عرض الحملات")
    campaigns = load_campaigns()
    accounts = load_accounts()
    if campaigns:
        selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))
        if selected_account in campaigns and campaigns[selected_account]:
            st.subheader(f"الحملات لحساب: {selected_account}")
            df = pd.DataFrame(campaigns[selected_account])

            # إضافة عمود لحذف الحملة
            df['حذف'] = ''

            # عرض الحملات مع خيار الحذف
            for idx, row in df.iterrows():
                st.write(f"**اسم الزبون:** {row['customer_name']}")
                st.write(f"**المبلغ:** {row['amount']:,.2f} $")
                st.write(f"**عدد الأيام:** {row['days']} يوم")
                st.write(f"**تاريخ البداية:** {row['start_date']}")
                st.write(f"**تاريخ النهاية:** {row['end_date']}")
                if st.button("حذف الحملة", key=f"delete_{selected_account}_{idx}"):
                    campaigns[selected_account].pop(idx)
                    save_campaigns(campaigns)
                    st.success("تم حذف الحملة بنجاح!")
                    st.experimental_rerun()
                st.write("---")
        else:
            st.info("لا توجد حملات لهذا الحساب.")
    else:
        st.info("لا توجد حملات مسجلة.")

# لوحة التحكم
def dashboard_page():
    st.header("لوحة التحكم - متابعة الحسابات الإعلانية")
    accounts = load_accounts()
    campaigns = load_campaigns()

    if accounts:
        for account_name, account in accounts.items():
            st.subheader(f"حساب: {account_name}")
            if account_name in campaigns:
                show_notifications(account_name, account, campaigns[account_name])
            else:
                # حتى لو لم يكن هناك حملات، نظهر التنبيهات المتعلقة بتاريخ الدفع
                show_notifications(account_name, account, [])
                st.info(f"لا توجد حملات مسجلة لهذا الحساب.")
    else:
        st.info("لا توجد حسابات حالياً.")

# تشغيل التطبيق
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.title("اختر من القائمة")
page = st.sidebar.selectbox(" ", ["الصفحة الرئيسية", "لوحة التحكم", "إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

if page == "الصفحة الرئيسية":
    accueil_page()
elif page == "لوحة التحكم":
    dashboard_page()
elif page == "إدارة الحسابات":
    manage_accounts_page()
elif page == "إضافة حملة":
    add_campaign_page()
elif page == "عرض الحملات":
    view_campaigns_page()
