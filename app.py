import streamlit as st

# إعدادات الصفحة لتظهر كالتطبيق
st.set_page_config(page_title="حاسبة الكهرباء الاحترافية", layout="centered")

st.title("⚡ نظام حساب الكميات والمواد")

# المرحلة 1: المدخلات (حسب شروطك تماماً)
with st.form("main_form"):
    st.subheader("📝 مدخلات المشروع")
    massa7a = st.number_input("المساحة الإجمالية (m²)", min_value=1)
    rooms = st.number_input("عدد الغرف / المناطق", min_value=1)
    
    col1, col2 = st.columns(2)
    with col1:
        s_normal = st.number_input("مقابس عادية (L+N)", min_value=0)
        l_normal = st.number_input("مصابيح عادية", min_value=0)
    with col2:
        s_ground = st.number_input("مقابس أرضي (L+N+T)", min_value=0)
        l_spot = st.number_input("مصابيح SPOT", min_value=0)
    
    submit = st.form_submit_button("حساب كميات مواد البناء")

# المرحلة 2: المخرجات (باقي مواد البناء)
if submit:
    # منطق الحساب بناءً على مدخلاتك
    total_sockets = s_normal + s_ground
    total_lamps = l_normal + l_spot
    
    # تقدير الأسلاك (بالأمتار)
    wire_15 = (l_normal * 7) + (l_spot * 4)
    wire_25 = (s_normal * 10) + (s_ground * 12)
    
    # تقدير الأنابيب والعلب
    tubes_16 = massa7a * 1.5
    pots = total_sockets + total_lamps
    
    st.divider()
    st.subheader("🏗️ قائمة مواد البناء المطلوبة:")
    
    res1, res2 = st.columns(2)
    with res1:
        st.write(f"🔹 **الأسلاك:**")
        st.write(f"- سلك 1.5 مم: {wire_15} متر")
        st.write(f"- سلك 2.5 مم: {wire_25} متر")
        st.write(f"🔹 **الأنابيب:**")
        st.write(f"- خرطوم 16 مم: {int(tubes_16)} متر")
    
    with res2:
        st.write(f"🔹 **العلب واللوحات:**")
        st.write(f"- علب تثبيت (Pot): {pots} قطعة")
        st.write(f"- علب تفريع (BD): {rooms} قطع")
        st.write(f"- لوحة توزيع: {rooms + 4} قواطع")

    st.success("✅ تم حساب الكميات بناءً على المعايير التقنية الجزائرية.")
        # ... (بقية الكود السابق)

    # إضافة معلومات التواصل الخاصة بك
    st.markdown(f"""
    ---
    ** المطور:**باهية إبراهيم  
    **التخصص:** ماستر هندسة كهربائية  
    **للتواصل وتطوير البيانات:** [0784178506](tel:0784178506)
    """)

    # تنبيه الذكاء الاصطناعي
    st.warning("⚠️ ملاحظة: هذا النموذج يعمل بتقنيات الذكاء الاصطناعي وهو في طور التجريب، لذا قد تحدث أخطاء في التقدير. يرجى المراجعة الميدانية.")
