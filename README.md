# NewsBot Kurulum Talimatları

## 1. Kütüphaneleri Kur
```bash
pip3 install -r requirements.txt
```

## 2. WordPress Uygulama Şifresi Oluştur
1. WordPress admin paneline gir (monarqscreen.com/wp-admin)
2. Sağ üstte kullanıcı adına tıkla → **Profil**
3. Aşağı kaydır → **Uygulama Şifreleri** bölümü
4. Yeni şifre adı: "NewsBot" → **Ekle**
5. Çıkan şifreyi kopyala (örn: `xxxx xxxx xxxx xxxx`)

## 3. config.py Dosyasını Doldur
```python
ANTHROPIC_API_KEY = "sk-ant-..."        # Yeni API key'in
WP_URL = "https://monarqscreen.com"
WP_USERNAME = "admin"                    # WordPress kullanıcı adın
WP_APP_PASSWORD = "xxxx xxxx xxxx"      # Az önce kopyaladığın şifre
```

## 4. Çalıştır
```bash
cd ~/Desktop/newsbot
python3 newsbot.py
```

## 5. Arka Planda Sürekli Çalıştır (Mac)
Terminal'i kapatsan da çalışsın için:
```bash
nohup python3 newsbot.py > newsbot.log 2>&1 &
```

Durdurmak için:
```bash
pkill -f newsbot.py
```

Logları görmek için:
```bash
tail -f newsbot.log
```
