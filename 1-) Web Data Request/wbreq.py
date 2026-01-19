import requests
from bs4 import BeautifulSoup

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }

#r = requests.get("https://www.bilgisayarhocam.com/")

# if r.status_code == 200:
#     print("siteden veri çekilebilir")

#     soup = BeautifulSoup(r.content, "html.parser")

#     # sayfanın ilk <p> etiketini yazdır
#     print(soup.p)
# else:
#     print("olmadi ❌", r.status_code)

# if r.status_code==200:
#     print("veri çekilebilir")
# else:
#     print("veri çeklilemez")


# soup=BeautifulSoup(r.content,"html.parser")
# print(soup.prettify())
# print(soup.head.title.text)
# print(soup.find("p").text)
# fa=soup.find_all("p")
# for i in fa:
#     print(i.text)

# div_cek=soup.find("div",{"class":"the-subtitle"})
# print(div_cek.get("href"))



#-----------------Yağ Fiyatları Link-----------------------------#

url=requests.get("https://www.gittigidiyor.com/gida/siviyag")
if url.status_code==200:
    print("sistemden veri çekilebilir")
else:
    print("sistemden veri çeklilemez")

soup= BeautifulSoup(url.content,"html.parer")

for i in soup.find("ul", {"class": "catalog-view"}).find_all("li", class_="gg-uw-6"):
    # print(i)
    baslık_al=i.find("div",{"class":"gg-w-24"}).span.text
    # print(baslık_al)
    fiyat_al=i.find("p",{"class":"fiyat"}).text.strip()
    print(fiyat_al)

