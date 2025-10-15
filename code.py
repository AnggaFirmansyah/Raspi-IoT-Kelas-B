import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json

# --- Konfigurasi Sensor ---
# Inisialisasi sensor DHT22 pada GPIO pin 21
dht_sensor = adafruit_dht.DHT22(board.D21)

# --- Konfigurasi MQTT ---
MQTT_BROKER = "10.4.137.107"  # Ganti dengan alamat broker Anda jika perlu
MQTT_PORT = 1883
# Topik untuk mengirim data sensor dalam format JSON
MQTT_TOPIC_JSON = "raspberry/dht22/data" 
# Topik individual (opsional, jika Anda lebih suka cara ini)
MQTT_TOPIC_TEMP = "raspberry/dht22/temperature"
MQTT_TOPIC_HUMIDITY = "raspberry/dht22/humidity"

# --- Fungsi Callback MQTT ---
def on_connect(client, userdata, flags, rc):
    """Callback yang dipanggil saat client berhasil terhubung ke broker."""
    if rc == 0:
        print("✅ Berhasil terhubung ke MQTT Broker!")
    else:
        print(f"Gagal terhubung, kode status: {rc}")

# --- Setup Client MQTT ---
client = mqtt.Client()
client.on_connect = on_connect
print(f"Menghubungkan ke broker di {MQTT_BROKER}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Memulai loop MQTT di background thread
client.loop_start()

print("Memulai pembacaan sensor. Tekan Ctrl+C untuk keluar.")

try:
    while True:
        try:
            # Membaca suhu dan kelembaban dari sensor
            temperature_c = dht_sensor.temperature
            humidity = dht_sensor.humidity

            # Pastikan pembacaan valid sebelum melanjutkan
            if humidity is not None and temperature_c is not None:
                temperature_f = temperature_c * (9 / 5) + 32
                
                # Menampilkan data di terminal
                print(f"Temp={temperature_c:0.1f}°C  {temperature_f:0.1f}°F    Humidity={humidity:0.1f}%")

                # --- Mempersiapkan Payload ---
                # Cara 1: Mengirim sebagai JSON (Direkomendasikan)
                payload = {
                    "temperature_celsius": round(temperature_c, 1),
                    "humidity_percent": round(humidity, 1)
                }
                # Mengubah dictionary menjadi string JSON
                payload_json = json.dumps(payload)
                
                # --- Publikasi ke Topik MQTT ---
                # Publikasi payload JSON ke topik utama
                client.publish(MQTT_TOPIC_JSON, payload_json)
                
                # Publikasi ke topik individual (jika diperlukan)
                # client.publish(MQTT_TOPIC_TEMP, f"{temperature_c:0.1f}")
                # client.publish(MQTT_TOPIC_HUMIDITY, f"{humidity:0.1f}")
                
            else:
                print("Gagal membaca sensor, mencoba lagi...")

        except RuntimeError as error:
            # Error sesekali wajar terjadi, cetak dan lanjutkan
            print(error.args[0])
        
        # Tunggu 5 detik sebelum pembacaan berikutnya
        time.sleep(5.0)

except KeyboardInterrupt:
    print("\nProgram dihentikan.")
finally:
    # Menghentikan loop dan memutuskan koneksi dengan bersih
    print("Memutuskan koneksi MQTT...")
    dht_sensor.exit()
    client.loop_stop()
    client.disconnect()
