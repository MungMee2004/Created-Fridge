"""
fridge1.py  --  ตู้เย็นเครื่องที่ 1 (ของสด & เนื้อสัตว์)
รันเดี่ยวๆ ได้:  python fridge1.py
"""
from fridge_core import Item, FridgeConfig, d


def create_items():
    f = "ตู้เย็น 1"
    return [
        Item("ผักกาดหอม", "veg",   d(3),  "lettuce", 0, f),
        Item("ปลาทู",     "meat",  d(1),  "fish",    9, f),
        Item("นมสด",      "dairy", d(5),  "milk",    1, f),
        Item("มันฝรั่งทอด", "snack", d(60), "chips",  0, f),
        Item("ไก่สด",     "meat",  d(3),  "chicken", 5, f),
        Item("แอปเปิ้ล",   "fruit", d(12), "apple",   0, f),
    ]


FRIDGE = FridgeConfig(
    fid="1",
    title="ตู้เย็นเครื่องที่ 1",
    subtitle="ของสด & เนื้อสัตว์",
    accent="#2a9d8f",
    body_color="#e3f2ef",
    interior_color="#f6fffd",
    temp="4 °C",
    create_items=create_items,
)

if __name__ == "__main__":
    from fridge_ui import App
    App([FRIDGE]).mainloop()
