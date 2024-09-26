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

    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = ""
    if 'campaign_amount' not in st.session_state:
        st.session_state.campaign_amount = 0.0
    if 'campaign_days' not in st.session_state:
        st.session_state.campaign_days = 1

    selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()))

    if selected_account:
        # إضافة خانة لاسم الزبون
        customer_name = st.text_input("اسم الزبون", value=st.session_state.customer_name)
        
        campaign_amount = st.number_input("المبلغ للحملة", min_value=0.0, format="%.2f", value=st.session_state.campaign_amount)
        campaign_days = st.number_input("عدد الأيام", min_value=1, value=st.session_state.campaign_days)
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

            # إعادة تعيين القيم لإفراغ الحقول
            st.session_state.customer_name = ""
            st.session_state.campaign_amount = 0.0
            st.session_state.campaign_days = 1

            st.success("تم تسجيل الحملة بنجاح!")

# صفحة عرض الحملات
if page == "عرض الحملات":
    st.header("الحملات المسجلة")

    selected_account = st.selectbox("اختر حسابًا", list(campaigns.keys()))

    if selected_account in campaigns and campaigns[selected_account]:
        # حساب حالة الحساب بناءً على الفارق بين التاريخ المحدد واليوم الحالي
        days_left = calculate_days_left(accounts[selected_account]["date"])
        total_amount = sum(campaign["amount"] for campaign in campaigns[selected_account])
        account_limit = accounts[selected_account]["limit"]
        
        # تنبيه لقرب وصول المبلغ أو التاريخ المحدد
        if total_amount >= account_limit:
            st.warning(f"حساب {selected_account}: المبلغ الإجمالي ({total_amount:,.2f} $) بلغ أو تجاوز المبلغ المحدد للحساب ({account_limit:,.2f} $).")
            total_amount = 0  # تصفير المبلغ عند تجاوز الحد
        elif days_left <= 2:
            st.warning(f"حساب {selected_account}: تبقى {days_left} يوم/أيام للوصول إلى تاريخ الدفع المحدد ({accounts[selected_account]['date']}).")

        # تنبيه لحالة الحساب بناءً على الفارق بين التاريخ واليوم
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

        # تنسيق الأرقام لتكون برقمين بعد الفاصلة وإضافة فراغ بين الرقم والوحدة (الدولار)
        df["المبلغ"] = df["المبلغ"].map(lambda x: f"{x:,.2f} $")
        df["عدد الأيام"] = df["عدد الأيام"].map(lambda x: f"{x} يوم")

        # منطق عرض وتعديل الحملة
        for i, row in df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{row['اسم الزبون']} - {row['المبلغ']} - {row['عدد الأيام']} يوم")
            with col2:
                if st.button(f"✏️ تعديل {i+1}", key=f"edit_{i}"):
                    with st.form(f"edit_form_{i}"):
                        new_customer_name = st.text_input("اسم الزبون", value=row["اسم الزبون"])
                        new_amount = st.number_input("المبلغ", value=float(row["المبلغ"].replace("$", "").replace(",", "")))
                        new_days = st.number_input("عدد الأيام", value=int(row["عدد الأيام"].replace(" يوم", "")))
                        new_start_date = st.date_input("تاريخ البداية", value=pd.to_datetime(row["تاريخ البداية"]))
                        new_end_date = st.date_input("تاريخ النهاية", value=pd.to_datetime(row["تاريخ النهاية"]))

                        if st.form_submit_button("حفظ التعديلات"):
                            # تحديث الحملة في قائمة الحملات
                            campaigns[selected_account][i]["customer_name"] = new_customer_name
                            campaigns[selected_account][i]["amount"] = round(new_amount, 2)
                            campaigns[selected_account][i]["days"] = new_days
                            campaigns[selected_account][i]["start_date"] = str(new_start_date)
                            campaigns[selected_account][i]["end_date"] = str(new_end_date)

                            # حفظ التعديلات في ملف JSON
                            save_campaigns(campaigns)
                            st.success(f"تم تعديل الحملة {i+1} بنجاح!")
                            st.experimental_rerun()  # إعادة تحميل الصفحة لتحديث البيانات

            with col3:
                if st.button(f"🗑️ حذف {i+1}", key=f"delete_{i}"):
                    campaigns[selected_account].pop(i)
                    save_campaigns(campaigns)
                    st.success(f"تم حذف الحملة {i+1}")
                    st.experimental_rerun()  # إعادة تحميل الصفحة بعد الحذف
    else:
        st.write("لا توجد حملات مسجلة.")
