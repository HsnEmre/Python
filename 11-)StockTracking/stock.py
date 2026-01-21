import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class StokTakipUygulamasi:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stok Takip Uygulaması")
        self.root.geometry("820x520")

        # --- DB ---
        self.conn = sqlite3.connect("stock.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                id TEXT PRIMARY KEY,
                urun_adi TEXT NOT NULL,
                adet INTEGER NOT NULL,
                birim_fiyat REAL NOT NULL,
                toplam_deger REAL NOT NULL
            )
        """)
        self.conn.commit()

        # --- Layout ayarları ---
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(7, weight=1)

        # --- Giriş Alanları ---
        tk.Label(root, text="ID").grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=6)

        tk.Label(root, text="Ürün Adı").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.urun_adi_entry = tk.Entry(root)
        self.urun_adi_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=6)

        tk.Label(root, text="Adet").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.adet_entry = tk.Entry(root)
        self.adet_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=6)

        tk.Label(root, text="Birim Fiyat").grid(row=3, column=0, sticky="w", padx=10, pady=6)
        self.birim_fiyat_entry = tk.Entry(root)
        self.birim_fiyat_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=6)

        # --- Butonlar ---
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=6)
        btn_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        tk.Button(btn_frame, text="Ekle", command=self.ekle).grid(row=0, column=0, sticky="ew", padx=4)
        tk.Button(btn_frame, text="Düzelt", command=self.duzelt).grid(row=0, column=1, sticky="ew", padx=4)
        tk.Button(btn_frame, text="Sil", command=self.sil).grid(row=0, column=2, sticky="ew", padx=4)
        tk.Button(btn_frame, text="Temizle", command=self.girisleri_temizle).grid(row=0, column=3, sticky="ew", padx=4)

        # --- Arama ---
        tk.Label(root, text="Arama").grid(row=5, column=0, sticky="w", padx=10, pady=6)
        self.arama_entry = tk.Entry(root)
        self.arama_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=6)
        self.arama_entry.bind("<KeyRelease>", self.arama)

        # --- Tablo + Scrollbar ---
        table_frame = tk.Frame(root)
        table_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("ID", "Urun Adi", "Adet", "Birim Fiyat", "Toplam Deger")
        self.tablo = ttk.Treeview(table_frame, columns=cols, show="headings")
        self.tablo.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tablo.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tablo.configure(yscrollcommand=scroll_y.set)

        # başlıklar + kolon genişlikleri
        for col in cols:
            self.tablo.heading(col, text=col)
            self.tablo.column(col, width=140, anchor="w")

        self.tablo.column("ID", width=120)
        self.tablo.column("Adet", width=80, anchor="center")
        self.tablo.column("Birim Fiyat", width=110, anchor="e")
        self.tablo.column("Toplam Deger", width=120, anchor="e")

        # satır seçme
        self.tablo.bind("<ButtonRelease-1>", self.satir_sec)

        # ilk yükleme
        self.verileri_yukle()

        # kapatırken db kapansın
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------------------
    # Yardımcılar
    # -------------------------
    def on_close(self):
        try:
            self.conn.close()
        finally:
            self.root.destroy()

    def girisleri_temizle(self):
        self.id_entry.delete(0, tk.END)
        self.urun_adi_entry.delete(0, tk.END)
        self.adet_entry.delete(0, tk.END)
        self.birim_fiyat_entry.delete(0, tk.END)
        self.id_entry.focus_set()

    def tabloyu_temizle(self):
        for item in self.tablo.get_children():
            self.tablo.delete(item)

    def verileri_yukle(self):
        self.tabloyu_temizle()
        for row in self.cursor.execute("SELECT id, urun_adi, adet, birim_fiyat, toplam_deger FROM stock ORDER BY urun_adi"):
            self.tablo.insert("", "end", values=row)

    def secili_id(self):
        secili = self.tablo.selection()
        if not secili:
            return None
        values = self.tablo.item(secili[0])["values"]
        return values[0] if values else None

    def oku_form(self):
        _id = self.id_entry.get().strip()
        urun_adi = self.urun_adi_entry.get().strip()

        try:
            adet = int(self.adet_entry.get().strip())
        except ValueError:
            raise ValueError("Adet sayı olmalı.")

        try:
            birim_fiyat = float(self.birim_fiyat_entry.get().strip().replace(",", "."))
        except ValueError:
            raise ValueError("Birim fiyat sayı olmalı.")

        if not _id:
            raise ValueError("ID boş olamaz.")
        if not urun_adi:
            raise ValueError("Ürün adı boş olamaz.")
        if adet < 0:
            raise ValueError("Adet negatif olamaz.")
        if birim_fiyat < 0:
            raise ValueError("Birim fiyat negatif olamaz.")

        toplam_deger = adet * birim_fiyat
        return _id, urun_adi, adet, birim_fiyat, toplam_deger

    # -------------------------
    # CRUD
    # -------------------------
    def ekle(self):
        try:
            _id, urun_adi, adet, birim_fiyat, toplam_deger = self.oku_form()
            self.cursor.execute(
                "INSERT INTO stock (id, urun_adi, adet, birim_fiyat, toplam_deger) VALUES (?,?,?,?,?)",
                (_id, urun_adi, adet, birim_fiyat, toplam_deger)
            )
            self.conn.commit()
            self.verileri_yukle()
            self.girisleri_temizle()
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu ID zaten var. Farklı bir ID gir.")
        except Exception as ex:
            messagebox.showerror("Hata", str(ex))

    def duzelt(self):
        sec_id = self.secili_id()
        if not sec_id:
            messagebox.showwarning("Uyarı", "Önce tablodan bir satır seç.")
            return

        try:
            _id, urun_adi, adet, birim_fiyat, toplam_deger = self.oku_form()

            # Seçili satırın id'si değiştiriliyorsa önce çakışma kontrol
            if _id != sec_id:
                self.cursor.execute("SELECT 1 FROM stock WHERE id=?", (_id,))
                if self.cursor.fetchone():
                    messagebox.showerror("Hata", "Yeni ID başka bir kayıtta var.")
                    return

            self.cursor.execute(
                "UPDATE stock SET id=?, urun_adi=?, adet=?, birim_fiyat=?, toplam_deger=? WHERE id=?",
                (_id, urun_adi, adet, birim_fiyat, toplam_deger, sec_id)
            )
            self.conn.commit()
            self.verileri_yukle()
            self.girisleri_temizle()
        except Exception as ex:
            messagebox.showerror("Hata", str(ex))

    def sil(self):
        sec_id = self.secili_id()
        if not sec_id:
            messagebox.showwarning("Uyarı", "Silmek için tablodan bir satır seç.")
            return

        if not messagebox.askyesno("Onay", f"ID={sec_id} kaydı silinsin mi?"):
            return

        try:
            self.cursor.execute("DELETE FROM stock WHERE id=?", (sec_id,))
            self.conn.commit()
            self.verileri_yukle()
            self.girisleri_temizle()
        except Exception as ex:
            messagebox.showerror("Hata", str(ex))

    # -------------------------
    # Events
    # -------------------------
    def satir_sec(self, event=None):
        secili = self.tablo.selection()
        if not secili:
            return
        values = self.tablo.item(secili[0])["values"]
        if not values:
            return

        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])

        self.urun_adi_entry.delete(0, tk.END)
        self.urun_adi_entry.insert(0, values[1])

        self.adet_entry.delete(0, tk.END)
        self.adet_entry.insert(0, values[2])

        self.birim_fiyat_entry.delete(0, tk.END)
        self.birim_fiyat_entry.insert(0, values[3])

    def arama(self, event=None):
        q = self.arama_entry.get().strip().lower()

        # boşsa hepsini geri yükle
        if not q:
            self.verileri_yukle()
            return

        self.tabloyu_temizle()
        like = f"%{q}%"
        rows = self.cursor.execute(
            """
            SELECT id, urun_adi, adet, birim_fiyat, toplam_deger
            FROM stock
            WHERE lower(id) LIKE ? OR lower(urun_adi) LIKE ?
            ORDER BY urun_adi
            """,
            (like, like)
        ).fetchall()

        for row in rows:
            self.tablo.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = StokTakipUygulamasi(root)
    root.mainloop()
