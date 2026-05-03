import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (يجب أن تكون في البداية)
st.set_page_config(page_title="حاسبة الكهرباء المتطورة", layout="centered")

# 2. تحميل قاعدة البيانات
@st.cache_data
def load_data():
    try:
        data = pd.read_excel("Electrical_Materials_Inventory.xlsx")
        cols_to_fix = ["المساحة m2", "سلك 1.5 (لفة)", "سلك 2.5 (لفة)", "الغرف"]
        for col in cols_to_fix:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        return data.dropna(subset=cols_to_fix)
    except:
        # في حال عدم وجود الملف، إنشاء جدول فارغ لتجنب تعطل التطبيق
        return pd.DataFrame(columns=["المساحة m2", "سلك 1.5 (لفة)", "سلك 2.5 (لفة)", "الغرف"])

df = load_data()

# 3. العنوان الرئيسي
st.title("⚡ نظام تقدير الكميات والتكاليف")

# 4. إعدادات القائمة الجانبية
with st.sidebar:
    st.header("⚙️ إعدادات الأسعار (دج)")
    
    p_socket = st.number_input("سعر المقبس الواحد", value=650)
    p_lamp = st.number_input("سعر المصباح الواحد", value=700)
    p_jb = st.number_input("سعر علبة التفريع", value=800)
    
    st.markdown("---")
    st.subheader("📦 أسعار لوحات التوزيع")
    p_8p = st.number_input("سعر لوحة 8P", value=4000)
    p_12p = st.number_input("سعر لوحة 12P", value=5000)
    p_24p = st.number_input("سعر لوحة 24P", value=7000)
    
    st.info("💡 يمكنك تعديل الأسعار حسب منطقتك قبل الضغط على حساب.")

# 5. مدخلات المشروع
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

# 6. المخرجات والعمليات الحسابية
if submit:
    if df.empty:
        st.error("⚠️ قاعدة البيانات غير موجودة أو فارغة. يرجى التأكد من رفع ملف Excel.")
    else:
        # البحث عن أقرب حالة (الذكاء الاصطناعي)
        df["score"] = (abs(df["الغرف"] - rooms) + abs(df["المساحة m2"] - massa7a))
        best_match = df.loc[df["score"].idxmin()]

        # حساب النسب بناءً على المرجع المختار
        if best_match["المساحة m2"] > 0:
            ratio_15 = float(best_match["سلك 1.5 (لفة)"]) / float(best_match["المساحة m2"])
            ratio_25 = float(best_match["سلك 2.5 (لفة)"]) / float(best_match["المساحة m2"])
        else:
            ratio_15, ratio_25 = 0, 0
    
        # تطبيق النسب على مساحة المستخدم الحالية
        calc_wire_15 = round(ratio_15 * massa7a, 2)
        calc_wire_25 = round(ratio_25 * massa7a, 2)
        
        # حساب العلب واللوحات
        total_points = s_normal + s_ground + l_normal + l_spot
        pots = total_points
        breaker_slots = rooms + 4
        
        # اختيار سعر اللوحة
        if breaker_slots <= 8:
            p_tableau = p_8p
        elif breaker_slots <= 12:
            p_tableau = p_12p
        else:
            p_tableau = p_24p

        # الحساب المالي
        total_cost = (total_points * p_socket) + (rooms * p_jb) + p_tableau

        # عرض النتائج
        st.success("✅ تم توليد النتائج بناءً على معايير المشاريع السابقة")
        
        st.subheader("🏗️ الكميات المحسوبة")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("سلك 1.5 مم", f"{calc_wire_15} لفة")
            st.write(f"🔹 علب التثبيت: {pots} قطعة")
        with res_col2:
            st.metric("سلك 2.5 مم", f"{calc_wire_25} لفة")
            st.write(f"🔹 علب التفريع: {rooms} قطعة")
            
        st.divider()
        st.subheader("💰 التقدير المالي")
        st.metric("إجمالي تكلفة المواد", f"{total_cost:,} دج")
        
        st.warning("⚠️ ملاحظة: هذا النموذج يعمل بتقنيات الذكاء الاصطناعي وهو في طور التجريب، لذا قد تحدث أخطاء في التقدير. يرجى المراجعة الميدانية.")

        # معلومات التواصل
        st.markdown(f"""
        ---
        **المطور:** باهية إبراهيم  
        **التخصص:** ماستر هندسة كهربائية  
        **للتواصل وتطوير البيانات:** [0784178506](tel:0784178506)
        """)

