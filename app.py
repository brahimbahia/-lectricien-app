import re
import streamlit as st
import pandas as pd
import numpy as np

# ─── 1. إعدادات الصفحة ────────────────────────────────────────────────────────
st.set_page_config(page_title="حاسبة الكهرباء المتطورة", layout="centered")

# ─── 2. دالة تنظيف الخلايا ────────────────────────────────────────────────────
# تتعامل مع قيم مثل "11m"، "03 لفة"، "2 لفة" وتستخرج منها الرقم فقط
def clean_cell(val):
    if pd.isna(val):
        return np.nan
    m = re.match(r"[\d]+\.?[\d]*", str(val).strip())
    return float(m.group()) if m else np.nan

# ─── 3. تحميل قاعدة البيانات ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        data = pd.read_excel("Electrical_Materials_Inventory.xlsx")
        cols_to_fix = [
            "المساحة m2", "الغرف",
            "سلك 1.5 (لفة)", "سلك 2.5 (لفة)",
            "سلك 12", "سلك 16",
            "قاطعة دائرية (ذهاب وإياب)", "قاطعة مزدوجة", "قاطعة عادية",
            "علب التفريع BD",
            "مقابس L+N+T", "مقابس عادية L+N",
            "مصابيح SPOT", "مصابيح عادية",
        ]
        for col in cols_to_fix:
            if col in data.columns:
                data[col] = data[col].apply(clean_cell)
        data.dropna(subset=["المساحة m2", "الغرف"], inplace=True)
        data.fillna(0, inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data
    except FileNotFoundError:
        return pd.DataFrame(columns=["المساحة m2", "الغرف",
                                     "سلك 1.5 (لفة)", "سلك 2.5 (لفة)"])

df = load_data()

# ─── 4. العنوان الرئيسي ───────────────────────────────────────────────────────
st.title("⚡ نظام تقدير الكميات والتكاليف")

# ─── 5. القائمة الجانبية – الأسعار ───────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ إعدادات الأسعار (دج)")

    p_socket_lnt = st.number_input("سعر المقبس الأرضي (L+N+T)", value=650)
    p_socket_ln  = st.number_input("سعر المقبس العادي (L+N)",   value=500)
    p_lamp_spot  = st.number_input("سعر مصباح SPOT",             value=700)
    p_lamp_std   = st.number_input("سعر المصباح العادي",         value=500)
    p_jb         = st.number_input("سعر علبة التفريع",           value=800)

    st.markdown("---")
    st.subheader("📦 أسعار لوحات التوزيع")
    p_8p  = st.number_input("سعر لوحة 8P",  value=4000)
    p_12p = st.number_input("سعر لوحة 12P", value=5000)
    p_24p = st.number_input("سعر لوحة 24P", value=7000)

    st.info("💡 يمكنك تعديل الأسعار حسب منطقتك قبل الضغط على حساب.")

# ─── 6. مدخلات المشروع ───────────────────────────────────────────────────────
with st.form("main_form"):
    st.subheader("📝 مدخلات المشروع")

    massa7a = st.number_input("المساحة الإجمالية (m²)", min_value=1.0, value=80.0, step=1.0)
    rooms   = st.number_input("عدد الغرف / المناطق",    min_value=1,   value=3,    step=1)

    col1, col2 = st.columns(2)
    with col1:
        s_normal = st.number_input("مقابس عادية (L+N)",   min_value=0, value=4)
        l_normal = st.number_input("مصابيح عادية",         min_value=0, value=4)
    with col2:
        s_ground = st.number_input("مقابس أرضي (L+N+T)",  min_value=0, value=6)
        l_spot   = st.number_input("مصابيح SPOT",          min_value=0, value=8)

    submit = st.form_submit_button("حساب كميات مواد البناء")

# ─── 7. المخرجات والحسابات ───────────────────────────────────────────────────
if submit:
    if df.empty:
        st.error("⚠️ قاعدة البيانات غير موجودة أو فارغة. يرجى التأكد من رفع ملف Excel.")
    else:
        # ── البحث عن أقرب حالة ──────────────────────────────────────────────
        scores = abs(df["الغرف"] - rooms) + abs(df["المساحة m2"] - massa7a)
        scores = scores.dropna()                          # ← الإصلاح الأساسي

        if scores.empty:
            st.error("⚠️ تعذّر إيجاد مشروع مرجعي — تحقق من بيانات Excel.")
            st.stop()

        best_match = df.loc[scores.idxmin()]

        # ── حساب نسب السلك ──────────────────────────────────────────────────
        ref_area = float(best_match["المساحة m2"])
        if ref_area > 0:
            ratio_15 = float(best_match["سلك 1.5 (لفة)"]) / ref_area
            ratio_25 = float(best_match["سلك 2.5 (لفة)"]) / ref_area
        else:
            ratio_15, ratio_25 = 0, 0

        calc_wire_15 = round(ratio_15 * massa7a, 2)
        calc_wire_25 = round(ratio_25 * massa7a, 2)

        # ── اختيار اللوحة ───────────────────────────────────────────────────
        # اختيار لوحة الكهرباء حسب العدد
if breaker_slots <= 8:
    p_tableau = p_8p
elif breaker_slots <= 10:
    p_tableau = p_10p
elif breaker_slots <= 12:
    p_tableau = p_12p
elif breaker_slots <= 16:
    p_tableau = p_16p
else:
    p_tableau = p_24p

        # ── الحساب المالي ────────────────────────────────────────────────────
        total_points = s_normal + s_ground + l_normal + l_spot
        total_cost = (
            s_ground * p_socket_lnt +
            s_normal * p_socket_ln  +
            l_spot   * p_lamp_spot  +
            l_normal * p_lamp_std   +
            rooms    * p_jb         +
            p_tableau
        )

        # ── عرض النتائج ──────────────────────────────────────────────────────
        st.success("✅ تم توليد النتائج بناءً على معايير المشاريع السابقة")
        st.caption(
            f"المشروع المرجعي: **{ref_area} m²** | "
            f"**{int(best_match['الغرف'])} غرف**"
        )

        st.subheader("🏗️ الكميات المحسوبة")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("سلك 1.5 مم", f"{calc_wire_15} لفة")
            st.write(f"🔹 علب التثبيت: {total_points} قطعة")
        with res_col2:
            st.metric("سلك 2.5 مم", f"{calc_wire_25} لفة")
            st.write(f"🔹 علب التفريع: {rooms} قطعة")

        st.divider()
        st.subheader("💰 التقدير المالي")

        cost_df = pd.DataFrame([
            ("مقابس أرضي (L+N+T)",  f"{s_ground * p_socket_lnt:,} دج"),
            ("مقابس عادية (L+N)",   f"{s_normal * p_socket_ln:,} دج"),
            ("مصابيح SPOT",          f"{l_spot * p_lamp_spot:,} دج"),
            ("مصابيح عادية",         f"{l_normal * p_lamp_std:,} دج"),
            ("علب التفريع",          f"{rooms * p_jb:,} دج"),
            (f"لوحة توزيع",          f"{p_tableau:,} دج"),
        ], columns=["البند", "التكلفة"])
        st.dataframe(cost_df, use_container_width=True, hide_index=True)

        st.metric("💵 إجمالي تكلفة المواد", f"{total_cost:,} دج")

        st.divider()
        st.warning("⚠️ ملاحظة: هذا النموذج يعمل بتقنيات الذكاء الاصطناعي وهو في طور التجريب، لذا قد تحدث أخطاء في التقدير. يرجى المراجعة الميدانية.")

        st.markdown("""
        ---
        **المطوّر:** باهية إبراهيم  
        **التخصص:** ماستر هندسة كهربائية  
        **للتواصل وتطوير البيانات:** [0784178506](tel:0784178506)
        """)
