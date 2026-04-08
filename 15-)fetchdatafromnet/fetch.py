import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def fiyatlari_getir():
    # URL kısmına gerçek bir site adresi eklemelisin (Örn: döviz sitesi)
    url = "https://www.tcmb.gov.tr/kurlar/today.xml" # Örnektir, senin html yapına göre değişir
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Buradaki seçiciler (ul, li class vs.) çektiğin siteye göre doğru olmalı
            ul_list = soup.find_all('ul', style=True)
            fiyatlar = []
            for ul in ul_list:
                doviz_cinsi_element = ul.find('li', class_='cel1010 tal')
                if doviz_cinsi_element:
                    doviz_cinsi = doviz_cinsi_element.text.strip()
                    satis_fiyat_elements = ul.find_all('li', class_='cel1005')
                    if len(satis_fiyat_elements) > 0:
                        # Virgülü noktaya çevirip float yapıyoruz
                        fiyat_text = satis_fiyat_elements[0].text.strip().replace(',', '.')
                        satis_fiyati = float(fiyat_text)
                        fiyatlar.append((doviz_cinsi, satis_fiyati))
            return fiyatlar
        else:
            messagebox.showerror("Hata", "Döviz fiyatları çekilemedi.")
            return None
    except Exception as e:
        messagebox.showerror("Hata", f"Bağlantı hatası: {e}")
        return None

def Hesapla():
    try:
        tl_miktari = float(entry_yatirim.get())
        fiyatlar = fiyatlari_getir()

        if fiyatlar:
            # winfo_children() yazımı düzeltildi
            for widget in result_canvas_frame.winfo_children():
                widget.destroy()

            # enumerate yazımı ve hesaplama mantığı düzeltildi
            for i, (doviz_cinsi, satis_fiyati) in enumerate(fiyatlar):
                alinabilecek_miktar = tl_miktari / satis_fiyati # "=" yerine "+" kullanmışsın
                
                doviz_label = tk.Label(result_canvas_frame, text=doviz_cinsi, font=("Arial", 12), anchor="w")
                doviz_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                
                # Değişken ismi ve f-string hatası düzeltildi
                miktar_label = tk.Label(result_canvas_frame, text=f"{alinabilecek_miktar:.2f}", font=("Arial", 12), anchor="e")
                miktar_label.grid(row=i, column=1, padx=10, pady=5, sticky="e")
            
            # Scroll ayarları yazımı düzeltildi
            result_canvas.update_idletasks()
            result_canvas.config(scrollregion=result_canvas.bbox("all"))
            
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı giriniz.")

# --- Tkinter Arayüz Kurulumu (Eksik kısımları tamamladım) ---
root = tk.Tk()
root.title("Döviz Hesaplayıcı")
root.geometry("400x500")

tk.Label(root, text="Yatırım Miktarı (TL):").pack(pady=5)
entry_yatirim = tk.Entry(root)
entry_yatirim.pack(pady=5)

tk.Button(root, text="Hesapla", command=Hesapla).pack(pady=10)

# Scrollbar için Canvas yapısı
result_canvas = tk.Canvas(root)
result_canvas.pack(side="left", fill="both", expand=True)

result_canvas_frame = tk.Frame(result_canvas)
result_canvas.create_window((0, 0), window=result_canvas_frame, anchor="nw")

root.mainloop()