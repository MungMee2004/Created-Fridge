"""
fridge_ui.py  --  หน้าต่าง CustomTkinter สำหรับตู้เย็น (ใช้ร่วมกันทั้ง 2 ตู้)
ติดตั้ง:  pip install customtkinter pillow
"""
import tkinter.font as tkfont

import customtkinter as ctk

from fridge_core import (CATEGORY_TH, Item, FridgeConfig, d, fmt_dt, fmt_now,
                         countdown_text, seconds_left,
                         bubble_sort_by_expiry, is_sorted_by_expiry,
                         insertion_sort_insert, insertion_sort_all,
                         selection_sort_by_smell, merge_sort, merge_fridges,
                         sequential_search_snack, binary_search_by_name)
from fridge_icons import make_icon, ICON_LABELS

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
#บับเบิลปุ่ม 247
        btn("เรียงวันหมดอายุ\n(Bubble sort)", self.action_bubble, 0)
        btn("เพิ่มของใหม่\n(Insertion sort)", self.action_add, 1)
        btn("เนื้อสัตว์ไว้ล่างสุด\n(Selection sort)", self.action_selection, 2)
        btn("หาขนม\n(Sequential search)", self.action_sequential, 0, 1)
        #ไบนารี่หาของ 251-255
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
    #บับเบิลยูไอ 359-369
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
#แทรก 371-400
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
#เลือก 402-412
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
#ลำดับยูไอ 425-434
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

    #ไบนารี่ยูไอ 435-450
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
