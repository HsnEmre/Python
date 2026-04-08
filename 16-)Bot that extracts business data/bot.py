import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException,
)
import time
import threading
import pandas as pd
import webbrowser
import re


class GoogleMapsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Haritalar Arama Botu")
        self.root.geometry("1120x760")
        self.root.configure(bg="#FFFFFF")

        self.is_running = False
        self.scraped_data = []

        self.frame_top = tk.Frame(self.root, bg="#FFFFFF", bd=10, relief=tk.FLAT)
        self.frame_top.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.22)

        self.label_search = tk.Label(
            self.frame_top,
            text="Aramak İstediğiniz Kelime:",
            bg="#FFFFFF",
            font=("Helvetica", 10, "bold"),
        )
        self.label_search.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_search = tk.Entry(
            self.frame_top,
            font=("Helvetica", 10),
            bd=3,
            relief=tk.FLAT,
            fg="black",
            bg="#F8D8E8",
            width=40,
        )
        self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.label_count = tk.Label(
            self.frame_top,
            text="Çekilecek İşletme Sayısı:",
            bg="#FFFFFF",
            font=("Helvetica", 10, "bold"),
        )
        self.label_count.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_count = tk.Entry(
            self.frame_top,
            font=("Helvetica", 10),
            bd=3,
            relief=tk.FLAT,
            fg="black",
            bg="#F8D8E8",
            width=15,
        )
        self.entry_count.insert(0, "10")
        self.entry_count.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.button_frame = tk.Frame(self.frame_top, bg="#FFFFFF")
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="w")

        self.button_start = tk.Button(
            self.button_frame,
            text="Verileri Çek",
            command=self.start_scraping_thread,
            font=("Helvetica", 10, "bold"),
            bg="#FF0000",
            fg="#FFFFFF",
            relief=tk.RAISED,
            padx=10,
            pady=6,
        )
        self.button_start.pack(side=tk.LEFT, padx=5)

        self.button_export = tk.Button(
            self.button_frame,
            text="Excel'e Aktar",
            command=self.export_to_excel,
            font=("Helvetica", 10, "bold"),
            bg="#008000",
            fg="#FFFFFF",
            relief=tk.RAISED,
            padx=10,
            pady=6,
        )
        self.button_export.pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar(value="Hazır")
        self.label_status = tk.Label(
            self.frame_top,
            textvariable=self.status_var,
            bg="#FFFFFF",
            fg="#333333",
            font=("Helvetica", 10),
        )
        self.label_status.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        self.frame_bottom = tk.Frame(self.root, bg="#FFFFFF", bd=10, relief=tk.FLAT)
        self.frame_bottom.place(relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67)

        columns = ("İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Mesaj Gönder")
        self.tree = ttk.Treeview(
            self.frame_bottom,
            columns=columns,
            show="headings",
            height=18,
        )

        self.tree.heading("İşletme Adı", text="İşletme Adı")
        self.tree.heading("Adres", text="Adres")
        self.tree.heading("İletişim No", text="İletişim No")
        self.tree.heading("Mesaj Atıldı Mı?", text="Mesaj Atıldı Mı?")
        self.tree.heading("Mesaj Gönder", text="Mesaj Gönder")

        self.tree.column("İşletme Adı", width=220)
        self.tree.column("Adres", width=420)
        self.tree.column("İletişim No", width=150)
        self.tree.column("Mesaj Atıldı Mı?", width=120, anchor="center")
        self.tree.column("Mesaj Gönder", width=120, anchor="center")

        self.scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#F5F5F5",
            foreground="black",
            rowheight=28,
            fieldbackground="#F5F5F5",
        )
        style.map("Treeview", background=[("selected", "#000000")], foreground=[("selected", "#FFFFFF")])

        self.tree.bind("<Button-1>", self.on_tree_click)

    def set_status(self, text: str):
        self.root.after(0, lambda: self.status_var.set(text))

    def set_button_state(self, enabled: bool):
        def _update():
            self.button_start.config(
                state=tk.NORMAL if enabled else tk.DISABLED,
                text="Verileri Çek" if enabled else "Çekiliyor..."
            )
        self.root.after(0, _update)

    def clear_table(self):
        def _clear():
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.scraped_data.clear()
        self.root.after(0, _clear)

    def add_row(self, business_name, address, phone_number):
        def _insert():
            row = (business_name, address, phone_number, "Hayır", "Mesaj Gönder")
            self.scraped_data.append(row)
            self.tree.insert("", "end", values=row)
        self.root.after(0, _insert)

    def show_error(self, msg):
        self.root.after(0, lambda: messagebox.showerror("Hata", msg))

    def show_info(self, title, msg):
        self.root.after(0, lambda: messagebox.showinfo(title, msg))

    def start_scraping_thread(self):
        if self.is_running:
            return

        search_query = self.entry_search.get().strip()
        if not search_query:
            messagebox.showwarning("Uyarı", "Lütfen bir arama terimi girin.")
            return

        try:
            target_count = int(self.entry_count.get().strip())
            if target_count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Uyarı", "Çekilecek işletme sayısı geçerli bir sayı olmalı.")
            return

        self.is_running = True
        self.clear_table()
        self.set_button_state(False)
        self.set_status("Tarayıcı başlatılıyor...")

        thread = threading.Thread(target=self.scrape_data, daemon=True)
        thread.start()

    def build_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--lang=tr-TR")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(60)
        return driver

    def try_accept_dialogs(self, driver):
        possible_buttons = [
            (By.XPATH, "//button[contains(., 'Tümünü kabul et')]"),
            (By.XPATH, "//button[contains(., 'Kabul et')]"),
            (By.XPATH, "//button[contains(., 'Accept all')]"),
            (By.XPATH, "//button[contains(., 'I agree')]"),
            (By.XPATH, "//button[@aria-label='Tümünü kabul et']"),
        ]

        for by, selector in possible_buttons:
            try:
                btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector)))
                btn.click()
                time.sleep(1.5)
                return
            except Exception:
                pass

    def wait_for_search_box(self, driver):
        wait = WebDriverWait(driver, 25)

        # Önce olası popup/çerezleri geçmeye çalış
        self.try_accept_dialogs(driver)

        selectors = [
            (By.ID, "searchboxinput"),
            (By.CSS_SELECTOR, "input[aria-label*='Ara']"),
            (By.CSS_SELECTOR, "input[aria-label*='Search']"),
            (By.CSS_SELECTOR, "input#searchboxinput"),
        ]

        last_error = None
        for selector in selectors:
            try:
                elem = wait.until(EC.element_to_be_clickable(selector))
                return elem
            except Exception as ex:
                last_error = ex

        raise TimeoutException(f"Arama kutusu bulunamadı. Son hata: {last_error}")

    def wait_for_results_feed(self, driver):
        wait = WebDriverWait(driver, 20)
        feed_selectors = [
            (By.XPATH, "//div[@role='feed']"),
            (By.CSS_SELECTOR, "div[role='feed']"),
        ]

        for selector in feed_selectors:
            try:
                return wait.until(EC.presence_of_element_located(selector))
            except Exception:
                pass

        return None

    def get_business_cards(self, driver):
        selectors = [
            (By.CSS_SELECTOR, "a.hfpxzc"),
            (By.CSS_SELECTOR, "div.Nv2PK a.hfpxzc"),
            (By.CSS_SELECTOR, "div.Nv2PK"),
        ]

        for by, selector in selectors:
            try:
                elements = driver.find_elements(by, selector)
                if elements:
                    return elements
            except Exception:
                pass

        return []

    def safe_click(self, driver, element):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.click()
            return True
        except (ElementClickInterceptedException, StaleElementReferenceException, WebDriverException):
            try:
                driver.execute_script("arguments[0].click();", element)
                return True
            except Exception:
                return False

    def extract_text_first(self, driver, selectors):
        for by, selector in selectors:
            try:
                el = driver.find_element(by, selector)
                text = el.text.strip()
                if text:
                    return text
            except Exception:
                pass
        return "Bilgi bulunamadı"

    def normalize_phone(self, raw_phone):
        if not raw_phone or raw_phone == "Bilgi bulunamadı":
            return "Bilgi bulunamadı"

        digits = re.sub(r"\D", "", raw_phone)

        if digits.startswith("90") and len(digits) >= 12:
            return f"+{digits}"
        if digits.startswith("0") and len(digits) >= 11:
            return f"+90{digits[1:11]}"
        if len(digits) >= 10:
            return f"+90{digits[-10:]}"
        return "Bilgi bulunamadı"

    def extract_phone(self, driver):
        phone_selectors = [
            (By.CSS_SELECTOR, "button[data-item-id^='phone']"),
            (By.CSS_SELECTOR, "button[data-tooltip='Telefon numarasını kopyala']"),
            (By.XPATH, "//button[contains(@data-item-id, 'phone')]"),
        ]

        for by, selector in phone_selectors:
            try:
                el = driver.find_element(by, selector)
                text = el.text.strip()
                if text:
                    return self.normalize_phone(text)

                data_item = el.get_attribute("data-item-id") or ""
                if "phone:tel:" in data_item:
                    raw = data_item.split("phone:tel:")[-1]
                    return self.normalize_phone(raw)
            except Exception:
                pass

        return "Bilgi bulunamadı"

    def open_business_and_extract(self, driver, card):
        if not self.safe_click(driver, card):
            return None

        time.sleep(2.0)

        name = self.extract_text_first(driver, [
            (By.CSS_SELECTOR, "h1.DUwDvf"),
            (By.CLASS_NAME, "DUwDvf"),
            (By.CSS_SELECTOR, "div.fontHeadlineLarge"),
        ])

        if not name or name == "Bilgi bulunamadı":
            return None

        address = self.extract_text_first(driver, [
            (By.CSS_SELECTOR, "button[data-item-id='address'] .Io6YTe"),
            (By.CSS_SELECTOR, "button[data-item-id='address']"),
            (By.XPATH, "//button[@data-item-id='address']"),
        ])

        phone = self.extract_phone(driver)

        return {
            "name": name,
            "address": address,
            "phone": phone,
        }

    def scroll_results_panel(self, driver, feed):
        try:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 1400;", feed)
            time.sleep(2)
            return
        except Exception:
            pass

        try:
            actions = ActionChains(driver)
            actions.move_to_element(feed).click(feed).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
        except Exception:
            pass

    def scrape_data(self):
        driver = None
        added_names = set()

        try:
            search_query = self.entry_search.get().strip()
            target_count = int(self.entry_count.get().strip())

            driver = self.build_driver()
            self.set_status("Google Maps açılıyor...")
            driver.get("https://www.google.com/maps")

            search_box = self.wait_for_search_box(driver)
            self.set_status("Arama yapılıyor...")
            search_box.clear()
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.ENTER)

            time.sleep(4)
            feed = self.wait_for_results_feed(driver)

            if feed is None:
                raise Exception("Sonuç listesi bulunamadı. Arama sonucu ekranı açılmadı.")

            self.set_status("İşletmeler çekiliyor...")

            no_new_rounds = 0

            while len(added_names) < target_count and no_new_rounds < 8:
                cards = self.get_business_cards(driver)

                if not cards:
                    self.scroll_results_panel(driver, feed)
                    no_new_rounds += 1
                    continue

                before_count = len(added_names)

                for i in range(len(cards)):
                    if len(added_names) >= target_count:
                        break

                    try:
                        cards = self.get_business_cards(driver)
                        if i >= len(cards):
                            break

                        result = self.open_business_and_extract(driver, cards[i])
                        if not result:
                            continue

                        business_name = result["name"].strip()
                        if business_name in added_names:
                            continue

                        added_names.add(business_name)
                        self.add_row(
                            business_name,
                            result["address"],
                            result["phone"],
                        )
                        self.set_status(f"{len(added_names)} / {target_count} işletme çekildi...")
                        time.sleep(1.0)

                    except StaleElementReferenceException:
                        continue
                    except Exception:
                        continue

                if len(added_names) == before_count:
                    no_new_rounds += 1
                else:
                    no_new_rounds = 0

                self.scroll_results_panel(driver, feed)

            self.set_status(f"Tamamlandı. {len(added_names)} işletme çekildi.")
            self.show_info("Bitti", f"{len(added_names)} adet işletme başarıyla çekildi.")

        except TimeoutException:
            current_url = ""
            page_title = ""
            try:
                if driver:
                    current_url = driver.current_url
                    page_title = driver.title
            except Exception:
                pass

            msg = (
                "Google Maps arama kutusu veya sonuç listesi zamanında bulunamadı.\n\n"
                f"Sayfa başlığı: {page_title}\n"
                f"URL: {current_url}\n\n"
                "Bu genelde çerez ekranı, geç yükleme veya Google Maps arayüz değişikliği yüzünden olur."
            )
            self.set_status("Zaman aşımı oluştu.")
            self.show_error(msg)

        except Exception as e:
            self.set_status("Hata oluştu.")
            self.show_error(str(e))

        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

            self.is_running = False
            self.set_button_state(True)

    def export_to_excel(self):
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            data.append(values)

        if not data:
            messagebox.showwarning("Uyarı", "Aktarılacak veri yok.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        df = pd.DataFrame(
            data,
            columns=["İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Mesaj Gönder"]
        )
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Başarılı", "Veriler Excel dosyasına aktarıldı.")

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        if column != "#5":
            return

        selected_item = self.tree.identify_row(event.y)
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        values = item["values"]
        phone_number = values[2]

        if phone_number and phone_number != "Bilgi bulunamadı":
            try:
                wa_number = phone_number.replace("+", "")
                webbrowser.open(f"https://wa.me/{wa_number}")
                self.tree.set(selected_item, column="Mesaj Atıldı Mı?", value="Evet")
            except Exception as e:
                messagebox.showerror("Hata", f"Mesaj penceresi açılamadı: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleMapsApp(root)
    root.mainloop()
# Gerekli pip paketleri:
# selenium, pandas, tk


# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import threading
# import pandas as pd
# import webbrowser
# import re

# class GoogleMapsApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Google Haritalar Arama Botu")
#         self.root.geometry("1100x750")
#         self.root.configure(bg="#FFFFFF")

#         # UI Tasarımı
#         self.frame_top = tk.Frame(self.root, bg="#FFFFFF", bd=10)
#         self.frame_top.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.25)

#         tk.Label(self.frame_top, text="Aramak İstediğiniz Kelime:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
#         self.entry_search = tk.Entry(self.frame_top, font=("Helvetica", 10), bd=2, bg="#F0F0F0")
#         self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#         tk.Label(self.frame_top, text="Çekilecek İşletme Sayısı:", bg="#FFFFFF", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
#         self.entry_count = tk.Entry(self.frame_top, font=("Helvetica", 10), bd=2, bg="#F0F0F0")
#         self.entry_count.insert(0, "10")
#         self.entry_count.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

#         self.button_frame = tk.Frame(self.frame_top, bg="#FFFFFF")
#         self.button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

#         self.button_start = tk.Button(self.button_frame, text="Verileri Çek", command=self.start_scraping_thread, bg="#FF0000", fg="white", font=("Helvetica", 10, "bold"), padx=15)
#         self.button_start.pack(side=tk.LEFT, padx=5)

#         self.button_export = tk.Button(self.button_frame, text="Excel'e Aktar", command=self.export_to_excel, bg="#008000", fg="white", font=("Helvetica", 10, "bold"), padx=15)
#         self.button_export.pack(side=tk.LEFT, padx=5)

#         # Tablo
#         self.frame_bottom = tk.Frame(self.root, bg="#FFFFFF", bd=10)
#         self.frame_bottom.place(relx=0.02, rely=0.3, relwidth=0.96, relheight=0.65)

#         columns = ("İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Mesaj Gönder")
#         self.tree = ttk.Treeview(self.frame_bottom, columns=columns, show='headings')
        
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=150)

#         self.tree.column("Adres", width=300)
#         self.tree.column("Mesaj Gönder", width=100)
        
#         self.scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscroll=self.scrollbar.set)
#         self.scrollbar.pack(side="right", fill="y")
#         self.tree.pack(fill=tk.BOTH, expand=True)

#         self.tree.bind("<Double-1>", self.on_tree_click)

#     def start_scraping_thread(self):
#         if not self.entry_search.get():
#             messagebox.showwarning("Uyarı", "Lütfen bir arama terimi girin!")
#             return
#         self.button_start.config(state=tk.DISABLED, text="Çekiliyor...")
#         # Tabloyu temizle
#         for item in self.tree.get_children():
#             self.tree.delete(item)
            
#         thread = threading.Thread(target=self.scrape_data, daemon=True)
#         thread.start()

#     def scrape_data(self):
#         search_query = self.entry_search.get()
#         try:
#             target_count = int(self.entry_count.get())
#         except:
#             target_count = 10

#         scraped_count = 0
#         processed_names = set()
#         driver = None

#         try:
#             options = webdriver.ChromeOptions()
#             options.add_argument("--disable-notifications")
#             options.add_argument("--disable-blink-features=AutomationControlled")
#             options.add_experimental_option("excludeSwitches", ["enable-automation"])
#             options.add_experimental_option('useAutomationExtension', False)
            
#             # Selenium 4.6+ sürümü için otomatik sürücü yönetimi
#             driver = webdriver.Chrome(options=options)
#             wait = WebDriverWait(driver, 15)

#             driver.get("https://www.google.com.tr/maps/")
            
#             search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
#             search_box.send_keys(search_query)
#             search_box.send_keys(Keys.ENTER)
            
#             time.sleep(5)

#             while scraped_count < target_count:
#                 # İşletme kartlarını bul
#                 business_elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                
#                 if not business_elements:
#                     time.sleep(2)
#                     continue

#                 for i in range(len(business_elements)):
#                     if scraped_count >= target_count: break
                    
#                     try:
#                         # Listeyi tazele
#                         current_elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
#                         if i >= len(current_elements): break
                        
#                         biz = current_elements[i]
#                         driver.execute_script("arguments[0].scrollIntoView();", biz)
#                         time.sleep(0.5)
#                         biz.click()
#                         time.sleep(2) # Bilgilerin dolması için kritik bekleme

#                         # Detayları çek
#                         try:
#                             name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
#                         except:
#                             continue
                        
#                         if name in processed_names: continue
                        
#                         address = "Bilgi yok"
#                         phone = "Bilgi yok"
                        
#                         try:
#                             address = driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']").text
#                         except: pass
                        
#                         try:
#                             phone_elem = driver.find_element(By.CSS_SELECTOR, "[data-item-id^='phone:tel:']")
#                             raw_phone = phone_elem.get_attribute("data-item-id").replace("phone:tel:", "").replace(" ", "")
#                             clean_phone = re.sub(r'\D', '', raw_phone)
#                             if clean_phone.startswith("0"): clean_phone = "90" + clean_phone[1:]
#                             elif not clean_phone.startswith("90"): clean_phone = "90" + clean_phone
#                             phone = clean_phone
#                         except: pass

#                         self.tree.insert("", "end", values=(name, address, phone, "Hayır", "MESAJ AT"))
#                         processed_names.add(name)
#                         scraped_count += 1
                        
#                     except Exception:
#                         continue

#                 # Scroll yap
#                 try:
#                     scroll_panel = driver.find_element(By.XPATH, "//div[@role='feed']")
#                     driver.execute_script("arguments[0].scrollTop += 1200", scroll_panel)
#                     time.sleep(2)
#                 except:
#                     break

#         except Exception as e:
#             messagebox.showerror("Hata", f"Tarayıcı hatası: {e}")
#         finally:
#             if driver:
#                 driver.quit()
#             self.button_start.config(state=tk.NORMAL, text="Verileri Çek")
#             messagebox.showinfo("Bitti", f"{scraped_count} adet işletme başarıyla çekildi.")

#     def export_to_excel(self):
#         data = []
#         for item in self.tree.get_children():
#             data.append(self.tree.item(item, "values"))
        
#         if not data:
#             messagebox.showwarning("Hata", "Aktarılacak veri yok!")
#             return

#         file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
#         if file_path:
#             df = pd.DataFrame(data, columns=["İşletme Adı", "Adres", "İletişim No", "Mesaj Atıldı Mı?", "Buton"])
#             df.to_excel(file_path, index=False)
#             messagebox.showinfo("Başarılı", "Veriler Excel'e aktarıldı.")

#     def on_tree_click(self, event):
#         item_id = self.tree.identify_row(event.y)
#         column = self.tree.identify_column(event.x)
#         if column == "#5" and item_id:
#             values = self.tree.item(item_id, "values")
#             phone = values[2]
#             if phone != "Bilgi yok":
#                 webbrowser.open(f"https://wa.me/{phone}")
#                 self.tree.set(item_id, column="Mesaj Atıldı Mı?", value="Evet")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = GoogleMapsApp(root)
#     root.mainloop()