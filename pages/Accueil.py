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
            font-family: 'Arial', sans-serif;
            animation: fadeIn 2s ease-in-out;
        }
        .sub-title {
            text-align: center;
            font-size: 30px;
            color: #2980B9;
            margin-top: 10px;
            font-family: 'Arial', sans-serif;
        }
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        </style>
        """, unsafe_allow_html=True
    )

    # عرض اسم الشركة مع تأثير
    st.markdown('<p class="main-title">Al Nour Elite</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">إدارة الحملات بسهولة وفعالية</p>', unsafe_allow_html=True)

    st.write("اختر من القائمة الجانبية للبدء في العمل.")
