import socket
import random

HOST = "127.0.0.1"
PORT = 8000

ID_SENSORE = "S1"
TEMPERATURA = round(random.uniform(18.0, 30.0), 2)
UMIDITA = round(random.uniform(30.0, 70.0), 2)

# Messaggio corretto
messaggio = f"{ID_SENSORE};{TEMPERATURA};{UMIDITA}"

# Per test errore formato, usare ad esempio:
# messaggio = f"{ID_SENSORE}-{TEMPERATURA}"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(messaggio.encode())

        risposta = client.recv(1024).decode()

        if risposta == "OK":
            print("Dati inviati correttamente")
        else:
            print("Errore nel formato")

except ConnectionRefusedError:
    print("Server non raggiungibile")
