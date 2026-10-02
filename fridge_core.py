"""
fridge_core.py  --  ข้อมูลและอัลกอริทึมกลาง (ไม่มี GUI)

1) การเรียงลำดับข้อมูล (Sorting)
   Bubble / Insertion / Selection / Merge sort
2) การค้นหาข้อมูล (Searching)
   Sequential search / Binary search
"""
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable, List

CATEGORY_TH = {"meat": "เนื้อสัตว์", "veg": "ผัก", "dairy": "นม/ไข่",
               "snack": "ขนม", "fruit": "ผลไม้"}


def d(days: int) -> date:
    """วันที่ที่อีก days วันนับจากวันนี้"""
    return date.today() + timedelta(days=days)


@dataclass
class Item:
    name: str
    category: str          # meat / veg / dairy / snack / fruit
    expiry: date
    icon: str              # ชื่อไอคอนใน fridge_icons
    smell: int = 0         # ความแรงของกลิ่น 0-10 (ใช้กับเนื้อสัตว์)
    fridge: str = ""       # ชื่อตู้เย็นที่เก็บอยู่

    def days_left(self) -> int:
        return (self.expiry - date.today()).days


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
