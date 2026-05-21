# Sunum Slayt Taslağı: Network Programming - Async REST API

Bu doküman, sınıf sunumunuzda kullanabileceğiniz 6 slaytlık akışı içerir.

---

## Slayt 1: Başlık Slaydı
**Başlık:** Python ile Asenkron REST API Mimarisi
**Alt Başlık:** asyncio ve FastAPI ile Yüksek Performanslı Ağ Programlama
**İçerik:**
- Adınız Soyadınız
- Dersin Adı: Network Programming
- Projenin Kısa Tanıtımı: Birden fazla kaynaktan eşzamanlı veri çeken asenkron hava durumu ve loglama servisi.

---

## Slayt 2: Senkron vs. Asenkron Yaklaşım Farkı
**Başlık:** Senkron vs. Asenkron Yaklaşım Farkı
**İçerik:**
- **Senkron (Synchronous) I/O:** Bloklayan yapı. İplik (thread), ağ isteği tamamlanana kadar kilitlenir ve boşta bekler. Kaynak israfı yaratır.
- **Asenkron (Asynchronous) I/O:** Bloklamayan yapı. Ağ isteği yapıldıktan sonra iplik serbest kalır ve diğer işlemleri yürütür. Yanıt geldiğinde asıl işleme kaldığı yerden devam eder.
- **Gerçek Hayat Örneği:** Restoranda garsonun, aşçının yemeği hazırlamasını mutfakta beklemesi (Senkron) vs. siparişi aşçıya verip diğer masalarla ilgilenmeye gitmesi (Asenkron).

---

## Slayt 3: Neden Bu Projede asyncio Kullandık?
**Başlık:** Neden bu projede asyncio kullandık?
**İçerik:**
- **I/O Bound İşlemler:** Ağ programlamasında dar boğaz (bottleneck) genellikle CPU değil, ağ/veritabanı gecikmeleridir (Network Latency). `asyncio` tam olarak bunun için tasarlandı.
- **Yüksek Ölçeklenebilirlik:** Tek bir iplik (single thread) üzerinde binlerce eşzamanlı bağlantı (concurrent connection) çok düşük bellek tüketimiyle yönetilebilir.
- **Zaman Tasarrufu:** Birden fazla kaynaktan (API'lerden) bağımsız veri çekilirken toplam bekleme süresi, isteklerin toplamı değil, *en yavaş isteğin süresi* kadar olur.

---

## Slayt 4: Proje Mimarisi
**Başlık:** Proje Mimarisi ve Teknolojiler
**İçerik:**
- **Python `asyncio`:** Asenkron I/O döngüsü (Event Loop) için temel yapı taşı.
- **FastAPI:** Doğrudan asenkron desteği (ASGI) sunan, modern ve çok hızlı web framework'ü.
- **Uvicorn:** Event loop üzerinde çalışan asenkron web sunucusu (ASGI server).
- **Proje Senaryosu:** 
  - 3 farklı kaynaktan asenkron olarak aynı anda hava durumu verisi çeken GET API.
  - Kullanıcıya anında yanıt dönüp, log yazma işlemini arka planda (background tasks) gerçekleştiren POST API.

---

## Slayt 5: Koda Bakış (Asenkronluğun Kanıtı)
**DIKKAT: Bu slaytta sınıfa main.py dosyasındaki kodu göstermeniz gerekir.**

**Başlık:** Kod Üzerinde Asenkron Mantığı İnceleme
**İçerik:**
- **`await asyncio.sleep(delay)`:** Klasik `time.sleep` tüm programı durdururken, `asyncio.sleep` ağ beklemesini simüle eder ve kontrolü döngüye bırakır (Non-blocking).
- **`asyncio.gather` kullanımı:** `task1 (1.5s)`, `task2 (2.0s)` ve `task3 (1.0s)` görevlerini aynı anda başlattık.
- **Kanıt:** Senkron çalışsaydı toplam yürütme **4.5 saniye** sürecekti. Projemizde asenkron çalıştığı için tüm işlemler **2.0 saniye** (en yavaş olanın süresi) içinde bitmektedir.

---

## Slayt 6: Sonuç ve Soru-Cevap
**Başlık:** Sonuç
**İçerik:**
- Ağ programlamasında asenkron mimari, sunucu donanım kaynaklarının en verimli şekilde kullanılmasını sağlar.
- Dosya okuma, veri tabanı sorguları ve HTTP istekleri gibi CPU yormayan (I/O-bound) her senaryoda asenkron programlama devasa hız artışı getirir.
- Dinlediğiniz için teşekkürler.
- Soru & Cevap.
