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
        .sub-title {
            text-align: center;
            font-size: 30px;
            color: #2980B9;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # تحميل الصورة من مجلد 'assets'
    st.image("assets/logo.png", use_column_width=False, width=200, caption="شعار الشركة")
    st.markdown('<p class="main-title">مرحبًا بكم في تطبيق إدارة الحملات</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">إدارة الحملات بسهولة وفعالية</p>', unsafe_allow_html=True)

    st.write("اختر من القائمة الجانبية للبدء في العمل.")
