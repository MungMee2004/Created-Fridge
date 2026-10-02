import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random
import threading 

from ไฟล์ที่1 import *

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AnimatedAlgorithmApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎵 Rhythm Algorithm Simulator")
        self.geometry("950x850") 
        self.current_data = []
        self.is_running = False 
        
        self.comparisons = 0
        self.swaps = 0

        self.setup_ui()
        self.generate_data()

    def setup_ui(self):
        # ==========================================
        # 1. แผงควบคุมส่วนหัว (Header & Data Controls)
        # ==========================================
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.pack(pady=(15, 5), padx=20, fill="x")

        # บรรทัดบนของ Header (ชื่อแอป และ ความเร็ว)
        top_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_header.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(top_header, text="🎹 Piano Roll Algorithm Simulator", font=("Helvetica", 20, "bold")).pack(side="left")
        
        self.btn_stop = ctk.CTkButton(top_header, text="🛑 หยุดการทำงาน", command=self.stop_animation, fg_color="#e74c3c", hover_color="#c0392b", state="disabled", width=120, font=("Helvetica", 13, "bold"))
        self.btn_stop.pack(side="right", padx=5)

        self.speed_slider = ctk.CTkSlider(top_header, from_=0.01, to=0.5, width=120)
        self.speed_slider.set(0.1) 
        self.speed_slider.pack(side="right", padx=15)
        ctk.CTkLabel(top_header, text="ความเร็ว:", font=("Helvetica", 13)).pack(side="right")

        # บรรทัดล่างของ Header (การจัดการข้อมูล)
        bottom_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        bottom_header.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(bottom_header, text="จัดการตัวโน้ต:", font=("Helvetica", 14, "bold")).pack(side="left")
        
        self.btn_generate = ctk.CTkButton(bottom_header, text="🔄 สุ่มโน้ตใหม่แบบสุ่ม", command=self.generate_data, fg_color="#28a745", hover_color="#218838", width=140)
        self.btn_generate.pack(side="left", padx=10)

        ctk.CTkLabel(bottom_header, text="หรือพิมพ์เอง:").pack(side="left", padx=(10, 5))
        self.entry_custom = ctk.CTkEntry(bottom_header, placeholder_text="เช่น: 50,10,80,30", width=180)
        self.entry_custom.pack(side="left", padx=5)
        
        self.btn_apply_custom = ctk.CTkButton(bottom_header, text="นำไปใช้", command=self.apply_custom_data, fg_color="#8e44ad", hover_color="#9b59b6", width=80)
        self.btn_apply_custom.pack(side="left", padx=5)

        # ==========================================
        # 2. จอแสดงผลหลัก (Canvas)
        # ==========================================
        self.canvas = tk.Canvas(self, width=900, height=350, bg="#181820", highlightthickness=2, highlightbackground="#333344")
        self.canvas.pack(pady=10)

        # ==========================================
        # 3. โซนสถิติ และ กล่องอธิบาย
        # ==========================================
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=5)

        self.lbl_stats = ctk.CTkLabel(info_frame, text="📊 เปรียบเทียบ: 0 ครั้ง  |  🔄 สลับที่: 0 ครั้ง", font=("Helvetica", 15, "bold"), text_color="#2ecc71")
        self.lbl_stats.pack(side="top", anchor="e", pady=(0, 5))

        self.txt_explanation = ctk.CTkTextbox(info_frame, height=65, font=("Helvetica", 16, "bold"), fg_color="#2a2a35", text_color="#f1c40f", state="disabled", corner_radius=8)
        self.txt_explanation.pack(fill="x")

        # ==========================================
        # 4. เครื่องมืออัลกอริทึม (แบบ Tabview จัดระเบียบ)
        # ==========================================
        self.tabview = ctk.CTkTabview(self, height=100, corner_radius=10)
        self.tabview.pack(fill="x", padx=20, pady=(10, 0))

        self.tabview.add("📊 การเรียงลำดับ (Sorting)")
        self.tabview.add("🔍 การค้นหา (Searching)")

        # --- แท็บ: การเรียงลำดับ ---
        sort_tab = self.tabview.tab("📊 การเรียงลำดับ (Sorting)")
        ctk.CTkLabel(sort_tab, text="เลือกวิธีการจัดเรียงระดับเสียงดนตรี:", font=("Helvetica", 14)).pack(side="left", padx=15)
        
        btn_w = 110
        ctk.CTkButton(sort_tab, text="Bubble Sort", width=btn_w, fg_color="#f39c12", hover_color="#d68910", command=lambda: self.run_in_thread(self.anim_bubble_sort)).pack(side="left", padx=5)
        ctk.CTkButton(sort_tab, text="Insertion Sort", width=btn_w, fg_color="#f39c12", hover_color="#d68910", command=lambda: self.run_in_thread(self.anim_insertion_sort)).pack(side="left", padx=5)
        ctk.CTkButton(sort_tab, text="Selection Sort", width=btn_w, fg_color="#f39c12", hover_color="#d68910", command=lambda: self.run_in_thread(self.anim_selection_sort)).pack(side="left", padx=5)
        ctk.CTkButton(sort_tab, text="Merge Sort", width=btn_w, fg_color="#f39c12", hover_color="#d68910", command=lambda: self.run_in_thread(self.anim_merge_sort)).pack(side="left", padx=5)

        # --- แท็บ: การค้นหา ---
        search_tab = self.tabview.tab("🔍 การค้นหา (Searching)")
        ctk.CTkLabel(search_tab, text="ตัวโน้ตเป้าหมาย:", font=("Helvetica", 14)).pack(side="left", padx=15)
        
        self.entry_search = ctk.CTkEntry(search_tab, placeholder_text="ใส่ตัวเลข...", width=100)
        self.entry_search.pack(side="left", padx=10)
        
        ctk.CTkButton(search_tab, text="Sequential Search", fg_color="#3498db", hover_color="#2980b9", command=lambda: self.run_in_thread(self.anim_seq_search)).pack(side="left", padx=5)
        ctk.CTkButton(search_tab, text="Binary Search", fg_color="#9b59b6", hover_color="#8e44ad", command=lambda: self.run_in_thread(self.anim_bin_search)).pack(side="left", padx=5)


    # =======================================================
    # ส่วนของฟังก์ชันระบบ (ทำงานเหมือนเดิม)
    # =======================================================
    def run_in_thread(self, target_function):
        if self.is_running: return 
        self.is_running = True
        self.disable_ui()
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()
        threading.Thread(target=target_function, daemon=True).start()

    def update_stats(self):
        self.lbl_stats.configure(text=f"📊 เปรียบเทียบ: {self.comparisons} ครั้ง  |  🔄 สลับที่ (Swaps/Writes): {self.swaps} ครั้ง")

    def update_explanation(self, text, color="#f1c40f"):
        def _update():
            self.txt_explanation.configure(state="normal", text_color=color)
            self.txt_explanation.delete("1.0", "end")
            self.txt_explanation.insert("1.0", text)
            self.txt_explanation.configure(state="disabled")
        self.after(0, _update)

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height = 350
        c_width = 900
        x_width = c_width / (len(data) + 1)
        offset = 20
        spacing = 5
        note_thickness = 12 

        max_val = max(data) if len(data) > 0 and max(data) > 0 else 1
        
        for i in range(1, 6):
            y_grid = i * (c_height / 6)
            self.canvas.create_line(0, y_grid, c_width, y_grid, fill="#2a2a35", dash=(4, 4))

        for i, color in enumerate(color_array):
            if color == "#e74c3c" or color == "#f1c40f": 
                self.canvas.create_rectangle(i * x_width + offset, 0, 
                                             (i+1) * x_width + offset - spacing, c_height, 
                                             fill="#3a1c24" if color == "#e74c3c" else "#3a3820", outline="")

        normalized_data = [v / max_val for v in data]
        for i, height_ratio in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            x1 = (i + 1) * x_width + offset
            y_center = c_height - 30 - (height_ratio * (c_height - 60))
            y0 = y_center - note_thickness
            y1 = y_center + note_thickness

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], outline="#ffffff", width=1)
            self.canvas.create_text(x0 + (x_width-spacing)/2, y0 - 10, text=str(data[i]), fill="white", font=("Helvetica", 10, "bold"))
        
        self.update_idletasks()

    def generate_data(self):
        if self.is_running: return 
        self.current_data = [random.randint(10, 100) for _ in range(15)] 
        self.draw_data(self.current_data, ["#00d2ff"] * len(self.current_data))
        self.update_explanation("✅ สุ่มแทร็กเสียงใหม่แล้ว", "#2ecc71")
        self.comparisons = self.swaps = 0
        self.update_stats()

    def apply_custom_data(self):
        if self.is_running: return
        raw_text = self.entry_custom.get()
        try:
            new_data = [int(x.strip()) for x in raw_text.split(",") if x.strip()]
            if len(new_data) < 2:
                messagebox.showwarning("เตือน", "กรุณาใส่ตัวเลขอย่างน้อย 2 ตัว (คั่นด้วยลูกน้ำ ,)")
                return
            if len(new_data) > 30:
                messagebox.showwarning("เตือน", "เพื่อความสวยงาม ไม่ควรใส่ข้อมูลเกิน 30 ตัว")
                return
                
            self.current_data = new_data
            self.draw_data(self.current_data, ["#00d2ff"] * len(self.current_data))
            self.update_explanation("✅ นำชุดข้อมูลของคุณมาใช้เรียบร้อยแล้ว", "#2ecc71")
            self.comparisons = self.swaps = 0
            self.update_stats()
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "รูปแบบไม่ถูกต้อง! กรุณาใส่เฉพาะตัวเลขคั่นด้วยลูกน้ำ เช่น 40, 15, 80, 20")

    def stop_animation(self):
        self.is_running = False
        self.update_explanation("🛑 หยุดการทำงานชั่วคราว!", "#e74c3c")
        self.btn_stop.configure(state="disabled")
        self.btn_generate.configure(state="normal")
        self.btn_apply_custom.configure(state="normal")

    def disable_ui(self):
        self.btn_generate.configure(state="disabled")
        self.btn_apply_custom.configure(state="disabled")
        self.btn_stop.configure(state="normal")

    def enable_ui(self, msg, color="#2ecc71"):
        self.is_running = False
        self.btn_generate.configure(state="normal")
        self.btn_apply_custom.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.update_explanation(msg, color)

    def get_search_target(self):
        val = self.entry_search.get()
        if not val.isdigit():
            self.after(0, lambda: messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกตัวเลขจำนวนเต็มเท่านั้น!"))
            self.enable_ui("❌ การค้นหาถูกยกเลิก (กรุณาใส่ตัวเลข)", "#e74c3c")
            return None
        return int(val)

    # ==========================================
    # แอนิเมชันอัลกอริทึม
    # ==========================================
    def anim_bubble_sort(self):
        self.update_explanation("⚙️ เริ่มทำงาน Bubble Sort: จะไล่เปรียบเทียบเสียงไปทีละคู่")
        data = self.current_data
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if not self.is_running: return
                
                colors = ["#00d2ff"] * n
                colors[j] = colors[j+1] = "#e74c3c"
                for k in range(n-i, n): colors[k] = "#2ecc71"
                self.draw_data(data, colors)
                
                self.comparisons += 1 
                self.update_stats()
                self.update_explanation(f"เปรียบเทียบ [ {data[j]} ] กับ [ {data[j+1]} ]")
                time.sleep(self.speed_slider.get())

                if data[j] > data[j+1]:
                    self.swaps += 1 
                    self.update_stats()
                    self.update_explanation(f"⚠️ [ {data[j]} ] สูงกว่า [ {data[j+1]} ] -> สลับตำแหน่ง!", "#e67e22")
                    data[j], data[j+1] = data[j+1], data[j]
                    self.draw_data(data, colors)
                    time.sleep(self.speed_slider.get())

        if self.is_running:
            self.draw_data(data, ["#2ecc71"] * n)
            self.enable_ui("✅ Bubble Sort จัดเรียงเสียงเสร็จสมบูรณ์!")

    def anim_insertion_sort(self):
        data = self.current_data
        n = len(data)
        for i in range(1, n):
            if not self.is_running: return
            key = data[i]
            j = i-1
            
            self.update_explanation(f"หยิบโน้ตเสียง [ {key} ] ขึ้นมาพิจารณาหาตำแหน่งที่เหมาะสม")
            time.sleep(self.speed_slider.get())
            
            while j >= 0:
                self.comparisons += 1
                self.update_stats()
                if not self.is_running: return
                
                colors = ["#2ecc71" if x < i else "#00d2ff" for x in range(n)]
                colors[j], colors[j+1] = "#e74c3c", "#e74c3c"
                self.draw_data(data, colors)
                
                if key < data[j]:
                    self.swaps += 1
                    self.update_stats()
                    self.update_explanation(f"เสียง [ {key} ] ต่ำกว่า [ {data[j]} ] -> เลื่อน [ {data[j]} ] ถอยหลัง", "#e67e22")
                    data[j + 1] = data[j]
                    j -= 1
                    time.sleep(self.speed_slider.get())
                else:
                    break
                
            data[j + 1] = key
            self.swaps += 1
            self.update_stats()
            
            colors = ["#2ecc71" if x <= i else "#00d2ff" for x in range(n)]
            self.draw_data(data, colors)
            time.sleep(self.speed_slider.get())
            
        if self.is_running:
            self.draw_data(data, ["#2ecc71"] * n)
            self.enable_ui("✅ Insertion Sort จัดเรียงเสียงเสร็จสมบูรณ์!")

    def anim_selection_sort(self):
        data = self.current_data
        n = len(data)
        for i in range(n):
            if not self.is_running: return
            min_idx = i
            
            for j in range(i+1, n):
                if not self.is_running: return
                self.comparisons += 1
                self.update_stats()
                
                colors = ["#2ecc71" if x < i else "#00d2ff" for x in range(n)]
                colors[min_idx] = "#f1c40f" 
                colors[j] = "#e74c3c" 
                self.draw_data(data, colors)
                
                self.update_explanation(f"กำลังสแกนหาเสียงที่ต่ำกว่า [ {data[min_idx]} ] ... ตรวจสอบ [ {data[j]} ]")
                time.sleep(self.speed_slider.get())
                
                if data[min_idx] > data[j]:
                    min_idx = j
                    self.update_explanation(f"💡 พบเสียงต่ำที่สุดค่าใหม่คือ [ {data[min_idx]} ]", "#f1c40f")
                    time.sleep(self.speed_slider.get())
                    
            if i != min_idx:
                self.swaps += 1
                self.update_stats()
                self.update_explanation(f"สลับเสียงต่ำสุด [ {data[min_idx]} ] มาไว้ด้านหน้าสุด", "#2ecc71")        
                data[i], data[min_idx] = data[min_idx], data[i]
                time.sleep(self.speed_slider.get())
            
        if self.is_running:
            self.draw_data(data, ["#2ecc71"] * n)
            self.enable_ui("✅ Selection Sort จัดเรียงเสียงเสร็จสมบูรณ์!")

    def anim_merge_sort(self):
        self.update_explanation("⚙️ เริ่ม Merge Sort")
        def merge_visual(data, l, m, r):
            if not self.is_running: return
            left_part = data[l:m+1]
            right_part = data[m+1:r+1]
            
            i = j = 0; k = l
            while i < len(left_part) and j < len(right_part):
                if not self.is_running: return
                self.comparisons += 1
                self.update_stats()
                
                colors = ["#00d2ff"] * len(data)
                colors[l+i] = colors[m+1+j] = "#e74c3c"
                self.draw_data(data, colors)
                
                self.update_explanation(f"เปรียบเทียบ [ {left_part[i]} ] กับ [ {right_part[j]} ]")
                time.sleep(self.speed_slider.get())
                
                self.swaps += 1 
                self.update_stats()
                if left_part[i] <= right_part[j]:
                    data[k] = left_part[i]; i += 1
                else:
                    data[k] = right_part[j]; j += 1
                k += 1
                
            while i < len(left_part): 
                self.swaps += 1
                self.update_stats()
                data[k] = left_part[i]; i += 1; k += 1
            while j < len(right_part): 
                self.swaps += 1
                self.update_stats()
                data[k] = right_part[j]; j += 1; k += 1
            
            if not self.is_running: return
            colors = ["#00d2ff"] * len(data)
            for x in range(l, r+1): colors[x] = "#2ecc71"
            self.draw_data(data, colors)
            time.sleep(self.speed_slider.get())

        def merge_sort_recursive(data, l, r):
            if not self.is_running: return
            if l < r:
                m = (l + r) // 2
                merge_sort_recursive(data, l, m)
                merge_sort_recursive(data, m + 1, r)
                merge_visual(data, l, m, r)

        merge_sort_recursive(self.current_data, 0, len(self.current_data) - 1)
        if self.is_running:
            self.draw_data(self.current_data, ["#2ecc71"] * len(self.current_data))
            self.enable_ui("✅ Merge Sort จัดเรียงเสียงเสร็จสมบูรณ์!")

    def anim_seq_search(self):
        target = self.get_search_target()
        if target is None or not self.is_running: return
        self.update_explanation(f"🔍 เริ่ม Sequential Search: หาเป้าหมาย [ {target} ]")
        
        data = self.current_data
        for i in range(len(data)):
            if not self.is_running: return
            self.comparisons += 1
            self.update_stats()
            
            colors = ["#00d2ff"] * len(data)
            colors[i] = "#e74c3c" 
            self.draw_data(data, colors)
            
            self.update_explanation(f"ตรวจสอบจังหวะที่ {i+1} : ระดับเสียงคือ [ {data[i]} ]")
            time.sleep(self.speed_slider.get())
            
            if data[i] == target:
                colors[i] = "#2ecc71" 
                self.draw_data(data, colors)
                self.enable_ui(f"✅ ค้นพบแล้ว! โน้ต [ {target} ] อยู่ที่ตำแหน่งที่ {i}")
                return
        if self.is_running:
            self.enable_ui(f"❌ ไม่มีโน้ต [ {target} ] อยู่ในชุดข้อมูลนี้", "#e74c3c")

    def anim_bin_search(self):
        target = self.get_search_target()
        if target is None or not self.is_running: return
        
        self.update_explanation("⚠️ ระบบทำการเรียงลำดับให้อัตโนมัติ (กฎก่อนเริ่ม Binary Search)", "#f1c40f")
        self.current_data = sorted(self.current_data)
        self.draw_data(self.current_data, ["#00d2ff"] * len(self.current_data))
        time.sleep(1.5)
        
        data = self.current_data
        low, high = 0, len(data) - 1
        
        while low <= high:
            if not self.is_running: return
            self.comparisons += 1
            self.update_stats()
            
            mid = (low + high) // 2
            colors = ["#222230"] * len(data) 
            for i in range(low, high+1): colors[i] = "#00d2ff" 
            colors[mid] = "#f1c40f" 
            
            self.draw_data(data, colors)
            self.update_explanation(f"หยิบค่าตรงกลางมาเทียบคือ [ {data[mid]} ]")
            time.sleep(max(0.5, self.speed_slider.get() * 2)) 
            
            if data[mid] == target:
                colors[mid] = "#2ecc71"
                self.draw_data(data, colors)
                self.enable_ui(f"✅ ค้นพบแล้ว! โน้ต [ {target} ] อยู่ที่ตำแหน่งที่ {mid}")
                return
            elif data[mid] < target:
                self.comparisons += 1
                self.update_stats()
                self.update_explanation(f"[ {target} ] สูงกว่าค่ากลาง [ {data[mid]} ] -> ตัดซ้ายทิ้ง!", "#e74c3c")
                low = mid + 1
            else:
                self.comparisons += 1
                self.update_stats()
                self.update_explanation(f"[ {target} ] ต่ำกว่าค่ากลาง [ {data[mid]} ] -> ตัดขวาทิ้ง!", "#e74c3c")
                high = mid - 1
                
            time.sleep(max(0.5, self.speed_slider.get() * 2))
                
        if self.is_running:
            self.draw_data(data, ["#222230"] * len(data))
            self.enable_ui(f"❌ ไม่พบโน้ต [ {target} ] ในแทร็กนี้", "#e74c3c")