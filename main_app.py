"""
main_app.py  --  รันตู้เย็นทั้ง 2 เครื่องพร้อมกันในหน้าต่างเดียว
ติดตั้งก่อน:  pip install customtkinter pillow
รัน:          python main_app.py
"""
from fridge1 import FRIDGE as FRIDGE_1
from fridge2 import FRIDGE as FRIDGE_2
from fridge_ui import App

if __name__ == "__main__":
    App([FRIDGE_1, FRIDGE_2]).mainloop()
