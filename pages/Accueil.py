def accueil_page():
    try:
        st.image("assets/logo.jpg", use_column_width=False, width=200, caption="شعار الشركة")
    except Exception as e:
        st.write(f"حدث خطأ أثناء تحميل الصورة: {e}")
    
    st.write("مرحبًا بكم في تطبيق إدارة الحملات")
