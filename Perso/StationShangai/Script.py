import oracledb
import numpy as np
import matplotlib.pyplot as plt

horaires = []
no2_values = []

with oracledb.connect(user="system", password="andres",
                      host="localhost", port=1521, service_name="XEPDB1") as connection:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT HORAIRE, NO2
            FROM MESURE_SHANGHAI_STATION2001
            WHERE STATION_ID = 2001
            ORDER BY HORAIRE
        """)

        for row in cursor:
            horaires.append(row[0])
            no2_values.append(float(row[1]) if row[1] is not None else np.nan)

x = np.array(horaires)
y = np.array(no2_values)

plt.figure(figsize=(14, 6))
plt.plot(x, y, marker='o', linestyle='-', color='royalblue')
plt.title("Évolution du NO₂ - Station 2001 (toutes valeurs)")
plt.xlabel("Date et heure")
plt.ylabel("NO₂ (µg/m³)")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("Tout_les_Valeur_Pour_la_Station_2001_Shangai.png")
plt.show()