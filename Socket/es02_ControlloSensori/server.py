import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8000
LOG_FILE = "dati_sensori.log"

def valida_messaggio(msg):
    parti = msg.split(";")
    if len(parti) != 3:
        return False
    try:
        float(parti[1])
        float(parti[2])
        return True
    except ValueError:
        return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server in ascolto sulla porta {PORT}...")

    while True:
        conn, addr = server.accept()
        with conn:
            print(f"Connessione da {addr}")

            try:
                data = conn.recv(1024)
                if not data:
                    print("Connessione chiusa prima dell'invio dati")
                    continue

                messaggio = data.decode().strip()
                print("Ricevuto:", messaggio)

                if valida_messaggio(messaggio):
                    id_s, temp, umi = messaggio.split(";")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    with open(LOG_FILE, "a") as f:
                        f.write(f"{timestamp} | {id_s} | {temp} | {umi}\n")

                    conn.sendall(b"OK")
                else:
                    conn.sendall(b"FORMATO_NON_VALIDO")

            except Exception as e:
                print("Errore:", e)
