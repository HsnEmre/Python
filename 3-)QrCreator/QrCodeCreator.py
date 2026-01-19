import tkinter as tk
from tkinter import filedialog
import pyqrcode
from pyqrcode import QRCode

def qr_codu_olustur():
    url=url_girdi.get()

    if url:
        qr_url=pyqrcode.create(url)
        dosya_yolu=filedialog.asksaveasfile(defaultextension=".svg",filetypes=[("SVG Dosyaları","*.svg")])

        if dosya_yolu:
            qr_url.svg(dosya_yolu,scale=8)
            durum_etiketi.config(text="Qr kod oluşturuldu")


#tasarım
uygulama_penceresi=tk.Tk()
uygulama_penceresi.title("qr kod oluyşturucu")

etiket=tk.Label(uygulama_penceresi,text="URL giriniz")
url_girdi=tk.Entry(uygulama_penceresi,width=40)

qr_kodu_olustur_butonu=tk.Button(uygulama_penceresi,text="qr kodu oluştur",command=qr_codu_olustur)

durum_etiketi=tk.Label(uygulama_penceresi,text="")

#paketleme kullanilabilir amka tavsiye edilmez
# etiket.pack()
# qr_kodu_olustur_butonu.pack()
# url_girdi.pack()
# durum_etiketi.pack()

etiket.grid(row=0,column=0,padx=10,pady=10)
url_girdi.grid(row=0,column=1,padx=10,pady=10)
qr_kodu_olustur_butonu.grid(row=0,column=2,padx=10,pady=10)
durum_etiketi.grid(row=0,column=3,padx=10,pady=10)


uygulama_penceresi.mainloop()








uygulama_penceresi.mainloop()