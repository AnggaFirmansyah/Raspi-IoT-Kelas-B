# 🌡️ Raspberry Pi IoT — Monitoring Suhu & Kelembaban (DHT22 + MQTT)

## 👥 Anggota Kelompok

| Nama | NRP |
|------|-----|
| Angga Firmansyah | 5027241062 |
| Muhammad Ardiansyah Tri Wibowo | 5027241098 |
| Yasykur Khalis Jati Maulana Yuwono | 5027241112 |

---

## 📘 Deskripsi Proyek

Proyek ini bertujuan untuk **membaca data suhu dan kelembaban** dari sensor **DHT22** menggunakan **Raspberry Pi**, lalu **mengirimkan hasilnya ke broker MQTT** dalam format **JSON**.  
Data dapat dimanfaatkan untuk integrasi dengan dashboard IoT seperti **Node-RED**, **Home Assistant**, atau **Grafana**.

---

## ⚙️ Perangkat & Perangkat Lunak

### 🧩 Hardware
| Komponen | Deskripsi |
|-----------|------------|
| Raspberry Pi | Model 3/4/5 dengan Raspbian OS |
| Sensor DHT22 | Sensor suhu & kelembaban digital |
| Kabel Jumper | Male-to-Female |
| Breadboard | (Opsional, untuk koneksi lebih rapi) |

### 💻 Software / Library
- Python ≥ 3.9  
- `adafruit_dht` — library pembacaan sensor  
- `paho-mqtt` — library komunikasi MQTT  
- `board` — modul GPIO Raspberry Pi  

#### Instalasi:
sudo pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
pip install paho-mqtt

---

## 🔌 Skema Koneksi
| Pin DHT22 | Raspberry Pi GPIO |
|------------|------------------|
| VCC | 5V |
| GND | GND |
| DATA | GPIO 21 |

📝 Pastikan menggunakan resistor 10KΩ antara pin DATA dan VCC untuk kestabilan pembacaan.

---

## 💾 Kode Program (Python)
```
import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json

# --- Konfigurasi Sensor ---
dht_sensor = adafruit_dht.DHT22(board.D21)

# --- Konfigurasi MQTT ---
MQTT_BROKER = "10.4.137.107"
MQTT_PORT = 1883
MQTT_TOPIC_JSON = "raspberry/dht22/data"
MQTT_TOPIC_TEMP = "raspberry/dht22/temperature"
MQTT_TOPIC_HUMIDITY = "raspberry/dht22/humidity"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Berhasil terhubung ke MQTT Broker!")
    else:
        print(f"Gagal terhubung, kode status: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
print(f"Menghubungkan ke broker di {MQTT_BROKER}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("Memulai pembacaan sensor. Tekan Ctrl+C untuk keluar.")

try:
    while True:
        try:
            temperature_c = dht_sensor.temperature
            humidity = dht_sensor.humidity

            if humidity is not None and temperature_c is not None:
                temperature_f = temperature_c * (9 / 5) + 32
                print(f"Temp={temperature_c:0.1f}°C  {temperature_f:0.1f}°F    Humidity={humidity:0.1f}%")

                payload = {
                    "temperature_celsius": round(temperature_c, 1),
                    "humidity_percent": round(humidity, 1)
                }
                payload_json = json.dumps(payload)
                client.publish(MQTT_TOPIC_JSON, payload_json)

            else:
                print("Gagal membaca sensor, mencoba lagi...")

        except RuntimeError as error:
            print(error.args[0])
        time.sleep(5.0)

except KeyboardInterrupt:
    print("\nProgram dihentikan.")
finally:
    print("Memutuskan koneksi MQTT...")
    dht_sensor.exit()
    client.loop_stop()
    client.disconnect()
```
---

## 🧠 Penjelasan Kode
| Bagian | Fungsi |
|---------|--------|
| adafruit_dht.DHT22(board.D21) | Menginisialisasi sensor DHT22 pada GPIO21 |
| on_connect() | Callback saat berhasil terhubung ke broker MQTT |
| client.publish() | Mengirim data sensor ke topik MQTT |
| json.dumps() | Mengubah data dictionary menjadi format JSON |
| try...except RuntimeError | Menangani error pembacaan sensor yang bersifat sementara |
| time.sleep(5.0) | Interval antar pembacaan data selama 5 detik |

---

## 📡 Struktur Data (Payload MQTT)
Data dikirim ke topik `raspberry/dht22/data` dalam format JSON seperti berikut:

{
  "temperature_celsius": 27.3,
  "humidity_percent": 65.2
}

---

## 🖥️ Output Terminal
Menghubungkan ke broker di 10.4.137.107...
✅ Berhasil terhubung ke MQTT Broker!
Memulai pembacaan sensor. Tekan Ctrl+C untuk keluar.
Temp=27.3°C  81.1°F    Humidity=65.2%
Temp=27.4°C  81.3°F    Humidity=65.0%

---

## 📸 Dokumentasi

| No | Keterangan | Gambar / Bukti |
|----|-------------|----------------|
| 1 | Foto rangkaian alat | ![WhatsApp Image 2025-10-15 at 11 48 40 (1)](https://github.com/user-attachments/assets/b6a942d7-fd6c-49c1-927e-c3dd1569fb5e) |
| 2 | Screenshot data di dashboard MQTT | ![WhatsApp Image 2025-10-15 at 11 48 39 (1)](https://github.com/user-attachments/assets/7594bba0-ad73-4632-975d-bc4b12253db2) |



---

## 🔍 Troubleshooting
| Masalah | Penyebab | Solusi |
|----------|-----------|--------|
| RuntimeError: Failed to read sensor data | Pembacaan tidak stabil | Cek kabel atau tambahkan delay |
| Tidak terkoneksi ke broker MQTT | IP broker salah / server mati | Pastikan alamat broker benar dan server MQTT aktif |
| Data tidak tampil di dashboard | Salah topik MQTT | Sesuaikan topik dengan konfigurasi di subscriber |

---

## 🧾 Lisensi
Proyek ini bersifat **open-source** dan dapat dimodifikasi sesuai kebutuhan untuk pengembangan sistem IoT berbasis Raspberry Pi.

---

📘 **Cara pakai:**
- Cukup copy blok ini dan paste langsung ke file `README.md` GitHub kamu.  
- Tampilan akan tetap rapi seperti Markdown biasa (judul, tabel, dan blok kode akan diformat otomatis).
