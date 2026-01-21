import tkinter as tk
from tkinter import ttk,messagebox

def hesapla():
    try:
        resolution=resulation_var.get()
        duration=int(duration_var.get())

        #bit hizlarini cozunurluklerini gore ayarlayalim
        bit_rates={
            "360p":750,
            "480p":1500,
            "720p":3000,
            "1080p":4500,

        }
        bit_rate=bit_rates[resolution]
        #dosya boyutuna gore hesaplama
        file_size_mb=bit_rate*duration*60/8/1024
        result_label.config(text=f"{file_size_mb} MB")
    except ValueError:
        messagebox.showerror("Error","Please enter a valid resolution")

#ana pencee
root=tk.Tk()
root.title("Video Size")
root.geometry("400x450")
root.resizable(False,False)

#stil ayarlari
style=ttk.Style()
style.configure("TLabel",font=("Helvatica",12))
style.configure("TButton",font=("Helvatica",12))
style.configure("TCombobox",font=("Helvatica",12))

#buton stili
style.map("TButton",foreground=[('active','black'),('!disabled','black')],
          background=[('active','#45a049'),('!disabled','#45a049')])

#cozunurluk secimi
resulation_label=ttk.Label(root,text="Resolution")
resulation_label.pack(pady=10)
resulation_var=tk.StringVar()
resulation_combobox=ttk.Combobox(root,textvariable=resulation_var,state="readonly")
resulation_combobox['values']=('360p','480p','720p','1080p')
resulation_combobox.current(0)
resulation_combobox.pack(pady=10)



#sure girisi
duration_label=ttk.Label(root,text="Duration")
duration_label.pack(pady=10)
duration_var=tk.StringVar()
duration_entry=ttk.Entry(root,textvariable=duration_var)
duration_entry.pack(pady=10)

#hesapla butonu
calculate_button=ttk.Button(root,text="Calculate",command=hesapla)
calculate_button.pack(pady=10)

#sonuc etiketi
result_label=ttk.Label(root,text="Result")
result_label.pack(pady=10)

root.mainloop()
























