import instaloader
import tkinter as tk 
from tkinter import messagebox

def download_post():
    ##kullanici adini alma
    user_name=entry_username.get()

    try:
        #nesne olustur
        bot=instaloader.Instaloader()

        ##profil nesnesi olusturma
        profile=instaloader.Profile.from_username(bot.context,user_name)
        #kullanici gonderilerini al 
        posts=profile.get_posts()
        #gonderileri indir


        for index,post in enumerate(posts,1):
            bot.download_post(post,target=f"{profile.username}_{index}")

        #basari mesaji
        messagebox.showinfo("Basarili","gonderiler indirildi")
    except Exception as e:
        messagebox.showerror("Hata",str(e))    

            
#tkinter
root=tk.Tk()
root.title("Instagram post downloader")
root.geometry("300x200")

##kullanici adi
label=tk.Label(root,text="Kullanici adi:")
label.pack(pady=10)

#kullanici adi giris
entry_username=tk.Entry(root)
entry_username.pack()


#indirme butonu
download_button=tk.Button(root,text="Bilgileri indir",command=download_post)
download_button.pack()

root.mainloop()