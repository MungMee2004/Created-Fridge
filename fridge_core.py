"""
fridge_core.py  --  ข้อมูลและอัลกอริทึมกลาง (ไม่มี GUI)

1) การเรียงลำดับข้อมูล (Sorting)
   Bubble / Insertion / Selection / Merge sort
2) การค้นหาข้อมูล (Searching)
   Sequential search / Binary search
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, List

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
    icon: str              # ชื่อไอคอนใน fridge_icons
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
