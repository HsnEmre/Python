from flask import Flask, render_template, request
import os
import contextlib

# stderr yönlendirmesi ile import aşamasındaki logları bastırma
with open(os.devnull, 'w') as devnull, contextlib.redirect_stderr(devnull):
    import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Oturum yönetimi için gerekli

# API anahtarını yapılandırma
genai.configure(api_key="BURAYA APİ KEYİNİ GİR")

# Model oluşturma konfigürasyonu
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Parametre	Açıklama
# temperature	Çıktının rastgelelik derecesini belirler. 1 değeri varsayılan dengeli bir seviye olup, daha büyük değerler (örn. 1.5) daha yaratıcı ve rastgele çıktılar, daha küçük değerler (örn. 0.2) ise daha tutarlı ve belirli kalıplara dayalı çıktılar üretir.
# top_p	Çekirdek örnekleme (nucleus sampling) tekniğini kontrol eder. 0.95 değeri, modelin %95 olasılıkla en yüksek ihtimalli kelimeleri seçmesini sağlar. Düşük olursa daha dar kelime seçimi olur, yüksek olursa daha geniş kelime havuzundan seçim yapar.
# top_k	Kelime seçim havuzunu sınırlar. 40 değeri, modelin her adımdaki en olası 40 kelime arasından seçim yapmasını sağlar. Daha düşük olursa daha kontrollü, yüksek olursa daha rastgele olur.
# max_output_tokens	Çıktı uzunluğunu sınırlar. 8192 değeri, modelin maksimum 8192 kelime veya token üretmesine izin verir. Eğer yanıtlar çok kısa geliyorsa, bu değeri artırmak gerekir.
# response_mime_type	Modelin çıktısının MIME türünü belirler. "text/plain" değeri, düz metin formatında cevap üreteceğini gösterir. Alternatif olarak "application/json" gibi farklı formatlarda da olabilir.


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# Kurumsal metin (sadece arka planda kullanılacak, kullanıcıya gösterilmeyecek)
corporate_text = (
    "Aşağıda \"Hasan Emre  İşletmesi\" için hazırlanmış kurumsal işletme kuralları yer almaktadır. "
    "Bu metin belgesinde işletmenin çalışma saatleri, çalışma günleri, kurs bilgileri ve fiyatları gibi temel "
    "bilgiler detaylandırılmıştır.\n\n"
    "──────────────────────────────\n"
    "Tuncaylore İşletmesi Kurumsal Kuralları\n\n"
    "1. İşletme Tanımı\n"
    "Tuncaylore İşletmesi, eğitim alanında faaliyet gösteren, kurumsal yapıya sahip bir eğitim kuruluşudur. "
    "İşletme, çeşitli kurslar aracılığıyla öğrencilere bilgi ve beceri kazandırmayı hedeflemektedir.\n\n"
    "2. Çalışma Saatleri ve Günleri\n\n"
    "Çalışma Saatleri: 07:00 – 17:00\n"
    "İşletme, sabah 07:00’de açılır ve akşam 17:00’de kapanır.\n"
    "Çalışma Günleri: Pazartesi, Salı, Çarşamba, Perşembe, Cuma\n"
    "İşletme hafta içi günlerinde hizmet vermektedir.\n"
    "(Not: Hafta sonları ve resmi tatillerde işletme kapalıdır.)\n\n"
    "3. Kurslar ve Ücretlendirme\n\n"
    "Tuncaylore İşletmesi bünyesinde aşağıdaki kurslar sunulmaktadır:\n"
    "   - Python Kursu: 199 TL\n"
    "   - Web Tasarım Kursu: 199 TL\n"
    "   - Hack Kursu: 199 TL\n\n"
    "   -En uygun kursumu CMD ile kodlama 129 TL\n\n"
    "-Kargo Adresimi : İstanbul/Kadiköy Boğa sokağı no/24 daire-2"
    "Cevap verirken bana bir müşteriymişim gibi davran ve direkt sorduğum soruya tam cevap ya da metinde benzer bir yer görürsen oradaki veriyi aktar ve cevap verirken emoji kullan ki samimi gözükürsün - Kullanıcın sorduğu sorulara bir işletme sahibi gibi cevap ver"
)

# Sohbet oturumunu başlatıyoruz (kurumsal metin arka planda kullanılacak)
chat_session = model.start_chat(history=[])

# Sohbet geçmişi (başlangıçta sadece hoş geldiniz mesajı)
conversation = [
    {"sender": "Tuncay Lore", "message": "Sisteme Hoşgeldiniz"}
]

@app.route("/", methods=["GET", "POST"])
def chat():
    global conversation
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input.lower() in ["exit", "quit"]:
            conversation.append({"sender": "Sistem", "message": "Sohbet sonlandırıldı."})
            return render_template("chat.html", conversation=conversation)
        
        # Kullanıcı mesajını sohbet geçmişine ekle
        conversation.append({"sender": "Müşteri", "message": user_input})
        
        # Kullanıcının sorgusunu, kurumsal metinle birleştirerek modele gönderiyoruz
        combined_input = corporate_text + "\nSoru: " + user_input
        response = chat_session.send_message(combined_input)
        
        conversation.append({"sender": "Tuncay Lore", "message": response.text})
    
    return render_template("chat.html", conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask,render_template,request
import os 
import contextlib

#log kayitlarini bastirma
with open(os.devnull,'w') as devnull,contextlib.redirect_stderr__strderr(devnull):
    import google.generativeai as genai

app=Flask(__name__)    
#api anahtarini cagir

genai.configure(api_key="your api key")

generation_config={
    "tempature":1,
    "top_p":0.95,
    "top_k":40,
    "max_output_tokens":8192,
    "response_mine_type":"text/plain",
}

mode=genai.GenerativeModel(
    model_name="gemini=2.0-flash",
    generation_config=generation_config
)

