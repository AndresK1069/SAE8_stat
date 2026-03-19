import oracledb
import numpy as np
import matplotlib.pyplot as plt

jours = []
valeurs_no2 = []


with oracledb.connect(user="system", password="andres", host="localhost", port="1521",service_name="XEPDB1") as connection:
    with connection.cursor() as cursor:
        sql = """
            SELECT TRUNC(HORAIRE) AS DAY, AVG(NO2) AS MOYENNE_NO2
            FROM V_MESURES_FRANCE
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
    plt.figure(figsize=(12, 6))


    plt.subplot(1, 2, 1)  # 1 ligne, 2 colonnes, graphique n°1
    plt.plot(x, y, marker='o', color='royalblue', linewidth=2)
    plt.title('Évolution du NO2 (Juillet)')
    plt.xlabel('Jour du mois')
    plt.ylabel('Moyenne NO2')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.subplot(1, 2, 2)
    plt.bar(x, y, color='skyblue', edgecolor='navy')
    plt.title('NO2 par jour')
    plt.xlabel('Jour du mois')

    plt.tight_layout()
    plt.savefig("MOYENNE_JUILLET_FRANCE_GRAPH.png")
    plt.show()


