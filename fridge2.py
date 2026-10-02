"""
fridge2.py  --  ตู้เย็นเครื่องที่ 2 (นม ไข่ ผัก & ขนม)
รันเดี่ยวๆ ได้:  python fridge2.py
"""
from fridge_core import Item, FridgeConfig, d


# =====================================================================
# [แก้ไขตรงนี้ 1]  รายการวัตถุดิบในตู้เย็นเครื่องที่ 2   (ฟังก์ชัน create_items)
#   รูปแบบการเขียนเหมือน fridge1.py (ดูคำอธิบายในไฟล์นั้น)
# =====================================================================
def create_items():
    f = "ตู้เย็น 2"
    return [
        Item("ช็อกโกแลต", "snack", d(90, 23, 59), "chocolate", 0, f),
        Item("เนื้อวัว",   "meat",  d(2, 7, 45),   "steak",     6, f),
        Item("โยเกิร์ต",  "dairy", d(7, 10, 0),   "yogurt",    0, f),
        Item("แครอท",     "veg",   d(10, 17, 30), "carrot",    0, f),
        Item("ไข่ไก่",     "dairy", d(14, 12, 0),  "egg",       0, f),
        Item("ชีส",       "dairy", d(4, 21, 0),   "cheese",    1, f),
    ]


# =====================================================================
# [แก้ไขตรงนี้ 2]  ชื่อ / สี / อุณหภูมิ ของตู้เย็นเครื่องที่ 2
# =====================================================================
FRIDGE = FridgeConfig(
    fid="2",
    title="ตู้เย็นเครื่องที่ 2",
    subtitle="นม ไข่ ผัก & ขนม",
    accent="#e07a5f",
    body_color="#fbece6",
    interior_color="#fffaf7",
    temp="5 °C",
    create_items=create_items,
)

if __name__ == "__main__":
    from fridge_ui import App
    App([FRIDGE]).mainloop()
