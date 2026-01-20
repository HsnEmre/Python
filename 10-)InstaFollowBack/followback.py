import os
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk, filedialog, messagebox

from bs4 import BeautifulSoup
from fpdf import FPDF

followers_list = []


def update_table(data):
    table.delete(*table.get_children())
    for index, item in enumerate(data, start=1):
        table.insert("", "end", values=(index, item))


def open_files_and_show_followers():
    global file_paths
    file_paths = []
    for i in range(1, 100):  # followers_1.html, followers_2.html, ..., followers_99.html
        file_path = f"followers_{i}.html"
        if os.path.exists(file_path):
            file_paths.append(file_path)
        else:
            break

    if not file_paths:
        messagebox.showwarning("Uyarı", "Dosya bulunamadı!")
        return

    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)


def open_file_and_show_followers():
    global file_paths
    file_paths = filedialog.askopenfilenames(title="Dosya Seç", filetypes=[("HTML Files", "*.html")])
    file_listbox.delete(0, tk.END)
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)


def show_all_followers():
    t = threading.Thread(target=show_followers, args=(file_paths,))
    t.start()


def show_followers(file_paths):
    global followers_list
    followers_list.clear()
    progress_label.config(text="Takipçiler yükleniyor...")
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        names = [item.get_text() for item in soup.find_all("a", target="_blank")]
        followers_list.extend(names)
    update_table(followers_list)
    progress_label.config(text="Takipçiler yüklendi.")
    show_followers_count()  # Takipçi sayısını göster


def show_followers_count():
    if followers_list:
        messagebox.showinfo("Toplam Takipçi Sayısı", f"Toplam Takipçi Sayısı: {len(followers_list)}")
    else:
        messagebox.showwarning("Uyarı", "Henüz takipçi bulunmamaktadır.")


def show_non_followers():
    if not file_paths:
        messagebox.showwarning("Uyarı", "Lütfen önce dosyaları seçin.")
        return

    t = threading.Thread(target=find_non_followers)
    t.start()


def find_non_followers():
    global followers_list
    followers_list.clear()
    progress_label.config(text="Takip etmeyenler bulunuyor...")
    following_path = "following.html"
    if not os.path.exists(following_path):
        tk.messagebox.showerror("Hata", "following.html dosyası bulunamadı!")
        return

    with open(following_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    following_list = [item.get_text() for item in soup.find_all("a", target="_blank")]

    followers_list.clear()
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        names = [item.get_text() for item in soup.find_all("a", target="_blank")]
        followers_list.extend(names)

    non_followers_list = [follower for follower in following_list if follower not in followers_list]
    update_table(non_followers_list)
    progress_label.config(text="Takip etmeyenler bulundu.")


def search_followers():
    search_text = search_var.get().lower()
    if search_text:
        search_result = [follower for follower in followers_list if search_text in follower.lower()]
        update_table(search_result)
    else:
        update_table(followers_list)


def clear_search():
    search_var.set("")
    update_table(followers_list)


def export_to_excel():
    if followers_list:
        df = pd.DataFrame({"Takipçiler": followers_list})
        excel_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if excel_file_path:
            df.to_excel(excel_file_path, index=False)
            messagebox.showinfo("Başarılı", "Excel dosyası başarıyla oluşturuldu!")
    else:
        messagebox.showwarning("Uyarı", "Aktarılacak takipçi bulunmamaktadır.")


def export_non_followers_to_pdf():
    if followers_list:
        non_followers_list = table.get_children()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for follower in non_followers_list:
            follower_username = table.item(follower)["values"][1]
            pdf.cell(200, 10, txt=follower_username, ln=True)
            pdf.cell(200, 10, txt=f"https://www.instagram.com/{follower_username}/", ln=True)

        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            pdf.output(pdf_file_path)
            messagebox.showinfo("Başarılı", "PDF dosyası başarıyla oluşturuldu!")
    else:
        messagebox.showwarning("Uyarı", "Aktarılacak takip etmeyen kişi bulunmamaktadır.")


def open_non_followers_in_browser():
    non_followers_list = table.get_children()
    for follower in non_followers_list:
        follower_username = table.item(follower)["values"][1]
        webbrowser.open(f"https://www.instagram.com/{follower_username}/")


# Tkinter App
app = tk.Tk()
app.title("Takipçi Analiz Uygulaması V2 @Tuncay.Lore")
app.geometry("1000x700")  # Yeni boyutlar
app.configure(bg="#0f0f0f")  # Hacker temalı arka plan rengi

# Başlık Etiketi
title_label = tk.Label(app, text="Takipçi Karşılaştırma Uygulaması", font=("Courier", 24, "bold"), bg="#0f0f0f",
                       fg="#4caf50", pady=20)
title_label.pack(fill="x")

# Butonlar
button_frame = tk.Frame(app, bg="#0f0f0f")
button_frame.pack(pady=20)

select_file_button = tk.Button(button_frame, text="Dosyaları Seç ve Takipçileri Göster",
                               command=open_file_and_show_followers, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
select_file_button.grid(row=0, column=0, padx=10)

select_auto_fetch_button = tk.Button(button_frame, text="Otomatik Çek", command=open_files_and_show_followers,
                                     bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
select_auto_fetch_button.grid(row=0, column=1, padx=10)

show_all_button = tk.Button(button_frame, text="Tüm Takipçileri Göster", command=show_all_followers, bg="#4caf50",
                            fg="white", padx=10, pady=5, bd=0)
show_all_button.grid(row=0, column=2, padx=10)

show_non_followers_button = tk.Button(button_frame, text="Takip Etmeyenleri Göster", command=show_non_followers,
                                      bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
show_non_followers_button.grid(row=0, column=3, padx=10)

export_to_excel_button = tk.Button(button_frame, text="Takipçileri Excel'e Aktar", command=export_to_excel,
                                   bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
export_to_excel_button.grid(row=0, column=4, padx=10)

export_to_pdf_button = tk.Button(button_frame, text="Takip Etmeyenleri PDF'e Aktar",
                                 command=export_non_followers_to_pdf, bg="#4caf50", fg="white", padx=10, pady=5, bd=0)
export_to_pdf_button.grid(row=0, column=5, padx=10)

open_in_browser_button = tk.Button(button_frame, text="Takip Etmeyenleri Tarayıcıda Aç",
                                   command=open_non_followers_in_browser, bg="#4caf50", fg="white", padx=10, pady=5,
                                   bd=0)
open_in_browser_button.grid(row=0, column=6, padx=10)

# İlerleme Etiketi
progress_label = tk.Label(app, text="", bg="#0f0f0f", fg="#4caf50")
progress_label.pack(pady=10)

# Seçilen Dosyalar Listesi
file_listbox = tk.Listbox(app, width=90, height=5, bg="#212121", fg="white", borderwidth=0, highlightthickness=0)
file_listbox.pack(pady=10)

# Arama Çubuğu ve Temizle Butonu
search_var = tk.StringVar()
search_entry = ttk.Entry(app, textvariable=search_var, width=70, font=("Courier", 12), style="search.TEntry")
search_entry.pack(pady=5)

clear_button = tk.Button(app, text="Aramayı Temizle", command=clear_search, bg="#4caf50", fg="#0f0f0f", bd=0)
clear_button.pack(pady=5)

# Tablo ve Dikey Scrollbar
frame = tk.Frame(app, bg="#0f0f0f")
frame.pack(padx=10, pady=10)

columns = ("Sıra No.", "İsim")
table = ttk.Treeview(frame, columns=columns, show="headings", style="Custom.Treeview")
table.heading("Sıra No.", text="Sıra No.")
table.heading("İsim", text="İsim")
table.pack(side="left")

vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
vsb.pack(side="right", fill="y")
table.configure(yscrollcommand=vsb.set)

# Stil tanımları
style = ttk.Style()
style.configure("search.TEntry", foreground="#4caf50", background="#212121", bordercolor="#4caf50")
style.configure("Custom.Treeview", background="#212121", foreground="white", fieldbackground="#212121",
                highlightthickness=0)

app.mainloop()
