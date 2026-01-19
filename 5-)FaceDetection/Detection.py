import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            return
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 'minNeighbors' doğru yazıldı
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Insan", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)

        canvas.img = img_tk 
        # BURASI ÖNEMLİ: 'image' küçük harf olmalı!
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# XML dosyasının tam yolunu otomatik belirliyoruz
current_dir = os.path.dirname(os.path.abspath(__file__))
xml_full_path = os.path.join(current_dir, 'face_detector.xml')
face_cascade = cv2.CascadeClassifier(xml_full_path)

# Arayüz
root = tk.Tk()
root.title("Face Detection")

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()
open_button = tk.Button(root, text="Dosya Seç", command=open_file)
open_button.pack()

root.mainloop()