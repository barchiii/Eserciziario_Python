import socket

HOST = "127.0.0.1"
PORT = 9000

def elabora_dati(dati):
    righe = dati.strip().split("\n")

    temperature = []
    giorni = 0

    for riga in righe:
        try:
            data, t12, t24 = riga.split(";")
            t12 = float(t12)
            t24 = float(t24)

            temperature.append(t12)
            temperature.append(t24)
            giorni += 1

        except ValueError:
            # riga malformata
            continue

    if not temperature:
        return "Errore: nessun dato valido ricevuto."

    media = sum(temperature) / len(temperature)
    t_max = max(temperature)
    t_min = min(temperature)

    risposta = (
        f"Numero giorni analizzati: {giorni}\n"
        f"Numero rilevazioni totali: {len(temperature)}\n\n"
        f"Temperatura media: {media:.2f} °C\n"
        f"Temperatura massima: {t_max:.1f} °C\n"
        f"Temperatura minima: {t_min:.1f} °C"
    )

    return risposta


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server in ascolto sulla porta {PORT}...")

    conn, addr = server.accept()
    with conn:
        print("Connessione da:", addr)

        dati = conn.recv(4096).decode()
        print("Dati ricevuti:\n", dati)

        risposta = elabora_dati(dati)
        conn.sendall(risposta.encode())

    print("Connessione chiusa.")
