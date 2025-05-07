import sqlite3
import requests
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Telegram Bot API bilgileri
TELEGRAM_BOT_TOKEN = "8137856403:AAFjP28Inr4hqNxrQJNAp-ek7ZxkHkiyOAk"
CAYCI_CHAT_ID = "5977292175"

# Veritabanı bağlantısı
def veritabani_baglanti():
    conn = sqlite3.connect("siparisler.db")
    conn.row_factory = sqlite3.Row  # Verileri sözlük formatında almak için
    return conn

# Telegram mesaj gönderme fonksiyonu
def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CAYCI_CHAT_ID, "text": mesaj}
    response = requests.post(url, data=data)
    print("Telegram API Yanıtı:", response.status_code, response.json())  

# Ana sayfa (Sipariş formu)
@app.route("/")
def ana_sayfa():
    return render_template("index.html")

# Sipariş alma fonksiyonu
@app.route("/siparis", methods=["POST"])
def siparis():
    icecekler = request.form.getlist("icecek[]")
    adetler = request.form.getlist("adet[]")
    seker_durumlari = request.form.getlist("seker_durumu[]")
    lokasyon = request.form.get("lokasyon")

    # Hata ayıklama: Formdan gelen verileri terminalde yazdır
    print("📌 Gelen Sipariş Verileri:")
    print("İçecekler:", icecekler)
    print("Adetler:", adetler)
    print("Şeker Durumları:", seker_durumlari)
    print("Lokasyon:", lokasyon)

    # Eğer listeler boşsa hata mesajı ver
    if not icecekler or not adetler or not seker_durumlari or not lokasyon:
        return "Hata: Sipariş verileri eksik veya yanlış formatta!", 400

    conn = veritabani_baglanti()
    cursor = conn.cursor()

    mesaj = "☕ Yeni siparişiniz var!\n\n"
    for i in range(len(icecekler)):
        cursor.execute("INSERT INTO siparisler (icecek, adet, lokasyon, seker_durumu) VALUES (?, ?, ?, ?)", 
                       (icecekler[i], adetler[i], lokasyon, seker_durumlari[i]))
        mesaj += f"🍽 **Sipariş:** {icecekler[i]}\n🔢 **Adet:** {adetler[i]}\n🍬 **Şeker Durumu:** {seker_durumlari[i]}\n\n"

    conn.commit()
    conn.close()

    mesaj += f"📍 **Lokasyon:** {lokasyon}\n\nSiparişiniz en kısa sürede hazırlanacaktır. 😊"
    telegram_gonder(mesaj)

    return render_template("onay.html")

if __name__ == "__main__":
    app.run(debug=True)