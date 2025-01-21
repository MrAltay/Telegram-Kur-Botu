import yfinance as yf
import requests
import time
from datetime import datetime

# Telegram bot token'ınızı buraya ekleyin
TELEGRAM_TOKEN = "tokengir"
# Mesajın gönderileceği chat ID'yi buraya ekleyin
CHAT_ID = "idgir"

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data)
        if not response.ok:
            print(f"Telegram mesajı gönderilemedi: {response.text}")
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {str(e)}")

def get_rates():
    try:
        # Yahoo Finance'dan sembolleri tanımlama ve verileri alma
        dolar = yf.download("TRY=X", period="1d", interval="1m", progress=False)
        euro = yf.download("EURTRY=X", period="1d", interval="1m", progress=False)
        altin = yf.download("GC=F", period="1d", interval="1m", progress=False)
        
        if len(dolar) == 0 or len(euro) == 0 or len(altin) == 0:
            return "Veri alınamadı. Piyasalar kapalı olabilir."
        
        # En son fiyatları alma (önerilen yeni yöntemle)
        dolar_kuru = float(dolar['Close'].iloc[-1].item())
        euro_kuru = float(euro['Close'].iloc[-1].item())
        altin_usd = float(altin['Close'].iloc[-1].item())
        
        # Gram altın hesaplama (1 ons = 31.1 gram)
        gram_altin = (altin_usd * dolar_kuru) / 31.1
        
        # Kurları formatla
        return (
            f"💰 <b>Güncel Kurlar</b> 💰\n\n"
            f"💵 Dolar: {dolar_kuru:,.2f} TL\n"
            f"💶 Euro: {euro_kuru:,.2f} TL\n"
            f"🧈 Gram Altın: {gram_altin:,.2f} TL"
        )
    except Exception as e:
        return f"Hata oluştu: {str(e)}\nLütfen internet bağlantınızı kontrol edin."

def main():
    print("Güncel Kur Botu Başlatıldı (Yahoo Finance + Telegram)...")
    print("Veriler 10 dakikada bir güncelleniyor...")
    print("-" * 50)
    
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        rates = get_rates()
        
        print(f"\nGüncelleme Zamanı: {current_time}")
        print(rates)
        print("-" * 50)
        
        # Telegram'a mesaj gönder
        send_telegram_message(f"🕒 {current_time}\n\n{rates}")
        
        time.sleep(600)  # 10 dakika bekle

if __name__ == "__main__":
    main() 