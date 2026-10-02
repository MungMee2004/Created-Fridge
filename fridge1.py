"""
fridge1.py  --  ตู้เย็นเครื่องที่ 1 (ของสด & เนื้อสัตว์)
รันเดี่ยวๆ ได้:  python fridge1.py
"""
from fridge_core import Item, FridgeConfig, d


# =====================================================================
# [แก้ไขตรงนี้ 1]  รายการวัตถุดิบในตู้เย็นเครื่องที่ 1   (ฟังก์ชัน create_items)
#
#   Item(ชื่อ, หมวด, วันเวลาหมดอายุ, ชื่อรูป, ความแรงกลิ่น 0-10, ชื่อตู้)
#   - หมวด: "meat" "veg" "dairy" "snack" "fruit"
#   - วันเวลาหมดอายุ: d(จำนวนวันจากนี้, ชั่วโมง, นาที)  เช่น d(3, 18, 30)
#       หรือระบุวันตายตัว: datetime(2026, 10, 15, 18, 0)  (ต้อง import datetime)
#   - ชื่อรูป: fish chicken steak egg milk lettuce carrot yogurt
#              chocolate chips apple cheese
#   - ตู้เก็บได้สูงสุด 9 ช่อง
# =====================================================================
def create_items():
    f = "ตู้เย็น 1"
    return [
        Item("ผักกาดหอม",   "veg",   d(3, 18, 0),   "lettuce", 0, f),
        Item("ปลาทู",       "meat",  d(1, 9, 30),   "fish",    9, f),
        Item("นมสด",        "dairy", d(5, 12, 0),   "milk",    1, f),
        Item("มันฝรั่งทอด", "snack", d(60, 23, 59), "chips",   0, f),
        Item("ไก่สด",       "meat",  d(3, 20, 15),  "chicken", 5, f),
        Item("แอปเปิ้ล",    "fruit", d(12, 8, 0),   "apple",   0, f),
    ]


# =====================================================================
# [แก้ไขตรงนี้ 2]  ชื่อ / สี / อุณหภูมิ ของตู้เย็นเครื่องที่ 1
# =====================================================================
FRIDGE = FridgeConfig(
    fid="1",
    title="ตู้เย็นเครื่องที่ 1",
    subtitle="ของสด & เนื้อสัตว์",
    accent="#2a9d8f",          # สีปุ่ม/ขอบตู้
    body_color="#e3f2ef",      # สีตัวตู้
    interior_color="#f6fffd",  # สีด้านในตู้
    temp="4 °C",
    create_items=create_items,
)

if __name__ == "__main__":
    from fridge_ui import App
    App([FRIDGE]).mainloop()
