import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImagePredictor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("واجهة التنبؤ بالصور")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #1e1e2f; color: #f0f0f0;")
        
        self.layout = QVBoxLayout()
        
        # عرض الصورة
        self.image_label = QLabel("لم يتم اختيار صورة")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            border: 2px dashed #6c63ff;
            border-radius: 10px;
            padding: 10px;
            background-color: #2b2b3d;
            font-size: 16px;
        """)
        self.layout.addWidget(self.image_label)
        
        # زر اختيار الصورة
        self.choose_button = QPushButton("اختر صورة")
        self.choose_button.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            color: #fff;
            background-color: #6c63ff;
            border: none;
            border-radius: 8px;
        """)
        self.choose_button.clicked.connect(self.choose_image)
        self.layout.addWidget(self.choose_button)
        
        # زر التنبؤ
        self.predict_button = QPushButton("تنبؤ")
        self.predict_button.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            color: #fff;
            background-color: #ff6584;
            border: none;
            border-radius: 8px;
        """)
        self.predict_button.clicked.connect(self.predict_image)
        self.layout.addWidget(self.predict_button)
        
        # مكان عرض النتيجة
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            font-size: 14px;
            padding: 10px;
            border-radius: 8px;
            background-color: #2b2b3d;
            color: #ffffff;
        """)
        self.layout.addWidget(self.result_text)
        
        self.setLayout(self.layout)
        self.image_path = None
        
    def choose_image(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "اختر صورة", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.image_path = path
            pixmap = QPixmap(path).scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
    
    def predict_image(self):
        if not self.image_path:
            self.result_text.setText("الرجاء اختيار صورة أولاً.")
            return
        
        api_url = "http://localhost:8050"  # 🔴 ضع رابط الـ API الخاص بك
        try:
            with open(self.image_path, "rb") as f:
                files = {"file": f}
                response = requests.post(api_url, files=files)
            
            if response.status_code == 200:
                result = response.json()  # نفترض أن الـ API يعيد JSON
                self.result_text.setText(f"نتيجة التنبؤ:\n{result}")
            else:
                self.result_text.setText(f"حدث خطأ، رمز الحالة: {response.status_code}")
        except Exception as e:
            self.result_text.setText(f"خطأ في الاتصال بالـ API:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImagePredictor()
    window.show()
    sys.exit(app.exec())
