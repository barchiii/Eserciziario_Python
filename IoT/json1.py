
# Realizzare un file (non in formato JSON) con salvataggi periodici della temperatura,
# creando un insieme di oggetti JSON (una riga = un oggetto JSON -> NDJSON)

import json
import random
import time
import datetime
import os


def on_temp(N, MIN, MAX):
	"""Simulazione sensore temperatura, da MIN a MAX gradi con N decimali."""
	TEMP = round(random.uniform(MIN, MAX), N)
	return TEMP


def save_readings_periodic(num_readings: int = 10, interval: float = 1.0, filename: str = 'json1.dbt',
						   gradi_min: float = 10.0, gradi_max: float = 30.0,
						   n_decimali: int = 1, sensor_id: str = "0021"):
	"""Esegue misure periodiche e salva ogni misura come singolo oggetto JSON su una nuova riga (NDJSON).

	- `num_readings` : numero di letture (da 1 a 30)
	- `interval` : intervallo in secondi tra letture
	- `filename` : file di output (viene creato se non esiste, aperto in append)
	"""
	# Validazione: num_readings deve essere tra 1 e 30
	if num_readings < 1:
		print(f"Attenzione: numero richiesto {num_readings} non valido. Impostato a 1 (minimo).")
		num_readings = 1
	elif num_readings > 30:
		print(f"Attenzione: numero richiesto {num_readings} modificato a 30 (massimo consentito).")
		num_readings = 30

	# Assicuriamoci che la cartella esista
	os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

	count = 0
	try:
		with open(filename, 'a', encoding='utf-8') as fh:
			while True:
				count += 1
				temp = on_temp(n_decimali, gradi_min, gradi_max)
				ts_epoch = datetime.datetime.now().timestamp()
				ts_iso = datetime.datetime.now().isoformat()
				record = {
					"MISURE": count,
					"IDSENSORE": sensor_id,
					"TIPO": "DHT11",
					"PRODUTTORE": "Joy-It",
					"MODELLO": "KY-015",
					"TEMP": temp,
					"UMID": 76,
					"TIMESTAMP": ts_epoch,
					"TIME_ISO": ts_iso
				}
				json.dump(record, fh, ensure_ascii=False)
				fh.write('\n')
				fh.flush()
				print(f"Lettura {count}: temp={temp} °C salvata in {filename}")

				if count >= num_readings:
					break

				time.sleep(interval)
	except KeyboardInterrupt:
		print('\nInterrotto dall\'utente. Uscita pulita.')


if __name__ == '__main__':
	print('-----------------------------')
	print('Avvio rilevamento periodico temperature')
	print('-----------------------------')
	save_readings_periodic(num_readings=10, interval=1.0, filename='json1.dbt')
	print('Rilevamento completato.')

