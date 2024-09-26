import streamlit as st

def accueil_page():
    st.markdown(
        """
        <style>
        .main-title {
            text-align: center;
            font-size: 50px;
            color: #2E86C1;
            margin-top: 20px;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 150px;
        }
        .sub-title {
            text-align: center;
            font-size: 30px;
            color: #2980B9;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # اللوقو والعنوان الرئيسي
    st.image("logo.png", use_column_width=False, width=200, output_format="auto", caption="شعار الشركة",)
    st.markdown('<p class="main-title">مرحبًا بكم في تطبيق إدارة الحملات</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">إدارة الحملات بسهولة وفعالية</p>', unsafe_allow_html=True)

    st.write("اختر من القائمة الجانبية للبدء في العمل.")
