import socket
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9000


def valida_input(testo):
    righe = testo.strip().split("\n")

    for riga in righe:
        try:
            data, t12, t24 = riga.split(";")
            datetime.strptime(data, "%d/%m/%Y")
            float(t12)
            float(t24)
        except Exception:
            return False

    return True


def invia_dati():
    dati = text_input.get("1.0", tk.END).strip()

    if not dati:
        messagebox.showerror("Errore", "Inserire almeno un giorno di dati.")
        return

    if not valida_input(dati):
        messagebox.showerror(
            "Errore formato",
            "Formato non valido.\nUsare:\nGG/MM/AAAA;TEMP12;TEMP24"
        )
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(dati.encode())

            risposta = client.recv(4096).decode()
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, risposta)

    except ConnectionRefusedError:
        messagebox.showerror("Errore", "Server non raggiungibile.")


# --- GUI ---
root = tk.Tk()
root.title("Invio Temperature Giornaliere – Stazione Meteo")
root.geometry("600x500")

label_input = tk.Label(root, text="Inserisci i dati (una riga per giorno):")
label_input.pack()

text_input = tk.Text(root, height=10)
text_input.pack(fill=tk.X, padx=10)

btn = tk.Button(root, text="Invia dati", command=invia_dati)
btn.pack(pady=10)

label_output = tk.Label(root, text="Risultati dal server:")
label_output.pack()

text_output = tk.Text(root, height=10, bg="#f0f0f0")
text_output.pack(fill=tk.BOTH, padx=10, pady=5)

root.mainloop()
