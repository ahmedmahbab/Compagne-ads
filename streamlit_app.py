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

# حفظ الحسابات إلى ملف JSON
def save_accounts(accounts):
    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

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
def show_notifications(account, campaigns):
    due_date = account["date"]
    days_left = days_until_due(due_date)
    total_amount = total_campaigns_amount(campaigns)  # حساب المجموع الكلي للحملات اليومية
    account_limit = account["limit"]

    # تنبيه عند اقتراب تاريخ الدفع (7 أيام قبل الموعد)
    if days_left <= 7 and days_left > 0:
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
        if account_name in campaigns and campaigns[account_name]:
            show_notifications(account, campaigns[account_name])
        else:
            st.info(f"لا توجد حملات مسجلة لهذا الحساب.")

# عرض الحملات مع إمكانية حذفها
def view_campaigns_page():
    st.header("عرض الحملات وحذفها")

    accounts = load_accounts()
    campaigns = load_campaigns()

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        df = pd.DataFrame(campaigns[selected_account])

        st.write("قائمة الحملات:")
        st.dataframe(df)

        # اختيار الحملة المراد حذفها
        selected_campaign = st.selectbox("اختر حملة لحذفها", df.index)

        if st.button("حذف الحملة"):
            campaigns[selected_account].pop(selected_campaign)
            save_campaigns(campaigns)
            st.success(f"تم حذف الحملة رقم {selected_campaign} بنجاح!")

# واجهة التطبيق
st.sidebar.title("التنقل")
page = st.sidebar.selectbox("اختر الصفحة", ["لوحة التحكم", "إضافة حملة", "عرض الحملات"])

if page == "لوحة التحكم":
    dashboard_page()
elif page == "عرض الحملات":
    view_campaigns_page()
