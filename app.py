def electricity_app_v2_pro():
    print("--- تطبيق حساب التكاليف والمواد (إصدار متطور) ---")
    
    # إعدادات الأسعار وتقدير المواد (سلك/متر لكل نقطة)
    p_lamp, p_socket, p_tab = 500, 500, 3000
    
    all_rooms = []
    try:
        num_areas = int(input("كم عدد الغرف أو المناطق؟ "))
    except: return print("خطأ في الإدخال")

    for i in range(num_areas):
        name = input(f"\nاسم المنطقة {i+1}: ")
        s, l = int(input(f"عدد المقابس: ")), int(input(f"عدد اللمبات: "))
        all_rooms.append({"name": name, "s": s, "l": l, "jb": 1})

    # الحسابات الإجمالية
    total_s = sum(r['s'] for r in all_rooms)
    total_l = sum(r['l'] for r in all_rooms)
    total_jb = sum(r['jb'] for r in all_rooms)
    
    # منطق حساب المواد (تنبؤ تقريبي بناءً على النقاط)
    wire_15_m = total_l * 8  # 8 أمتار لكل مصباح
    wire_25_m = total_s * 10 # 10 أمتار لكل مقبس
    
    labor_cost = (total_l * p_lamp) + (total_s * p_socket) + (total_jb * p_socket) + p_tab

    print("\n" + "="*40 + "\nملخص المخرجات:")
    print(f"إجمالي النقاط: {total_s} مقبس | {total_l} لمبة | {total_jb} علبة")
    print(f"حجم الطبلون: {num_areas + 4}P | يد عاملة: {labor_cost} دج")
    
    print("-" * 20 + " المواد اللازمة " + "-" * 20)
    print(f"- سلك 1.5 مم: {wire_15_m} متر (حوالي {round(wire_15_m/100, 1)} لفة)")
    print(f"- سلك 2.5 مم: {wire_25_m} متر (حوالي {round(wire_25_m/100, 1)} لفة)")
    print(f"- علب تثبيت (Pot): {total_s + total_l} علبة")
    print("="*40)

electricity_app_v2_pro()
