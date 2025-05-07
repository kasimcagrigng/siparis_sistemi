import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect("siparisler.db")
cursor = conn.cursor()

# Eğer tablo varsa önce silelim
cursor.execute("DROP TABLE IF EXISTS siparisler")

# Siparişler tablosunu yeniden oluştur (Şeker seçeneği eklendi)
cursor.execute("""
CREATE TABLE siparisler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icecek TEXT NOT NULL,
    adet INTEGER NOT NULL,
    lokasyon TEXT NOT NULL,
    seker_durumu TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Eski tablo silindi ve yeni veritabanı başarıyla oluşturuldu!")