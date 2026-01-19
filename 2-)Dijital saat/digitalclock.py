from tkinter import Label,Tk
import time

app_window=Tk()
app_window.title("Digital Clock")
app_window.geometry("500x500")
app_window.resizable(1,1)
app_window.configure(bg="black")


text_font=("Boulder",36,'bold')
background="black"
foreground="white"
border_width=20



#saat etieti

label=Label(app_window,font=("Boulder",18),bg=background,fg=foreground)
label.grid(row=0,column=1,padx=10,pady=10)



#tarih etiketi
date_label=Label(app_window,font=("boulder",18),bg=background,fg=foreground)
date_label.grid(row=1,column=1,padx=10,pady=10)



def digitalcloc():
    time_live=time.strftime("%H:%M:%S")
    label.config(text=time_live)
    #tarih alanı
    date_info=time.strftime("%d %B %Y")
    date_label.config(text=date_info)
    label.after(200,digitalcloc)


digitalcloc()




app_window.mainloop()
