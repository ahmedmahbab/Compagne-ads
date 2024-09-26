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

    # استخدام رابط مباشر للصورة بدلاً من تحميلها محليًا
    st.image("https://lh6.googleusercontent.com/uUBr22ZS3x71Gr_HslpAWK8jRN4LqJ-sA1vb2YOlrw8w89M0UUdzX9eI8QDc9RgDru6wC225QkKHONrynX_7V3hd911H05bJ4nf5W-d9IixSOvs_Msjq48lOv22wEkNI1Q=w1280", use_column_width=False, width=200, caption="شعار الشركة")
    st.markdown('<p class="main-title">مرحبًا بكم في تطبيق إدارة الحملات</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">إدارة الحملات بسهولة وفعالية</p>', unsafe_allow_html=True)

    st.write("اختر من القائمة الجانبية للبدء في العمل.")
