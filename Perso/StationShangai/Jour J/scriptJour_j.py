import oracledb
import numpy as np
import matplotlib.pyplot as plt

horaires = []
no2_values = []

date_souhaitee = "28-08-2013"

with oracledb.connect(user="system", password="andres",
                      host="localhost", port=1521, service_name="XEPDB1") as connection:
    with connection.cursor() as cursor:

        cursor.execute(f"""
            SELECT HORAIRE, NO2
            FROM MESURE_SHANGHAI_STATION2001
            WHERE STATION_ID = 2001
              AND HORAIRE >= TO_DATE('{date_souhaitee} 00:00:00', 'DD-MM-YYYY HH24:MI:SS')
              AND HORAIRE <= TO_DATE('{date_souhaitee} 23:59:59', 'DD-MM-YYYY HH24:MI:SS')
            ORDER BY HORAIRE
        """)

        for row in cursor:
            horaires.append(row[0])
            no2_values.append(float(row[1]) if row[1] is not None else np.nan)

x = np.array(horaires)
y = np.array(no2_values)

plt.figure(figsize=(14, 6))
plt.plot(x, y, marker='o', linestyle='-', color='orange')
plt.title(f"Évolution du NO₂ - Station 2001 le {date_souhaitee}")
plt.xlabel("Heure")
plt.ylabel("NO₂ (µg/m³)")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"NO2_Station_2001_{date_souhaitee}.png")
plt.show()