from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import os
import time

# استدعاء ملفات النواة (تأكد أن مجلد core بجانب هذا الملف)
from core.wallet import Wallet
from core.fabric import HolographicFabric
from core.device_metrics import DeviceScanner

class HNFMobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Purple"
        
        # تهيئة النظام
        self.init_system()

        # --- بناء الواجهة (Tabs) ---
        screen = MDScreen()
        nav_layout = MDBottomNavigation(selected_color_background="00000000", text_color_active="00d2d3")

        # 1. شاشة التعدين
        self.screen_mine = MDBottomNavigationItem(name='screen_mine', text='Mining', icon='pickaxe')
        self.build_mining_ui()
        nav_layout.add_widget(self.screen_mine)

        # 2. شاشة المحفظة
        self.screen_wallet = MDBottomNavigationItem(name='screen_wallet', text='Wallet', icon='wallet')
        self.build_wallet_ui()
        nav_layout.add_widget(self.screen_wallet)

        # 3. شاشة السحابة
        self.screen_cloud = MDBottomNavigationItem(name='screen_cloud', text='Cloud', icon='cloud-upload')
        self.build_cloud_ui()
        nav_layout.add_widget(self.screen_cloud)

        screen.add_widget(nav_layout)
        return screen

    def init_system(self):
        # إعداد مسار التخزين للهاتف
        self.storage_path = "/sdcard/HNF_Network" # مسار الأندرويد
        if not os.path.exists(self.storage_path):
            try: os.makedirs(self.storage_path)
            except: self.storage_path = "." # احتياطي للكمبيوتر

        self.wallet = Wallet()
        self.fabric = HolographicFabric(port=5000)
        self.scanner = DeviceScanner()
        self.scanner.scan_device()
        self.is_mining = False

    # --- تصميم التعدين ---
    def build_mining_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, pos_hint={'center_y': 0.6})
        
        layout.add_widget(MDLabel(text="HNF CORE ⌖", halign="center", font_style="H3", theme_text_color="Custom", text_color=(0, 1, 0.8, 1)))
        
        self.lbl_balance = MDLabel(text="0.00 HLN", halign="center", font_style="H2", theme_text_color="Primary")
        layout.add_widget(self.lbl_balance)
        
        self.btn_mine = MDFillRoundFlatButton(text="START MOBILE MINING", font_size=20, size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.btn_mine.bind(on_release=self.toggle_mining)
        layout.add_widget(self.btn_mine)
        
        self.lbl_log = MDLabel(text="System Ready...", halign="center", theme_text_color="Secondary", font_style="Caption")
        layout.add_widget(self.lbl_log)
        
        self.screen_mine.add_widget(layout)

    # --- تصميم المحفظة ---
    def build_wallet_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, pos_hint={'top': 0.9})
        
        layout.add_widget(MDLabel(text="My Wallet Address", halign="center", font_style="H6"))
        
        addr_field = MDTextField(text=self.wallet.address, readonly=True, mode="rectangle")
        layout.add_widget(addr_field)
        
        self.input_to = MDTextField(hint_text="Receiver Address", mode="rectangle")
        layout.add_widget(self.input_to)
        
        self.input_amt = MDTextField(hint_text="Amount", input_filter="float", mode="rectangle")
        layout.add_widget(self.input_amt)
        
        btn_send = MDRaisedButton(text="SEND P2P", size_hint_x=1, md_bg_color=(0.5, 0, 0.8, 1))
        btn_send.bind(on_release=self.send_money)
        layout.add_widget(btn_send)
        
        self.screen_wallet.add_widget(layout)

    # --- تصميم السحابة ---
    def build_cloud_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, pos_hint={'center_y': 0.5})
        layout.add_widget(MDLabel(text="Holo Cloud Storage", halign="center", font_style="H4"))
        
        # ملاحظة: اختيار الملفات في الأندرويد يتطلب مكتبة خاصة (plyer)
        # هنا سنضع زراً للمحاكاة
        btn_upload = MDFillRoundFlatButton(text="Simulate File Upload", size_hint_x=0.8, pos_hint={'center_x': 0.5})
        btn_upload.bind(on_release=self.mock_upload)
        layout.add_widget(btn_upload)
        
        self.lbl_cloud_status = MDLabel(text="No active tasks", halign="center", theme_text_color="Secondary")
        layout.add_widget(self.lbl_cloud_status)
        
        self.screen_cloud.add_widget(layout)

    # --- المنطق ---
    def update_ui(self, dt):
        bal = self.fabric.get_balance(self.wallet.address)
        self.lbl_balance.text = f"{bal:.2f} HLN"

    def toggle_mining(self, instance):
        self.is_mining = not self.is_mining
        if self.is_mining:
            self.btn_mine.text = "STOP MINING"
            self.btn_mine.md_bg_color = (1, 0, 0, 1)
            threading.Thread(target=self.mining_loop, daemon=True).start()
        else:
            self.btn_mine.text = "START MOBILE MINING"
            self.btn_mine.md_bg_color = self.theme_cls.primary_color

    def mining_loop(self):
        while self.is_mining:
            time.sleep(1) # سرعة التعدين
            reward = 10 * self.scanner.get_reward_multiplier()
            self.fabric.add_mining_reward(self.wallet.address, reward)
            
            # تحديث الواجهة من الخيط الرئيسي
            Clock.schedule_once(lambda dt: setattr(self.lbl_log, 'text', f"Mined +{reward:.2f}"), 0)
            Clock.schedule_once(self.update_ui, 0)

    def send_money(self, instance):
        try:
            amt = float(self.input_amt.text)
            to = self.input_to.text
            success, msg = self.fabric.transfer_funds(self.wallet.address, to, amt)
            self.show_dialog("Transaction", msg)
            Clock.schedule_once(self.update_ui, 0)
        except: pass

    def mock_upload(self, instance):
        self.lbl_cloud_status.text = "Uploading sample data to Swarm..."
        Clock.schedule_once(lambda dt: setattr(self.lbl_cloud_status, 'text', "✅ Uploaded (50 Nodes)"), 2)

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

if __name__ == "__main__":
    HNFMobileApp().run()