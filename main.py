from fastapi import FastAPI, BackgroundTasks
import asyncio
from pydantic import BaseModel
import time
from typing import Dict

app = FastAPI(
    title="Async Weather Aggregator API",
    description="A showcase of asynchronous REST architecture using FastAPI and asyncio.",
    version="1.0.0"
)

# -----------------
# Pydantic Modelleri / Pydantic Models
# -----------------
class LogEntry(BaseModel):
    user_id: str
    action: str
    timestamp: str

# -----------------
# Simüle Edilmiş Asenkron İşlevler / Simulated Async Functions
# -----------------

async def fetch_weather_from_source(source_name: str, city: str, delay: float) -> Dict[str, str]:
    """
    Dış bir API'den asenkron olarak veri çekmeyi simüle eder.
    Simulates fetching data from an external API asynchronously.
    """
    print(f"[{source_name}] '{city}' için veri çekilmeye başlandı... (Bekleme süresi: {delay}s)")
    
    # Burada gerçek bir I/O işlemi (HTTP isteği vs.) yerine asyncio.sleep() kullanıyoruz.
    # time.sleep() kullansaydık bu tüm sunucuyu bloklardı (senkron yaklaşım).
    # asyncio.sleep() ise event loop'u serbest bırakır (asenkron yaklaşım).
    await asyncio.sleep(delay)
    
    print(f"[{source_name}] '{city}' verisi başarıyla alındı.")
    return {"source": source_name, "data": f"{city} is sunny", "latency": f"{delay}s"}

async def process_log_to_db(log: LogEntry):
    """
    Log verisini asenkron olarak veritabanına kaydetmeyi simüle eder.
    Simulates saving log data to a database asynchronously.
    """
    print(f"[DB] Log işleniyor: {log.action} (Kullanıcı: {log.user_id})")
    
    # Simüle edilmiş veritabanı yazma gecikmesi
    await asyncio.sleep(2.5) 
    
    print(f"[DB] Log başarıyla kaydedildi: {log.action}")

# -----------------
# API Uç Noktaları / API Endpoints
# -----------------

@app.get("/weather/{city}")
async def get_aggregated_weather(city: str):
    """
    Birden fazla kaynaktan eşzamanlı (concurrent) olarak veri çeken GET endpoint'i.
    A GET endpoint that fetches data concurrently from multiple sources.
    """
    start_time = time.time()
    
    # 3 farklı simüle edilmiş kaynaktan veri çekme görevini tanımlıyoruz.
    task1 = fetch_weather_from_source("Source_A", city, 1.5)
    task2 = fetch_weather_from_source("Source_B", city, 2.0)
    task3 = fetch_weather_from_source("Source_C", city, 1.0)
    
    # asyncio.gather ile bu görevleri aynı anda (eşzamanlı) çalıştırıyoruz.
    # Senkron olsaydı toplam bekleme 1.5 + 2.0 + 1.0 = 4.5 saniye olurdu.
    # Asenkron olduğu için sadece en uzun süren görevin süresi (2.0s) kadar bekleriz.
    results = await asyncio.gather(task1, task2, task3)
    
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    return {
        "city": city,
        "results": results,
        "total_execution_time_seconds": total_time,
        "explanation": "Senkron çalışsaydı 4.5 saniye sürecekti. asyncio.gather ile concurrency sağlandığı için yaklaşık 2.0 saniye sürdü."
    }

@app.post("/log", status_code=202)
async def create_log(log: LogEntry, background_tasks: BackgroundTasks):
    """
    Asenkron arka plan görevlerini gösteren POST endpoint'i.
    A POST endpoint demonstrating asynchronous background tasks.
    """
    # Gelen isteği anında cevaplayıp (non-blocking), uzun süren loglama işlemini arka plana atıyoruz.
    # Kullanıcı 2.5 saniye DB işlemini beklemek zorunda kalmaz.
    background_tasks.add_task(process_log_to_db, log)
    
    return {
        "message": "Log isteği alındı ve asenkron olarak arka planda işleniyor.",
        "status": "Accepted"
    }
