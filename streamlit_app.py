import json
import streamlit as st

# تحميل الحسابات من ملف JSON
try:
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    accounts = {}

# عرض الحسابات المتاحة
selected_account = st.selectbox("اختر حسابًا", list(accounts.keys()) + ["إضافة حساب جديد"])

# إضافة حساب جديد
if selected_account == "إضافة حساب جديد":
    new_account_name = st.text_input("أدخل اسم الحساب الجديد")
    
    if st.button("إضافة حساب"):
        if new_account_name:
            if new_account_name not in accounts:
                accounts[new_account_name] = {"next_campaign_id": 1, "campaigns": []}
                # حفظ البيانات
                with open('accounts.json', 'w') as f:
                    json.dump(accounts, f)
                st.success("تم إضافة الحساب الجديد بنجاح!")
            else:
                st.error("هذا الحساب موجود بالفعل.")
        else:
            st.error("يرجى إدخال اسم الحساب.")
else:
    # تحقق من وجود الحساب
    if selected_account in accounts:
        # تعيين القيمة الافتراضية للرقم التسلسلي
        if "next_campaign_id" not in accounts[selected_account]:
            accounts[selected_account]["next_campaign_id"] = 1

        # تأكد من وجود مفتاح الحملات في الحساب
        if "campaigns" not in accounts[selected_account]:
            accounts[selected_account]["campaigns"] = []

        # عرض الحملات المسجلة في الحساب
        st.write("الحملات المسجلة:")
        campaigns = accounts[selected_account]["campaigns"]
        
        for campaign in campaigns:
            with st.expander(f"حملة ID: {campaign['id']}"):
                campaign_amount = st.number_input("المبلغ", value=campaign['amount'], key=f"amount_{campaign['id']}")
                campaign_days = st.number_input("عدد الأيام", value=campaign['days'], key=f"days_{campaign['id']}")
                start_date = st.date_input("تاريخ بداية الحملة", value=pd.to_datetime(campaign['start_date']).date(), key=f"start_{campaign['id']}")
                end_date = st.date_input("تاريخ نهاية الحملة", value=pd.to_datetime(campaign['end_date']).date(), key=f"end_{campaign['id']}")

                if st.button("تحديث الحملة", key=f"update_{campaign['id']}"):
                    campaign['amount'] = campaign_amount
                    campaign['days'] = campaign_days
                    campaign['start_date'] = str(start_date)
                    campaign['end_date'] = str(end_date)

                    # حفظ البيانات بعد التحديث
                    with open('accounts.json', 'w') as f:
                        json.dump(accounts, f)

                    st.success("تم تحديث الحملة بنجاح!")

                if st.button("حذف الحملة", key=f"delete_{campaign['id']}"):
                    campaigns.remove(campaign)  # حذف الحملة من القائمة
                    with open('accounts.json', 'w') as f:
                        json.dump(accounts, f)
                    st.success("تم حذف الحملة بنجاح!")
                    break  # للخروج من الحلقة بعد الحذف

        # إدخال بيانات الحملة الجديدة
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
