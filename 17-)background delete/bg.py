import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk
import io

def arka_plan_kaldir():
    try:
        # 1. Giriş dosyasını seç
        girdi_yolu = filedialog.askopenfilename(
            title="Bir resim seçin",
            filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png")]
        )
        
        if not girdi_yolu:
            return

        # 2. Çıkış dosyasının kaydedileceği yeri seç
        cikti_yolu = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG dosyası", "*.png")],
            title="Sonucu Kaydet"
        )

        if not cikti_yolu:
            return

        # Durum bilgisi ver (Arayüzde işlem yapıldığını belirtmek için)
        label_durum.config(text="İşleniyor... Lütfen bekleyin.", fg="blue")
        pencere.update()

        # 3. Arka planı silme işlemi
        with open(girdi_yolu, "rb") as dosya:
            girdi = dosya.read()
            sonuc = remove(girdi)

        # 4. Dosyayı kaydet
        with open(cikti_yolu, "wb") as dosya:
            dosya.write(sonuc)

        # 5. Önizleme oluşturma
        sonuc_goruntu = Image.open(io.BytesIO(sonuc))
        sonuc_goruntu.thumbnail((300, 300))  # Önizleme boyutunu ayarla
        sonuc_img = ImageTk.PhotoImage(sonuc_goruntu)
        
        label_cikti.config(image=sonuc_img)
        label_cikti.image = sonuc_img  # Garbage collector tarafından silinmemesi için referans tutulur
        
        label_durum.config(text="İşlem Başarılı!", fg="green")
        messagebox.showinfo("Başarılı", "Arka plan başarıyla kaldırıldı ve kaydedildi.")

    except Exception as e:
        label_durum.config(text="Hata oluştu!", fg="red")
        messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")

# --- Arayüz Oluşturma ---
pencere = tk.Tk()
pencere.title("AI Arka Plan Silici")
pencere.geometry("400x500")

# Başlık
baslik = tk.Label(pencere, text="Arka Plan Kaldırma Uygulaması", font=("Arial", 14, "bold"))
baslik.pack(pady=20)

# İşlem Butonu
buton_sec = tk.Button(
    pencere, 
    text="Resim Seç ve Arka Planı Sil", 
    command=arka_plan_kaldir,
    bg="#4CAF50", 
    fg="white", 
    padx=10, 
    pady=5
)
buton_sec.pack(pady=10)

# Durum Mesajı
label_durum = tk.Label(pencere, text="Hazır", font=("Arial", 10))
label_durum.pack(pady=5)

# Önizleme Alanı
label_cikti = tk.Label(pencere, text="Önizleme burada görünecek", bg="lightgrey", width=40, height=15)
label_cikti.pack(pady=20)

# Uygulamayı çalıştır
pencere.mainloop()