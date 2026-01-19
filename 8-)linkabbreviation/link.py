import tkinter as tk
from tkinter import messagebox

import pyperclip
import requests

short_url_value = ""  # global saklayacağız


def shorten_url():
    global short_url_value
    long_url = entry.get().strip()

    if not long_url:
        messagebox.showwarning("Uyarı", "Lütfen bir link gir.")
        return

    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={long_url}", timeout=10)
        response.raise_for_status()
        short_url_value = response.text.strip()

        result_label.config(text=f"Short URL: {short_url_value}")
        copy_button.config(state=tk.NORMAL)

    except Exception as ex:
        messagebox.showerror("Hata", f"URL kısaltılamadı:\n{ex}")
        copy_button.config(state=tk.DISABLED)


def copy_to_clipboard():
    if not short_url_value:
        messagebox.showwarning("Uyarı", "Önce linki kısalt.")
        return

    pyperclip.copy(short_url_value)
    messagebox.showinfo("Success", "URL copied to clipboard")


# tkinter area
app = tk.Tk()
app.title("Link Abbreviation")
app.geometry("450x220")

label = tk.Label(app, text="Long link")
label.pack(pady=10)

entry = tk.Entry(app, width=55)
entry.pack(pady=10)

shorten_button = tk.Button(app, text="Shorten URL", command=shorten_url)
shorten_button.pack(pady=10)

result_label = tk.Label(app, text="Short URL burada görünecek")
result_label.pack(pady=10)

copy_button = tk.Button(app, text="Copy to clipboard", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack(pady=10)

app.mainloop()
