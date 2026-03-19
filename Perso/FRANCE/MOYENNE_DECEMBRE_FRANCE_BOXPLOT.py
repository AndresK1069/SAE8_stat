import oracledb
import numpy as np
import matplotlib.pyplot as plt

jours = []
valeurs_no2 = []

with oracledb.connect(user="system", password="andres", host="localhost", port="1521", service_name="XEPDB1") as connection:
    with connection.cursor() as cursor:

        sql = """
                SELECT TRUNC(HORAIRE) AS DAY, AVG(NO2) AS MOYENNE_NO2
                FROM V_MESURES_FRANCE
                WHERE EXTRACT(MONTH FROM HORAIRE) = 12
                GROUP BY TRUNC(HORAIRE)
                ORDER BY DAY
             """

        for row in cursor.execute(sql):
            jours.append(row[0].day)
            valeurs_no2.append(row[1])

        x = np.array(jours)
        y = np.array(valeurs_no2)

        if x.size > 0:
            plt.figure(figsize=(8, 6))

            plt.boxplot(y, patch_artist=True,
                        boxprops=dict(facecolor='plum', color='purple'),
                        medianprops=dict(color='red', linewidth=2),
                        flierprops=dict(marker='d', markerfacecolor='black', markersize=6))

            plt.title('Distribution des moyennes de NO2 - Décembre (France)')
            plt.ylabel('Concentration NO2')
            plt.xticks([1], ['Décembre'])
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            plt.tight_layout()
            plt.savefig("BOXPLOT_DECEMBRE_FRANCE.png")
            plt.show()