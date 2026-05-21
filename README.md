# Async Weather Aggregator & Analytics API

Bu proje, üniversite "Network Programming" dersi için tasarlanmış, **asenkron (async) REST mimarisini** gösteren tam teşekküllü bir Python projesidir.

## Proje Hakkında
Projenin amacı, Python'un `asyncio` kütüphanesi ve `FastAPI` framework'ü kullanılarak asenkron I/O işlemlerinin senkron işlemlere göre avantajlarını kanıtlamaktır.
Proje, sahte bir Hava Durumu Toplayıcı (Weather Aggregator) ve Loglama servisi olarak çalışır.

### Asenkron Mimarinin Bu Projedeki Avantajı
Senkron (bloklayan) bir mimaride, üç farklı dış API'den (sırasıyla 1.5 sn, 2.0 sn, 1.0 sn gecikmeli) veri çekmek istediğinizde toplam bekleme süreniz **4.5 saniye** olacaktır. Çünkü her ağ isteği sırayla yapılır ve biri bitmeden diğeri başlamaz.

Bu projede kullanılan **asenkron mimari (`asyncio.gather`)** sayesinde, tüm ağ istekleri eşzamanlı (concurrent) olarak başlatılır. Sunucu işlemciyi boşta bekletmek yerine diğer işlemlere geçer. Sonuç olarak toplam bekleme süresi, isteklerin toplamı değil, **en uzun süren istek kadar (yaklaşık 2.0 saniye)** olur. Bu da yüksek trafikli sistemlerde performans ve ölçeklenebilirlik açısından devasa bir avantaj sağlar.

## Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleme
Öncelikle bir sanal ortam (virtual environment) oluşturmanız önerilir. Daha sonra aşağıdaki komutla gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

### 2. Sunucuyu Başlatma
Uvicorn ASGI sunucusunu kullanarak FastAPI uygulamasını başlatın:

```bash
uvicorn main:app --reload
```

Bu komut, sunucuyu `http://127.0.0.1:8000` adresinde başlatır. `--reload` parametresi, kodda bir değişiklik yaptığınızda sunucunun otomatik yeniden başlamasını sağlar.

## API Endpoint'lerini Test Etme

Sunucu çalıştıktan sonra, FastAPI'nin otomatik olarak oluşturduğu Swagger arayüzüne giderek (tarayıcınızda `http://127.0.0.1:8000/docs` adresine girerek) tüm endpoint'leri kullanıcı dostu bir arayüzden test edebilirsiniz. 

Alternatif olarak terminal üzerinden aşağıdaki komutlarla test edebilirsiniz:

### 1. GET `/weather/{city}` (Eşzamanlı Veri Çekme Simülasyonu)
Bu uç nokta, 3 farklı simüle edilmiş veri kaynağından eşzamanlı olarak hava durumu verisi çeker.

**Test Komutu:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/weather/Istanbul' -H 'accept: application/json'
```

**Beklenen Sonuç:**
Çıktıda `total_execution_time_seconds` değerinin 4.5 yerine yaklaşık 2.0 saniye olduğunu göreceksiniz. Bu, `asyncio.sleep` ve `asyncio.gather` ile asenkron yapının kanıtıdır.

### 2. POST `/log` (Arka Plan Görevleri Simülasyonu)
Bu uç nokta, gelen log verisini arka planda işlemeye alır. İstek anında tamamlanır (`202 Accepted`) ancak sunucu konsolunda işlemin 2.5 saniye sonra bittiğini görürsünüz. İstemci (client), log işleminin bitmesini beklemez.

**Test Komutu:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/log' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user123",
  "action": "login",
  "timestamp": "2023-10-25T10:00:00Z"
}'
```
