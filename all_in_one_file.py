"""
Fridge Inventory Manager - ระบบจัดการตู้เย็นและวันหมดอายุ  (ไฟล์เดียวจบ)

ติดตั้ง:   pip install customtkinter pillow
รัน:
    python fridge_manager.py        # ตู้เย็นทั้ง 2 เครื่องในหน้าต่างเดียว
    python fridge_manager.py 1      # ตู้เย็นเครื่องที่ 1 อย่างเดียว
    python fridge_manager.py 2      # ตู้เย็นเครื่องที่ 2 อย่างเดียว

โครงสร้างในไฟล์ (ค้นหาด้วยหัวข้อด้านล่างได้เลย):
    1) รูปไอคอนอาหาร            (วาดด้วย Pillow)
    2) ข้อมูลกลาง + อัลกอริทึม    (Bubble / Insertion / Selection / Merge sort,
                                  Sequential / Binary search, วันเวลา)
    3) ตู้เย็นเครื่องที่ 1 และ 2  (ข้อมูลของแต่ละตู้ แยกกัน)
    4) หน้าต่าง CustomTkinter    (ชั้นวาง การ์ด ปุ่มต่างๆ นาฬิกา)
    5) ส่วนเริ่มโปรแกรม
"""
import sys
import tkinter.font as tkfont
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, List

import customtkinter as ctk
from PIL import Image, ImageDraw


# ====================================================================
# 1) รูปไอคอนอาหาร (ไม่มีหมู) - วาดด้วย Pillow ไม่ต้องใช้ไฟล์รูป
# ====================================================================

S = 400  # ขนาดผืนผ้าใบตอนวาด (จะย่อลงให้เนียน)

ICON_LABELS = {
    "fish": "ปลา", "chicken": "ไก่", "steak": "เนื้อ",
    "egg": "ไข่", "milk": "นม", "lettuce": "ผักกาดหอม",
    "carrot": "แครอท", "yogurt": "โยเกิร์ต", "chocolate": "ช็อกโกแลต",
    "chips": "มันฝรั่งทอด", "apple": "แอปเปิ้ล", "cheese": "ชีส",
}


def _fish(d):
    d.polygon([(290, 200), (370, 130), (370, 270)], fill=(70, 130, 180))
    d.polygon([(150, 140), (210, 80), (250, 150)], fill=(60, 110, 160))
    d.ellipse((50, 130, 320, 270), fill=(110, 170, 215))
    d.pieslice((50, 130, 320, 270), 20, 160, fill=(190, 220, 240))
    for x in (170, 205, 240):
        d.arc((x - 30, 150, x + 30, 250), 280, 80, fill=(60, 110, 160), width=7)
    d.ellipse((95, 175, 125, 205), fill="white")
    d.ellipse((104, 183, 120, 199), fill=(20, 20, 30))


def _chicken(d):
    d.line([(150, 230), (80, 320)], fill=(250, 240, 220), width=34)
    d.ellipse((50, 295, 95, 340), fill=(250, 240, 220))
    d.ellipse((78, 310, 123, 355), fill=(250, 240, 220))
    d.ellipse((110, 50, 340, 260), fill=(205, 115, 45))
    d.ellipse((135, 70, 280, 190), fill=(225, 145, 70))
    d.ellipse((160, 85, 220, 125), fill=(245, 190, 120))


def _steak(d):
    d.ellipse((45, 90, 355, 315), fill=(235, 215, 205))
    d.ellipse((65, 105, 335, 300), fill=(150, 40, 45))
    d.ellipse((95, 125, 305, 280), fill=(205, 75, 80))
    for a in [(130, 170, 210, 185), (200, 215, 285, 232), (150, 235, 215, 248)]:
        d.rounded_rectangle(a, 8, fill=(240, 200, 200))
    d.ellipse((235, 150, 290, 205), fill=(250, 240, 220))
    d.ellipse((250, 165, 275, 190), fill=(205, 75, 80))


def _egg(d):
    d.ellipse((100, 60, 300, 340), fill=(240, 225, 195))
    d.ellipse((110, 70, 290, 330), fill=(255, 246, 228))
    d.ellipse((140, 110, 185, 190), fill=(255, 255, 255))


def _milk(d):
    d.polygon([(115, 140), (165, 60), (245, 60), (285, 140)], fill=(60, 120, 200))
    d.rectangle((115, 140, 285, 350), fill=(245, 248, 252))
    d.rectangle((115, 140, 150, 350), fill=(225, 232, 242))
    d.rectangle((115, 135, 285, 155), fill=(60, 120, 200))
    d.rounded_rectangle((140, 190, 260, 300), 18, fill=(90, 160, 230))
    d.polygon([(200, 205), (170, 260), (230, 260)], fill="white")
    d.ellipse((170, 235, 230, 285), fill="white")


def _lettuce(d):
    d.ellipse((50, 80, 350, 340), fill=(70, 150, 60))
    d.ellipse((80, 70, 320, 300), fill=(105, 185, 80))
    d.ellipse((120, 100, 280, 260), fill=(150, 215, 110))
    d.ellipse((160, 130, 240, 220), fill=(200, 240, 160))
    for ang in [(200, 300, 200, 150), (200, 300, 120, 170), (200, 300, 280, 170)]:
        d.line(ang, fill=(70, 150, 60), width=6)


def _carrot(d):
    for box in [(120, 20, 175, 120), (165, 10, 225, 105), (205, 40, 265, 130)]:
        d.ellipse(box, fill=(70, 160, 70))
    d.polygon([(95, 120), (230, 90), (310, 340)], fill=(240, 130, 30))
    d.polygon([(95, 120), (230, 90), (205, 170)], fill=(255, 165, 70))
    for a in [(150, 150, 190, 160), (185, 200, 225, 210), (215, 250, 250, 260)]:
        d.line(a, fill=(200, 95, 15), width=8)


def _yogurt(d):
    d.polygon([(95, 140), (305, 140), (275, 345), (125, 345)], fill=(250, 250, 255))
    d.polygon([(103, 195), (297, 195), (290, 280), (112, 280)], fill=(240, 120, 150))
    d.rounded_rectangle((85, 110, 315, 145), 10, fill=(150, 120, 220))
    d.ellipse((175, 205, 225, 265), fill=(220, 50, 70))
    d.polygon([(190, 205), (210, 205), (200, 192)], fill=(70, 160, 70))


def _chocolate(d):
    d.rounded_rectangle((80, 80, 320, 330), 16, fill=(110, 65, 40))
    for i in range(1, 3):
        d.line([(80 + 80 * i, 80), (80 + 80 * i, 235)], fill=(80, 45, 28), width=6)
    for j in range(1, 3):
        d.line([(80, 80 + 52 * j), (320, 80 + 52 * j)], fill=(80, 45, 28), width=6)
    d.rounded_rectangle((70, 230, 330, 335), 16, fill=(215, 45, 55))
    d.rectangle((70, 258, 330, 285), fill=(250, 210, 70))


def _chips(d):
    d.polygon([(95, 70), (305, 70), (325, 340), (75, 340)], fill=(235, 70, 55))
    d.rectangle((95, 60, 305, 95), fill=(250, 200, 60))
    for x in range(95, 305, 22):
        d.polygon([(x, 60), (x + 11, 40), (x + 22, 60)], fill=(250, 200, 60))
    d.ellipse((135, 150, 265, 280), fill=(255, 215, 80))
    d.ellipse((160, 185, 240, 245), fill=(240, 140, 50))


def _apple(d):
    d.ellipse((60, 100, 235, 340), fill=(215, 45, 50))
    d.ellipse((165, 100, 340, 340), fill=(215, 45, 50))
    d.ellipse((90, 130, 150, 220), fill=(240, 100, 95))
    d.line([(200, 120), (215, 50)], fill=(110, 70, 40), width=14)
    d.polygon([(215, 80), (290, 40), (275, 110)], fill=(80, 170, 70))


def _cheese(d):
    d.polygon([(55, 255), (330, 160), (345, 195), (70, 300)], fill=(255, 225, 120))
    d.polygon([(70, 300), (345, 195), (345, 310), (70, 330)], fill=(245, 190, 40))
    d.polygon([(55, 255), (70, 300), (70, 330), (55, 300)], fill=(225, 165, 30))
    for c in [(130, 270, 30), (220, 240, 24), (290, 235, 18)]:
        d.ellipse((c[0] - c[2], c[1] - c[2], c[0] + c[2], c[1] + c[2]), fill=(225, 165, 30))
    d.ellipse((170, 295, 210, 325), fill=(225, 165, 30))


_DRAWERS = {
    "fish": _fish, "chicken": _chicken, "steak": _steak, "egg": _egg,
    "milk": _milk, "lettuce": _lettuce, "carrot": _carrot, "yogurt": _yogurt,
    "chocolate": _chocolate, "chips": _chips, "apple": _apple, "cheese": _cheese,
}


def make_icon(kind, size=128):
    """คืนค่า PIL.Image (RGBA) ของไอคอนตามชื่อ kind"""
    big = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    _DRAWERS.get(kind, _apple)(ImageDraw.Draw(big))
    return big.resize((size, size), Image.LANCZOS)


# ====================================================================
# 2) ข้อมูลกลาง + อัลกอริทึม (Sorting / Searching) + วันเวลา
# ====================================================================

CATEGORY_TH = {"meat": "เนื้อสัตว์", "veg": "ผัก", "dairy": "นม/ไข่",
               "snack": "ขนม", "fruit": "ผลไม้"}

# =====================================================================
# [แก้ไขตรงนี้ A]  การตั้งค่าการแสดงวันที่
# =====================================================================
BUDDHIST_ERA = True      # True = แสดงปี พ.ศ. (2569) / False = แสดงปี ค.ศ. (2026)

THAI_MONTHS_SHORT = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
                     "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
THAI_MONTHS_FULL = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
THAI_WEEKDAYS = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]


# =====================================================================
# [แก้ไขตรงนี้ B]  แหล่งอ้างอิงเวลาปัจจุบัน
#   ทุกอย่าง (เวลาที่เหลือ, สีป้าย, นาฬิกา) คำนวณจากฟังก์ชัน now() นี้
#   ปกติอ่านจากนาฬิกาเครื่อง จึงเปลี่ยนเองอัตโนมัติทุกวินาที
#   (ถ้าอยากจำลองวันอื่นเพื่อทดสอบ ให้แก้ให้คืน datetime(2026, 10, 20, 8, 0))
# =====================================================================
def now() -> datetime:
    return datetime.now()


def d(days: int, hour: int = 23, minute: int = 59) -> datetime:
    """วัน-เวลาที่อีก days วันนับจากวันนี้ (ที่ชั่วโมง:นาที ที่กำหนด)
    ตัวอย่าง d(3, 18, 30) = อีก 3 วัน เวลา 18:30"""
    t = now() + timedelta(days=days)
    return t.replace(hour=hour, minute=minute, second=0, microsecond=0)


def _year(dt: datetime) -> int:
    return dt.year + 543 if BUDDHIST_ERA else dt.year


def fmt_dt(dt: datetime) -> str:
    """เช่น 9 ต.ค. 2569 18:30"""
    return f"{dt.day} {THAI_MONTHS_SHORT[dt.month - 1]} {_year(dt)} {dt:%H:%M}"


def fmt_now() -> str:
    """เช่น วันศุกร์ที่ 2 ตุลาคม 2569  เวลา 14:23:05"""
    t = now()
    return (f"วัน{THAI_WEEKDAYS[t.weekday()]}ที่ {t.day} {THAI_MONTHS_FULL[t.month - 1]} "
            f"{_year(t)}  เวลา {t:%H:%M:%S}")


def seconds_left(expiry: datetime) -> int:
    return int((expiry - now()).total_seconds())


def countdown_text(expiry: datetime) -> str:
    """ข้อความเวลาที่เหลือ/เลยกำหนด คำนวณจากเวลาปัจจุบันทุกครั้งที่เรียก"""
    secs = seconds_left(expiry)
    expired = secs < 0
    days, rem = divmod(abs(secs), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    if days:
        body = f"{days} วัน {hours} ชม."
    elif hours:
        body = f"{hours} ชม. {minutes} น."
    else:
        body = f"{minutes} น. {seconds} วิ"
    return ("หมดอายุแล้ว " if expired else "เหลือ ") + body


@dataclass
class Item:
    name: str
    category: str          # meat / veg / dairy / snack / fruit
    expiry: datetime       # วัน-เวลาหมดอายุ
    icon: str              # ชื่อไอคอน (ดู ICON_LABELS)
    smell: int = 0         # ความแรงของกลิ่น 0-10 (ใช้กับเนื้อสัตว์)
    fridge: str = ""       # ชื่อตู้เย็นที่เก็บอยู่

    def days_left(self) -> int:
        return (self.expiry - now()).days


@dataclass
class FridgeConfig:
    """ค่าตั้งต้นของตู้เย็น 1 เครื่อง (แต่ละเครื่องเขียนแยกไฟล์กัน)"""
    fid: str
    title: str
    subtitle: str
    accent: str            # สีขอบ/ปุ่มของตู้
    body_color: str        # สีตัวตู้
    interior_color: str    # สีภายในตู้
    temp: str
    create_items: Callable[[], List[Item]] = field(repr=False, default=lambda: [])


# ---------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------
def bubble_sort_by_expiry(items):
    """Bubble sort: ของใกล้หมดอายุขยับมาอยู่หน้าสุด"""
    data = items[:]
    n = len(data)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if data[j].expiry > data[j + 1].expiry:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data


def is_sorted_by_expiry(items):
    return all(items[i].expiry <= items[i + 1].expiry for i in range(len(items) - 1))


def insertion_sort_insert(sorted_list, new_item):
    """Insertion sort: แทรกของใหม่ลงรายการที่เรียงตามวันหมดอายุอยู่แล้ว
    คืนค่า (รายการใหม่, ตำแหน่งที่แทรก)"""
    data = sorted_list[:] + [new_item]
    i = len(data) - 1
    while i > 0 and data[i - 1].expiry > data[i].expiry:
        data[i - 1], data[i] = data[i], data[i - 1]
        i -= 1
    return data, i


def insertion_sort_all(items):
    result = []
    for it in items:
        result, _ = insertion_sort_insert(result, it)
    return result


def selection_sort_by_smell(items):
    """Selection sort: เรียงกลิ่นน้อย -> มาก (ตัวสุดท้ายกลิ่นแรงที่สุด)"""
    data = items[:]
    n = len(data)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if data[j].smell < data[m].smell:
                m = j
        if m != i:
            data[i], data[m] = data[m], data[i]
    return data


def merge_sort(items, key=lambda x: x.expiry):
    """Merge sort: แบ่งครึ่งแล้วรวมกลับตาม key"""
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left, right = merge_sort(items[:mid], key), merge_sort(items[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def merge_fridges(*fridges):
    """รวมรายการจากหลายตู้เย็นเป็นรายการเดียว เรียงตามวันหมดอายุ"""
    combined = []
    for f in fridges:
        combined.extend(f)
    return merge_sort(combined)


# ---------------------------------------------------------------
# Searching
# ---------------------------------------------------------------
def sequential_search_snack(slots):
    """Sequential search: ไล่เปิดทีละช่อง (slots อาจมี None = ช่องว่าง)
    คืนค่า (index ที่เจอ หรือ -1, จำนวนช่องที่เปิดดู)"""
    for i, it in enumerate(slots):
        if it is not None and it.category == "snack":
            return i, i + 1
    return -1, len(slots)


def binary_search_by_name(sorted_items, target):
    """Binary search: sorted_items ต้องเรียงตามชื่อแล้ว
    คืนค่า (index หรือ -1, จำนวนรอบที่เทียบ)"""
    low, high, steps = 0, len(sorted_items) - 1, 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        name = sorted_items[mid].name
        if name == target:
            return mid, steps
        if name < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps


# ====================================================================
# 3) ตู้เย็นเครื่องที่ 1 (ของสด & เนื้อสัตว์)
# ====================================================================

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
def create_items_1():
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
FRIDGE_1 = FridgeConfig(
    fid="1",
    title="ตู้เย็นเครื่องที่ 1",
    subtitle="ของสด & เนื้อสัตว์",
    accent="#2a9d8f",          # สีปุ่ม/ขอบตู้
    body_color="#e3f2ef",      # สีตัวตู้
    interior_color="#f6fffd",  # สีด้านในตู้
    temp="4 °C",
    create_items=create_items_1,
)


# ====================================================================
# 3) ตู้เย็นเครื่องที่ 2 (นม ไข่ ผัก & ขนม)
# ====================================================================

# =====================================================================
# [แก้ไขตรงนี้ 1]  รายการวัตถุดิบในตู้เย็นเครื่องที่ 2   (ฟังก์ชัน create_items)
#   รูปแบบการเขียนเหมือน fridge1.py (ดูคำอธิบายในไฟล์นั้น)
# =====================================================================
def create_items_2():
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
FRIDGE_2 = FridgeConfig(
    fid="2",
    title="ตู้เย็นเครื่องที่ 2",
    subtitle="นม ไข่ ผัก & ขนม",
    accent="#e07a5f",
    body_color="#fbece6",
    interior_color="#fffaf7",
    temp="5 °C",
    create_items=create_items_2,
)


# ====================================================================
# 4) หน้าต่าง CustomTkinter (ใช้ร่วมกันทั้ง 2 ตู้)
# ====================================================================

SHELVES, SLOTS = 3, 3
N = SHELVES * SLOTS
CARD_W, CARD_H = 140, 172

FONT = "Tahoma"
_ICON_CACHE = {}


# ---------------------------------------------------------------- helpers
def F(size, bold=False):
    return ctk.CTkFont(family=FONT, size=size, weight="bold" if bold else "normal")


def pick_font(root):
    """เลือกฟอนต์ที่รองรับภาษาไทยและมีในเครื่อง"""
    global FONT
    families = set(tkfont.families(root))
    for name in ("Leelawadee UI", "Tahoma", "Thonburi", "Noto Sans Thai",
                 "Sarabun", "Arial"):
        if name in families:
            FONT = name
            return


def icon(kind, size):
    key = (kind, size)
    if key not in _ICON_CACHE:
        img = make_icon(kind, size * 2)           # วาดใหญ่ 2 เท่าให้คมบนจอ HiDPI
        _ICON_CACHE[key] = ctk.CTkImage(light_image=img, dark_image=img,
                                        size=(size, size))
    return _ICON_CACHE[key]


def darken(hex_color, factor=0.82):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * factor), int(g * factor), int(b * factor))


# =====================================================================
# [แก้ไขตรงนี้ C]  เกณฑ์สีของป้ายวันหมดอายุ (คำนวณจากเวลาปัจจุบัน ณ ขณะนั้น)
#   เปลี่ยนจำนวนวัน 3 และ 7 ได้ตามต้องการ
# =====================================================================
def expiry_style(item):
    """คืนค่า (สีป้าย, ข้อความเวลาที่เหลือ) ของวัตถุดิบ"""
    secs = seconds_left(item.expiry)
    text = countdown_text(item.expiry)
    if secs < 0:
        return "#8b1e1e", text
    if secs <= 3 * 86400:
        return "#e03131", text
    if secs <= 7 * 86400:
        return "#f08c00", text
    return "#2f9e44", text


# ---------------------------------------------------------------- dialog
class AddItemDialog(ctk.CTkToplevel):
    """หน้าต่างเพิ่มของใหม่เข้าตู้เย็น"""

    def __init__(self, master, cfg: FridgeConfig, on_submit):
        super().__init__(master)
        self.cfg, self.on_submit = cfg, on_submit
        self.title(f"เพิ่มของใหม่ - {cfg.title}")
        self.geometry("380x520")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="เพิ่มของที่เพิ่งซื้อมา", font=F(20, True)
                     ).pack(pady=(18, 8))
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="x", padx=28)

        ctk.CTkLabel(body, text="ชื่อวัตถุดิบ", font=F(13), anchor="w").pack(fill="x")
        self.name = ctk.CTkEntry(body, font=F(14), placeholder_text="เช่น ปลาแซลมอน")
        self.name.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(body, text="หมวดหมู่", font=F(13), anchor="w").pack(fill="x")
        self.cat = ctk.CTkOptionMenu(body, values=list(CATEGORY_TH.values()),
                                     font=F(13), dropdown_font=F(13),
                                     fg_color=cfg.accent,
                                     button_color=darken(cfg.accent))
        self.cat.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(body, text="หมดอายุในอีกกี่วัน  /  เวลา (ชม.:นาที)", font=F(13),
                     anchor="w").pack(fill="x")
        row_exp = ctk.CTkFrame(body, fg_color="transparent")
        row_exp.pack(fill="x", pady=(2, 10))
        self.days = ctk.CTkEntry(row_exp, font=F(14), width=120)
        self.days.insert(0, "7")
        self.days.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.time = ctk.CTkEntry(row_exp, font=F(14), width=120)
        self.time.insert(0, "18:00")
        self.time.pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.smell_label = ctk.CTkLabel(body, text="ความแรงของกลิ่น (เนื้อสัตว์): 5",
                                        font=F(13), anchor="w")
        self.smell_label.pack(fill="x")
        self.smell = ctk.CTkSlider(body, from_=0, to=10, number_of_steps=10,
                                   command=self._on_smell, button_color=cfg.accent,
                                   progress_color=cfg.accent)
        self.smell.set(5)
        self.smell.pack(fill="x", pady=(4, 10))

        ctk.CTkLabel(body, text="รูปที่ใช้แสดง", font=F(13), anchor="w").pack(fill="x")
        self.icon = ctk.CTkOptionMenu(body, values=list(ICON_LABELS.values()),
                                      font=F(13), dropdown_font=F(13),
                                      fg_color=cfg.accent,
                                      button_color=darken(cfg.accent))
        self.icon.pack(fill="x", pady=(2, 10))

        self.error = ctk.CTkLabel(body, text="", text_color="#ff6b6b", font=F(12))
        self.error.pack()
        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", pady=6)
        ctk.CTkButton(row, text="ยกเลิก", font=F(14), fg_color="#4b5563",
                      hover_color="#374151", command=self.destroy
                      ).pack(side="left", expand=True, padx=(0, 6), fill="x")
        ctk.CTkButton(row, text="เพิ่มเข้าตู้เย็น", font=F(14, True),
                      fg_color=cfg.accent, hover_color=darken(cfg.accent),
                      command=self._submit).pack(side="left", expand=True,
                                                 padx=(6, 0), fill="x")
        self.after(150, self._focus)

    def _focus(self):
        try:
            self.lift()
            self.focus_force()
            self.grab_set()
        except Exception:
            pass

    def _on_smell(self, value):
        self.smell_label.configure(text=f"ความแรงของกลิ่น (เนื้อสัตว์): {int(value)}")

    def _submit(self):
        name = self.name.get().strip()
        if not name:
            self.error.configure(text="กรุณาใส่ชื่อวัตถุดิบ")
            return
        try:
            days = int(self.days.get())
        except ValueError:
            self.error.configure(text="จำนวนวันต้องเป็นตัวเลขจำนวนเต็ม")
            return
        try:
            hh, mm = (int(x) for x in self.time.get().strip().split(":"))
            expiry = d(days, hh, mm)
        except ValueError:
            self.error.configure(text="เวลาต้องเป็นรูปแบบ ชม.:นาที เช่น 18:30")
            return
        cat = {v: k for k, v in CATEGORY_TH.items()}[self.cat.get()]
        kind = {v: k for k, v in ICON_LABELS.items()}[self.icon.get()]
        item = Item(name, cat, expiry, kind,
                    int(self.smell.get()) if cat == "meat" else 0,
                    f"ตู้เย็น {self.cfg.fid}")
        self.on_submit(item)
        self.destroy()


# ---------------------------------------------------------------- panel
class FridgePanel(ctk.CTkFrame):
    """ตู้เย็น 1 เครื่อง (ตัวตู้ + ชั้นวาง 3 ชั้น + ปุ่มอัลกอริทึม)"""

    def __init__(self, master, cfg: FridgeConfig):
        super().__init__(master, corner_radius=36, fg_color=cfg.body_color,
                         border_width=4, border_color=cfg.accent)
        self.cfg = cfg
        self.slots = [None] * N                    # index 0 = ชั้นบนสุดช่องซ้าย
        for i, it in enumerate(cfg.create_items()[:N]):
            self.slots[i] = it
        self._widgets, self._flash_job = [], None
        self._undo = None                          # (วัตถุดิบ, ช่องเดิม) ที่เพิ่งนำออก
        self._pills = []                           # (วัตถุดิบ, ป้ายเวลาที่เหลือ)
        self.selected = None                       # วัตถุดิบที่คลิกเลือกไว้
        self._build()
        self.render()

    # ---------- สร้างหน้าตา
    def _build(self):
        cfg = self.cfg
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=22, pady=(16, 6))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text=cfg.title, font=F(24, True), text_color="#1f2937",
                     anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text=cfg.subtitle, font=F(13), text_color="#4b5563",
                     anchor="w").grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(header, text=f"  {cfg.temp}  ", font=F(15, True),
                     text_color="white", fg_color=cfg.accent, corner_radius=14,
                     height=30).grid(row=0, column=1, rowspan=2, sticky="e")

        # มือจับตู้เย็น
        ctk.CTkFrame(self, width=10, height=150, corner_radius=5,
                     fg_color=cfg.accent).grid(row=1, column=0, padx=(14, 0), sticky="w")

        interior = ctk.CTkFrame(self, fg_color=cfg.interior_color, corner_radius=22)
        interior.grid(row=1, column=1, sticky="nsew", padx=(8, 18), pady=(0, 8))
        interior.grid_columnconfigure(1, weight=1)
        self.shelf_frames = []
        for s in range(SHELVES):
            ctk.CTkLabel(interior, text=str(s + 1), width=26, height=26,
                         corner_radius=13, fg_color=cfg.accent, text_color="white",
                         font=F(13, True)).grid(row=2 * s, column=0, padx=(10, 0))
            row = ctk.CTkFrame(interior, fg_color="transparent")
            row.grid(row=2 * s, column=1, sticky="ew", padx=(4, 10), pady=(10, 0))
            for c in range(SLOTS):
                row.grid_columnconfigure(c, weight=1, uniform="slot")
            self.shelf_frames.append(row)
            ctk.CTkFrame(interior, height=8, corner_radius=4, fg_color="#b5c4cb"
                         ).grid(row=2 * s + 1, column=0, columnspan=2, sticky="ew",
                                padx=10, pady=(0, 2))
        ctk.CTkLabel(interior, text="ชั้น 1 = บนสุด  |  ชั้น 3 = ล่างสุด",
                     font=F(11), text_color="#7b8a92"
                     ).grid(row=2 * SHELVES, column=0, columnspan=2, pady=(2, 8))

        # ปุ่มอัลกอริทึม
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 4))
        bar.grid_columnconfigure((0, 1, 2), weight=1, uniform="b")

        def btn(text, cmd, col, row=0):
            b = ctk.CTkButton(bar, text=text, command=cmd, font=F(12, True), height=46,
                              corner_radius=14, fg_color=cfg.accent,
                              hover_color=darken(cfg.accent))
            b.grid(row=row, column=col, padx=4, pady=3, sticky="ew")
            return b

        btn("เรียงวันหมดอายุ\n(Bubble sort)", self.action_bubble, 0)
        btn("เพิ่มของใหม่\n(Insertion sort)", self.action_add, 1)
        btn("เนื้อสัตว์ไว้ล่างสุด\n(Selection sort)", self.action_selection, 2)
        btn("หาขนม\n(Sequential search)", self.action_sequential, 0, 1)
        self.entry = ctk.CTkEntry(bar, placeholder_text="ชื่อวัตถุดิบที่จะหา",
                                  font=F(13), height=46, corner_radius=14)
        self.entry.grid(row=1, column=1, padx=4, pady=3, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.action_binary())
        btn("ค้นหาชื่อ\n(Binary search)", self.action_binary, 2, 1)
        rm = btn("นำวัตถุดิบออกจากตู้  (คลิกการ์ดเพื่อเลือกก่อน)", self.action_remove, 0, 2)
        rm.configure(fg_color="#c92a2a", hover_color="#a61e1e", height=38)
        rm.grid_configure(columnspan=3)

        self.status = ctk.CTkLabel(self, text="พร้อมใช้งาน - กดปุ่ม × สีแดงที่มุมการ์ดเพื่อนำของออกจากตู้",
                                   font=F(13), text_color="#374151", anchor="w",
                                   justify="left", wraplength=470, height=44)
        self.status.grid(row=3, column=0, columnspan=2, sticky="ew", padx=22, pady=(2, 12))
        self.undo_btn = ctk.CTkButton(self, text="เลิกทำ - นำของกลับเข้าตู้", font=F(13, True),
                                      height=34, corner_radius=12, fg_color="#4b5563",
                                      hover_color="#374151", command=self.undo_remove)
        self.undo_btn.grid(row=4, column=0, columnspan=2, padx=22, pady=(0, 14))
        self.undo_btn.grid_remove()

    # ---------- วาดของในตู้
    def render(self, highlight=None):
        highlight = highlight or set()
        for w in self._widgets:
            w.destroy()
        self._widgets, self._pills = [], []
        for idx in range(N):
            shelf, col = divmod(idx, SLOTS)
            it = self.slots[idx]
            if it is not None and id(it) in highlight:
                border, bcolor = 4, "#ffb703"          # เหลือง = ผลการค้นหา/จัดเรียง
            elif it is not None and it is self.selected:
                border, bcolor = 4, "#3b82f6"          # น้ำเงิน = คลิกเลือกไว้
            else:
                border, bcolor = 0, "#ffb703"
            slot = ctk.CTkFrame(self.shelf_frames[shelf], width=CARD_W, height=CARD_H,
                                corner_radius=16, fg_color="white" if it else "#e4eef2",
                                border_width=border, border_color=bcolor)
            slot.grid(row=0, column=col, padx=4, pady=(0, 4))
            slot.pack_propagate(False)
            self._widgets.append(slot)
            if it is None:
                ctk.CTkLabel(slot, text="ว่าง", font=F(13), text_color="#9db0b8"
                             ).pack(expand=True)
                continue
            color, text = expiry_style(it)
            meta = f"กลิ่น {it.smell}/10" if it.category == "meat" else CATEGORY_TH[it.category]
            parts = [
                ctk.CTkLabel(slot, text="", image=icon(it.icon, 52)),
                ctk.CTkLabel(slot, text=it.name, font=F(15, True), text_color="#1f2937"),
                ctk.CTkLabel(slot, text=meta, font=F(11), text_color="#6b7280"),
                ctk.CTkLabel(slot, text=fmt_dt(it.expiry), font=F(11), text_color="#374151"),
            ]
            parts[0].pack(pady=(8, 0))
            for lbl in parts[1:]:
                lbl.pack()
            pill = ctk.CTkLabel(slot, text=text, font=F(11, True), text_color="white",
                                fg_color=color, corner_radius=10, height=22)
            pill.pack(pady=(4, 0), padx=8)
            self._pills.append((it, pill))
            for w in [slot] + parts + [pill]:          # คลิกที่ไหนในการ์ดก็เลือกได้
                w.bind("<Button-1>", lambda e, i=idx: self._select(i))
            # ปุ่ม × มุมขวาบนของการ์ด: กดแล้วนำวัตถุดิบนี้ออกทันที (มีปุ่มเลิกทำ)
            ctk.CTkButton(slot, text="×", width=26, height=26, corner_radius=13,
                          font=F(17, True), fg_color="#e03131", hover_color="#a61e1e",
                          text_color="white", command=lambda x=it: self.remove_item(x)
                          ).place(relx=1.0, x=-5, y=5, anchor="ne")

    def refresh_countdowns(self):
        """อัปเดตป้ายเวลาที่เหลือตามนาฬิกาปัจจุบัน (เรียกทุกวินาทีจาก App)"""
        for it, pill in self._pills:
            color, text = expiry_style(it)
            pill.configure(text=text, fg_color=color)

    def _select(self, idx):
        it = self.slots[idx]
        self.selected = None if (it is None or it is self.selected) else it
        if self.selected is not None:
            self.say(f"เลือก '{it.name}' แล้ว - กดปุ่ม × ที่มุมการ์ด หรือปุ่มแดงด้านล่างเพื่อนำออก")
        self.after(1, self.render)

    def flash(self, ids):
        """ไฮไลต์การ์ดด้วยกรอบสีเหลือง 2.5 วินาที"""
        if self._flash_job:
            try:
                self.after_cancel(self._flash_job)
            except Exception:
                pass
        self.render(highlight=set(ids))
        self._flash_job = self.after(2500, self.render)

    def say(self, message):
        self.status.configure(text=message)

    # ---------- เครื่องมือช่วย
    def get_items(self):
        return [x for x in self.slots if x is not None]

    def _slot_of(self, item):
        return next(i for i, x in enumerate(self.slots) if x is item)

    @staticmethod
    def _pos_text(idx):
        shelf, col = divmod(idx, SLOTS)
        return f"ชั้น {shelf + 1} ช่อง {col + 1}"

    # ---------- 1.1 Bubble sort
    def action_bubble(self):
        pos = [i for i, x in enumerate(self.slots) if x and x.category != "meat"]
        if not pos:
            self.say("ไม่มีของนอกจากเนื้อสัตว์ให้เรียง")
            return
        ordered = bubble_sort_by_expiry([self.slots[i] for i in pos])
        for i, it in zip(pos, ordered):
            self.slots[i] = it
        self.flash({id(ordered[0])})
        self.say(f"Bubble sort: เรียงตามวันหมดอายุแล้ว  ใกล้หมดอายุที่สุดคือ "
                 f"'{ordered[0].name}' ขยับมาอยู่หน้าสุด ({self._pos_text(pos[0])})")

    # ---------- 1.2 Insertion sort
    def action_add(self):
        AddItemDialog(self.winfo_toplevel(), self.cfg, self.add_item)

    def add_item(self, item):
        empties = [i for i, x in enumerate(self.slots) if x is None]
        if not empties:
            self.say("ตู้เย็นเต็มแล้ว (9 ช่อง) - ไม่สามารถเพิ่มของได้")
            return
        if item.category == "meat":                 # เนื้อสัตว์ลงช่องว่างล่างสุดก่อน
            self.slots[empties[-1]] = item
            self._compose_meat_bottom()
            self.flash({id(item)})
            self.say(f"Insertion + Selection: เพิ่ม '{item.name}' แล้วจัดเนื้อสัตว์ตามกลิ่น "
                     f"-> อยู่ที่ {self._pos_text(self._slot_of(item))}")
            return
        e = empties[0]                              # ของทั่วไปลงช่องว่างบนสุด
        pos = sorted([i for i, x in enumerate(self.slots)
                      if x and x.category != "meat"] + [e])
        current = [self.slots[i] for i in pos if i != e]
        if is_sorted_by_expiry(current):            # ชั้นเรียงอยู่แล้ว -> แทรกเข้าไปตรงๆ
            ordered, at = insertion_sort_insert(current, item)
        else:
            ordered = insertion_sort_all(current + [item])
            at = next(i for i, x in enumerate(ordered) if x is item)
        for i, it in zip(pos, ordered):
            self.slots[i] = it
        self.flash({id(item)})
        self.say(f"Insertion sort: แทรก '{item.name}' ({countdown_text(item.expiry)}) "
                 f"ลำดับที่ {at + 1} ของชั้นวาง -> {self._pos_text(self._slot_of(item))}")

    # ---------- 1.3 Selection sort
    def _compose_meat_bottom(self):
        meats = selection_sort_by_smell([x for x in self.slots if x and x.category == "meat"])
        others = [x for x in self.slots if x and x.category != "meat"]
        new = [None] * N
        for i, it in enumerate(others):
            new[i] = it
        for k, it in enumerate(reversed(meats)):    # กลิ่นแรงสุดไปท้ายสุด = ล่างสุด
            new[N - 1 - k] = it
        self.slots = new
        return meats

    def action_selection(self):
        meats = self._compose_meat_bottom()
        if not meats:
            self.say("ไม่มีเนื้อสัตว์ในตู้เย็นนี้")
            return
        strongest = meats[-1]
        self.flash({id(strongest)})
        self.say(f"Selection sort: ย้ายเนื้อสัตว์ลงล่างสุดเรียงตามกลิ่น  "
                 f"'{strongest.name}' กลิ่นแรงที่สุด ({strongest.smell}/10) "
                 f"อยู่ที่ {self._pos_text(self._slot_of(strongest))}")

    # ---------- 2.1 Sequential search
    def action_sequential(self):
        idx, steps = sequential_search_snack(self.slots)
        if idx < 0:
            self.say(f"Sequential search: เปิดดูครบ {steps} ช่อง ไม่พบขนมในตู้นี้")
            return
        it = self.slots[idx]
        self.flash({id(it)})
        self.say(f"Sequential search: เปิดดูทีละช่อง {steps} ช่อง เจอ '{it.name}' "
                 f"ที่ {self._pos_text(idx)}")

    # ---------- 2.2 Binary search
    def action_binary(self):
        name = self.entry.get().strip()
        if not name:
            self.say("กรุณาพิมพ์ชื่อวัตถุดิบที่ต้องการค้นหาในช่องข้างปุ่มก่อน")
            return
        by_name = merge_sort(self.get_items(), key=lambda x: x.name)   # ต้องเรียงชื่อก่อน
        idx, steps = binary_search_by_name(by_name, name)
        if idx < 0:
            self.say(f"Binary search: ไม่พบ '{name}' (เทียบ {steps} รอบ) - ไม่เหลือในตู้นี้")
            return
        it = by_name[idx]
        self.flash({id(it)})
        self.say(f"Binary search: พบ '{it.name}' ใน {steps} รอบ ที่ {self._pos_text(self._slot_of(it))} "
                 f"({countdown_text(it.expiry)})")


    # ---------- นำวัตถุดิบออก
    def action_remove(self):
        """ปุ่มแดงด้านล่าง: นำการ์ดที่เลือกไว้ (หรือชื่อที่พิมพ์ในช่องค้นหา) ออก"""
        it = self.selected
        if it is None or all(x is not it for x in self.slots):
            name = self.entry.get().strip()
            if not name:
                self.say("กดปุ่ม × ที่มุมการ์ดได้เลย หรือคลิกเลือกการ์ด/พิมพ์ชื่อในช่องค้นหาก่อนกดปุ่มนี้")
                return
            it = next((x for x in self.slots if x and x.name == name), None)
            if it is None:
                self.say(f"ไม่พบ '{name}' ในตู้นี้")
                return
        self.remove_item(it)

    def remove_item(self, it):
        idx = self._slot_of(it)
        self.slots[idx] = None
        if self.selected is it:
            self.selected = None
        self._undo = (it, idx)
        self.render()
        self.undo_btn.grid()
        self.say(f"นำ '{it.name}' ออกจากตู้แล้ว (เดิมอยู่ {self._pos_text(idx)}) - "
                 f"กำหนดหมดอายุ {fmt_dt(it.expiry)}")

    def undo_remove(self):
        if self._undo is None:
            return
        it, idx = self._undo
        if self.slots[idx] is not None:                # ช่องเดิมถูกใช้แล้ว -> หาช่องว่างอื่น
            empties = [i for i, x in enumerate(self.slots) if x is None]
            if not empties:
                self.say("ตู้เย็นเต็มแล้ว ไม่สามารถนำ '" + it.name + "' กลับเข้าตู้ได้")
                return
            idx = empties[0]
        self.slots[idx] = it
        self._undo = None
        self.undo_btn.grid_remove()
        self.flash({id(it)})
        self.say(f"นำ '{it.name}' กลับเข้าตู้แล้ว ({self._pos_text(idx)})")


# ---------------------------------------------------------------- app
class App(ctk.CTk):
    """หน้าต่างหลัก: วางตู้เย็นหลายเครื่องเคียงกัน"""

    def __init__(self, configs):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()
        pick_font(self)
        self.configs = configs
        self.title("Fridge Inventory Manager - ระบบจัดการตู้เย็นและวันหมดอายุ")
        height = min(940, self.winfo_screenheight() - 80)
        self.geometry(f"{min(1240, 80 + 580 * len(configs))}x{height}")
        self.minsize(620, 520)
        self.configure(fg_color="#11151c")

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(16, 6))
        titles = ctk.CTkFrame(top, fg_color="transparent")
        titles.pack(side="left")
        ctk.CTkLabel(titles, text="Fridge Inventory Manager", font=F(28, True)
                     ).pack(anchor="w")
        ctk.CTkLabel(titles, text="ระบบจัดการตู้เย็นและวันหมดอายุ", font=F(14),
                     text_color="#9ca3af").pack(anchor="w")
        self._merge_pills = []
        if len(configs) > 1:
            ctk.CTkButton(top, text="รวมรายการทุกตู้เย็น\n(Merge sort)", font=F(13, True),
                          height=52, corner_radius=16, fg_color="#7048e8",
                          hover_color="#5f3dc4", command=self.show_merge
                          ).pack(side="right")
        clock_box = ctk.CTkFrame(top, fg_color="#1f2530", corner_radius=14)
        clock_box.pack(side="right", padx=14)
        ctk.CTkLabel(clock_box, text="เวลาปัจจุบัน (อ้างอิงนาฬิกาเครื่อง)", font=F(11),
                     text_color="#9ca3af").pack(padx=14, pady=(6, 0))
        self.clock = ctk.CTkLabel(clock_box, text=fmt_now(), font=F(15, True))
        self.clock.pack(padx=14, pady=(0, 6))

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")   # จอเตี้ยก็เลื่อนลงไปกดปุ่มได้
        content.pack(fill="both", expand=True, padx=14, pady=4)
        self.panels = []
        for c, cfg in enumerate(configs):
            content.grid_columnconfigure(c, weight=1, uniform="fridge")
            p = FridgePanel(content, cfg)
            p.grid(row=0, column=c, padx=10, pady=6, sticky="nsew")
            self.panels.append(p)
        content.grid_rowconfigure(0, weight=1)

        legend = ctk.CTkFrame(self, fg_color="transparent")
        legend.pack(pady=(0, 10))
        ctk.CTkLabel(legend, text="สีป้ายวันหมดอายุ:", font=F(12),
                     text_color="#9ca3af").pack(side="left", padx=6)
        for color, text in (("#2f9e44", "มากกว่า 7 วัน"), ("#f08c00", "4-7 วัน"),
                            ("#e03131", "ภายใน 3 วัน"), ("#c92a2a", "หมดอายุแล้ว")):
            ctk.CTkLabel(legend, text=f"  {text}  ", font=F(12, True), text_color="white",
                         fg_color=color, corner_radius=10, height=24
                         ).pack(side="left", padx=4)
        self._tick()

    def _tick(self):
        """รันทุก 1 วินาที: อัปเดตนาฬิกาและเวลาที่เหลือของทุกการ์ด"""
        self.clock.configure(text=fmt_now())
        for p in self.panels:
            p.refresh_countdowns()
        alive = []
        for it, lbl in self._merge_pills:              # ป้ายในหน้าต่าง Merge (ถ้าเปิดอยู่)
            try:
                color, text = expiry_style(it)
                lbl.configure(text=f"  {text}  ", fg_color=color)
                alive.append((it, lbl))
            except Exception:
                pass
        self._merge_pills = alive
        self.after(1000, self._tick)

    # ---------- 1.4 Merge sort
    def show_merge(self):
        win = ctk.CTkToplevel(self)
        win.title("รวมรายการจากทุกตู้เย็น (Merge sort)")
        win.geometry("760x680")
        merged = merge_fridges(*[p.get_items() for p in self.panels])
        accents = {f"ตู้เย็น {c.fid}": c.accent for c in self.configs}
        self._merge_pills = []

        ctk.CTkLabel(win, text="รวมรายการจากทุกตู้เย็น", font=F(22, True)
                     ).pack(pady=(16, 0))
        ctk.CTkLabel(win, text=f"Merge sort: {len(merged)} รายการ เรียงตามวันหมดอายุ "
                               f"(ใกล้หมดอายุอยู่บนสุด)", font=F(13), text_color="#9ca3af"
                     ).pack(pady=(0, 8))
        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        for rank, it in enumerate(merged, 1):
            row = ctk.CTkFrame(scroll, corner_radius=16, fg_color="#1f2530")
            row.pack(fill="x", pady=4, padx=4)
            row.grid_columnconfigure(2, weight=1)
            ctk.CTkLabel(row, text=str(rank), width=36, font=F(16, True),
                         text_color="#9ca3af").grid(row=0, column=0, padx=(10, 0), pady=8)
            ctk.CTkLabel(row, text="", image=icon(it.icon, 46)
                         ).grid(row=0, column=1, padx=6)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.grid(row=0, column=2, sticky="w", padx=6)
            ctk.CTkLabel(info, text=it.name, font=F(16, True), anchor="w").pack(anchor="w")
            ctk.CTkLabel(info, text=f"หมดอายุ {fmt_dt(it.expiry)}  |  {CATEGORY_TH[it.category]}",
                         font=F(12), text_color="#9ca3af").pack(anchor="w")
            ctk.CTkLabel(row, text=f"  {it.fridge}  ", font=F(12, True), text_color="white",
                         fg_color=accents.get(it.fridge, "#555"), corner_radius=10,
                         height=24).grid(row=0, column=3, padx=6)
            color, text = expiry_style(it)
            pill = ctk.CTkLabel(row, text=f"  {text}  ", font=F(12, True),
                                text_color="white", fg_color=color,
                                corner_radius=10, height=24)
            pill.grid(row=0, column=4, padx=(0, 12))
            self._merge_pills.append((it, pill))
        win.after(100, win.lift)


# ====================================================================
# 5) เริ่มโปรแกรม
# ====================================================================

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which == "1":
        fridges = [FRIDGE_1]
    elif which == "2":
        fridges = [FRIDGE_2]
    else:
        fridges = [FRIDGE_1, FRIDGE_2]
    App(fridges).mainloop()