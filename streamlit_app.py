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
    st.title("Al Nour Elite")
    
    # عرض اسم الشركة
    st.header("مرحبًا بك في تطبيق إدارة الحملات")
    
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

st.sidebar.title("اختر من القائمة")

# استخدام selectbox لتقديم قائمة أنيقة
page = st.sidebar.selectbox(" ", ["الصفحة الرئيسية", "إدارة الحسابات", "إضافة حملة", "عرض الحملات"])

# استدعاء الصفحة المختارة
if page == "الصفحة الرئيسية":
    accueil_page()
elif page == "إدارة الحسابات":
    manage_accounts_page()
elif page == "إضافة حملة":
    add_campaign_page()
elif page == "عرض الحملات":
    view_campaigns_page()
import streamlit as st
import json
from datetime import datetime, timedelta

# تحميل الحسابات والحملات
def load_accounts():
    try:
        with open('accounts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_campaigns():
    try:
        with open('campaigns.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

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
def show_notifications(account, campaigns):
    due_date = account["date"]
    days_left = days_until_due(due_date)
    total_amount = total_campaigns_amount(campaigns)  # حساب المجموع الكلي للحملات اليومية
    account_limit = account["limit"]

    # تنبيه عند اقتراب تاريخ الدفع (7 أيام قبل الموعد)
    if days_left <= 3 and days_left > 0:
        st.warning(f"حساب {account['name']}: تبقى {days_left} يوم/أيام حتى موعد الدفع ({due_date}).")
    elif days_left == 0:
        st.error(f"حساب {account['name']}: اليوم هو موعد الدفع ({due_date}).")
    elif days_left < 0:
        st.error(f"حساب {account['name']}: لقد تجاوزت تاريخ الدفع منذ {-days_left} يوم/أيام.")

    # تنبيه عند اقتراب المبلغ المحدد
    if total_amount >= account_limit:
        st.warning(f"حساب {account['name']}: المبلغ الإجمالي للحملات ({total_amount:,.2f} $) قد بلغ أو تجاوز الحد المحدد ({account_limit:,.2f} $).")

    # تنبيه عند اقتراب المبلغ من الحد المحدد (90%)
    elif total_amount >= 0.9 * account_limit:
        st.info(f"حساب {account['name']}: المبلغ الإجمالي ({total_amount:,.2f} $) يقترب من الحد المحدد ({account_limit:,.2f} $).")

# تحديث تاريخ الدفع إلى الشهر التالي
def update_due_date(account):
    current_due_date = datetime.strptime(account["date"], "%Y-%m-%d")
    next_due_date = current_due_date + timedelta(days=30)  # التحديث للشهر القادم
    account["date"] = next_due_date.strftime("%Y-%m-%d")
    return account

# واجهة المستخدم
def dashboard_page():
    st.header("لوحة التحكم - متابعة الحسابات الإعلانية")

    # تحميل الحسابات والحملات
    accounts = load_accounts()
    campaigns = load_campaigns()

    # عرض الحسابات والتنبيهات
    for account_name, account in accounts.items():
        st.subheader(f"حساب: {account_name}")
        if account_name in campaigns:
            show_notifications(account, campaigns[account_name])
        else:
            st.info(f"لا توجد حملات مسجلة لهذا الحساب.")

# واجهة التطبيق
st.sidebar.title("التنقل")
page = st.sidebar.selectbox("اختر الصفحة", ["لوحة التحكم", "إضافة حملة", "إدارة الحسابات"])

if page == "لوحة التحكم":
    dashboard_page()
