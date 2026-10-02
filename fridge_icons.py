"""
สร้างรูปไอคอนอาหาร (ไม่มีหมู) ด้วย Pillow โดยวาดเองทั้งหมด
-> ไม่ต้องดาวน์โหลดไฟล์รูป ไม่ต้องต่ออินเทอร์เน็ต
"""
from PIL import Image, ImageDraw

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
