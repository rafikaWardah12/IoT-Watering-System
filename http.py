import network
import urequests
# import uping

def connectWifi(ssid, password):
    
    # Hubungkan ke Wi-Fi

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Tunggu hingga terhubung
    while not wlan.isconnected():
        pass

    print("Connected to Wi-Fi!")
    print(wlan.ifconfig())

def sendData(endpoint, suhu, kelembapan, phTanah):
    # URL endpoint API
    url = "{}/api/sensor".format(endpoint)

    # Header
    headers = {
        "Content-Type": "application/json"
    }

    # Data yang akan dikirim
    print("suhu = {}. Kelembapan = {}. PHTanah = {}".format(str(suhu), str(kelembapan), str(phTanah)))
    data = {
        "suhu": str(suhu),
        "kelembapan": str(kelembapan),
        "cahaya" : "5",
        "phTanah": str(phTanah),
        "published": True
    }

    # Kirim permintaan POST dengan header
    response = urequests.post(url, json=data, headers=headers)

    # Periksa status kode
    if response.status_code == 200:
        print("Data sent successfully!")
        print("Response JSON:")
        print(response.json())
    else:
        print("Failed to send data. Status code:", response.status_code)

    response.close()

def getActive(endpoint):
    # URL endpoint API
    url = "{}/api/checkActive".format(endpoint)

    # Header
    headers = {
        "Content-Type": "application/json"
    }
    
    response = urequests.get(url, headers=headers)
    print(response.json())
    result = response.json()
    response.close()

    return result
   