
import streamlit as st
import pandas as pd

# تحميل قاعدة البيانات
@st.cache_data # هذه الميزة تجعل التحميل سريعاً جداً
def load_data():
    return pd.read_excel("Electrical_Materials_Inventory.xlsx")

df = load_data()



st.set_page_config(page_title="حاسبة الكهرباء المتطورة", layout="centered")


# إعدادات الصفحة لتظهر كالتطبيق
# 1. العنوان يوضع هنا (خارج الـ sidebar ليكون في وسط الشاشة)
st.title("⚡ نظام تقدير الكميات والتكاليف")

# 2. إعدادات القائمة الجانبية
with st.sidebar:
    st.header("⚙️ إعدادات الأسعار (دج)")
    
    # أسعار القطع الأساسية
    p_socket = st.number_input("سعر المقبس الواحد", value=650)
    p_lamp = st.number_input("سعر المصباح الواحد", value=700)
    p_jb = st.number_input("سعر علبة التفريع", value=800)
    
    st.markdown("---")
    
    # أسعار لوحات التوزيع
    st.subheader("📦 أسعار لوحات التوزيع")
    p_8p = st.number_input("سعر لوحة 8P", value=4000)
    p_12p = st.number_input("سعر لوحة 12P", value=5000)
    p_24p = st.number_input("سعر لوحة 24P", value=7000)
    
    st.info("💡 يمكنك تعديل الأسعار حسب منطقتك قبل الضغط على حساب.")

    # --- كود أسعار لوحات التوزيع (الذي أعطيتك إياه مؤخراً) يوضع هنا أيضاً ---


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
    # 1. البحث عن أقرب حالة في الجدول (الذكاء الاصطناعي)
    df["score"] = (abs(df["الغرف"] - rooms) + abs(df["المساحة m2"] - massa7a))
    best_match = df.loc[df["score"].idxmin()]

    # 2. حساب النتائج بناءً على نسب الجدول (التناسب الطردي)
    # نحسب كم متر يحتاج كل 1 متر مربع بناءً على أفضل مطابقة
    ratio_15 = best_match["سلك 1.5 (لفة)"] / best_match["المساحة m2"]
    ratio_25 = best_match["سلك 2.5 (لفة)"] / best_match["المساحة m2"]
    
    # تطبيق النسب على مساحة المستخدم الحالية
    calc_wire_15 = round(ratio_15 * massa7a, 2)
    calc_wire_25 = round(ratio_25 * massa7a, 2)
    
    # حساب العلب واللوحة (منطق تقني)
    total_points = s_normal + s_ground + l_normal + l_spot
    pots = total_points
    breaker_slots = rooms + 4
    
    # 3. الحساب المالي (باستخدام الأسعار من الـ Sidebar)
    # ملاحظة: p_socket و p_lamp و p_jb معرفة في الـ Sidebar
    total_cost = (total_points * p_socket) + (rooms * p_jb) + p_12p # مثال للوحة

    # --- بداية عرض النتائج في التطبيق ---
    st.success("✅ تم توليد النتائج بناءً على معايير المشاريع السابقة")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("سلك 1.5 مم (محسوب)", f"{calculated_wire15} لفة")
    with col2:
        st.metric("سلك 2.5 مم (محسوب)", f"{calculated_wire25} لفة")
        
    st.write(f"🔹 **علب التثبيت المطلوبة فعلياً:** {calculated_pots} قطعة")

    
    

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
