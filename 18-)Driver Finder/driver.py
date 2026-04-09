import wmi  # Windows bileşenleri için
import json
import os
import tkinter as tk
from tkinter import ttk
import webbrowser


def list_drivers(save_to_file=False):
    try:
        computer = wmi.WMI()
        drivers = []

        for device in computer.Win32_PnPEntity():  # Tak çalıştır cihazlar
            if device.Name and device.DeviceID:
                status = "Yuklu" if device.Status == "OK" else "Yuklu degil"

                driver_info = {
                    "Cihaz": device.Name,
                    "Device ID": device.DeviceID,
                    "Uretici": getattr(device, "Manufacturer", "Bilinmiyor"),
                    "Durum": status,
                    "Surucu Linki": "Surucuyu Arastir"
                }
                drivers.append(driver_info)

        if save_to_file:
            file_path = os.path.join(os.getcwd(), "drivers_info.json")
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(drivers, file, ensure_ascii=False, indent=4)
            print(f"Surucu bilgileri {file_path} dosyasina kayit edildi")

        return drivers

    except Exception as e:
        print(f"Hata: {str(e)}")
        return []


def display_drivers_in_table():
    drivers = list_drivers()

    root = tk.Tk()
    root.title("Bilgisayar Suruculeri")
    root.geometry("1000x500")

    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = tk.Label(search_frame, text="Ara:")
    search_label.pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    columns = ("Cihaz", "Device ID", "Uretici", "Durum", "Surucu Linki")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    def populate_treeview(data):
        for item in tree.get_children():
            tree.delete(item)

        for driver in data:
            item_id = tree.insert("", tk.END, values=(
                driver.get("Cihaz", "Bilinmiyor"),
                driver.get("Device ID", "Bilinmiyor"),
                driver.get("Uretici", "Bilinmiyor"),
                driver.get("Durum", "Bilinmiyor"),
                "Surucuyu Arastir"
            ))

            if driver.get("Durum") == "Yuklu":
                tree.item(item_id, tags=("yuklu",))
            else:
                tree.item(item_id, tags=("yuklu_degil",))

    tree.tag_configure("yuklu", background="lightgreen")
    tree.tag_configure("yuklu_degil", background="lightcoral")

    populate_treeview(drivers)
    tree.pack(expand=True, fill="both")

    def search_drivers(event=None):
        query = search_entry.get().lower()

        filtered_drivers = [
            driver for driver in drivers
            if query in driver.get("Cihaz", "").lower()
            or query in driver.get("Device ID", "").lower()
            or query in driver.get("Uretici", "").lower()
            or query in driver.get("Durum", "").lower()
        ]

        populate_treeview(filtered_drivers)

    search_entry.bind("<KeyRelease>", search_drivers)

    def on_treeview_double_click(event):
        selected = tree.selection()
        if not selected:
            return

        item = selected[0]
        device_name = tree.item(item, "values")[0]
        driver_link = f"https://www.google.com/search?q={device_name}+driver"
        webbrowser.open(driver_link)

    tree.bind("<Double-1>", on_treeview_double_click)

    root.mainloop()


if __name__ == "__main__":
    display_drivers_in_table()