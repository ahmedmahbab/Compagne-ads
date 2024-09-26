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

    # **عرض المبلغ الإجمالي للحساب**
    st.write(f"**💰 المبلغ الإجمالي للحساب حتى الآن:** {total_amount:,.2f} $")

    # تنبيه عند اقتراب تاريخ الدفع (3 أيام قبل الموعد)
    if days_left <= 3 and days_left > 0:
        st.warning(f"⏰ حساب {account_name}: تبقى {days_left} يوم/أيام حتى موعد الدفع ({due_date}).")
    elif days_left == 0:
        st.error(f"🚨 حساب {account_name}: اليوم هو موعد الدفع ({due_date}).")
    elif days_left < 0:
        st.error(f"⚠️ حساب {account_name}: لقد تجاوزت تاريخ الدفع منذ {-days_left} يوم/أيام.")

    # تنبيه عند اقتراب المبلغ المحدد
    if total_amount >= account_limit:
        st.warning(f"📈 حساب {account_name}: المبلغ الإجمالي للحملات ({total_amount:,.2f} $) قد بلغ أو تجاوز الحد المحدد ({account_limit:,.2f} $).")
    # تنبيه عند اقتراب المبلغ من الحد المحدد (90%)
    elif total_amount >= 0.9 * account_limit:
        st.info(f"🔔 حساب {account_name}: المبلغ الإجمالي ({total_amount:,.2f} $) يقترب من الحد المحدد ({account_limit:,.2f} $).")

# الصفحة الرئيسية
def accueil_page():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌟 Al Nour Elite 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>مرحبًا بك في تطبيق إدارة الحملات</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>إدارة الحملات بسهولة وفعالية</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>اختر من القائمة الجانبية للبدء في العمل.</p>", unsafe_allow_html=True)

# إدارة الحسابات
def manage_accounts_page():
    st.markdown("<h2>🔧 إدارة الحسابات</h2>", unsafe_allow_html=True)
    accounts = load_accounts()

    # إضافة حساب جديد
    st.markdown("<h3>➕ إضافة حساب جديد</h3>", unsafe_allow_html=True)
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
            st.success(f"✅ تم إضافة الحساب {new_account_name} بنجاح!")
        else:
            st.error("❌ يرجى إدخال اسم حساب صحيح أو الحساب موجود بالفعل.")

    # تعديل الحسابات القديمة
    st.markdown("<h3>📝 تعديل الحسابات القديمة</h3>", unsafe_allow_html=True)
    if accounts:
        selected_account = st.selectbox("اختر حسابًا لتعديله", list(accounts.keys()))
        if selected_account:
            st.write(f"**تعديل الحساب:** {selected_account}")
            account_limit = accounts[selected_account].get("limit", 0.0)
            updated_limit = st.number_input("تعديل المبلغ المحدد", min_value=0.0, value=float(account_limit), format="%.2f", key="update_limit")
            updated_date = st.date_input("تعديل التاريخ المحدد", value=datetime.strptime(accounts[selected_account]["date"], "%Y-%m-%d"), key="update_date")
            if st.button(f"تأكيد التعديلات على الحساب {selected_account}", key="update_account"):
                accounts[selected_account]["limit"] = round(updated_limit, 2)
                accounts[selected_account]["date"] = updated_date.strftime("%Y-%m-%d")
                save_accounts(accounts)
                st.success(f"✅ تم تحديث الحساب {selected_account} بنجاح!")
    else:
        st.info("ℹ️ لا توجد حسابات حالياً.")

# إضافة حملة
def add_campaign_page():
    st.markdown("<h2>📢 إضافة حملة</h2>", unsafe_allow_html=True)
    accounts = load_accounts()
    campaigns = load_campaigns()

    if accounts:
        selected_account = st.selectbox("اختر حسابًا لإضافة الحملة إليه", list(accounts.keys()))
        if selected_account:
            st.markdown(f"<h3>إضافة حملة إلى الحساب: {selected_account}</h3>", unsafe_allow_html=True)
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
                st.success("✅ تم إضافة الحملة بنجاح!")
    else:
        st.info("ℹ️ لا توجد حسابات حالياً. يرجى إضافة حساب أولاً.")

# عرض الحملات
def view_campaigns_page():
    st.markdown("<h2>📄 عرض الحملات</h2>", unsafe_allow_html=True)
    campaigns = load_campaigns()
    accounts = load_accounts()
    if campaigns:
        selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))
        if selected_account in campaigns and campaigns[selected_account]:
            st.markdown(f"<h3>الحملات لحساب: {selected_account}</h3>", unsafe_allow_html=True)
            df = pd.DataFrame(campaigns[selected_account])

            # عرض الحملات مع خيار الحذف
            for idx, row in df.iterrows():
                st.markdown(f"""
                <div style='border:1px solid #ccc; padding:10px; border-radius:5px; margin-bottom:10px;'>
                    <p><strong>👤 اسم الزبون:</strong> {row['customer_name']}</p>
                    <p><strong>💵 المبلغ:</strong> {row['amount']:,.2f} $</p>
                    <p><strong>📆 عدد الأيام:</strong> {row['days']} يوم</p>
                    <p><strong>🚀 تاريخ البداية:</strong> {row['start_date']}</p>
                    <p><strong>🏁 تاريخ النهاية:</strong> {row['end_date']}</p>
                </div>
                """, unsafe_allow_html=True)

                # زر حذف الحملة باستخدام st.button
                if st.button("🗑️ حذف الحملة", key=f"delete_{selected_account}_{idx}"):
                    campaigns[selected_account].pop(idx)
                    save_campaigns(campaigns)
                    st.success("✅ تم حذف الحملة بنجاح!")

                    # استبدل st.experimental_rerun() بالسطر المناسب
                    st.experimental_rerun()  # إذا لم يعمل هذا السطر، جرب السطر التالي:
                    # st.experimental_rerun()
                    # أو إذا كان كلاهما لا يعمل، جرب:
                    # st.rerun()

            else:
                st.info("ℹ️ لا توجد حملات لهذا الحساب.")
    else:
        st.info("ℹ️ لا توجد حملات مسجلة.")

# لوحة التحكم
def dashboard_page():
    st.markdown("<h2>📊 لوحة التحكم - متابعة الحسابات الإعلانية</h2>", unsafe_allow_html=True)
    accounts = load_accounts()
    campaigns = load_campaigns()

    if accounts:
        for account_name, account in accounts.items():
            st.markdown(f"<h3>حساب: {account_name}</h3>", unsafe_allow_html=True)
            if account_name in campaigns:
                show_notifications(account_name, account, campaigns[account_name])
            else:
                # حتى لو لم يكن هناك حملات، نظهر التنبيهات المتعلقة بتاريخ الدفع
                show_notifications(account_name, account, [])
                st.info("ℹ️ لا توجد حملات مسجلة لهذا الحساب.")
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ لا توجد حسابات حالياً.")

# تشغيل التطبيق
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Cairo&display=swap');
    body {
        font-family: 'Cairo', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.title("🔍 التنقل")
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
