import PyPDF2
from gtts import gTTS ##metni sese cevir
import os #sistem 
import tkinter as tk
from tkinter import filedialog 

def pdf_metni_cikar(pdf_yolu):
    metin=""
    pdf_okuyucu=PyPDF2.PdfReader(open(pdf_yolu,'rb'))
    for sayfa_num in range(len(pdf_okuyucu.pages)):
        metin+=pdf_okuyucu.pages[sayfa_num].extract_text()  ##okudugun metinleri disariya at
    return metin 
    
#metni sesli hale getiren fonksiyon 

def metni_sese_cevir(metin,cikti_dosyasi):
    sesli_cevirici=gTTS(text=metin,lang='tr')
    sesli_cevirici.save(cikti_dosyasi)

#dosya secme fonksiyonu 
def dosya_sec():
    dosya_yolu=filedialog.askopenfilename(filetypes=[("PDF Dosyalari","*pdf")])
    if dosya_yolu:
        pdf_metin=pdf_metni_cikar(dosya_yolu)
        metni_sese_cevir(pdf_metin,"save.mp3")
        os.system("start save.mp3")
    

#tkinter arayuzu
app=tk.Tk()
app.title("Audiobook creator")

secim_butonu=tk.Button(app,text="PDF Sec",command=dosya_sec,padx=20,pady=20)
secim_butonu.pack(pady=20)




app.mainloop()
   

