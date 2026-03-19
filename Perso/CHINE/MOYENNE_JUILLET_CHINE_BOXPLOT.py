import oracledb
import numpy as np
import matplotlib.pyplot as plt

jours = []
valeurs_no2 = []

with oracledb.connect(user="system", password="andres", host="localhost", port="1521", service_name="XEPDB1") as connection:
    with connection.cursor() as cursor:

        sql = """
        SELECT TRUNC(HORAIRE) AS DAY, AVG(NO2) AS MOYENNE_NO2
        FROM V_MESURES_CHINE
        WHERE EXTRACT(MONTH FROM HORAIRE) = 7
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
                        boxprops=dict(facecolor='lightgreen', color='darkgreen'),
                        medianprops=dict(color='red', linewidth=2),
                        flierprops=dict(marker='o', markerfacecolor='orange', markersize=8))

            plt.title('Distribution des moyennes de NO2 - Juillet (Chine)')
            plt.ylabel('Concentration NO2')
            plt.xticks([1], ['Juillet'])
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            plt.tight_layout()
            plt.savefig("BOXPLOT_JUILLET_CHINE.png")
            plt.show()